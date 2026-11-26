#!/usr/bin/env python3
"""Valida o plano de estudos e gera PROGRESSO.md.

Uso:
    python scripts/progresso.py              # valida e reescreve PROGRESSO.md
    python scripts/progresso.py --checar     # só valida; sai com erro se houver problema
    python scripts/progresso.py --limite 3   # sobrepõe o limite de plano.yml
"""
import argparse
import datetime as dt
import pathlib
import re
import sys

import yaml

from autonomia import ancoras_validas, autonomia, validar_autonomia
from config import PADROES, carregar_config
from fixacao import avisos_fixacao, sortear_fixacao
from mapa import gerar_mapa
from verificar import avisos_intercalacao, verificar
from competencias import competencias, validar_competencias
from respostas import carregar_respostas, conferir_resumos, validar_respostas
from catalogo import avisos_catalogo, validar_catalogo
from diagrama import diagrama_desatualizado
from esquema import validar_esquemas
from estado import STATUS_VALIDOS, aplicar_estado, carregar_estado, validar_estado

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIR_DISC = RAIZ / "disciplinas"
REGISTRO = RAIZ / "registro" / "semanal.md"
AVALIACOES = RAIZ / "registro" / "avaliacoes.md"
RESPOSTAS = RAIZ / "registro" / "respostas.csv"
CONFIG = RAIZ / "plano.yml"
SAIDA = RAIZ / "PROGRESSO.md"
SAIDA_MAPA = RAIZ / "MAPA.md"
DIR_EXERCICIOS = RAIZ / "exercicios"
RITMO_REFERENCIA = 24  # h por semana, usado enquanto não houver registro semanal

FEITAS = {"concluida", "dispensada", "em_revisao"}
ABERTOS = {"em_andamento", "no_portao"}
TIPOS_AVALIACAO = {"diagnostico", "exercicios", "saida", "revisao"}
REVISOES_DIAS = [7, 30, 90]
ROTULO = {
    "concluida": "🟢 Concluída",
    "dispensada": "⏭️ Dispensada",
    "em_revisao": "🔵 Em revisão",
    "no_portao": "🟠 No portão",
    "em_andamento": "🟡 Em andamento",
    "liberada": "⚪ Liberada",
    "bloqueada": "🔒 Bloqueada",
}
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
CODIGO = re.compile(r"\b([A-Z]{1,2}\d+)\b")


def carregar_disciplinas(estado=None):
    """Cabeçalhos de disciplinas/ com o andamento de registro/estado.yml aplicado (padrões se ele não existir)."""
    disc = {}
    for arq in sorted(DIR_DISC.glob("*.md")):
        m = FM.match(arq.read_text(encoding="utf-8"))
        if not m:
            raise SystemExit(f"{arq.name}: cabeçalho YAML ausente")
        d = yaml.safe_load(m.group(1))
        d["arquivo"] = f"disciplinas/{arq.name}"
        disc[d["codigo"]] = d
    return aplicar_estado(disc, carregar_estado(RAIZ) if estado is None else estado)


def numero(txt):
    txt = str(txt).strip().replace(",", ".")
    try:
        return float(txt) if txt else 0.0
    except ValueError:
        return 0.0


def linhas_tabela(caminho, minimo):
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        cel = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(cel) >= minimo and re.match(r"\d{4}-\d{2}-\d{2}$", cel[0]):
            yield cel


def carregar_registro():
    """Semana | Manhã | Almoço | Noite | Fim de semana | Disciplinas | Observações.
    Na coluna Disciplinas: "NM3: 6, NL1: 4,5"."""
    semanas, horas = [], {}
    for cel in linhas_tabela(REGISTRO, 6):
        semanas.append((cel[0], sum(numero(c) for c in cel[1:5])))
        for cod, h in re.findall(r"([A-Z]{1,2}\d+)\s*:\s*(\d+(?:[.,]\d+)?)", cel[5]):
            horas[cod] = horas.get(cod, 0.0) + numero(h)
    return semanas, horas


