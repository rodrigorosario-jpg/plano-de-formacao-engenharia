"""Regressões dos achados da revisão final da fase A."""
import datetime as dt

from config import PADROES
from mapa import gerar_mapa
from respostas import COLUNAS, carregar_respostas, conferir_resumos, validar_respostas
from verificar import normalizar, verificar
import progresso

COMPS = {"XA1.c01": {"codigo": "XA1", "nome": "Soma"}}
LINHA = "2026-11-20,s1,,1,XA1,XA1.c01,fluencia,1,certo,,0,"


def csv(tmp_path, corpo, encoding="utf-8"):
    arq = tmp_path / "r.csv"
    arq.write_bytes((",".join(COLUNAS) + "\n" + corpo).encode(encoding))
    return validar_respostas(carregar_respostas(arq), COMPS, tmp_path)


def test_coluna_a_mais_vira_csv_invalido(tmp_path):
    erros = csv(tmp_path, LINHA + ",conta armada, depois mental\n")
    assert erros and erros[0].startswith("csv-invalido: linha 2") and "colunas a mais" in erros[0]


def test_aspa_nao_fechada_vira_csv_invalido(tmp_path):
    erros = csv(tmp_path, LINHA + ',"aspas abertas\n' + LINHA.replace(",1,XA1", ",2,XA1") + ",\n")
    assert any("aspa" in e for e in erros)


def test_csv_em_latin1_vira_csv_invalido(tmp_path):
    erros = csv(tmp_path, LINHA + ",divisão\n", encoding="latin-1")
    assert erros == ["csv-invalido: arquivo não está em UTF-8; salve como CSV UTF-8"]


def test_item_deve_ser_inteiro_positivo(tmp_path):
    erros = csv(tmp_path, LINHA.replace(",1,XA1", ",abc,XA1") + ",\n")
    assert any("coluna item" in e for e in erros)


def test_normalizar_tira_unidade_e_porcentagem():
    assert normalizar("57 m") == 57 and normalizar("6.760 reais") == 6760
    assert normalizar("R$ 12,00") == 12 and normalizar("50%") == 50 and normalizar("−5") == -5
    assert normalizar("84 km/h") == 84


def test_dois_resumos_mesma_lista_mesmo_dia_somam():
    d = dt.date(2026, 11, 20)
    avs = [{"data": d, "lista": "L.md", "acertos": 5, "total": 5}, {"data": d, "lista": "L.md", "acertos": 0, "total": 3}]
    linhas = [{"data": d, "lista": "L.md", "resultado": "certo"}] * 5 + [{"data": d, "lista": "L.md", "resultado": "errado"}] * 3
    assert conferir_resumos(avs, linhas) == []


def _yml(tmp_path, texto, gabarito=True):
    (tmp_path / "g.md").write_text("| 1 | 3 |\n", encoding="utf-8") if gabarito else None
    arq = tmp_path / "v.yml"
    arq.write_text(texto, encoding="utf-8")
    return verificar(arq, tmp_path)


def test_yaml_malformado_nao_derruba(tmp_path):
    assert _yml(tmp_path, "")[0].startswith("gabarito-divergente")
    assert _yml(tmp_path, "lista: x\nitens: []\n")[0].startswith("gabarito-divergente")
    assert _yml(tmp_path, "gabarito: nada.md\nitens: []\n")[0].startswith("gabarito-divergente")
    msgs = _yml(tmp_path, "gabarito: g.md\nitens:\n  - {item: 1, predicado: 'n ==', intervalo: [1, 5]}\n")
    assert msgs and msgs[0].startswith("gabarito-divergente")


def test_intervalo_e_expoente_limitados(tmp_path):
    assert _yml(tmp_path, "gabarito: g.md\nitens:\n  - {item: 1, calculo: '9**9**9'}\n")[0].startswith("gabarito-divergente")
    msgs = _yml(tmp_path, "gabarito: g.md\nitens:\n  - {item: 1, predicado: 'n == 3', intervalo: [1, 50000000]}\n")
    assert msgs and "intervalo" in msgs[0]


def test_mapa_descarta_so_linhas_invalidas(disc_min):
    disc_min["XA1"]["competencias"] = [{"id": "XA1.c01", "nome": "Soma"}]
    boa = {"_linha": 2, "competencia": "XA1.c01", "data": dt.date(2026, 11, 20), "resultado": "errado", "classe_erro": "conceito", "ajuda": 0}
    ruim = {**boa, "_linha": 3, "competencia": "XA1.c09"}
    usadas = progresso.respostas_para_mapa([boa, ruim], ["csv-invalido: linha 3, coluna competencia: x"])
    assert usadas == [boa]
