"""Autonomia: problemas-âncora resolvidos sem ajuda, contados ao longo do tempo (design 6.3)."""
import datetime as dt
import pathlib

import yaml

INICIO_REGRA = dt.date(2026, 11, 20)  # portões anteriores a esta data não exigem autonomia


def autonomia(linhas, codigo, cfg):
    """(âncoras autônomas distintas, dias distintos) de um módulo."""
    ok = [l for l in linhas if l.get("codigo") == codigo and l.get("tipo_item") == "ancora"
          and l.get("resultado") == "certo" and l.get("ajuda") == 0
          and not str(l.get("observacao", "")).startswith("treino")]
    return len({(l.get("lista"), l.get("item")) for l in ok}), len({l.get("data") for l in ok})


def validar_autonomia(disc, linhas, cfg):
    erros = [f"plano.yml: autonomia_por_laboratorio: {c} não é um módulo do nivelamento"
             for c in (cfg.get("autonomia_por_laboratorio") or [])
             if c not in disc or disc[c].get("fase") != "nivelamento"]
    for cod, d in disc.items():
        if d.get("status") not in ("concluida", "dispensada") or d.get("fase") != "nivelamento":
            continue
        if cod in (cfg.get("autonomia_por_laboratorio") or []):
            continue  # autonomia pelo laboratório (ADR 0010); a evidência fica no portão
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
