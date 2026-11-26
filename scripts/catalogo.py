#!/usr/bin/env python3
"""Validações cruzadas entre disciplinas, catálogo, listas e escalas (Marco 3 do Knowledge Core).

validar_catalogo(disc, raiz) devolve erros; avisos_catalogo(disc) devolve avisos.
`disc` é o dicionário código → cabeçalho que scripts/progresso.py monta (com a chave "arquivo").
A ausência ou o formato errado de um arquivo do catálogo é erro de scripts/esquema.py; aqui as regras
que dependem dele são puladas.
"""
import pathlib
import re

import yaml

from esquema import FM, ler_yaml

FEITAS = {"concluida", "dispensada", "em_revisao"}
NIVELAMENTO = "nivelamento"
PCT_MINIMO_NIVELAMENTO = 80
PROJETO = re.compile(r"\bPJ(\d+)\b")
CODIGO_CAB = re.compile(r"^codigo:\s*[\"']?([^\"'\s#]+)", re.M)
UNIDADE = re.compile(r"^U\d+\.\d+$")
SECAO_NIVEIS = "## Níveis de exercício"


def _ler(caminho):
    if not caminho.exists():
        return None
    try:
        dados = ler_yaml(caminho.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return None
    return dados if isinstance(dados, dict) else None


def caminho_valido(raiz, rel):
    """True se `rel` é relativo, fica dentro de `raiz` e existe."""
    if not rel or pathlib.PurePath(str(rel)).is_absolute():
        return False
    raiz = pathlib.Path(raiz).resolve()
    alvo = (raiz / str(rel)).resolve()
    return alvo.is_relative_to(raiz) and alvo.exists()


def _verificacoes_no_lugar(raiz):
    """Cada exercicios/<d>/verificacao/<n>.yml aponta para a própria lista e o próprio gabarito."""
    erros = []
    for yml in sorted(pathlib.Path(raiz).glob("exercicios/*/verificacao/*.yml")):
        dados = _ler(yml) or {}
        d, n = yml.parent.parent.name, yml.stem
        esperado = {"lista": f"exercicios/{d}/{n}.md", "gabarito": f"exercicios/{d}/gabaritos/{n}.md"}
        for campo, valor in esperado.items():
            if dados.get(campo) != valor:
                erros.append(f"verificacao-fora-do-lugar: exercicios/{d}/verificacao/{n}.yml: {campo} é "
                             f"{dados.get(campo)!r}; o esperado é {valor!r}")
    return erros


def carregar_catalogo(raiz):
    """Nome → conteúdo de cada arquivo do catálogo (None se ausente ou ilegível)."""
    raiz = pathlib.Path(raiz)
    return {n: _ler(raiz / "catalogo" / f"{n}.yml") for n in ("eixos", "unidades", "projetos", "escalas", "aposentados", "fora-do-plano")}


def _lista(dados, chave):
    v = (dados or {}).get(chave)
    return [x for x in v if isinstance(x, dict)] if isinstance(v, list) else []


def _codigos(itens, chave="codigo"):
    return {str(x.get(chave)) for x in itens if x.get(chave) is not None}


def codigos_repetidos(raiz):
    """Lê o campo codigo de cada disciplinas/*.md direto do arquivo, porque o carregador sobrescreve em silêncio."""
    onde = {}
    for arq in sorted((pathlib.Path(raiz) / "disciplinas").glob("*.md")):
        m = FM.match(arq.read_text(encoding="utf-8"))
        cod = CODIGO_CAB.search(m.group(1)) if m else None
        if cod:
            onde.setdefault(cod.group(1), []).append(f"disciplinas/{arq.name}")
    return {c: arqs for c, arqs in onde.items() if len(arqs) > 1}


def referencias(disc, raiz, cat=None):
    """Cada referência a unidade ou projeto: (origem, tipo, código citado, resolvida)."""
    raiz = pathlib.Path(raiz)
    cat = cat or carregar_catalogo(raiz)
    refs = []
    if cat["unidades"] is not None:
        unidades = _lista(cat["unidades"], "unidades")
        cods_u = _codigos(unidades)
        for c, d in sorted(disc.items()):
            for campo in ("requer_unidades", "unidades_relacionadas"):
                for u in d.get(campo) or []:
                    refs.append((f"{c}: {campo}", "unidade", str(u), str(u) in cods_u))
        for u in unidades:
            for p in u.get("prerequisitos") or []:
                p = str(p)
                tipo = "unidade" if UNIDADE.match(p) else "disciplina"
                refs.append((f"{u.get('codigo')}: prerequisitos", tipo, p, p in (cods_u if tipo == "unidade" else disc)))
    if cat["projetos"] is not None:
        cods_p = _codigos(_lista(cat["projetos"], "projetos"))
        for arq in sorted((raiz / "disciplinas").glob("*.md")):
            for n in sorted(set(PROJETO.findall(arq.read_text(encoding="utf-8"))), key=int):
                refs.append((f"disciplinas/{arq.name}", "projeto", f"PJ{n}", f"PJ{n}" in cods_p))
    return refs


def situacao_listas(raiz):
    """(erros, [(lista, "verificacao" | "excecao" | "faltando")]) das listas em exercicios/<código>/."""
    raiz = pathlib.Path(raiz)
    excecoes = _lista(_ler(raiz / "exercicios" / "sem-verificacao.yml"), "listas")
    nomes_exc = {str(e.get("lista")) for e in excecoes}
    erros, situacao = [], []
    for lista in sorted(raiz.glob("exercicios/*/*.md")):
        rel = lista.relative_to(raiz).as_posix()
        yml = lista.parent / "verificacao" / f"{lista.stem}.yml"
        if yml.exists():
            situacao.append((rel, "verificacao"))
        elif rel in nomes_exc:
            situacao.append((rel, "excecao"))
        else:
            situacao.append((rel, "faltando"))
            erros.append(f"lista-sem-verificacao: {rel} sem verificacao/{lista.stem}.yml e fora de exercicios/sem-verificacao.yml")
    for e in excecoes:
        rel = str(e.get("lista"))
        if e.get("ver") and not caminho_valido(raiz, e.get("ver")):
            erros.append(f"excecao-sem-referencia: exercicios/sem-verificacao.yml: {rel}: ver aponta para {e.get('ver')}, "
                         "fora do repositório ou inexistente")
        caminho = raiz / rel
        if not caminho.exists():
            erros.append(f"excecao-sem-lista: exercicios/sem-verificacao.yml: {rel} não existe")
        elif (caminho.parent / "verificacao" / f"{caminho.stem}.yml").exists():
            erros.append(f"excecao-desnecessaria: exercicios/sem-verificacao.yml: {rel} já tem verificacao/{caminho.stem}.yml; "
                         "tire a entrada")
    return erros, situacao


def tabela_niveis(caminho):
    """Linhas (nível, nome, o que treina) da tabela "Níveis de exercício" de AVALIACOES.md."""
    if not caminho.exists():
        return None
    linhas, dentro = [], False
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        if linha.startswith("## "):
            dentro = linha.strip() == SECAO_NIVEIS
            continue
        if dentro and linha.startswith("|"):
            cel = [c.strip() for c in linha.strip().strip("|").split("|")]
            if cel and cel[0].isdigit():
                linhas.append((int(cel[0]), *cel[1:]))
    return linhas


def _escala(raiz, cat):
    if cat["escalas"] is None:
        return []
    escala = [(e.get("nivel"), e.get("nome"), e.get("o_que_treina")) for e in _lista(cat["escalas"], "dificuldade_exercicio")]
    tabela = tabela_niveis(pathlib.Path(raiz) / "AVALIACOES.md")
    if tabela is None:
        return ["escala-divergente: AVALIACOES.md não existe; a tabela \"Níveis de exercício\" repete catalogo/escalas.yml"]
    erros = []
    por_nivel = {t[0]: t for t in tabela}
    for nivel, nome, treina in escala:
        t = por_nivel.get(nivel)
        if t is None:
            erros.append(f"escala-divergente: AVALIACOES.md, \"Níveis de exercício\": falta o nível {nivel} de catalogo/escalas.yml")
        elif list(t[1:]) != [nome, treina]:
            erros.append(f"escala-divergente: AVALIACOES.md, \"Níveis de exercício\", nível {nivel}: "
                         f"'{' | '.join(t[1:])}' difere de catalogo/escalas.yml: '{nome} | {treina}'")
    for nivel in sorted(set(por_nivel) - {e[0] for e in escala}):
        erros.append(f"escala-divergente: AVALIACOES.md, \"Níveis de exercício\": nível {nivel} não existe em catalogo/escalas.yml")
    return erros


def _eixos(disc, cat):
    if cat["eixos"] is None:
        return []
    erros = []
    eixos = _lista(cat["eixos"], "eixos")
    todos_rotulos = {r for e in eixos for r in e.get("rotulos_nas_disciplinas") or []}
    listadas = {}
    for e in eixos:
        rotulos = e.get("rotulos_nas_disciplinas") or []
        for c in e.get("disciplinas") or []:
            listadas[c] = e
            if c not in disc:
                erros.append(f"disciplina-sem-arquivo: eixo {e.get('codigo')} lista {c}, que não tem arquivo em disciplinas/; "
                             "se for de propósito, mova para sem_arquivo")
            elif disc[c].get("eixo") not in rotulos:
                erros.append(f"eixo-divergente: {c}: eixo '{disc[c].get('eixo')}' não está nos rótulos do eixo "
                             f"{e.get('codigo')} ({e.get('nome')}): {', '.join(rotulos)}")
        for c in e.get("sem_arquivo") or []:
            if c in disc:
                erros.append(f"sem-arquivo-com-arquivo: eixo {e.get('codigo')} diz que {c} não tem arquivo, mas existe {disc[c].get('arquivo')}")
    for c, d in sorted(disc.items()):
        if c in listadas:
            continue
        if d.get("fase") == NIVELAMENTO:
            if d.get("eixo") not in todos_rotulos:
                erros.append(f"eixo-desconhecido: {c}: rótulo '{d.get('eixo')}' não existe em nenhum eixo de catalogo/eixos.yml")
        else:
            erros.append(f"eixo-ausente: {c} não está em nenhum eixo de catalogo/eixos.yml")
    return erros


def _projetos(disc, cat):
    if cat["projetos"] is None or cat["eixos"] is None:
        return []
    sem_arquivo = {c for e in _lista(cat["eixos"], "eixos") for c in e.get("sem_arquivo") or []}
    return [f"projeto-disciplina-desconhecida: {p.get('codigo')} cita {c}, que não tem arquivo nem está em sem_arquivo de catalogo/eixos.yml"
            for p in _lista(cat["projetos"], "projetos") for c in p.get("disciplinas") or []
            if c not in disc and c not in sem_arquivo]


def _aposentados(disc, raiz, cat):
    erros = []
    for a in _lista(cat["aposentados"], "aposentados"):
        c = a.get("codigo")
        if c in disc:
            erros.append(f"aposentado-com-arquivo: {c} está em catalogo/aposentados.yml e tem arquivo {disc[c].get('arquivo')}")
        for outro, d in sorted(disc.items()):
            if c in (d.get("prerequisitos") or []):
                erros.append(f"aposentado-como-prerequisito: {outro} tem como pré-requisito {c}, código aposentado")
        ver = a.get("ver")
        if ver and not caminho_valido(raiz, ver):
            erros.append(f"aposentado-sem-referencia: {c}: ver aponta para {ver}, fora do repositório ou inexistente")
        for p in _lista(cat["projetos"], "projetos"):
            if c in (p.get("disciplinas") or []):
                erros.append(f"aposentado-em-projeto: {p.get('codigo')} cita {c}, código aposentado")
        for u in _lista(cat["unidades"], "unidades"):
            if c in (u.get("prerequisitos") or []):
                erros.append(f"aposentado-em-unidade: {u.get('codigo')} tem como pré-requisito {c}, código aposentado")
    return erros


def _fora_do_plano(disc, cat):
    """Todo código de sem_arquivo tem motivo em fora-do-plano.yml (ou é aposentado), e vice-versa."""
    erros = []
    if cat["eixos"] is None or cat["fora-do-plano"] is None:
        return erros  # arquivo ausente já é apontado pelo schema
    sem_arquivo = {c for e in _lista(cat["eixos"], "eixos") for c in e.get("sem_arquivo") or []}
    aposentados = {a.get("codigo") for a in _lista(cat["aposentados"], "aposentados")}
    fora = {f.get("codigo"): f for f in _lista(cat["fora-do-plano"], "fora_do_plano")}
    for c in sorted(sem_arquivo - set(fora) - aposentados):
        erros.append(f"sem-arquivo-sem-motivo: {c} está em sem_arquivo de catalogo/eixos.yml sem motivo em catalogo/fora-do-plano.yml")
    for c in sorted(fora):
        if c in disc:
            erros.append(f"fora-do-plano-com-arquivo: {c} está em catalogo/fora-do-plano.yml, mas tem arquivo em disciplinas/")
        if c not in sem_arquivo:
            erros.append(f"fora-do-plano-fora-dos-eixos: {c} está em catalogo/fora-do-plano.yml, mas não em sem_arquivo de catalogo/eixos.yml")
    return erros


def validar_catalogo(disc, raiz):
    raiz = pathlib.Path(raiz)
    cat = carregar_catalogo(raiz)
    erros = [f"codigo-repetido: {c} em {' e '.join(arqs)}" for c, arqs in sorted(codigos_repetidos(raiz).items())]
    for origem, tipo, cod, ok in referencias(disc, raiz, cat):
        if ok:
            continue
        if tipo == "projeto":
            erros.append(f"projeto-desconhecido: {origem} cita {cod}, ausente de catalogo/projetos.yml")
        elif tipo == "unidade":
            erros.append(f"unidade-desconhecida: {origem} cita {cod}, ausente de catalogo/unidades.yml")
        else:
            erros.append(f"disciplina-desconhecida: {origem} cita {cod}, que não tem arquivo em disciplinas/")
    erros += _eixos(disc, cat)
    erros += _fora_do_plano(disc, cat)
    erros += _projetos(disc, cat)
    erros += _aposentados(disc, raiz, cat)
    erros += situacao_listas(raiz)[0]
    erros += _verificacoes_no_lugar(raiz)
    erros += _escala(raiz, cat)
    return erros


def porcentagem(resultado):
    """Menor porcentagem do resultado do portão ("75%", "79,5 %", "14/20" ou um número); senão None."""
    if isinstance(resultado, bool) or resultado is None:
        return None
    if isinstance(resultado, (int, float)):
        return float(resultado)
    texto = str(resultado)
    valores = [float(v.replace(",", ".")) for v in re.findall(r"(\d+(?:[.,]\d+)?)\s*%", texto)]
    valores += [100 * int(a) / int(b) for a, b in re.findall(r"\b(\d+)\s*/\s*(\d+)\b", texto) if int(b)]
    return min(valores) if valores else None


def avisos_catalogo(disc):
    avisos = []
    for c, d in sorted(disc.items()):
        if d.get("fase") != NIVELAMENTO or d.get("status") not in FEITAS:
            continue
        pct = porcentagem((d.get("portao") or {}).get("resultado"))
        if pct is not None and pct < PCT_MINIMO_NIVELAMENTO:
            avisos.append(f"portao-abaixo-de-80: {c}: portão com {pct:g}%, abaixo dos {PCT_MINIMO_NIVELAMENTO}% "
                          f"exigidos no nivelamento")
    return avisos