def carregar_avaliacoes():
    """Data | Códigos | Tipo | Acertos | Total | Observações | Lista (opcional).
    Códigos: um ou mais, separados por vírgula (uma revisão mista cobre vários).
    Lista: caminho da lista corrigida; liga o resumo às linhas de registro/respostas.csv."""
    avs = []
    for cel in linhas_tabela(AVALIACOES, 5):
        total = numero(cel[4])
        avs.append({
            "data": dt.date.fromisoformat(cel[0]),
            "codigos": CODIGO.findall(cel[1]),
            "tipo": cel[2].lower().replace("ã", "a").replace("í", "i").replace("é", "e"),
            "pct": round(100 * numero(cel[3]) / total) if total else None,
            "acertos": numero(cel[3]),
            "total": total,
            "lista": cel[6] if len(cel) > 6 and cel[6] else None,
        })
    return avs


def feita(d):
    return d["status"] in FEITAS


def status_exibido(d, disc):
    if d["status"] != "nao_iniciada":
        return d["status"]
    ok = all(feita(disc[p]) for p in d["prerequisitos"] if p in disc)
    return "liberada" if ok else "bloqueada"


def data_portao(d):
    v = (d.get("portao") or {}).get("data")
    if isinstance(v, dt.date):
        return v
    try:
        return dt.date.fromisoformat(str(v))
    except (TypeError, ValueError):
        return None


def revisoes_vencidas(disc, avs, hoje):
    """Para cada disciplina feita, a próxima revisão espaçada (7, 30 e 90 dias após o portão)."""
    venc = []
    for c, d in disc.items():
        dp = data_portao(d)
        if not feita(d) or not dp:
            continue
        feitas = sum(1 for a in avs if a["tipo"] == "revisao" and c in a["codigos"] and a["data"] > dp)
        if feitas >= len(REVISOES_DIAS):
            continue
        prox = dp + dt.timedelta(days=REVISOES_DIAS[feitas])
        if prox <= hoje:
            venc.append((prox, c))
    return sorted(venc)


def ciclos(disc):
    """Devolve cada dependência circular uma vez, como lista de códigos."""
    achados, cor = [], {}

    def visitar(c, caminho):
        cor[c] = 1
        for p in disc[c]["prerequisitos"]:
            if p not in disc:
                continue
            if cor.get(p) == 1:
                ciclo = caminho[caminho.index(p):] + [p]
                corpo = ciclo[:-1]
                i = corpo.index(min(corpo))
                norm = corpo[i:] + corpo[:i]
                if norm not in [a[:-1] for a in achados]:
                    achados.append(norm + [norm[0]])
            elif not cor.get(p):
                visitar(p, caminho + [p])
        cor[c] = 2

    for c in sorted(disc):
        if not cor.get(c):
            visitar(c, [c])
    return achados


LINK = re.compile(r"\]\(([^)\s]+)\)")


