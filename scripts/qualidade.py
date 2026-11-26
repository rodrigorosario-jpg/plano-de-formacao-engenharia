#!/usr/bin/env python3
"""Relatório de qualidade do Knowledge Core: a tabela "Critérios para o Core evoluir além do Marco 4"
da auditoria, medida no repositório. Só lê arquivos; imprime Markdown e não grava nada.

Uso:
    python scripts/qualidade.py
"""
import pathlib
from collections import Counter

from catalogo import carregar_catalogo, codigos_repetidos, referencias, situacao_listas, _lista
from esquema import CAMPOS_ANDAMENTO, CAMPOS_ANDAMENTO_PORTAO, RAIZ, carregar_cabecalhos, validar_por_arquivo

FASES = [("nivelamento", "nivelamento"), ("graduacao", "graduação"), ("pos_formatura", "depois da formatura")]


def _pct(parte, total):
    return f"{round(100 * parte / total)}%" if total else "—"


def medir(raiz=RAIZ):
    raiz = pathlib.Path(raiz)
    cabecalhos = carregar_cabecalhos(raiz)
    lidos = [(a, d) for a, d, e in cabecalhos if isinstance(d, dict)]
    disc = {d.get("codigo"): {**d, "arquivo": a} for a, d in lidos}
    cat = carregar_catalogo(raiz)

    ids = Counter()
    repetidos = codigos_repetidos(raiz)
    n_disc = sum(1 for a, d in lidos if d.get("codigo"))
    ids_unicos = n_disc - sum(len(v) for v in repetidos.values())
    for _, d in lidos:
        for c in d.get("competencias") or []:
            if isinstance(c, dict):
                ids[("competencia", c.get("id"))] += 1
    for nome, chave in (("unidades", "unidades"), ("projetos", "projetos")):
        for x in _lista(cat[nome], chave):
            ids[(nome, x.get("codigo"))] += 1
    total_ids = n_disc + sum(ids.values())
    ids_unicos += sum(n for n in ids.values() if n == 1)

    por_arquivo = validar_por_arquivo(raiz)
    refs = referencias(disc, raiz, cat)
    _, listas = situacao_listas(raiz)
    andamento = [a for a, d in lidos
                 if any(k in d for k in CAMPOS_ANDAMENTO)
                 or any(k in (d.get("portao") or {}) for k in CAMPOS_ANDAMENTO_PORTAO)]
    competencias = {}
    for fase, _ in FASES:
        da_fase = [d for _, d in lidos if d.get("fase") == fase]
        com = [d for d in da_fase if d.get("competencias")]
        competencias[fase] = (len(com), len(da_fase), sum(len(d["competencias"]) for d in com))
    return {
        "ids": (ids_unicos, total_ids),
        "esquema": (sum(1 for m in por_arquivo.values() if not m), len(por_arquivo)),
        "referencias": (sum(1 for r in refs if r[3]), len(refs)),
        "listas": (sum(1 for _, s in listas if s == "verificacao"), sum(1 for _, s in listas if s == "excecao"), len(listas)),
        "andamento": (len(andamento), len(lidos)),
        "progresso_separado": not andamento,
        "competencias": competencias,
    }


def gerar_relatorio(raiz=RAIZ):
    m = medir(raiz)
    ui, ti = m["ids"]
    ok, ta = m["esquema"]
    rr, tr = m["referencias"]
    lv, le, tl = m["listas"]
    na, tc = m["andamento"]
    comp = "; ".join(f"{nome}: {com} de {tot} arquivos com competências ({n} no total)"
                     for (fase, nome), (com, tot, n) in zip(FASES, m["competencias"].values()))
    linhas = [
        ("Itens com ID único verificado", f"{_pct(ui, ti)} ({ui} de {ti}: disciplinas, competências, unidades e projetos)", "100%"),
        ("Metadados validados por schema", f"{_pct(ok, ta)} ({ok} de {ta} arquivos)", "100%"),
        ("Referências a unidades e projetos resolvidas", f"{_pct(rr, tr)} ({rr} de {tr})", "100%"),
        ("Listas com verificação ou exceção registrada", f"{_pct(lv + le, tl)} ({lv + le} de {tl}: {lv} com verificação, {le} em exceção)",
         "100% ou exceção registrada"),
        ("Progresso separado do conhecimento",
         "Sim" if m["progresso_separado"] else f"Não ({na} de {tc} cabeçalhos têm campos de andamento)", "Sim"),
        ("Competências por fase", comp, "—"),
    ]
    out = ["# Relatório de qualidade", "",
           "Critérios para o Core evoluir além do Marco 4 (auditoria, seção 10), medidos no repositório por "
           "`scripts/qualidade.py`.", "",
           "| Critério | Hoje | Meta |", "| --- | --- | --- |"]
    out += [f"| {a} | {b} | {c} |" for a, b, c in linhas]
    out += ["", "Não medidos aqui: fatos de currículo com uma só origem e histórico preservado."]
    return "\n".join(out) + "\n"


def main():
    print(gerar_relatorio(RAIZ), end="")


if __name__ == "__main__":
    main()
