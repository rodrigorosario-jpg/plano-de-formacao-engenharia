import datetime as dt

import pytest

from estado import (CAMPOS, CAMPOS_PORTAO, PADRAO, aplicar_estado, carregar_estado, formatar_estado,
                    validar_estado)

CAB = """---
codigo: {cod}
portao:
  criterio: "80% na prova"
{extra}---
corpo
"""


def raiz_com(tmp_path, cabecalhos=None, estado=None):
    (tmp_path / "disciplinas").mkdir(exist_ok=True)
    for cod, extra in (cabecalhos or {"XA1": "", "XA2": ""}).items():
        (tmp_path / "disciplinas" / f"{cod}.md").write_text(CAB.format(cod=cod, extra=extra), encoding="utf-8")
    if estado is not None:
        (tmp_path / "registro").mkdir(exist_ok=True)
        (tmp_path / "registro" / "estado.yml").write_text(estado, encoding="utf-8")
    return tmp_path


def disc_base():
    return {c: {"codigo": c, "portao": {"criterio": "80% na prova"}} for c in ("XA1", "XA2")}


def test_estado_ausente_e_vazio(tmp_path):
    assert carregar_estado(tmp_path) == {}


def test_carrega_datas_como_datas(tmp_path):
    raiz = raiz_com(tmp_path, estado="schema_version: 1\nmodulos:\n  XA1: {status: em_andamento, inicio: 2026-11-23}\n")
    est = carregar_estado(raiz)
    assert est["modulos"]["XA1"] == {"status": "em_andamento", "inicio": dt.date(2026, 11, 23)}


def test_aplicar_sem_estado_preenche_padroes():
    disc = disc_base()
    aplicar_estado(disc, {})
    for d in disc.values():
        assert d["status"] == "nao_iniciada"
        assert d["inicio"] is None and d["diagnostico"] is None and d["nivel_atingido"] is None
        assert d["portao"] == {"criterio": "80% na prova", "data": None, "resultado": None, "evidencia": None}


def test_aplicar_com_estado_mantem_tipos():
    disc = disc_base()
    est = {"schema_version": 1, "modulos": {
        "XA1": {"status": "concluida", "inicio": dt.date(2026, 11, 1), "diagnostico": 0, "nivel_atingido": 3,
                "portao": {"data": dt.date(2026, 11, 20), "resultado": "85%", "evidencia": "prova"}}}}
    aplicar_estado(disc, est)
    d = disc["XA1"]
    assert d["status"] == "concluida" and d["inicio"] == dt.date(2026, 11, 1)
    assert d["diagnostico"] == 0 and isinstance(d["diagnostico"], int) and d["nivel_atingido"] == 3
    assert d["portao"] == {"criterio": "80% na prova", "data": dt.date(2026, 11, 20), "resultado": "85%", "evidencia": "prova"}
    assert disc["XA2"]["status"] == "nao_iniciada"


def test_aplicar_ignora_codigo_desconhecido():
    disc = disc_base()
    aplicar_estado(disc, {"modulos": {"ZZ9": {"status": "concluida"}}})
    assert set(disc) == {"XA1", "XA2"}


def test_validar_estado_ok(tmp_path):
    raiz = raiz_com(tmp_path)
    est = {"schema_version": 1, "modulos": {"XA1": {"status": "em_andamento", "portao": {"data": None}}}}
    assert validar_estado(disc_base(), est, raiz) == []
    assert validar_estado(disc_base(), {}, raiz) == []


def test_validar_estado_acusa_codigo_status_e_chave(tmp_path):
    raiz = raiz_com(tmp_path)
    est = {"modulos": {"ZZ9": {"status": "concluida"}, "XA1": {"status": "pausada", "inicial": None},
                       "XA2": {"portao": {"criterio": "x"}}}}
    erros = validar_estado(disc_base(), est, raiz)
    assert any("ZZ9" in e and "desconhecido" in e for e in erros)
    assert any("XA1" in e and "pausada" in e for e in erros)
    assert any("XA1" in e and "inicial" in e for e in erros)
    assert any("XA2" in e and "portao.criterio" in e for e in erros)
    assert all(e.startswith("registro/estado.yml: ") for e in erros)


def test_validar_estado_acusa_andamento_no_cabecalho(tmp_path):
    raiz = raiz_com(tmp_path, {"XA1": "", "XA2": ""})
    (raiz / "disciplinas/XA2.md").write_text(
        "---\ncodigo: XA2\nstatus: nao_iniciada\nportao:\n  criterio: x\n  data: null\n---\n", encoding="utf-8")
    erros = validar_estado(disc_base(), {}, raiz)
    assert len(erros) == 1
    assert erros[0].startswith("disciplinas/XA2.md: ")
    assert "status" in erros[0] and "portao.data" in erros[0]
    assert "migrar_estado.py" in erros[0] and "registro/estado.yml" in erros[0]


def test_padroes_e_campos():
    assert CAMPOS == ["status", "inicio", "diagnostico", "nivel_atingido"]
    assert CAMPOS_PORTAO == ["data", "resultado", "evidencia"]
    assert PADRAO["status"] == "nao_iniciada" and all(PADRAO[c] is None for c in CAMPOS[1:])


@pytest.mark.parametrize("modulos", [
    {},
    {"NM0": {"status": "em_andamento", "inicio": dt.date(2026, 11, 23)}, "NM1": {"diagnostico": 0}},
    {"NM0": {"status": "concluida", "portao": {"data": dt.date(2026, 11, 1), "resultado": "85%",
                                                "evidencia": "prova: \"saída\", 1/2"}}, "C1": {"diagnostico": 72.5}},
])
def test_formatar_estado_ida_e_volta(tmp_path, modulos):
    texto = formatar_estado(modulos)
    assert texto.startswith("# ")
    (tmp_path / "registro").mkdir()
    (tmp_path / "registro/estado.yml").write_text(texto, encoding="utf-8")
    assert carregar_estado(tmp_path) == {"schema_version": 1, "modulos": modulos}


def test_status_sem_aspas_e_palavras_reservadas_com_aspas():
    texto = formatar_estado({"NM0": {"status": "em_andamento", "inicio": dt.date(2026, 11, 23)},
                             "NM1": {"portao": {"resultado": "no", "evidencia": "null"}}})
    assert "  NM0: {status: em_andamento, inicio: 2026-11-23}\n" in texto
    assert '"no"' in texto and '"null"' in texto
