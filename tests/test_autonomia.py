import datetime as dt

from autonomia import autonomia
from config import PADROES
import progresso


def a(item, dia, resultado="certo", ajuda=0, lista="L.md", tipo="ancora", cod="XA1"):
    return {"codigo": cod, "lista": lista, "item": item, "tipo_item": tipo, "resultado": resultado,
            "ajuda": ajuda, "data": dt.date(2026, 11, dia)}


def test_conta_ancoras_distintas():
    assert autonomia([a(1, 20), a(1, 21)], "XA1", PADROES) == (1, 2)


def test_ignora_ancora_com_ajuda_e_outros_tipos():
    assert autonomia([a(1, 20, ajuda=1), a(2, 20, tipo="fluencia"), a(3, 20, resultado="parcial")], "XA1", PADROES) == (0, 0)


def test_dias_distintos():
    assert autonomia([a(1, 20), a(2, 20), a(3, 22)], "XA1", PADROES) == (3, 2)


def _concluido(disc_min, data="2026-11-25"):
    disc_min["XA1"].update(status="concluida", fase="nivelamento", portao={"data": data, "resultado": "85%"})
    return disc_min


def test_portao_sem_autonomia(disc_min):
    linhas = [a(i, 20 + i % 3) for i in range(1, 5)]
    erros, _ = progresso.validar(_concluido(disc_min), {}, [], 2, respostas=[], autonomia_linhas=linhas, cfg=PADROES)
    assert any(e.startswith("portao-sem-autonomia: XA1") for e in erros)


def test_portao_com_autonomia_passa(disc_min):
    linhas = [a(i, 20 + i % 3) for i in range(1, 6)]
    erros, _ = progresso.validar(_concluido(disc_min), {}, [], 2, respostas=[], autonomia_linhas=linhas, cfg=PADROES)
    assert not any(e.startswith("portao-sem-autonomia") for e in erros)


def test_dispensada_tambem_exige(disc_min):
    d = _concluido(disc_min)
    d["XA1"]["status"] = "dispensada"
    erros, _ = progresso.validar(d, {}, [], 2, respostas=[], autonomia_linhas=[], cfg=PADROES)
    assert any(e.startswith("portao-sem-autonomia: XA1") for e in erros)


def test_portao_anterior_a_regra_nao_e_afetado(disc_min):
    erros, _ = progresso.validar(_concluido(disc_min, "2026-11-01"), {}, [], 2, respostas=[], autonomia_linhas=[], cfg=PADROES)
    assert not any(e.startswith("portao-sem-autonomia") for e in erros)


def test_mapa_mostra_autonomia(disc_min):
    from mapa import gerar_mapa
    disc_min["XA1"].update(competencias=[{"id": "XA1.c01", "nome": "Soma"}], nome="Mod")
    comps = {"XA1.c01": {"codigo": "XA1", "nome": "Soma"}}
    linhas = [{**a(1, 20), "competencia": "XA1.c01", "classe_erro": ""}]
    assert "Autonomia: 1/5 âncoras em 1/3 dias" in gerar_mapa(disc_min, comps, linhas, PADROES, dt.date(2026, 11, 20))


def _lista(tmp_path, tipos):
    (tmp_path / "exercicios/XA1/verificacao").mkdir(parents=True)
    itens = "".join(f"  - {{item: {i}, tipo_item: {t}, calculo: '1'}}\n" for i, t in tipos.items())
    (tmp_path / "exercicios/XA1/verificacao/L.yml").write_text(f"lista: exercicios/XA1/L.md\ngabarito: g.md\nitens:\n{itens}", encoding="utf-8")


def test_ancora_so_conta_se_o_yml_da_lista_marca_ancora(tmp_path):
    from autonomia import ancoras_validas
    _lista(tmp_path, {1: "ancora", 2: "fluencia"})
    linhas = [a(1, 20, lista="exercicios/XA1/L.md"), a(2, 21, lista="exercicios/XA1/L.md"), a(3, 22, lista="")]
    r = ancoras_validas(linhas, tmp_path)
    assert len(r) == 3 and [l["item"] for l in r if l["tipo_item"] == "ancora"] == [1]


def test_treino_sem_prerequisito_nao_conta():
    linhas = [a(1, 20), {**a(2, 21), "observacao": "treino-sem-prerequisito: NM1 pendente"}]
    assert autonomia(linhas, "XA1", PADROES) == (1, 1)


def test_modulo_com_autonomia_por_laboratorio_nao_exige_ancoras(disc_min):
    cfg = {**PADROES, "autonomia_por_laboratorio": ["XA1"]}
    erros, _ = progresso.validar(_concluido(disc_min), {}, [], 2, respostas=[], autonomia_linhas=[], cfg=cfg)
    assert not any(e.startswith("portao-sem-autonomia") for e in erros)


def test_excecao_de_laboratorio_vale_so_para_o_modulo_listado(disc_min):
    cfg = {**PADROES, "autonomia_por_laboratorio": ["XB9"]}
    erros, _ = progresso.validar(_concluido(disc_min), {}, [], 2, respostas=[], autonomia_linhas=[], cfg=cfg)
    assert any(e.startswith("portao-sem-autonomia: XA1") for e in erros)


def test_excecao_de_laboratorio_com_codigo_desconhecido(disc_min):
    cfg = {**PADROES, "autonomia_por_laboratorio": ["XZ7"]}
    erros, _ = progresso.validar(disc_min, {}, [], 2, respostas=[], autonomia_linhas=[], cfg=cfg)
    assert any("autonomia_por_laboratorio: XZ7" in e for e in erros)
