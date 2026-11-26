import datetime as dt

from config import PADROES
from mapa import gerar_mapa, lacunas_prerequisitos, situacao


def r(resultado="certo", ajuda=0, classe="", dia=1, comp="XA1.c01"):
    return {"data": dt.date(2026, 11, dia), "competencia": comp, "codigo": comp.split(".")[0],
            "resultado": resultado, "ajuda": ajuda, "classe_erro": classe}


def test_sem_dados():
    assert situacao([], PADROES, False) == "sem_dados"


def test_conceito_recente_e_fraca():
    assert situacao([r("errado", classe="conceito")], PADROES, False) == "fraca"


def test_poucos_acertos_e_fraca():
    linhas = [r("errado", classe="atencao")] * 2 + [r()] + [r("errado", classe="atencao")]
    assert situacao(linhas, PADROES, False) == "fraca"


def test_forte():
    assert situacao([r(dia=d) for d in range(1, 6)], PADROES, False) == "forte"


def test_forte_exige_sem_ajuda():
    linhas = [r(dia=d) for d in range(1, 4)] + [r(ajuda=2, dia=4), r(ajuda=2, dia=5)]
    assert situacao(linhas, PADROES, False) == "em_formacao"


def test_janela_considera_so_as_ultimas():
    antigas = [r("errado", classe="atencao", dia=1)] * 10
    recentes = [r(dia=d) for d in range(2, 12)]
    assert situacao(antigas + recentes, PADROES, False) == "forte"


def test_em_queda_quando_concluido():
    assert situacao([r("errado", classe="conceito")], PADROES, True) == "em_queda"


def test_lacuna_em_prerequisito(disc_min):
    comps = {"XA1.c01": {"codigo": "XA1", "nome": "a"}, "XA2.c01": {"codigo": "XA2", "nome": "b"}}
    sit = {"XA1.c01": "fraca", "XA2.c01": "fraca"}
    assert lacunas_prerequisitos(disc_min, comps, sit) == [("XA2.c01", "XA1.c01")]


def test_mapa_com_csv_vazio(disc_min):
    disc_min["XA1"]["competencias"] = [{"id": "XA1.c01", "nome": "Soma"}]
    disc_min["XA1"]["nome"] = disc_min["XA2"]["nome"] = "Mod"
    comps = {"XA1.c01": {"codigo": "XA1", "nome": "Soma"}}
    texto = gerar_mapa(disc_min, comps, [], PADROES, dt.date(2026, 11, 20))
    assert "sem_dados" in texto and "não edite à mão" in texto


def test_conceito_na_mesma_sessao_conta_como_recente():
    # numa mesma lista (mesma data) a ordem dos itens não pode esconder um erro de conceito
    linhas = [r(dia=20), r("errado", classe="conceito", dia=20)] + [r(dia=20) for _ in range(5)]
    assert situacao(linhas, PADROES, False) == "fraca"
