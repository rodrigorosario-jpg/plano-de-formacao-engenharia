import verificar as verificar_mod
from fractions import Fraction

import pytest

from verificar import avaliar, normalizar, respostas_validas, verificar

CARTAS = "n % 2 == 0 and n % 3 == 0 and n % 4 == 0 and n % 6 == 0 and n % 8 == 0 and n < {lim}"


def preparar(tmp_path, gabarito, itens):
    (tmp_path / "exercicios/XA1/gabaritos").mkdir(parents=True)
    (tmp_path / "exercicios/XA1/L.md").write_text("1. x\n", encoding="utf-8")
    linhas = "".join(f"| {n} | {r} |\n" for n, r in gabarito)
    (tmp_path / "exercicios/XA1/gabaritos/L.md").write_text("| Nº | Resposta |\n| --- | --- |\n" + linhas, encoding="utf-8")
    import yaml
    arq = tmp_path / "exercicios/XA1/verificacao/L.yml"
    arq.parent.mkdir()
    arq.write_text(yaml.safe_dump({"lista": "exercicios/XA1/L.md", "gabarito": "exercicios/XA1/gabaritos/L.md", "itens": itens}), encoding="utf-8")
    return arq


def test_avaliar_fracoes_exatas():
    assert avaliar("F(3,4) + F(1,8)") == Fraction(7, 8)
    assert avaliar("0.1 + 0.2") == Fraction(3, 10)
    assert avaliar("-(2**3) // 3 + 17 % 5") == Fraction(-1)


def test_avaliar_rejeita_chamadas():
    for expr in ("__import__('os')", "open('x')", "(1).real", "[1, 2]", "F"):
        with pytest.raises(ValueError):
            avaliar(expr)


def test_normalizar_equivalentes():
    assert normalizar("0,75") == normalizar("3/4") == Fraction(3, 4)
    assert normalizar("12,0") == 12 and normalizar("-5") == -5
    assert normalizar("1 1/2") == Fraction(3, 2)
    assert normalizar(" Quinta-feira ") == "quinta-feira"
    assert normalizar("1.000") == 1000  # milhar no padrão brasileiro


def test_respostas_validas_e_caso_24_48():
    assert respostas_validas(CARTAS.format(lim=50), "n", 1, 200) == [24, 48]
    assert respostas_validas(CARTAS.format(lim=40), "n", 1, 200) == [24]


def test_item_ambiguo(tmp_path):
    arq = preparar(tmp_path, [(1, "24")], [{"item": 1, "predicado": CARTAS.format(lim=50), "variavel": "n", "intervalo": [1, 200]}])
    msgs = verificar(arq, tmp_path)
    assert len(msgs) == 1 and msgs[0].startswith("item-ambiguo:") and "24, 48" in msgs[0]


def test_item_unico_sem_mensagem(tmp_path):
    arq = preparar(tmp_path, [(1, "24 (o único múltiplo comum abaixo de 40)")], [{"item": 1, "predicado": CARTAS.format(lim=40), "variavel": "n", "intervalo": [1, 200]}])
    assert verificar(arq, tmp_path) == []


def test_gabarito_divergente(tmp_path):
    arq = preparar(tmp_path, [(1, "5/8")], [{"item": 1, "calculo": "F(3,4) + F(1,8)"}])
    msgs = verificar(arq, tmp_path)
    assert len(msgs) == 1 and msgs[0].startswith("gabarito-divergente:") and "7/8" in msgs[0]


def test_gabarito_equivalente_aceito(tmp_path):
    arq = preparar(tmp_path, [(1, "0,875")], [{"item": 1, "calculo": "F(3,4) + F(1,8)"}])
    assert verificar(arq, tmp_path) == []


def test_item_de_revisao_sem_nota_e_erro(tmp_path):
    arq = preparar(tmp_path, [(1, "Sim")], [{"item": 1, "revisao": "independente"}])
    assert any("nota" in m for m in verificar(arq, tmp_path))


def test_item_sem_gabarito_e_erro(tmp_path):
    arq = preparar(tmp_path, [(1, "3")], [{"item": 2, "calculo": "3"}])
    assert any("item 2" in m for m in verificar(arq, tmp_path))


def test_campos_do_mapa_de_itens_validos(tmp_path):
    arq = preparar(tmp_path, [(1, "3")], [{"item": 1, "calculo": "3", "nivel": 7, "tipo_item": "outro"}])
    msgs = verificar(arq, tmp_path)
    assert any("nivel" in m for m in msgs) and any("tipo_item" in m for m in msgs)


def test_sem_intercalacao_avisa(tmp_path):
    from verificar import avisos_intercalacao
    itens = [{"item": i, "competencia": c} for i, c in enumerate(["A.c01", "A.c01", "A.c01", "A.c02", "A.c03"], 1)]
    assert any(a.startswith("sem-intercalacao") for a in avisos_intercalacao({"lista": "L.md", "itens": itens}))


def test_lista_focada_nao_avisa(tmp_path):
    from verificar import avisos_intercalacao
    itens = [{"item": i, "competencia": "A.c01"} for i in range(1, 6)]
    assert avisos_intercalacao({"lista": "L.md", "itens": itens}) == []


def test_codigo_executado_compara_saida(tmp_path):
    arq = preparar(tmp_path, [(1, "6")], [{"item": 1, "codigo": "x = 0\nfor i in range(4):\n    x += i\nprint(x)"}])
    assert verificar(arq, tmp_path) == []


def test_codigo_divergente_e_travado(tmp_path, monkeypatch):
    monkeypatch.setattr(verificar_mod, "TEMPO_CODIGO", 0.5)
    arq = preparar(tmp_path, [(1, "7")], [{"item": 1, "codigo": "print(3 + 3)"}])
    assert verificar(arq, tmp_path)[0].startswith("gabarito-divergente")
    arq2 = tmp_path / "exercicios/XA1/verificacao/L.yml"
    arq2.write_text("gabarito: exercicios/XA1/gabaritos/L.md\nitens:\n  - {item: 1, codigo: 'while True: pass'}\n", encoding="utf-8")
    assert "tempo" in verificar(arq2, tmp_path)[0]
