#!/usr/bin/env python3
"""Migração única do andamento (ADR 0004): tira dos cabeçalhos de disciplinas/ os campos de andamento e grava
em registro/estado.yml os valores fora do padrão.

Script autônomo: usa só a biblioteca padrão e o PyYAML, sem importar outros módulos do repositório, para poder
ser trazido da main com `git show origin/main:scripts/migrar_estado.py` e rodado numa branch antiga.

Os cabeçalhos são editados linha a linha: saem só as linhas dos campos de andamento (status, inicio,
diagnostico, nivel_atingido, portao.data, portao.resultado, portao.evidencia) e os dois comentários que os
precedem. O resto do arquivo fica igual, byte a byte. Rodar de novo não muda nada.

Uso:
    python scripts/migrar_estado.py                      # na raiz do repositório, na branch de estudo
    python migrar_estado.py --raiz caminho/do/repo       # de outro lugar
    python scripts/migrar_estado.py --nao-gravar-estado  # na main: limpa os cabeçalhos sem criar o estado.yml
    python scripts/migrar_estado.py --simular            # só mostra o que faria
"""
import argparse
import copy
import datetime as dt
import json
import pathlib
import re
import sys

import yaml

ARQUIVO = "registro/estado.yml"
CAMPOS = ["status", "inicio", "diagnostico", "nivel_atingido"]
CAMPOS_PORTAO = ["data", "resultado", "evidencia"]
PADRAO = {"status": "nao_iniciada", "inicio": None, "diagnostico": None, "nivel_atingido": None}
PALAVRA = re.compile(r"^[a-z][a-z_]*$")  # como os valores de status: vão sem aspas
RESERVADAS = {"null", "true", "false", "yes", "no", "on", "off", "y", "n"}
CABECALHO = "# Andamento de cada módulo e disciplina. Só existe na branch de estudo (docs/fluxo-git.md).\n"
COMENTARIOS = ("# Atualize daqui para baixo", "# status: ")
CAMPO_TOPO = re.compile(r"^(%s):(\s|$)" % "|".join(CAMPOS))
CAMPO_PORTAO = re.compile(r"^(\s+)(%s):(\s|$)" % "|".join(CAMPOS_PORTAO))
PORTAO = re.compile(r"^portao:\s*(#.*)?$")


class ErroMigracao(Exception):
    pass


def _valor(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, (dt.date, dt.datetime)):
        return v.isoformat()
    if isinstance(v, dict):
        return "{" + ", ".join(f"{k}: {_valor(x)}" for k, x in v.items()) + "}"
    if PALAVRA.match(str(v)) and str(v) not in RESERVADAS:
        return str(v)
    return json.dumps(str(v), ensure_ascii=False)


def formatar_estado(modulos):
    """Texto de registro/estado.yml, uma linha por módulo, na ordem dada."""
    linhas = [CABECALHO, "schema_version: 1\n"]
    if not modulos:
        linhas.append("modulos: {}\n")
    else:
        linhas.append("modulos:\n")
        linhas += [f"  {c}: {_valor(m)}\n" for c, m in modulos.items()]
    return "".join(linhas)


def _indentada(linha):
    return linha[:1] in (" ", "\t") and linha.strip() != ""


def _linhas_a_remover(cab, nome):
    """Índices (nas linhas do cabeçalho) dos campos de andamento e dos dois comentários."""
    remover = []
    i = 0
    while i < len(cab):
        linha = cab[i].rstrip("\n")
        if linha.startswith(COMENTARIOS):
            remover.append(i)
        elif CAMPO_TOPO.match(linha):
            if i + 1 < len(cab) and _indentada(cab[i + 1]):
                raise ErroMigracao(f"{nome}: o campo '{linha.split(':')[0]}' ocupa mais de uma linha; migre à mão")
            remover.append(i)
        elif linha.startswith("portao:"):
            if not PORTAO.match(linha):
                raise ErroMigracao(f"{nome}: 'portao' não está no formato de bloco (uma linha por campo); migre à mão")
            j, recuo = i + 1, None
            while j < len(cab) and (_indentada(cab[j]) or cab[j].strip() == ""):
                filho = cab[j].rstrip("\n")
                if filho.strip():
                    r = len(filho) - len(filho.lstrip())
                    recuo = r if recuo is None else recuo
                    m = CAMPO_PORTAO.match(filho)
                    if m and len(m.group(1)) == recuo:
                        prox = cab[j + 1] if j + 1 < len(cab) else ""
                        if _indentada(prox) and len(prox) - len(prox.lstrip()) > recuo:
                            raise ErroMigracao(f"{nome}: o campo 'portao.{m.group(2)}' ocupa mais de uma linha; migre à mão")
                        remover.append(j)
                j += 1
            i = j
            continue
        i += 1
    return remover


