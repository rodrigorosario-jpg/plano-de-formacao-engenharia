from config import carregar_config


def test_padroes_quando_arquivo_ausente(tmp_path):
    assert carregar_config(tmp_path / "x.yml")["autonomia_n"] == 5


def test_arquivo_sobrepoe_padrao(tmp_path):
    arq = tmp_path / "p.yml"
    arq.write_text("limite_abertas: 3\n", encoding="utf-8")
    cfg = carregar_config(arq)
    assert cfg["limite_abertas"] == 3 and cfg["mapa_janela"] == 10
