"""Fixação: sorteio de competências de módulos feitos e avisos de queda (design 6.3 e 6.7)."""
import datetime as dt
import random

from mapa import FEITAS, situacao

PESO_SITUACAO = {"em_queda": 4, "fraca": 3, "em_formacao": 2, "forte": 1, "sem_dados": 2}


def _data_portao(d):
    v = (d.get("portao") or {}).get("data")
    if isinstance(v, dt.date):
        return v
    try:
        return dt.date.fromisoformat(str(v))
    except ValueError:
        return None


def _feitas(disc, comps):
    return [cid for cid, c in comps.items() if disc[c["codigo"]].get("status") in FEITAS]


def sortear_fixacao(disc, comps, linhas, cfg, hoje, n, semente=None):
    """Até n competências distintas de módulos feitos, com peso pela situação e pelo tempo sem prática."""
    rng = random.Random(semente)
    candidatas = _feitas(disc, comps)
    pesos = {}
    for cid in candidatas:
        ls = sorted((l for l in linhas if l.get("competencia") == cid), key=lambda l: l["data"])
        ultima = ls[-1]["data"] if ls else (_data_portao(disc[comps[cid]["codigo"]]) or hoje)
        pesos[cid] = PESO_SITUACAO[situacao(ls, cfg, True)] + max(0, (hoje - ultima).days) // 7
    escolhidas = []
    while candidatas and len(escolhidas) < n:
        cid = rng.choices(candidatas, weights=[pesos[c] for c in candidatas])[0]
        escolhidas.append(cid)
        candidatas.remove(cid)
    return escolhidas


def avisos_fixacao(disc, comps, linhas, cfg, hoje):
    avisos = []
    for cod, d in disc.items():
        if d.get("status") not in FEITAS:
            continue
        do_modulo = sorted((l for l in linhas if l.get("codigo") == cod), key=lambda l: l["data"])
        janela = do_modulo[-cfg["fixacao_janela"]:]
        falhas = sum(1 for l in janela if l["resultado"] != "certo" or l["ajuda"] > 0)
        if len(janela) >= 2 and falhas >= 2:
            avisos.append(f"autonomia-em-queda: {cod}: {falhas} das últimas {len(janela)} respostas com erro ou ajuda; "
                          f"faça uma revisão e, se ficar abaixo de 70%, mude o status para em_revisao")
        portao = _data_portao(d)
        for cid in [c for c in comps if comps[c]["codigo"] == cod]:
            ls = [l for l in do_modulo if l.get("competencia") == cid]
            ref = ls[-1]["data"] if ls else portao
            if ref and (hoje - ref).days > cfg["fixacao_vencida_dias"]:
                avisos.append(f"fixacao-vencida: {cid}: {(hoje - ref).days} dias sem prática")
    return avisos
