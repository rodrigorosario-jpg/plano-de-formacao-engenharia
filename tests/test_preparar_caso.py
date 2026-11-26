import datetime as dt
import importlib.util
import pathlib

from estado import aplicar_estado, carregar_estado

ARQ = pathlib.Path(__file__).resolve().parent / "skill" / "preparar_caso.py"


def modulo():
    spec = importlib.util.spec_from_file_location("preparar_caso", ARQ)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_mudar_status_grava_no_estado(tmp_path):
    pc = modulo()
    (tmp_path / "disciplinas").mkdir()
    cab = (tmp_path / "disciplinas/NM0-x.md")
    cab.write_text("---\ncodigo: NM0\nportao:\n  criterio: x\n---\n", encoding="utf-8")
    pc.mudar_status(tmp_path, "NM1", "em_andamento")
    pc.mudar_status(tmp_path, "NM0", "concluida", portao=True, data="2026-10-01")
    assert cab.read_text(encoding="utf-8") == "---\ncodigo: NM0\nportao:\n  criterio: x\n---\n"
    mods = carregar_estado(tmp_path)["modulos"]
    assert mods["NM1"] == {"status": "em_andamento"}
    assert mods["NM0"] == {"status": "concluida",
                           "portao": {"data": dt.date(2026, 10, 1), "resultado": "85%", "evidencia": "prova de saída"}}
    disc = aplicar_estado({"NM0": {"codigo": "NM0", "portao": {"criterio": "x"}}}, carregar_estado(tmp_path))
    assert disc["NM0"]["portao"]["data"] == dt.date(2026, 10, 1)


def test_estado_inicial_dos_casos(tmp_path):
    pc = modulo()
    pc.estado_inicial(tmp_path)
    pc.mudar_status(tmp_path, "NM1", "em_andamento")
    mods = carregar_estado(tmp_path)["modulos"]
    assert mods["NM1"] == {"diagnostico": 0, "status": "em_andamento"}
    assert [c for c in mods] == ["NM1", "NM2", "NM3", "NM4", "NM5"] and mods["NM5"] == {"diagnostico": 0}
