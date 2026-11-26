"""Autonomia: problemas-âncora resolvidos sem ajuda, contados ao longo do tempo (design 6.3)."""
import datetime as dt
import pathlib

import re

import yaml

CENARIO = re.compile(r"\bN[0-9]+-[a-z0-9-]+")

INICIO_REGRA = dt.date(2026, 11, 20)  # portões anteriores a esta data não exigem autonomia


def autonomia(linhas, codigo, cfg):
    """(âncoras autônomas distintas, dias distintos) de um módulo."""
    ok = [l for l in linhas if l.get("codigo") == codigo and l.get("tipo_item") == "ancora"
          and l.get("resultado") == "certo" and l.get("ajuda") == 0
          and not str(l.get("observacao", "")).startswith("treino")]
    return len({(l.get("lista"), l.get("item")) for l in ok}), len({l.get("data") for l in ok})


def laboratorio(avs, codigo):
    """(cenários distintos, dias distintos) resolvidos sem consulta, pelas linhas `laboratorio` de avaliacoes.md.

    Cada linha é um cenário conferido por scripts/laboratorio_git.py: Acertos 1 = passou sem consulta;
    o cenário é o primeiro código N<nível>-<nome> das Observações (ADR 0010)."""
    ok = [a for a in avs if a.get("tipo") == "laboratorio" and codigo in a.get("codigos", [])
          and a.get("acertos") == 1 and CENARIO.search(a.get("observacoes") or "")]
    return (len({CENARIO.search(a["observacoes"]).group(0) for a in ok}),
            len({a["data"] for a in ok}))


def _cenarios_do_laboratorio():
    import laboratorio_git
    return set(laboratorio_git.CENARIOS)


def validar_laboratorio(disc, avs, cfg):
    """Cenários desconhecidos nas linhas `laboratorio` e portão de módulo de laboratório sem a evidência."""
    erros, conhecidos = [], _cenarios_do_laboratorio()
    for a in avs:
        if a.get("tipo") != "laboratorio":
            continue
        m = CENARIO.search(a.get("observacoes") or "")
        if not m:
            erros.append(f"avaliações ({a['data']}): linha de laboratório sem o cenário nas Observações (ex.: N4-conflito)")
        elif m.group(0) not in conhecidos:
            erros.append(f"avaliações ({a['data']}): cenário de laboratório desconhecido {m.group(0)}")
    for cod in cfg.get("autonomia_por_laboratorio") or []:
        d = disc.get(cod)
        if not d or d.get("status") not in ("concluida", "dispensada"):
            continue
        n, dias = laboratorio(avs, cod)
        if n < len(conhecidos) or dias < cfg["autonomia_dias_distintos"]:
            erros.append(f"portao-sem-laboratorio: {cod}: {n} de {len(conhecidos)} cenários sem consulta em {dias} dias; "
                         f"o portão exige todos em {cfg['autonomia_dias_distintos']} dias distintos")
    return erros


def validar_autonomia(disc, linhas, cfg):
    erros = [f"plano.yml: autonomia_por_laboratorio: {c} não é um módulo do nivelamento"
             for c in (cfg.get("autonomia_por_laboratorio") or [])
             if c not in disc or disc[c].get("fase") != "nivelamento"]
    for cod, d in disc.items():
        if d.get("status") not in ("concluida", "dispensada") or d.get("fase") != "nivelamento":
            continue
        if cod in (cfg.get("autonomia_por_laboratorio") or []):
            continue  # autonomia pelo laboratório (ADR 0010): validar_laboratorio
        data = (d.get("portao") or {}).get("data")
        try:
            data = data if isinstance(data, dt.date) else dt.date.fromisoformat(str(data))
        except ValueError:
            data = None
        if data and data < INICIO_REGRA:
            continue
        n, dias = autonomia(linhas, cod, cfg)
        if n < cfg["autonomia_n"] or dias < cfg["autonomia_dias_distintos"]:
            erros.append(f"portao-sem-autonomia: {cod}: {n} âncoras autônomas em {dias} dias; "
                         f"o portão exige {cfg['autonomia_n']} em {cfg['autonomia_dias_distintos']} dias distintos")
    return erros


def ancoras_validas(linhas, raiz):
    """Só valem linhas de âncora cuja lista existe e cujo .yml de verificação marca o item como âncora.
    Evita contar como âncora um item que não foi gerado como tal (ou registrado sem lista)."""
    tipos = {}
    for arq in pathlib.Path(raiz).glob("exercicios/*/verificacao/*.yml"):
        try:
            spec = yaml.safe_load(arq.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        for it in spec.get("itens") or []:
            tipos[(spec.get("lista"), it.get("item"))] = it.get("tipo_item")
    validas = []
    for l in linhas:
        if l.get("tipo_item") == "ancora" and tipos.get((l.get("lista"), l.get("item"))) != "ancora":
            l = {**l, "tipo_item": "ancora_nao_confirmada"}  # continua no mapa, mas não conta como autonomia
        validas.append(l)
    return validas