def links_quebrados():
    ruins = []
    for arq in sorted(RAIZ.rglob("*.md")):
        if {".git", ".superpowers", "benchmark"} & set(arq.relative_to(RAIZ).parts) or arq == SAIDA:
            continue
        for alvo in LINK.findall(arq.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+:", alvo) or alvo.startswith("#"):
                continue
            caminho = alvo.split("#")[0]
            if caminho and not (arq.parent / caminho).resolve().exists():
                ruins.append((arq.relative_to(RAIZ).as_posix(), alvo))
    return ruins


def listas_sem_gabarito():
    problemas = []
    if not DIR_EXERCICIOS.exists():
        return problemas
    for lista in sorted(DIR_EXERCICIOS.glob("*/*.md")):
        gab = lista.parent / "gabaritos" / lista.name
        nome = lista.relative_to(RAIZ).as_posix()
        if not gab.exists():
            problemas.append(f"{nome}: lista sem gabarito")
            continue
        nl = [int(n) for n in re.findall(r"^(\d+)\. ", lista.read_text(encoding="utf-8"), re.M)]
        ng = [int(n) for n in re.findall(r"^\| (\d+) \|", gab.read_text(encoding="utf-8"), re.M)]
        if sorted(nl) != sorted(ng):
            faltam = sorted(set(nl) - set(ng))
            sobram = sorted(set(ng) - set(nl))
            det = []
            if faltam:
                det.append(f"sem resposta: {', '.join(map(str, faltam[:10]))}")
            if sobram:
                det.append(f"resposta sem exercício: {', '.join(map(str, sobram[:10]))}")
            if not det:
                det.append("numeração repetida")
            problemas.append(f"{nome}: lista e gabarito não batem ({'; '.join(det)})")
    return problemas


def respostas_para_mapa(respostas, erros):
    """O mapa descarta só as linhas do CSV com erro; erro de arquivo inteiro descarta todas."""
    ruins = set()
    for e in erros:
        if e.startswith("csv-invalido: linha "):
            ruins.add(int(e.split("linha ", 1)[1].split(",")[0].split(":")[0]))
        elif e.startswith("csv-invalido"):
            return []
    return [l for l in respostas if l.get("_linha") not in ruins]


def verificacoes():
    """Roda scripts/verificar.py sobre cada exercicios/<código>/verificacao/*.yml."""
    if not DIR_EXERCICIOS.exists():
        return []
    return [m for arq in sorted(DIR_EXERCICIOS.glob("*/verificacao/*.yml")) for m in verificar(arq, RAIZ)]


def validar(disc, horas, avs, limite, respostas=(), autonomia_linhas=None, cfg=None, fixacao_linhas=None, hoje=None,
            estado=None):
    erros, avisos = [], []
    erros.extend(validar_estado(disc, estado or {}, RAIZ))
    for c, d in disc.items():
        if d["status"] not in STATUS_VALIDOS:
            erros.append(f"{c}: status inválido '{d['status']}'")
        for p in d["prerequisitos"]:
            if p not in disc:
                erros.append(f"{c}: pré-requisito desconhecido {p}")
                continue
            if disc[p]["semestre_fim"] > d["semestre_inicio"]:
                erros.append(f"{c}: começa no semestre {d['semestre_inicio']}, mas {p} só termina no {disc[p]['semestre_fim']}")
            if d["status"] != "nao_iniciada" and not feita(disc[p]):
                erros.append(f"{c}: está '{d['status']}' sem o portão de {p} cumprido")
        if feita(d):
            pt = d.get("portao") or {}
            if not pt.get("data") or not pt.get("resultado"):
                erros.append(f"{c}: '{d['status']}' sem data e resultado do portão")
        prev, real = d["horas_previstas"], horas.get(c, 0)
        if real > 1.5 * prev:
            avisos.append(f"{c}: {real:g} h registradas, 50% acima das {prev} h previstas; vale revisar o método ou o plano")
    for cod in horas:
        if cod not in disc:
            erros.append(f"registro semanal: código desconhecido {cod}")
    for a in avs:
        if a["tipo"] not in TIPOS_AVALIACAO:
            erros.append(f"avaliações ({a['data']}): tipo '{a['tipo']}' inválido; use diagnostico, exercicios, saida ou revisao")
        for cod in a["codigos"]:
            if cod not in disc:
                erros.append(f"avaliações ({a['data']}): código desconhecido {cod}")
        if a["tipo"] == "revisao" and a["pct"] is not None and a["pct"] < 70:
            for cod in a["codigos"]:
                if cod in disc and disc[cod]["status"] in ("concluida", "dispensada"):
                    avisos.append(f"{cod}: revisão de {a['data']} com {a['pct']}%; mude o status para em_revisao")
    erros.extend(validar_competencias(disc))
    erros.extend(validar_respostas(list(respostas), competencias(disc), RAIZ))
    erros.extend(conferir_resumos(avs, list(respostas)))
    linhas_aut = ancoras_validas(list(respostas), RAIZ) if autonomia_linhas is None else autonomia_linhas
    erros.extend(validar_autonomia(disc, linhas_aut, cfg or PADROES))
    avisos.extend(avisos_fixacao(disc, competencias(disc), list(respostas) if fixacao_linhas is None else fixacao_linhas,
                                 cfg or PADROES, hoje or dt.date.today()))
    for ciclo in ciclos(disc):
        erros.append("dependência circular: " + " → ".join(ciclo))
    for origem, alvo in links_quebrados():
        erros.append(f"{origem}: link quebrado para {alvo}")
    erros.extend(listas_sem_gabarito())
    erros.extend(verificacoes())
    if DIR_EXERCICIOS.exists():
        for arq in sorted(DIR_EXERCICIOS.glob("*/verificacao/*.yml")):
            try:
                avisos.extend(avisos_intercalacao(yaml.safe_load(arq.read_text(encoding="utf-8")) or {}))
            except yaml.YAMLError:
                pass
    abertas = [c for c, d in disc.items() if d["status"] in ABERTOS]
    if len(abertas) > limite:
        avisos.append(f"{len(abertas)} disciplinas abertas ({', '.join(abertas)}); o limite é {limite}")
    return erros, avisos


def validar_repositorio(disc, raiz):
    """Regras que olham o repositório inteiro: schemas, catálogo e diagrama gerado."""
    erros = validar_esquemas(raiz) + validar_catalogo(disc, raiz) + diagrama_desatualizado(raiz)
    return erros, avisos_catalogo(disc)


def cabecalhos_invalidos(raiz):
    """Erros de schema em disciplinas/: com eles o resto do script não roda (campos que o código lê podem faltar)."""
    return [e for e in validar_esquemas(raiz) if e.startswith("disciplinas/")]


def fator_diagnostico(d):
    """Fração das horas máximas que o diagnóstico indica ser necessária."""
    dg = d.get("diagnostico")
    if dg is None or dg < 60:
        return 1.0
    return 0.2 if dg >= 85 else 0.5


def horas_restantes(d, horas):
    """Estimativa de horas que ainda faltam em um módulo do nivelamento."""
    if feita(d):
        return 0.0
    estimada = d["horas_previstas"] * fator_diagnostico(d)
    falta = estimada - horas.get(d["codigo"], 0)
    return max(falta, 0.1 * d["horas_previstas"])


def ritmo_semanal(semanas):
    if not semanas:
        return RITMO_REFERENCIA, "referência de 24 h por semana, até haver registros"
    ult = semanas[-4:]
    media = sum(t for _, t in ult) / len(ult)
    if media <= 0:
        return RITMO_REFERENCIA, "referência de 24 h por semana (as últimas semanas registradas somam zero)"
    return media, f"média das últimas {len(ult)} semanas registradas"


def fmt_h(x):
    return f"{x:g}".replace(".", ",")


def ultima_avaliacao(c, avs):
    da = [a for a in avs if c in a["codigos"] and a["pct"] is not None]
    if not da:
        return "—"
    a = da[-1]
    return f"{a['tipo']} {a['pct']}% ({a['data'].strftime('%d/%m')})"


def gerar(disc, semanas, horas, avs, erros, avisos, limite, sem_atual, hoje):
    ordem = sorted(disc.values(), key=lambda d: d["ordem"])
    exib = {d["codigo"]: status_exibido(d, disc) for d in ordem}

    def link(d):
        return f"[{d['codigo']} {d['nome']}]({d['arquivo']})"

    def pre_cel(d):
        return ", ".join(f"{p} {'✅' if p in disc and feita(disc[p]) else '⬜'}" for p in d["prerequisitos"]) or "—"

    out = [
        "# Progresso", "",
        f"Gerado por `scripts/progresso.py` em {hoje.isoformat()}. Não edite à mão: atualize o andamento "
        "em `registro/estado.yml` e os demais registros, e rode o script.", "",
        "## Resumo", "",
        "| Status | Nivelamento | Plano principal |",
        "| --- | --- | --- |",
    ]
    for chave in ["concluida", "dispensada", "em_revisao", "no_portao", "em_andamento", "liberada", "bloqueada"]:
        niv = sum(1 for d in ordem if d["fase"] == "nivelamento" and exib[d["codigo"]] == chave)
        pri = sum(1 for d in ordem if d["fase"] != "nivelamento" and exib[d["codigo"]] == chave)
        out.append(f"| {ROTULO[chave]} | {niv} | {pri} |")
    for fase, nome in [("nivelamento", "nivelamento (horas máximas)"), (None, "plano principal")]:
        sel = [d for d in ordem if (d["fase"] == "nivelamento") == (fase == "nivelamento")]
        out.append("")
        out.append(f"Horas no {nome}: {fmt_h(sum(horas.get(d['codigo'], 0) for d in sel))} de "
                   f"{sum(d['horas_previstas'] for d in sel)} previstas.")
    if semanas:
        ult = semanas[-4:]
        out.append("")
        out.append(f"Média das últimas {len(ult)} semanas registradas: "
                   f"{fmt_h(round(sum(t for _, t in ult) / len(ult), 1))} h por semana.")
    niv_todos = [d for d in ordem if d["fase"] == "nivelamento"]
    if niv_todos:
        falta = sum(horas_restantes(d, horas) for d in niv_todos)
        maximo = sum(d["horas_previstas"] for d in niv_todos)
        ritmo, origem = ritmo_semanal(semanas)
        out.append("")
        if falta == 0:
            out.append("**Previsão do nivelamento:** concluído.")
        else:
            semanas_faltam = falta / ritmo
            fim = hoje + dt.timedelta(weeks=semanas_faltam)
            out.append(f"**Previsão do nivelamento:** faltam cerca de {fmt_h(round(falta))} h, de {maximo} h no máximo. "
                       f"A {fmt_h(round(ritmo, 1))} h por semana ({origem}), são cerca de {fmt_h(round(semanas_faltam))} semanas: "
                       f"término por volta de {fim.strftime('%d/%m/%Y')}.")
            out.append("")
            out.append("A estimativa usa o diagnóstico de cada módulo: 20% das horas máximas com 85% ou mais, "
                       "50% entre 60% e 84%, e 100% abaixo de 60% ou sem diagnóstico, descontadas as horas já registradas.")
    out.append("")

    abertas = [d for d in ordem if d["status"] in ABERTOS]
    liberadas = [d for d in ordem if exib[d["codigo"]] == "liberada"]
    no_prazo = [d for d in liberadas if d["semestre_inicio"] <= sem_atual]
    adiante = [d for d in liberadas if sem_atual < d["semestre_inicio"] <= sem_atual + 1]
    atrasadas = [d for d in ordem if d["semestre_fim"] < sem_atual and not feita(d)]
    venc = revisoes_vencidas(disc, avs, hoje)
    etapa = "Nivelamento" if sem_atual == 0 else f"Semestre {sem_atual}"
    out += ["## Agora", "", f"**Etapa atual:** {etapa}", "",
            f"**Abertas ({len(abertas)} de {limite}):** " + (", ".join(link(d) for d in abertas) or "nenhuma"), "",
            "**Liberadas desta etapa, na ordem do plano:** " + (", ".join(link(d) for d in no_prazo) or "nenhuma"), "",
            "**Liberadas da próxima etapa, para adiantar com folga:** " + (", ".join(link(d) for d in adiante) or "nenhuma")]
    if atrasadas:
        out += ["", "**Atrasadas (deviam ter terminado):** " + ", ".join(link(d) for d in atrasadas)]
    out += ["", "**Revisões espaçadas vencidas:** "
            + (", ".join(f"{c} (desde {p.strftime('%d/%m')})" for p, c in venc) or "nenhuma"), ""]

    if erros or avisos:
        out += ["## Problemas", ""]
        out += [f"- ❌ {e}" for e in erros]
        out += [f"- ⚠️ {a}" for a in avisos]
        out.append("")

    niv = [d for d in ordem if d["fase"] == "nivelamento"]
    if niv:
        out += ["## Fase 0 — Nivelamento", ""]
        for bloco in sorted({d["bloco"] for d in niv}, key=lambda b: "ABCDELF".find(b[0])):
            out += [f"### Bloco {bloco}", "",
                    "| Módulo | Pré-req. | Status | Horas (máx / real / faltam) | Diagnóstico | Última avaliação | Portão |",
                    "| --- | --- | --- | --- | --- | --- | --- |"]
            for d in [d for d in niv if d["bloco"] == bloco]:
                c = d["codigo"]
                dg = f"{d['diagnostico']}%" if d.get("diagnostico") is not None else "—"
                res = (d.get("portao") or {}).get("resultado") or "—"
                out.append(f"| {link(d)} | {pre_cel(d)} | {ROTULO[exib[c]]} | {d['horas_previstas']} / "
                           f"{fmt_h(horas.get(c, 0))} / {fmt_h(round(horas_restantes(d, horas)))} | {dg} | "
                           f"{ultima_avaliacao(c, avs)} | {res} |")
            out.append("")

    for fase, titulo in [("graduacao", "Graduação"), ("pos_formatura", "Depois da formatura")]:
        out += [f"## {titulo}", ""]
        for s in sorted({d["semestre_inicio"] for d in ordem if d["fase"] == fase}):
            out += [f"### Semestre {s}", "",
                    "| Disciplina | Sem. | Pré-req. | Status | Horas (prev / real) | Portão | Evidência |",
                    "| --- | --- | --- | --- | --- | --- | --- |"]
            for d in [d for d in ordem if d["fase"] == fase and d["semestre_inicio"] == s]:
                c = d["codigo"]
                sem = str(d["semestre_inicio"]) if d["semestre_inicio"] == d["semestre_fim"] else f"{d['semestre_inicio']}–{d['semestre_fim']}"
                pt = d.get("portao") or {}
                ev = f"[link]({pt['evidencia']})" if pt.get("evidencia") else "—"
                out.append(f"| {link(d)} | {sem} | {pre_cel(d)} | {ROTULO[exib[c]]} | "
                           f"{d['horas_previstas']} / {fmt_h(horas.get(c, 0))} | {pt.get('resultado') or '—'} | {ev} |")
            out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checar", action="store_true", help="só valida, sem reescrever PROGRESSO.md")
    ap.add_argument("--limite", type=int, help="máximo de disciplinas abertas; sobrepõe plano.yml")
    ap.add_argument("--sortear-fixacao", type=int, metavar="N", help="sorteia N competências de módulos feitos para fixação")
    a = ap.parse_args()
    cfg = carregar_config(CONFIG)
    limite = a.limite or cfg.get("limite_abertas", 2)
    sem_atual = cfg.get("semestre_atual", 0)
    hoje = dt.date.today()

    invalidos = cabecalhos_invalidos(RAIZ)
    if invalidos:
        for e in invalidos:
            print("ERRO:", e)
        print("ERRO: corrija os cabeçalhos acima; as demais verificações só rodam com eles válidos.")
        if any("campo de andamento" in e for e in invalidos):
            print("ERRO: andamento no cabeçalho: rode python scripts/migrar_estado.py (veja docs/fluxo-git.md).")
        sys.exit(1)
    estado = carregar_estado(RAIZ)
    disc = carregar_disciplinas(estado)
    semanas, horas = carregar_registro()
    avs = carregar_avaliacoes()
    respostas = carregar_respostas(RESPOSTAS)
    if a.sortear_fixacao:
        comps = competencias(disc)
        sorteio = sortear_fixacao(disc, comps, respostas_para_mapa(respostas, []), cfg, hoje, a.sortear_fixacao)
        for cid in sorteio:
            print(f"{cid}\t{comps[cid]['nome']}")
        if not sorteio:
            print("Nenhum módulo concluído ainda: não há o que fixar.")
        sys.exit(0)
    erros, avisos = validar(disc, horas, avs, limite, respostas, cfg=cfg, estado=estado)
    erros_repo, avisos_repo = validar_repositorio(disc, RAIZ)
    erros += erros_repo
    avisos += avisos_repo
    for e in erros:
        print("ERRO:", e)
    for w in avisos:
        print("AVISO:", w)
    if not a.checar:
        SAIDA.write_text(gerar(disc, semanas, horas, avs, erros, avisos, limite, sem_atual, hoje) + "\n", encoding="utf-8")
        print(f"PROGRESSO.md atualizado: {len(disc)} disciplinas e módulos.")
        usadas = ancoras_validas(respostas_para_mapa(respostas, erros), RAIZ)
        SAIDA_MAPA.write_text(gerar_mapa(disc, competencias(disc), usadas, cfg, hoje) + "\n", encoding="utf-8")
        print("MAPA.md atualizado" + ("." if usadas or not respostas else " sem respostas: corrija o registro/respostas.csv"))
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
