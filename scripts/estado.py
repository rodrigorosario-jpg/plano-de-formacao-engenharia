#!/usr/bin/env python3
"""Andamento de quem estuda (decisão D4, ADR 0004): `registro/estado.yml`, que só existe na branch de estudo.

O cabeçalho de cada arquivo em disciplinas/ guarda só o currículo. O andamento (status, inicio, diagnostico,
nivel_atingido, portao.data, portao.resultado, portao.evidencia) fica em registro/estado.yml, com uma linha por
módulo que tenha algum valor fora do padrão. Sem o arquivo, como na main, tudo está no padrão.
"""
import datetime as dt
import json
import pathlib
import re

import yaml

ARQUIVO = "registro/estado.yml"
CAMPOS = ["status", "inicio", "diagnostico", "nivel_atingido"]
CAMPOS_PORTAO = ["data", "resultado", "evidencia"]
PADRAO = {"status": "nao_iniciada", "inicio": None, "diagnostico": None, "nivel_atingido": None}
STATUS_VALIDOS = {"nao_iniciada", "em_andamento", "no_portao", "concluida", "dispensada", "em_revisao"}
PALAVRA = re.compile(r"^[a-z][a-z_]*$")  # como os valores de status: vão sem aspas
RESERVADAS = {"null", "true", "false", "yes", "no", "on", "off", "y", "n"}
CABECALHO = "# Andamento de cada módulo e disciplina. Só existe na branch de estudo (docs/fluxo-git.md).\n"
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def carregar_estado(raiz):
    """Conteúdo de registro/estado.yml ({} se o arquivo não existe). Datas vêm como datetime.date."""
    arq = pathlib.Path(raiz) / ARQUIVO
    if not arq.exists():
        return {}
    dados = yaml.safe_load(arq.read_text(encoding="utf-8"))
    return dados if isinstance(dados, dict) else {}


def _modulos(estado):
    m = (estado or {}).get("modulos")
    return m if isinstance(m, dict) else {}


def aplicar_estado(disc, estado):
    """Preenche em cada disciplina os campos de andamento: o valor do estado, senão o padrão.

    Um campo que ainda esteja no cabeçalho (antes da migração) vale como reserva; validar_estado acusa o erro."""
    modulos = _modulos(estado)
    for c, d in disc.items():
        m = modulos.get(c) if isinstance(modulos.get(c), dict) else {}
        for campo in CAMPOS:
            d[campo] = m[campo] if campo in m else d.get(campo, PADRAO[campo])
        portao = dict(d.get("portao") or {})
        mp = m.get("portao") if isinstance(m.get("portao"), dict) else {}
        for campo in CAMPOS_PORTAO:
            portao[campo] = mp[campo] if campo in mp else portao.get(campo)
        d["portao"] = portao
    return disc


def andamento_no_cabecalho(d):
    """Campos de andamento presentes num cabeçalho já lido, como 'status' ou 'portao.data'."""
    if not isinstance(d, dict):
        return []
    achados = [c for c in CAMPOS if c in d]
    portao = d.get("portao")
    if isinstance(portao, dict):
        achados += [f"portao.{c}" for c in CAMPOS_PORTAO if c in portao]
    return achados


def _cabecalhos_com_andamento(raiz):
    res = []
    for arq in sorted((pathlib.Path(raiz) / "disciplinas").glob("*.md")):
        m = FM.match(arq.read_text(encoding="utf-8"))
        if not m:
            continue
        try:
            d = yaml.safe_load(m.group(1))
        except yaml.YAMLError:
            continue
        campos = andamento_no_cabecalho(d)
        if campos:
            res.append((f"disciplinas/{arq.name}", campos))
    return res


def validar_estado(disc, estado, raiz):
    """Erros do estado (código desconhecido, status inválido, chave desconhecida) e andamento esquecido no cabeçalho."""
    erros = []
    if estado and "modulos" in estado and not isinstance(estado["modulos"], dict):
        erros.append(f"{ARQUIVO}: modulos: deve ser um mapa de código para andamento")
    for c, m in _modulos(estado).items():
        if c not in disc:
            erros.append(f"{ARQUIVO}: {c}: código desconhecido")
            continue
        if not isinstance(m, dict):
            erros.append(f"{ARQUIVO}: {c}: o andamento deve ser um mapa, como {{status: em_andamento}}")
            continue
        for k in m:
            if k not in CAMPOS and k != "portao":
                erros.append(f"{ARQUIVO}: {c}: chave desconhecida '{k}'")
        if "status" in m and m["status"] not in STATUS_VALIDOS:
            erros.append(f"{ARQUIVO}: {c}: status inválido '{m['status']}'")
        portao = m.get("portao")
        if portao is not None and not isinstance(portao, dict):
            erros.append(f"{ARQUIVO}: {c}: portao deve ser um mapa com data, resultado e evidencia")
        elif isinstance(portao, dict):
            for k in portao:
                if k not in CAMPOS_PORTAO:
                    erros.append(f"{ARQUIVO}: {c}: chave desconhecida 'portao.{k}'")
    for arquivo, campos in _cabecalhos_com_andamento(raiz):
        erros.append(f"{arquivo}: campos de andamento no cabeçalho ({', '.join(campos)}); o andamento fica em "
                     f"{ARQUIVO}: rode `python scripts/migrar_estado.py` (veja docs/fluxo-git.md) ou grave os valores "
                     f"em {ARQUIVO} e apague-os do cabeçalho")
    return erros


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
