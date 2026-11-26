#!/usr/bin/env python3
"""Validação por JSON Schema (decisão D5): cabeçalhos de disciplinas, catálogo, verificações de listas,
plano.yml, exercicios/sem-verificacao.yml e registro/estado.yml e registro/estudante.yml (se existirem). Os schemas ficam em schemas/ e são lidos uma vez.

Uso:
    python scripts/esquema.py     # imprime os erros; sai com 1 se houver algum
"""
import datetime as dt
import functools
import json
import pathlib
import re
import sys

import yaml
from jsonschema import Draft202012Validator

from estado import CAMPOS as CAMPOS_ANDAMENTO, CAMPOS_PORTAO as CAMPOS_ANDAMENTO_PORTAO

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIR_ESQUEMAS = RAIZ / "schemas"
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)

ESQUEMAS = ["disciplina", "eixos", "unidades", "projetos", "escalas", "aposentados",
            "verificacao", "plano", "sem-verificacao", "estado", "estudante", "fora-do-plano"]
CATALOGO = ["eixos", "unidades", "projetos", "escalas", "aposentados"]


@functools.lru_cache(maxsize=None)
def carregar_esquema(nome):
    return json.loads((DIR_ESQUEMAS / f"{nome}.schema.json").read_text(encoding="utf-8"))


@functools.lru_cache(maxsize=None)
def validador(nome):
    esq = carregar_esquema(nome)
    Draft202012Validator.check_schema(esq)
    return Draft202012Validator(esq)


