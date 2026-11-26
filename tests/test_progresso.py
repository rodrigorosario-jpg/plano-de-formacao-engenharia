import pathlib

import progresso


def test_validar_inclui_erros_de_competencias(disc_min):
    disc_min["XA1"]["competencias"] = [{"id": "XX.c01", "nome": "A"}]
    erros, _ = progresso.validar(disc_min, {}, [], 2)
    assert any("XX.c01" in e for e in erros)


def test_validar_inclui_erros_do_csv(disc_min):
    disc_min["XA1"]["competencias"] = [{"id": "XA1.c01", "nome": "A"}]
    linha = {"_linha": 2, "item": 1, "data": "x", "codigo": "XA1", "competencia": "XA1.c01", "tipo_item": "fluencia",
             "resultado": "certo", "classe_erro": "", "nivel": 1, "ajuda": 0, "lista": ""}
    erros, _ = progresso.validar(disc_min, {}, [], 2, respostas=[linha])
    assert any(e.startswith("csv-invalido: linha 2, coluna data") for e in erros)


def test_carregar_avaliacoes_le_coluna_lista(tmp_path, monkeypatch):
    arq = tmp_path / "a.md"
    arq.write_text("| 2026-11-20 | NM0 | exercicios | 7 | 10 | obs | exercicios/NM0/1-adicao.md |\n"
                   "| 2026-11-18 | NM1 | diagnostico | 0 | 5 | obs |\n", encoding="utf-8")
    monkeypatch.setattr(progresso, "AVALIACOES", arq)
    a, b = progresso.carregar_avaliacoes()
    assert a["lista"] == "exercicios/NM0/1-adicao.md" and a["acertos"] == 7 and a["total"] == 10
    assert b["lista"] is None


def test_main_grava_mapa(tmp_path, monkeypatch):
    import sys
    monkeypatch.setattr(progresso, "SAIDA", tmp_path / "P.md")
    monkeypatch.setattr(progresso, "SAIDA_MAPA", tmp_path / "M.md", raising=False)
    monkeypatch.setattr(sys, "argv", ["progresso.py"])
    try:
        progresso.main()
    except SystemExit:
        pass
    assert "Mapa de deficiências" in (tmp_path / "M.md").read_text(encoding="utf-8")


def test_checar_roda_verificacoes(tmp_path, monkeypatch):
    (tmp_path / "exercicios/XA1/gabaritos").mkdir(parents=True)
    (tmp_path / "exercicios/XA1/verificacao").mkdir()
    (tmp_path / "exercicios/XA1/gabaritos/L.md").write_text("| 1 | 5 |\n", encoding="utf-8")
    (tmp_path / "exercicios/XA1/verificacao/L.yml").write_text(
        "lista: exercicios/XA1/L.md\ngabarito: exercicios/XA1/gabaritos/L.md\nitens:\n  - {item: 1, calculo: '2 + 2'}\n", encoding="utf-8")
    monkeypatch.setattr(progresso, "RAIZ", tmp_path)
    monkeypatch.setattr(progresso, "DIR_EXERCICIOS", tmp_path / "exercicios")
    assert any(m.startswith("gabarito-divergente") for m in progresso.verificacoes())


def test_mapa_usa_respostas_quando_erro_nao_e_do_csv():
    r = [{"_linha": 2}]
    assert progresso.respostas_para_mapa(r, ["NM1: está 'em_andamento' sem o portão de NM0 cumprido"]) == r
    assert progresso.respostas_para_mapa(r, ["csv-invalido: linha 2, coluna data: x"]) == []


def test_links_ignoram_saidas_brutas_do_benchmark(tmp_path, monkeypatch):
    (tmp_path / "benchmark/fase-a").mkdir(parents=True)
    (tmp_path / "benchmark/fase-a/x.md").write_text("[a](nao-existe.md)\n", encoding="utf-8")
    (tmp_path / "doc.md").write_text("[b](tambem-nao.md)\n", encoding="utf-8")
    monkeypatch.setattr(progresso, "RAIZ", tmp_path)
    assert [o for o, _ in progresso.links_quebrados()] == ["doc.md"]


def test_campo_ausente_no_cabecalho_da_mensagem_do_schema_e_nao_traceback(tmp_path):
    import shutil
    import subprocess
    import sys
    raiz = pathlib.Path(__file__).resolve().parents[1]
    dest = tmp_path / "r"
    shutil.copytree(raiz, dest, ignore=shutil.ignore_patterns(".git", "__pycache__", "benchmark", "tests"))
    arq = next((dest / "disciplinas").glob("NM13-*.md"))
    arq.write_text("\n".join(l for l in arq.read_text(encoding="utf-8").split("\n")
                             if not l.startswith(("bloco:", "status:"))), encoding="utf-8")
    r = subprocess.run([sys.executable, "scripts/progresso.py", "--checar"], cwd=dest, capture_output=True, text=True)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr
    assert "falta o campo obrigatório 'bloco'" in r.stdout


def test_carregar_disciplinas_aplica_estado(tmp_path, monkeypatch):
    import datetime as dt
    (tmp_path / "disciplinas").mkdir()
    for c in ("XA1", "XA2"):
        (tmp_path / "disciplinas" / f"{c}.md").write_text(f"---\ncodigo: {c}\nportao:\n  criterio: x\n---\n", encoding="utf-8")
    monkeypatch.setattr(progresso, "RAIZ", tmp_path)
    monkeypatch.setattr(progresso, "DIR_DISC", tmp_path / "disciplinas")
    disc = progresso.carregar_disciplinas()
    assert disc["XA1"]["status"] == "nao_iniciada" and disc["XA1"]["portao"]["data"] is None
    (tmp_path / "registro").mkdir()
    (tmp_path / "registro/estado.yml").write_text(
        "schema_version: 1\nmodulos:\n  XA1: {status: em_andamento, inicio: 2026-01-05}\n", encoding="utf-8")
    disc = progresso.carregar_disciplinas()
    assert disc["XA1"]["status"] == "em_andamento" and disc["XA1"]["inicio"] == dt.date(2026, 1, 5)
    assert disc["XA2"]["status"] == "nao_iniciada" and disc["XA1"]["arquivo"] == "disciplinas/XA1.md"


def test_validar_inclui_erros_do_estado(disc_min, tmp_path, monkeypatch):
    monkeypatch.setattr(progresso, "RAIZ", tmp_path)
    monkeypatch.setattr(progresso, "DIR_EXERCICIOS", tmp_path / "exercicios")
    for nome in ("diagrama_desatualizado", "validar_esquemas", "validar_catalogo"):
        monkeypatch.setattr(progresso, nome, lambda *a: [])
    erros, _ = progresso.validar(disc_min, {}, [], 2, estado={"modulos": {"ZZ9": {"status": "concluida"}}})
    assert any(e.startswith("registro/estado.yml: ZZ9") for e in erros)
    assert progresso.validar_estado(disc_min, {}, tmp_path) == []
