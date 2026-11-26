import datetime as dt

from config import PADROES
from fixacao import avisos_fixacao, sortear_fixacao

HOJE = dt.date(2026, 12, 20)


def disc_feito(disc_min, status="concluida", data="2026-11-25"):
    disc_min["XA1"].update(status=status, portao={"data": data, "resultado": "85%"},
                           competencias=[{"id": "XA1.c01", "nome": "a"}, {"id": "XA1.c02", "nome": "b"}])
    disc_min["XA2"]["competencias"] = [{"id": "XA2.c01", "nome": "c"}]
    return disc_min


COMPS = {"XA1.c01": {"codigo": "XA1", "nome": "a"}, "XA1.c02": {"codigo": "XA1", "nome": "b"},
         "XA2.c01": {"codigo": "XA2", "nome": "c"}}


def r(comp, dia, resultado="certo", ajuda=0, classe=""):
    return {"competencia": comp, "codigo": comp.split(".")[0], "data": dt.date(2026, 12, dia),
            "resultado": resultado, "ajuda": ajuda, "classe_erro": classe, "tipo_item": "fixacao"}


def test_so_sorteia_modulos_feitos(disc_min):
    sorteio = sortear_fixacao(disc_feito(disc_min), COMPS, [], PADROES, HOJE, n=5, semente=1)
    assert set(sorteio) <= {"XA1.c01", "XA1.c02"} and len(sorteio) == 2


def test_sem_modulo_feito_lista_vazia(disc_min):
    assert sortear_fixacao(disc_min, COMPS, [], PADROES, HOJE, n=3, semente=1) == []


def test_peso_maior_sai_mais(disc_min):
    d = disc_feito(disc_min)
    linhas = [r("XA1.c01", 19, "errado", classe="conceito")] + [r("XA1.c02", 19 - i) for i in range(6)]
    primeiros = [sortear_fixacao(d, COMPS, linhas, PADROES, HOJE, n=1, semente=s)[0] for s in range(200)]
    assert primeiros.count("XA1.c01") > primeiros.count("XA1.c02")


def test_semente_reprodutivel(disc_min):
    d = disc_feito(disc_min)
    assert sortear_fixacao(d, COMPS, [], PADROES, HOJE, 2, semente=7) == sortear_fixacao(d, COMPS, [], PADROES, HOJE, 2, semente=7)


def test_autonomia_em_queda(disc_min):
    linhas = [r("XA1.c01", 10), r("XA1.c01", 12, "errado", classe="procedimento"), r("XA1.c02", 14, ajuda=2)]
    avisos = avisos_fixacao(disc_feito(disc_min), COMPS, linhas, PADROES, HOJE)
    assert any(a.startswith("autonomia-em-queda: XA1") for a in avisos)


def test_sem_queda_quando_acerta(disc_min):
    linhas = [r("XA1.c01", 10), r("XA1.c01", 12), r("XA1.c02", 14)]
    assert not any(a.startswith("autonomia-em-queda") for a in avisos_fixacao(disc_feito(disc_min), COMPS, linhas, PADROES, HOJE))


def test_fixacao_vencida(disc_min):
    linhas = [r("XA1.c01", 18)]  # c02 nunca vista desde o portão em 25/11 → 25 dias; vence com 30
    avisos = avisos_fixacao(disc_feito(disc_min, data="2026-11-10"), COMPS, linhas, PADROES, HOJE)
    assert any(a.startswith("fixacao-vencida: XA1.c02") for a in avisos)
    assert not any(a.startswith("fixacao-vencida: XA1.c01") for a in avisos)


def test_progresso_inclui_avisos_de_fixacao(disc_min):
    import progresso
    linhas = [r("XA1.c01", 10), r("XA1.c01", 12, "errado", classe="procedimento"), r("XA1.c02", 14, ajuda=2)]
    d = disc_feito(disc_min, data="2026-11-01")
    _, avisos = progresso.validar(d, {}, [], 2, respostas=[], autonomia_linhas=[], cfg=PADROES, fixacao_linhas=linhas, hoje=HOJE)
    assert any(a.startswith("autonomia-em-queda") for a in avisos)
