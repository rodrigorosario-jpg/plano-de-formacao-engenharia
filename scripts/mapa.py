"""Mapa de deficiências: situação de cada competência a partir de registro/respostas.csv."""
from collections import Counter

from autonomia import autonomia

PESO = {"certo": 1.0, "parcial": 0.5}
FEITAS = {"concluida", "dispensada", "em_revisao"}
ROTULO = {
    "forte": "🟢 forte",
    "em_formacao": "🟡 em_formacao",
    "fraca": "🔴 fraca",
    "em_queda": "🟠 em_queda",
    "sem_dados": "⚪ sem_dados",
}
ORDEM = ["em_queda", "fraca", "em_formacao", "forte", "sem_dados"]


def _pct(linhas, cond):
    return 100 * sum(cond(l) for l in linhas) / len(linhas)


def situacao(linhas, cfg, concluido):
    """linhas: respostas de uma competência, em ordem de data."""
    janela = sorted(linhas, key=lambda l: l["data"])[-cfg["mapa_janela"]:]
    acerto = _pct(janela, lambda l: PESO.get(l["resultado"], 0.0)) if janela else 0
    recentes = janela[-3:] + [l for l in janela if janela and l["data"] == janela[-1]["data"]]
    if any(l["classe_erro"] == "conceito" for l in recentes):
        s = "fraca"
    elif len(janela) < 3:
        s = "sem_dados"
    elif acerto < cfg["mapa_pct_fraca"]:
        s = "fraca"
    elif (len(janela) >= cfg["mapa_min_forte"] and acerto >= cfg["mapa_pct_forte"]
          and _pct(janela, lambda l: l["ajuda"] == 0) >= cfg["mapa_pct_sem_ajuda_forte"]):
        s = "forte"
    else:
        s = "em_formacao"
    return "em_queda" if concluido and s == "fraca" else s


def lacunas_prerequisitos(disc, comps, sit):
    """Pares (competência fraca, competência fraca ou em formação de um pré-requisito direto)."""
    pares = []
    for cid, s in sit.items():
        if s not in ("fraca", "em_queda"):
            continue
        pre = disc[comps[cid]["codigo"]].get("prerequisitos", [])
        for outra, s2 in sit.items():
            if comps[outra]["codigo"] in pre and s2 in ("fraca", "em_queda", "em_formacao"):
                pares.append((cid, outra))
    return sorted(pares)


def gerar_mapa(disc, comps, linhas, cfg, hoje):
    por_comp = {cid: [l for l in linhas if l.get("competencia") == cid] for cid in comps}
    sit = {cid: situacao(ls, cfg, disc[comps[cid]["codigo"]]["status"] in FEITAS) for cid, ls in por_comp.items()}
    cont = Counter(sit.values())
    out = [
        "# Mapa de deficiências",
        "",
        f"Gerado por scripts/progresso.py em {hoje.isoformat()}, a partir de `registro/respostas.csv`; não edite à mão.",
        f"Situação calculada sobre as últimas {cfg['mapa_janela']} respostas de cada competência (regras em `docs/skills/design.md`, seção 6.2).",
        "",
        "## Resumo",
        "",
        "| Situação | Competências |",
        "| --- | --- |",
    ]
    out += [f"| {ROTULO[s]} | {cont.get(s, 0)} |" for s in ORDEM]
    out += ["", "## Por módulo", ""]
    modulos = sorted({c["codigo"] for c in comps.values()}, key=lambda c: disc[c].get("ordem", 0))
    for cod in modulos:
        n, dias = autonomia(linhas, cod, cfg)
        if cod in (cfg.get("autonomia_por_laboratorio") or []):
            linha_aut = "Autonomia: pelo laboratório (scripts/laboratorio_git.py), registrada na evidência do portão"
        else:
            linha_aut = f"Autonomia: {n}/{cfg['autonomia_n']} âncoras em {dias}/{cfg['autonomia_dias_distintos']} dias"
        out += [f"### {cod} · {disc[cod].get('nome', '')}", "", linha_aut, "",
                "| Competência | Situação | Acertos recentes | Erro mais frequente | Última resposta |",
                "| --- | --- | --- | --- | --- |"]
        for cid in [c for c in comps if comps[c]["codigo"] == cod]:
            ls = sorted(por_comp[cid], key=lambda l: l["data"])[-cfg["mapa_janela"]:]
            ac = f"{sum(PESO.get(l['resultado'], 0.0) for l in ls):g}/{len(ls)}" if ls else "—"
            erros = Counter(l["classe_erro"] for l in ls if l["classe_erro"])
            freq = erros.most_common(1)[0][0] if erros else "—"
            ult = ls[-1]["data"].isoformat() if ls else "—"
            out.append(f"| {cid} {comps[cid]['nome']} | {ROTULO[sit[cid]]} | {ac} | {freq} | {ult} |")
        out.append("")
    out += ["## Lacunas prováveis em pré-requisitos", ""]
    pares = lacunas_prerequisitos(disc, comps, sit)
    if pares:
        out += ["| Competência com dificuldade | Possível origem no pré-requisito |", "| --- | --- |"]
        out += [f"| {a} {comps[a]['nome']} | {b} {comps[b]['nome']} ({ROTULO[sit[b]]}) |" for a, b in pares]
    else:
        out.append("Nenhuma no momento.")
    return "\n".join(out)
