import pathlib

import pytest

from diagrama import FIM, INICIO, atualizar, diagrama_desatualizado, gerar_diagrama, main

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def modulo(raiz, codigo, ordem, bloco, prerequisitos, nome=None, fase="nivelamento", arquivo=None):
    pasta = raiz / "disciplinas"
    pasta.mkdir(exist_ok=True)
    linhas = [
        "---",
        f"codigo: {codigo}",
        f"ordem: {ordem}",
        f'nome: "{nome or "Módulo " + codigo}"',
        f"fase: {fase}",
    ]
    if bloco:
        linhas.append(f'bloco: "{bloco}"')
    linhas += [f"prerequisitos: [{', '.join(prerequisitos)}]", "---", "", f"# {codigo}", ""]
    (pasta / (arquivo or f"{codigo}-x.md")).write_text("\n".join(linhas), encoding="utf-8")


def repo(tmp_path, texto=None):
    modulo(tmp_path, "NM1", 2, "A · Aritmética e proporcionalidade (Ensino Fundamental)", ["NM0"])
    modulo(tmp_path, "NM0", 1, "A · Aritmética e proporcionalidade (Ensino Fundamental)", [])
    modulo(tmp_path, "NL1", 3, "L · Lógica de programação", [])
    modulo(tmp_path, "NF1", 4, "F · Física básica (Ensino Médio)", ["NM1", "NL1"])
    modulo(tmp_path, "M1", 5, None, ["NM1", "NL1"], fase="graduacao")
    if texto is None:
        texto = f"# Título\n\nAntes.\n\n{INICIO}\nvelho\n{FIM}\n\nDepois.\n"
    (tmp_path / "NIVELAMENTO.md").write_text(texto, encoding="utf-8")
    return tmp_path


def test_um_subgraph_por_bloco_com_rotulos_de_hoje(tmp_path):
    d = gerar_diagrama(repo(tmp_path))
    assert d.startswith("```mermaid\nflowchart LR\n") and d.endswith("```")
    assert '  subgraph A["A · Aritmética (Fundamental)"]' in d
    assert '  subgraph L["L · Lógica de programação"]' in d
    assert '  subgraph F["F · Física básica"]' in d
    assert d.count("subgraph ") == 3


def test_no_com_rotulo_curto_e_fallback_para_o_nome(tmp_path):
    d = gerar_diagrama(repo(tmp_path))
    assert '    NM0["NM0 Operações fundamentais"]' in d
    assert '    NM1["NM1 Inteiros"]' in d
    modulo(tmp_path, "NM99", 9, "A · Aritmética e proporcionalidade (Ensino Fundamental)", [], nome="Assunto novo")
    assert '    NM99["NM99 Assunto novo"]' in gerar_diagrama(tmp_path)


def test_uma_aresta_por_prerequisito_so_entre_modulos_de_nivelamento(tmp_path):
    d = gerar_diagrama(repo(tmp_path))
    setas = [l.strip() for l in d.splitlines() if "-->" in l]
    assert sorted(setas) == sorted(["NM0 --> NM1", "NM1 --> NF1", "NL1 --> NF1"])
    assert "M1" not in d.replace("NM1", "")


def test_aresta_dentro_do_bloco_fica_no_subgraph(tmp_path):
    linhas = gerar_diagrama(repo(tmp_path)).splitlines()
    assert "    NM0 --> NM1" in linhas
    assert "  NM1 --> NF1" in linhas


def test_ordem_estavel_por_ordem_e_nao_por_arquivo(tmp_path):
    d = gerar_diagrama(repo(tmp_path))
    assert d.index('NM0["') < d.index('NM1["')
    assert d.index("subgraph A") < d.index("subgraph L") < d.index("subgraph F")
    assert d == gerar_diagrama(tmp_path)


def test_atualizar_reescreve_so_o_trecho(tmp_path):
    raiz = repo(tmp_path)
    assert atualizar(raiz) is True
    texto = (raiz / "NIVELAMENTO.md").read_text(encoding="utf-8")
    assert texto.startswith("# Título\n\nAntes.\n\n")
    assert texto.endswith("\n\nDepois.\n")
    assert f"{INICIO}\n{gerar_diagrama(raiz)}\n{FIM}" in texto
    assert "velho" not in texto
    assert atualizar(raiz) is False


def test_desatualizado_quando_trecho_difere(tmp_path):
    raiz = repo(tmp_path)
    erros = diagrama_desatualizado(raiz)
    assert len(erros) == 1 and "NIVELAMENTO.md" in erros[0] and "diagrama.py" in erros[0]
    atualizar(raiz)
    assert diagrama_desatualizado(raiz) == []


@pytest.mark.parametrize("texto", ["sem marcadores\n", f"só o início\n{INICIO}\n", f"{FIM}\ninvertido\n{INICIO}\n"])
def test_desatualizado_quando_faltam_marcadores(tmp_path, texto):
    raiz = repo(tmp_path, texto)
    erros = diagrama_desatualizado(raiz)
    assert len(erros) == 1 and "marcadores" in erros[0]
    with pytest.raises(SystemExit):
        atualizar(raiz)


def test_cli_checar_sai_com_1_se_desatualizado(tmp_path, capsys):
    raiz = repo(tmp_path)
    antes = (raiz / "NIVELAMENTO.md").read_text(encoding="utf-8")
    assert main(["--checar"], raiz) == 1
    assert (raiz / "NIVELAMENTO.md").read_text(encoding="utf-8") == antes
    assert "ERRO" in capsys.readouterr().out
    assert main([], raiz) == 0
    assert main(["--checar"], raiz) == 0


def test_repositorio_real_esta_atualizado_e_tem_as_arestas_omitidas():
    assert diagrama_desatualizado(RAIZ) == []
    d = gerar_diagrama(RAIZ)
    assert "NM3 --> NF1" in d and "NM6 --> NF5" in d
    assert d.count("-->") == 45
    assert d.count("subgraph ") == 8  # 7 blocos + V (NG1, ADR 0010)