def para_json(valor):
    """Converte datas (que o yaml.safe_load devolve como datetime.date) em texto ISO, em qualquer nível."""
    if isinstance(valor, (dt.date, dt.datetime)):
        return valor.isoformat()
    if isinstance(valor, dict):
        return {str(k): para_json(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [para_json(v) for v in valor]
    return valor


def ler_yaml(texto):
    return yaml.load(texto, Loader=LOADER)


def ler_cabecalho(arq):
    """(dados, erro) do cabeçalho YAML de um arquivo de disciplina."""
    m = FM.match(arq.read_text(encoding="utf-8"))
    if not m:
        return None, "cabeçalho YAML ausente"
    try:
        return ler_yaml(m.group(1)), None
    except yaml.YAMLError as e:
        return None, f"YAML inválido ({e.__class__.__name__})"


def carregar_cabecalhos(raiz):
    """Lista de (caminho relativo, dados ou None, erro ou None) para cada disciplinas/*.md."""
    raiz = pathlib.Path(raiz)
    return [(f"disciplinas/{arq.name}", *ler_cabecalho(arq)) for arq in sorted((raiz / "disciplinas").glob("*.md"))]


def _caminho(erro):
    return ".".join(str(p) for p in erro.absolute_path) or "(raiz)"


def _mensagem(erro):
    v, val = erro.validator, erro.validator_value
    if v == "required":
        m = re.match(r"'(.+?)' is a required property", erro.message)
        return f"falta o campo obrigatório '{m.group(1) if m else val[0]}'"
    if v == "additionalProperties":
        extras = sorted(set(erro.instance) - set(erro.schema.get("properties", {})))
        return "campo não previsto no schema: " + ", ".join(f"'{c}'" for c in extras)
    if v == "not" or v is None:
        desc = erro.schema.get("description") if isinstance(erro.schema, dict) else None
        return f"campo não permitido aqui ({desc[0].lower() + desc[1:].rstrip('.')})" if desc else "campo não permitido aqui"
    if v == "enum":
        return f"valor {erro.instance!r} fora da lista: {', '.join(map(str, val))}"
    if v == "const":
        return f"valor {erro.instance!r}; o esperado é {val!r}"
    if v == "type":
        return f"valor {erro.instance!r} não é do tipo {val}"
    if v == "pattern":
        return f"valor {erro.instance!r} fora do formato {val}"
    if v in ("minimum", "maximum"):
        return f"valor {erro.instance!r} {'abaixo do mínimo' if v == 'minimum' else 'acima do máximo'} {val}"
    if v in ("anyOf", "oneOf"):
        if "description" in erro.schema and v == "anyOf" and all(
                isinstance(s, dict) and set(s) == {"required"} for s in val):
            return erro.schema["description"]
        tipos = [s.get("type") for s in val if isinstance(s, dict) and "type" in s]
        if tipos:
            return f"valor {erro.instance!r} não é {' nem '.join(map(str, tipos))} no formato esperado"
    if v == "uniqueItems":
        return "itens repetidos na lista"
    if v in ("minItems", "maxItems"):
        return f"a lista tem {len(erro.instance)} itens; o {'mínimo' if v == 'minItems' else 'máximo'} é {val}"
    if v == "minLength":
        return "texto vazio"
    return erro.message


def _erros_esquema(nome, dados, arquivo):
    erros = sorted(validador(nome).iter_errors(para_json(dados)), key=lambda e: (list(map(str, e.absolute_path)), e.validator or ""))
    return [f"{arquivo}: {_caminho(e)}: {_mensagem(e)}" for e in erros]


def _competencias_do_codigo(d, arquivo):
    """O schema só confere o formato geral do id; aqui se confere que o prefixo é o código do próprio arquivo."""
    if not isinstance(d, dict) or not isinstance(d.get("codigo"), str) or not isinstance(d.get("competencias"), list):
        return []
    cod = d["codigo"]
    padrao = re.compile(rf"^{re.escape(cod)}\.c\d{{2}}$")
    geral = re.compile(r"^[A-Z]{1,2}\d+\.c\d{2}$")
    msgs = []
    for i, c in enumerate(d["competencias"]):
        cid = c.get("id") if isinstance(c, dict) else None
        if isinstance(cid, str) and geral.match(cid) and not padrao.match(cid):
            msgs.append(f"{arquivo}: competencias.{i}.id: '{cid}' não está no formato {cod}.cNN")
    return msgs


def validar_por_arquivo(raiz=RAIZ):
    """Dicionário caminho relativo → lista de mensagens, para cada arquivo coberto por um schema."""
    raiz = pathlib.Path(raiz)
    res = {}
    for arquivo, d, erro in carregar_cabecalhos(raiz):
        if erro:
            res[arquivo] = [f"{arquivo}: (raiz): {erro}"]
        else:
            res[arquivo] = _erros_esquema("disciplina", d, arquivo) + _competencias_do_codigo(d, arquivo)

    alvos = [(f"catalogo/{n}.yml", n, True) for n in CATALOGO]
    alvos += [(arq.relative_to(raiz).as_posix(), "verificacao", True)
              for arq in sorted(raiz.glob("exercicios/*/verificacao/*.yml"))]
    alvos += [("plano.yml", "plano", False), ("exercicios/sem-verificacao.yml", "sem-verificacao", False),
              ("registro/estado.yml", "estado", False), ("registro/estudante.yml", "estudante", False),
              ("catalogo/fora-do-plano.yml", "fora-do-plano", False)]
    for arquivo, nome, obrigatorio in alvos:
        caminho = raiz / arquivo
        if not caminho.exists():
            if obrigatorio:
                res[arquivo] = [f"{arquivo}: (raiz): arquivo ausente"]
            continue
        try:
            dados = ler_yaml(caminho.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            res[arquivo] = [f"{arquivo}: (raiz): YAML inválido ({e.__class__.__name__})"]
            continue
        if nome == "plano" and dados is None:
            dados = {}
        res[arquivo] = _erros_esquema(nome, dados, arquivo)
    return res


def validar_esquemas(raiz=RAIZ):
    """Mensagens "<arquivo>: <caminho do campo>: <mensagem>" de todos os arquivos cobertos por schema."""
    return [m for msgs in validar_por_arquivo(raiz).values() for m in msgs]


def main():
    msgs = validar_esquemas(RAIZ)
    for m in msgs:
        print("ERRO:", m)
    if not msgs:
        print("Todos os arquivos validam nos schemas.")
    sys.exit(1 if msgs else 0)


if __name__ == "__main__":
    main()
