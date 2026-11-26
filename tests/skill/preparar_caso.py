#!/usr/bin/env python3
"""Prepara uma cópia isolada do repositório para executar um caso de teste da skill.

Uso:
    python tests/skill/preparar_caso.py <ID> <baseline|with_skill> <destino>

A cópia exclui os casos de teste, o benchmark e o histórico git (para que o executor não veja
o resultado esperado), copia os fixtures de exercícios, aplica a preparação do caso e inicia um
git novo com um commit inicial, para que `git status` e `git diff` mostrem só o que o executor mudou.
Na cópia do baseline, `skills/` é removida.
"""
import datetime as dt
import pathlib
import shutil
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
from estado import CAMPOS, carregar_estado, formatar_estado  # noqa: E402
FIX = RAIZ / "tests" / "skill" / "fixtures"
EXCLUIR = {".git", ".superpowers", "benchmark", "__pycache__", ".pytest_cache"}

PREPARO = {
    "A-L3-02": {"csv": "respostas-lacuna.csv", "status": {"NM1": "em_andamento", "NM2": "em_andamento"}},
    "A-L1-04": {"csv": "respostas-lacuna.csv"},
    "A-L4-02": {"csv": "respostas-injecao.csv"},
    "V-06": {"csv": "respostas-queda.csv", "concluir": ["NM0"]},
    "B-L3-03": {"csv": "respostas-autonomia-nm2.csv"},
    # Fase C: NM0 concluído (portão anterior à regra de autonomia, para não acusar falta de âncoras)
    "C-01": {"csv": "respostas-queda.csv", "concluir": ["NM0"]},
    "C-02": {"csv": "respostas-queda-recente.csv", "concluir": ["NM0"]},
    "C-04": {"csv": "respostas-vencida.csv", "concluir": ["NM0"], "portao_data": "2026-10-01"},
    "C-05": {"csv": "respostas-queda.csv", "concluir": ["NM0"]},
    "CV-01": {"csv": "respostas-vencida.csv", "concluir": ["NM0"], "portao_data": "2026-10-01"},
    "CV-02": {"csv": "respostas-queda-recente.csv", "concluir": ["NM0"]},
    "H-03": {"csv": "respostas-lacuna.csv"},
    "H-04": {"csv": "respostas-padrao-b.csv"},
    "H-05": {"csv": "respostas-queda.csv", "concluir": ["NM0"]},
}
# Casos da fase B (B-*, BV-*) partem do item 1 da lista de frações já corrigido e registrado.
PADRAO_B = {"csv": "respostas-padrao-b.csv"}
# Andamento inicial de todos os casos: o que os cabeçalhos da main tinham antes do Marco 4
# (diagnóstico do bloco A zerado de NM1 a NM5; nenhum módulo aberto).
ESTADO_INICIAL = {f"NM{i}": {"diagnostico": 0} for i in range(1, 6)}


def estado_inicial(destino):
    """Grava em registro/estado.yml da cópia o andamento inicial dos casos (substitui o que veio da origem)."""
    arq = pathlib.Path(destino) / "registro" / "estado.yml"
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text(formatar_estado({c: dict(v) for c, v in ESTADO_INICIAL.items()}), encoding="utf-8")


def mudar_status(destino, codigo, status, portao=False, data="2026-11-01"):
    """Grava o andamento do módulo em registro/estado.yml da cópia (ADR 0004)."""
    destino = pathlib.Path(destino)
    mods = dict(carregar_estado(destino).get("modulos") or {})
    m = dict(mods.get(codigo) or {})
    m["status"] = status
    if portao:
        m["portao"] = {"data": dt.date.fromisoformat(data), "resultado": "85%", "evidencia": "prova de saída"}
    mods[codigo] = {k: m[k] for k in CAMPOS + ["portao"] if k in m}
    arq = destino / "registro" / "estado.yml"
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text(formatar_estado(mods), encoding="utf-8")


def preparar(caso, grupo, destino):
    destino = pathlib.Path(destino)
    if destino.exists():
        shutil.rmtree(destino)
    if caso in ("A-L5-02", "H-08"):
        destino.mkdir(parents=True)
        if grupo == "with_skill":
            shutil.copytree(RAIZ / "skills", destino / "skills")
        return destino
    shutil.copytree(RAIZ, destino, ignore=lambda d, nomes: [n for n in nomes if n in EXCLUIR
                                                         or (pathlib.Path(d) == RAIZ / "tests" and n == "skill")])
    if grupo == "baseline":
        shutil.rmtree(destino / "skills")
    # Os relatórios da fase A são citados por docs/skills/09_final_validation.md; copiamos só os
    # arquivos do topo (sem saídas brutas nem avaliações) para não quebrar a validação de links.
    for rel in (RAIZ / "benchmark").rglob("*.md"):
        if {"baseline", "with_skill", "validation", "evaluations", "diffs"} & set(rel.relative_to(RAIZ).parts):
            continue
        alvo = destino / rel.relative_to(RAIZ)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(rel, alvo)
    shutil.copytree(FIX / "exercicios", destino / "exercicios", dirs_exist_ok=True)
    p = PREPARO.get(caso, PADRAO_B if caso.startswith(("B-", "BV-")) else {})
    if "csv" in p:
        shutil.copy(FIX / p["csv"], destino / "registro" / "respostas.csv")
    estado_inicial(destino)
    for cod, st in p.get("status", {}).items():
        mudar_status(destino, cod, st)
    for cod in p.get("concluir", []):
        mudar_status(destino, cod, "concluida", portao=True, data=p.get("portao_data", "2026-11-01"))
    subprocess.run(["python", "scripts/progresso.py"], cwd=destino, capture_output=True)
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "user.name=bench", "-c", "user.email=bench@local", "commit", "-qm", "estado inicial"]):
        subprocess.run(cmd, cwd=destino, check=True)
    return destino


if __name__ == "__main__":
    print(preparar(*sys.argv[1:4]))