def _sem_andamento(d):
    d = copy.deepcopy(d)
    for c in CAMPOS:
        d.pop(c, None)
    if isinstance(d.get("portao"), dict):
        for c in CAMPOS_PORTAO:
            d["portao"].pop(c, None)
    return d


def _fora_do_padrao(d):
    """Valores de andamento de um cabeçalho lido que diferem do padrão."""
    m = {c: d[c] for c in CAMPOS if c in d and d[c] != PADRAO[c]}
    portao = d.get("portao") if isinstance(d.get("portao"), dict) else {}
    p = {c: portao[c] for c in CAMPOS_PORTAO if portao.get(c) is not None}
    if p:
        m["portao"] = p
    return m


def _conferir(antes, depois, nome):
    """Confere, de forma independente, que o texto novo é o antigo menos linhas de andamento do cabeçalho."""
    a, d = antes.splitlines(keepends=True), depois.splitlines(keepends=True)
    fim = a.index("---\n", 1)
    j = 0
    for i, linha in enumerate(a):
        if j < len(d) and d[j] == linha:
            j += 1
            continue
        s = linha.rstrip("\n")
        if not (0 < i < fim and (s.startswith(COMENTARIOS) or CAMPO_TOPO.match(s) or CAMPO_PORTAO.match(s))):
            raise ErroMigracao(f"{nome}: a conferência achou uma mudança fora das linhas de andamento; nada foi mudado")
    if j != len(d):
        raise ErroMigracao(f"{nome}: a conferência achou uma linha nova; nada foi mudado")


def _migrar_arquivo(arq, raiz):
    """(texto novo ou None, código, ordem, valores fora do padrão, linhas removidas)."""
    nome = arq.relative_to(raiz).as_posix()
    texto = arq.read_text(encoding="utf-8")
    linhas = texto.splitlines(keepends=True)
    if not linhas or linhas[0] != "---\n":
        raise ErroMigracao(f"{nome}: cabeçalho YAML ausente")
    fim = next((i for i in range(1, len(linhas)) if linhas[i] == "---\n"), None)
    if fim is None:
        raise ErroMigracao(f"{nome}: cabeçalho YAML sem o '---' de fechamento")
    cab = linhas[1:fim]
    if any("\r" in l for l in cab):
        raise ErroMigracao(f"{nome}: fim de linha CRLF no cabeçalho; converta para LF antes")
    try:
        dados = yaml.safe_load("".join(cab))
    except yaml.YAMLError as e:
        raise ErroMigracao(f"{nome}: YAML inválido no cabeçalho ({e.__class__.__name__})")
    if not isinstance(dados, dict) or not dados.get("codigo"):
        raise ErroMigracao(f"{nome}: cabeçalho sem 'codigo'")
    remover = set(_linhas_a_remover(cab, nome))
    novo_cab = [l for i, l in enumerate(cab) if i not in remover]
    try:
        novos = yaml.safe_load("".join(novo_cab))
    except yaml.YAMLError as e:
        raise ErroMigracao(f"{nome}: o cabeçalho ficaria com YAML inválido ({e.__class__.__name__}); nada foi mudado")
    if novos != _sem_andamento(dados):
        raise ErroMigracao(f"{nome}: a remoção mudaria outros campos do cabeçalho ou deixaria andamento nele; migre à mão")
    removidas = [cab[i] for i in sorted(remover)]
    if not removidas:
        return None, dados["codigo"], dados.get("ordem"), {}, []
    novo_texto = linhas[0] + "".join(novo_cab) + "".join(linhas[fim:])
    _conferir(texto, novo_texto, nome)
    return novo_texto, dados["codigo"], dados.get("ordem"), _fora_do_padrao(dados), removidas


def _ler_estado(arq):
    if not arq.exists():
        return None
    dados = yaml.safe_load(arq.read_text(encoding="utf-8"))
    if dados is None:
        return {}
    if not isinstance(dados, dict) or not isinstance(dados.get("modulos") or {}, dict):
        raise ErroMigracao(f"{ARQUIVO}: formato inesperado; esperado schema_version e modulos")
    return dict(dados.get("modulos") or {})


