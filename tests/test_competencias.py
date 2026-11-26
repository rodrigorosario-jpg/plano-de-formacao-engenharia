from competencias import competencias, validar_competencias


def test_competencias_indexa_por_id(disc_min):
    disc_min["XA1"]["competencias"] = [{"id": "XA1.c01", "nome": "Soma"}]
    assert competencias(disc_min)["XA1.c01"] == {"codigo": "XA1", "nome": "Soma"}


def test_id_com_prefixo_errado(disc_min):
    disc_min["XA1"]["competencias"] = [{"id": "XA2.c01", "nome": "Soma"}]
    assert any("XA2.c01" in e for e in validar_competencias(disc_min))


def test_id_repetido_e_nome_vazio(disc_min):
    disc_min["XA1"]["competencias"] = [{"id": "XA1.c01", "nome": "A"}, {"id": "XA1.c01", "nome": ""}]
    erros = validar_competencias(disc_min)
    assert any("repetid" in e for e in erros) and any("nome" in e for e in erros)


def test_modulo_sem_competencias_e_permitido(disc_min):
    assert validar_competencias(disc_min) == []
