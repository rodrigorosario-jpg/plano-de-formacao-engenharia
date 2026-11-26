import datetime as dt

from respostas import COLUNAS, carregar_respostas, validar_respostas

COMPS = {"XA1.c01": {"codigo": "XA1", "nome": "Soma"}, "XA1.c02": {"codigo": "XA1", "nome": "Sub"}}


def linha(**kw):
    base = {"data": "2026-11-20", "sessao": "s1", "lista": "", "item": "1", "codigo": "XA1",
            "competencia": "XA1.c01", "tipo_item": "fluencia", "nivel": "1", "resultado": "certo",
            "classe_erro": "", "ajuda": "0", "metodo": "", "observacao": ""}
    base.update(kw)
    return base


def escrever(tmp_path, linhas, bom=False, eol="\n"):
    import csv, io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUNAS, lineterminator=eol)
    w.writeheader()
    for l in linhas:
        w.writerow(l)
    arq = tmp_path / "r.csv"
    arq.write_bytes((("﻿" if bom else "") + buf.getvalue()).encode("utf-8"))
    return arq


def validar(linhas_brutas, tmp_path, comps=COMPS):
    return validar_respostas(carregar_respostas(escrever(tmp_path, linhas_brutas)), comps, tmp_path)


def test_carrega_csv_com_bom_crlf_e_aspas(tmp_path):
    arq = escrever(tmp_path, [linha(observacao="errou, depois acertou")], bom=True, eol="\r\n")
    r = carregar_respostas(arq)
    assert r[0]["observacao"] == "errou, depois acertou"
    assert r[0]["data"] == dt.date(2026, 11, 20) and r[0]["ajuda"] == 0 and r[0]["_linha"] == 2


def test_competencia_inexistente_e_ajuda_negativa(tmp_path):
    erros = validar([linha(competencia="NM0.c99", ajuda="-1")], tmp_path)
    assert any("coluna competencia" in e for e in erros)
    assert any("coluna ajuda" in e for e in erros)
    assert all(e.startswith("csv-invalido: linha 2,") for e in erros)


def test_competencia_removida_invalida_linhas_antigas(tmp_path):
    erros = validar([linha(competencia="XA1.c02")], tmp_path, comps={"XA1.c01": COMPS["XA1.c01"]})
    assert any("XA1.c02" in e for e in erros)


def test_competencia_de_outro_codigo(tmp_path):
    comps = {**COMPS, "XA2.c01": {"codigo": "XA2", "nome": "x"}}
    erros = validar([linha(competencia="XA2.c01")], tmp_path, comps=comps)
    assert any("coluna competencia" in e for e in erros)


def test_classe_erro_com_resultado_certo(tmp_path):
    assert any("coluna classe_erro" in e for e in validar([linha(classe_erro="atencao")], tmp_path))


def test_valores_fora_dos_conjuntos(tmp_path):
    erros = validar([linha(tipo_item="outro", resultado="talvez", nivel="6", data="20/11/2026", lista="nao/existe.md")], tmp_path)
    for col in ("tipo_item", "resultado", "nivel", "data", "lista"):
        assert any(f"coluna {col}" in e for e in erros), col


def test_cabecalho_errado(tmp_path):
    arq = tmp_path / "r.csv"
    arq.write_text("data,outra\n2026-11-20,x\n", encoding="utf-8")
    assert validar_respostas(carregar_respostas(arq), COMPS, tmp_path) == ["csv-invalido: cabeçalho difere de " + ",".join(COLUNAS)]


def test_linha_valida_sem_erros(tmp_path):
    assert validar([linha(), linha(item="2", resultado="errado", classe_erro="conceito", ajuda="2")], tmp_path) == []


def test_arquivo_ausente_e_lista_vazia(tmp_path):
    assert carregar_respostas(tmp_path / "nada.csv") == []


def _av(lista, acertos, total):
    return {"data": dt.date(2026, 11, 20), "lista": lista, "acertos": acertos, "total": total}


def _r(lista, resultado):
    return {"data": dt.date(2026, 11, 20), "lista": lista, "resultado": resultado}


def test_resumo_bate():
    from respostas import conferir_resumos
    linhas = [_r("L.md", "certo"), _r("L.md", "parcial"), _r("L.md", "errado")]
    assert conferir_resumos([_av("L.md", 1.5, 3)], linhas) == []


def test_resumo_diverge():
    from respostas import conferir_resumos
    msgs = conferir_resumos([_av("L.md", 3, 3)], [_r("L.md", "certo"), _r("L.md", "errado")])
    assert len(msgs) == 1 and msgs[0].startswith("resumo-divergente: 2026-11-20 L.md")


def test_avaliacao_sem_lista_e_ignorada():
    from respostas import conferir_resumos
    assert conferir_resumos([_av(None, 3, 3)], []) == []