def migrar(raiz=".", gravar_estado=True, simular=False):
    """Migra os cabeçalhos de <raiz>/disciplinas. Nada é gravado se algum arquivo tiver problema."""
    raiz = pathlib.Path(raiz).resolve()
    pasta = raiz / "disciplinas"
    if not pasta.is_dir():
        raise ErroMigracao(f"{raiz}: não há a pasta disciplinas/; use --raiz com a raiz do repositório")
    mudancas, valores, ordem, erros = [], {}, {}, []
    for arq in sorted(pasta.glob("*.md")):
        try:
            novo, cod, ordem_cod, fora, removidas = _migrar_arquivo(arq, raiz)
        except ErroMigracao as e:
            erros.append(str(e))
            continue
        ordem[cod] = ordem_cod if isinstance(ordem_cod, int) else 10 ** 9
        if novo is not None:
            mudancas.append((arq, novo, len(removidas)))
        if fora:
            valores[cod] = fora
    if erros:
        raise ErroMigracao("\n".join(erros))

    arq_estado = raiz / ARQUIVO
    existente = _ler_estado(arq_estado)
    novo_estado = None
    if gravar_estado:
        mods = dict(existente or {})
        conflitos = []
        for cod, fora in valores.items():
            atual = mods.get(cod) if isinstance(mods.get(cod), dict) else {}
            junto = copy.deepcopy(atual)
            for k, v in fora.items():
                if k == "portao":
                    p = junto.get("portao") if isinstance(junto.get("portao"), dict) else {}
                    for pk, pv in v.items():
                        if pk in p and p[pk] != pv:
                            conflitos.append(f"{cod}: portao.{pk} é {p[pk]!r} em {ARQUIVO} e {pv!r} no cabeçalho")
                        p[pk] = pv
                    junto["portao"] = p
                else:
                    if k in junto and junto[k] != v:
                        conflitos.append(f"{cod}: {k} é {junto[k]!r} em {ARQUIVO} e {v!r} no cabeçalho")
                    junto[k] = v
            mods[cod] = {k: junto[k] for k in CAMPOS + ["portao"] if k in junto} | \
                        {k: v for k, v in junto.items() if k not in CAMPOS and k != "portao"}
        if conflitos:
            raise ErroMigracao("valores diferentes no cabeçalho e no estado; resolva à mão e rode de novo:\n"
                               + "\n".join(conflitos))
        ordenados = dict(sorted(mods.items(), key=lambda kv: (ordem.get(kv[0], 10 ** 9), list(mods).index(kv[0]))))
        if existente is None or ordenados != existente:
            texto = formatar_estado(ordenados)
            if yaml.safe_load(texto) != {"schema_version": 1, "modulos": ordenados or {}}:
                raise ErroMigracao(f"{ARQUIVO}: o texto gerado não relê os mesmos valores; nada foi mudado")
            novo_estado = texto

    if not simular:
        if novo_estado is not None:
            arq_estado.parent.mkdir(parents=True, exist_ok=True)
            arq_estado.write_text(novo_estado, encoding="utf-8")
        for arq, novo, _ in mudancas:
            arq.write_text(novo, encoding="utf-8")
    return {
        "arquivos": [(arq.relative_to(raiz).as_posix(), n) for arq, _, n in mudancas],
        "valores": valores,
        "estado_gravado": novo_estado is not None,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Leva o andamento dos cabeçalhos de disciplinas/ para registro/estado.yml.")
    ap.add_argument("--raiz", default=".", help="raiz do repositório (padrão: o diretório atual)")
    ap.add_argument("--nao-gravar-estado", action="store_true",
                    help="só limpa os cabeçalhos, sem criar ou mudar registro/estado.yml (para a main)")
    ap.add_argument("--simular", action="store_true", help="mostra o que faria, sem gravar nada")
    a = ap.parse_args(argv)
    try:
        rel = migrar(a.raiz, gravar_estado=not a.nao_gravar_estado, simular=a.simular)
    except ErroMigracao as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 1
    prefixo = "(simulação) " if a.simular else ""
    linhas = sum(n for _, n in rel["arquivos"])
    print(f"{prefixo}{len(rel['arquivos'])} arquivos de disciplinas/ alterados, {linhas} linhas removidas.")
    if rel["valores"]:
        destino = "descartados (--nao-gravar-estado)" if a.nao_gravar_estado else f"em {ARQUIVO}"
        print(f"Valores fora do padrão {destino}:")
        for cod, v in rel["valores"].items():
            print(f"  {cod}: {_valor(v)}")
    if not a.nao_gravar_estado:
        print(f"{ARQUIVO} " + ("gravado." if rel["estado_gravado"] else "já estava em dia."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
