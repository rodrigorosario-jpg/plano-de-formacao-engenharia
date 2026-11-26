#!/usr/bin/env python3
"""Gera o diagrama Mermaid do nivelamento a partir dos cabeçalhos YAML de disciplinas/.

O diagrama fica em NIVELAMENTO.md, entre os marcadores INICIO e FIM.

    python scripts/diagrama.py            reescreve o trecho
    python scripts/diagrama.py --checar   só confere; sai com 1 se estiver desatualizado
"""
import argparse
import pathlib
import re
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ARQUIVO = "NIVELAMENTO.md"
INICIO = "<!-- diagrama:inicio -->"
FIM = "<!-- diagrama:fim -->"
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)

# Rótulos de apresentação. Módulo ou bloco que não estiver aqui usa o nome do cabeçalho.
ROTULO_BLOCO = {
    "A": "A · Aritmética (Fundamental)",
    "F": "F · Física básica",
}
ROTULO_MODULO = {
    "NG1": "Git essencial",
    "NM0": "Operações fundamentais",
    "NM1": "Inteiros",
    "NM2": "Frações e decimais",
    "NM3": "Potências e raízes",
    "NM4": "Expressões",
    "NM5": "Proporção e porcentagem",
    "NM6": "1º grau",
    "NM7": "Fatoração",
    "NM8": "2º grau",
    "NM9": "Funções",
    "NM10": "Polinômios e complexos",
    "NM11": "Exponencial e log",
    "NM12": "PA e PG",
    "NM13": "Geometria plana",
    "NM14": "Trigonometria",
    "NM15": "Espacial e analítica",
    "NM16": "Combinatória",
    "NM17": "Probabilidade e estatística",
    "NM18": "Matrizes e sistemas",
    "NL1": "Lógica",
    "NL2": "Algoritmos",
    "NL3": "Controle e teste de mesa",
    "NL4": "Funções e listas em Python",
    "NF1": "Unidades e vetores",
    "NF2": "Cinemática",
    "NF3": "Dinâmica e energia",
    "NF4": "Térmica, ondas e óptica",
    "NF5": "Eletricidade",
}


def carregar_modulos(raiz):
    """Cabeçalhos dos módulos de fase `nivelamento`, por código."""
    mods = {}
    for arq in sorted((pathlib.Path(raiz) / "disciplinas").glob("*.md")):
        m = FM.match(arq.read_text(encoding="utf-8"))
        if not m:
            continue
        d = yaml.safe_load(m.group(1)) or {}
        if d.get("fase") == "nivelamento":
            mods[d["codigo"]] = d
    return mods


def _texto(s):
    return str(s).replace('"', "#quot;")


def _id_bloco(bloco):
    return bloco.split("·")[0].strip()


def gerar_diagrama(raiz):
    """Bloco ```mermaid``` completo: um subgraph por bloco, um nó por módulo, uma seta por pré-requisito."""
    mods = carregar_modulos(raiz)
    ordem = lambda c: (mods[c]["ordem"], c)
    blocos = {}
    for c in sorted(mods, key=ordem):
        blocos.setdefault(mods[c]["bloco"], []).append(c)
    setas = sorted(
        ((p, c) for c in mods for p in mods[c].get("prerequisitos") or [] if p in mods),
        key=lambda s: (ordem(s[0]), ordem(s[1])),
    )
    linhas = ["```mermaid", "flowchart LR"]
    for bloco, cods in blocos.items():
        bid = _id_bloco(bloco)
        linhas.append(f'  subgraph {bid}["{_texto(ROTULO_BLOCO.get(bid, bloco))}"]')
        for c in cods:
            linhas.append(f'    {c}["{c} {_texto(ROTULO_MODULO.get(c, mods[c]["nome"]))}"]')
        for p, c in setas:
            if mods[p]["bloco"] == bloco and mods[c]["bloco"] == bloco:
                linhas.append(f"    {p} --> {c}")
        linhas.append("  end")
    for p, c in setas:
        if mods[p]["bloco"] != mods[c]["bloco"]:
            linhas.append(f"  {p} --> {c}")
    linhas.append("```")
    return "\n".join(linhas)


def _partes(texto):
    """(antes, trecho, depois) ou None se os marcadores faltam ou estão fora de ordem."""
    i, f = texto.find(INICIO), texto.find(FIM)
    if i < 0 or f < 0 or f < i:
        return None
    return texto[: i + len(INICIO)], texto[i + len(INICIO): f], texto[f:]


def diagrama_desatualizado(raiz):
    """Lista de erros (vazia se o diagrama de NIVELAMENTO.md é igual ao gerado)."""
    texto = (pathlib.Path(raiz) / ARQUIVO).read_text(encoding="utf-8")
    partes = _partes(texto)
    if partes is None:
        return [f"{ARQUIVO}: marcadores {INICIO} e {FIM} ausentes ou fora de ordem"]
    if partes[1] != f"\n{gerar_diagrama(raiz)}\n":
        return [f"{ARQUIVO}: diagrama do nivelamento desatualizado; rode python scripts/diagrama.py"]
    return []


def atualizar(raiz):
    """Reescreve o trecho entre os marcadores. Devolve True se o arquivo mudou."""
    caminho = pathlib.Path(raiz) / ARQUIVO
    texto = caminho.read_text(encoding="utf-8")
    partes = _partes(texto)
    if partes is None:
        raise SystemExit(f"{ARQUIVO}: marcadores {INICIO} e {FIM} ausentes ou fora de ordem")
    novo = f"{partes[0]}\n{gerar_diagrama(raiz)}\n{partes[2]}"
    if novo == texto:
        return False
    caminho.write_text(novo, encoding="utf-8")
    return True


def main(argv=None, raiz=RAIZ):
    ap = argparse.ArgumentParser(description="Gera o diagrama do nivelamento em NIVELAMENTO.md.")
    ap.add_argument("--checar", action="store_true", help="só confere, sem reescrever; sai com 1 se desatualizado")
    a = ap.parse_args(argv)
    if a.checar:
        erros = diagrama_desatualizado(raiz)
        for e in erros:
            print("ERRO:", e)
        return 1 if erros else 0
    print(f"{ARQUIVO}: diagrama " + ("atualizado." if atualizar(raiz) else "já estava atualizado."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
