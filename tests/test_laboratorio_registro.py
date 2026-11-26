"""Linhas `laboratorio` de registro/avaliacoes.md e o portão dos módulos de laboratório (ADR 0010)."""
import datetime as dt

import laboratorio_git
import progresso
from autonomia import laboratorio
from config import PADROES
from mapa import gerar_mapa
from test_autonomia import _concluido

CENARIOS = sorted(laboratorio_git.CENARIOS)
CFG = {**PADROES, "autonomia_por_laboratorio": ["XA1"]}


def lab(dia, cenario, acertos=1, cod="XA1"):
    return {"data": dt.date(2026, 12, dia), "codigos": [cod], "tipo": "laboratorio", "pct": 100 * acertos,
            "acertos": acertos, "total": 1, "observacoes": f"{cenario}; conferido pelo script", "lista": None}


def _todos(dias=(1, 2, 3)):
    return [lab(dias[i % len(dias)], c) for i, c in enumerate(CENARIOS)]


def test_conta_cenarios_distintos_e_dias_so_sem_consulta():
    avs = [lab(1, "N1-primeiro-commit"), lab(2, "N1-primeiro-commit"), lab(2, "N4-conflito", acertos=0)]
    assert laboratorio(avs, "XA1") == (1, 2)


def test_portao_de_laboratorio_completo_passa(disc_min):
    erros, _ = progresso.validar(_concluido(disc_min), {}, _todos(), 2, respostas=[], autonomia_linhas=[], cfg=CFG)
    assert not any(e.startswith(("portao-sem-laboratorio", "portao-sem-autonomia")) for e in erros), erros


def test_portao_com_cenario_faltando_falha(disc_min):
    avs = _todos()[:-1]
    erros, _ = progresso.validar(_concluido(disc_min), {}, avs, 2, respostas=[], autonomia_linhas=[], cfg=CFG)
    assert any(e.startswith("portao-sem-laboratorio: XA1") for e in erros)


def test_portao_em_poucos_dias_falha(disc_min):
    erros, _ = progresso.validar(_concluido(disc_min), {}, _todos(dias=(1, 2)), 2, respostas=[], autonomia_linhas=[],
                                 cfg=CFG)
    assert any(e.startswith("portao-sem-laboratorio: XA1") for e in erros)


def test_cenario_desconhecido_e_linha_sem_cenario(disc_min):
    avs = [lab(1, "N9-inventado"), {**lab(1, "x"), "observacoes": "fiz tudo"}]
    erros, _ = progresso.validar(disc_min, {}, avs, 2, respostas=[], autonomia_linhas=[], cfg=CFG)
    assert any("desconhecido N9-inventado" in e for e in erros)
    assert any("sem o cenário" in e for e in erros)


def test_mapa_mostra_o_progresso_do_laboratorio(disc_min):
    disc_min["XA1"].update(competencias=[{"id": "XA1.c01", "nome": "Soma"}], nome="Mod")
    comps = {"XA1.c01": {"codigo": "XA1", "nome": "Soma"}}
    texto = gerar_mapa(disc_min, comps, [], CFG, dt.date(2026, 12, 3), avs=[lab(1, "N1-primeiro-commit")])
    assert f"Laboratório: 1/{len(CENARIOS)} cenários sem consulta em 1/3 dias" in texto
