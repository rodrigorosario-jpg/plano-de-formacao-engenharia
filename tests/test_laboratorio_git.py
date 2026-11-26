"""Cada cenário do laboratório falha antes de resolvido e passa depois da solução conhecida."""
import os
import pathlib
import shutil
import subprocess

import pytest

import laboratorio_git as lab

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="precisa de git")

ENV = {**os.environ, **lab.AMBIENTE_GIT}


def g(pasta, *args):
    r = subprocess.run(["git", "-c", "init.defaultBranch=main", *args], cwd=pasta, env=ENV,
                       capture_output=True, text=True)
    return r.stdout.strip()


def escrever(pasta, caminho, texto):
    (pathlib.Path(pasta) / caminho).write_text(texto, encoding="utf-8")


def sol_n1a(p):
    g(p, "init", "-q")
    g(p, "add", "README.md")
    g(p, "commit", "-q", "-m", "primeiro commit")


def sol_n1b(p):
    g(p, "add", "a.txt")
    g(p, "commit", "-q", "-m", "linha 2 de a")


def sol_n2a(p):
    g(p, "restore", "config.txt", "dados.txt")
    g(p, "restore", "--staged", "segredo.env")


def sol_n2b(p):
    alvo = g(p, "log", "--format=%h", "--grep=ajusta limite", "-1")
    g(p, "restore", "--source", alvo, "limites.cfg")
    g(p, "commit", "-q", "-am", "volta limites.cfg")


def sol_n3a(p):
    g(p, "switch", "-q", "-c", "feature/rodape")
    escrever(p, "rodape.html", "<footer>fim</footer>\n")
    g(p, "add", "rodape.html")
    g(p, "commit", "-q", "-m", "rodapé")
    g(p, "switch", "-q", "main")


def sol_n3b(p):
    g(p, "branch", "-d", "antiga")
    g(p, "branch", "-D", "experimento")


def sol_n4a(p):
    g(p, "merge", "-q", "--ff-only", "correcao")


def sol_n4b(p):
    g(p, "merge", "titulo")
    escrever(p, "README.md", f"{lab.TITULO_FINAL}\n\nTexto.\n")
    g(p, "add", "README.md")
    g(p, "commit", "-q", "--no-edit")


def sol_n5a(p):
    g(p, "clone", "-q", "remoto.git", "trabalho")
    t = p / "trabalho"
    escrever(t, "novo.txt", "oi\n")
    g(t, "add", "novo.txt")
    g(t, "commit", "-q", "-m", "novo")
    g(t, "push", "-q", "origin", "main")


def sol_n5b(p):
    t = p / "trabalho"
    g(t, "fetch", "-q", "origin")
    g(t, "merge", "-q", "--no-edit", "origin/main")
    g(t, "push", "-q", "-u", "origin", "main")


SOLUCOES = {
    "N1-primeiro-commit": sol_n1a, "N1-staging-parcial": sol_n1b,
    "N2-restaurar": sol_n2a, "N2-versao-antiga": sol_n2b,
    "N3-criar-branch": sol_n3a, "N3-limpar-branches": sol_n3b,
    "N4-fast-forward": sol_n4a, "N4-conflito": sol_n4b,
    "N5-clonar-e-enviar": sol_n5a, "N5-sincronizar": sol_n5b,
}


def test_todo_cenario_tem_solucao_testada():
    assert set(SOLUCOES) == set(lab.CENARIOS)
    assert len(lab.CENARIOS) == 10
    assert {c["nivel"] for c in lab.CENARIOS.values()} == {1, 2, 3, 4, 5}


@pytest.mark.parametrize("cid", sorted(lab.CENARIOS))
def test_falha_antes_e_passa_depois(cid, tmp_path):
    pasta = tmp_path / "lab"
    lab.preparar(cid, pasta)
    assert lab.conferir(cid, pasta), "o cenário sem resolver não pode passar"
    SOLUCOES[cid](pasta)
    assert lab.conferir(cid, pasta) == []


def test_conflito_mal_resolvido_falha(tmp_path):
    pasta = tmp_path / "lab"
    lab.preparar("N4-conflito", pasta)
    g(pasta, "merge", "titulo")
    g(pasta, "add", "README.md")  # com os marcadores de conflito
    g(pasta, "commit", "-q", "--no-edit")
    assert any("marcadores" in f for f in lab.conferir("N4-conflito", pasta))


def test_merge_com_commit_no_fast_forward_falha(tmp_path):
    pasta = tmp_path / "lab"
    lab.preparar("N4-fast-forward", pasta)
    g(pasta, "merge", "-q", "--no-ff", "--no-edit", "correcao")
    assert any("fast-forward" in f for f in lab.conferir("N4-fast-forward", pasta))


def test_recusa_pasta_nao_vazia(tmp_path):
    (tmp_path / "x.txt").write_text("x")
    with pytest.raises(lab.ErroLaboratorio, match="não está vazia"):
        lab.preparar("N1-primeiro-commit", tmp_path)


def test_recusa_pasta_dentro_do_repositorio():
    with pytest.raises(lab.ErroLaboratorio, match="dentro deste repositório"):
        lab.preparar("N1-primeiro-commit", lab.RAIZ / "tmp-lab-teste")
    assert not (lab.RAIZ / "tmp-lab-teste").exists()


def test_recusa_pasta_dentro_de_outro_repositorio(tmp_path):
    g(tmp_path, "init", "-q")
    with pytest.raises(lab.ErroLaboratorio, match="dentro do repositório"):
        lab.preparar("N1-primeiro-commit", tmp_path / "lab")


def test_cenario_desconhecido(tmp_path):
    with pytest.raises(lab.ErroLaboratorio, match="desconhecido"):
        lab.preparar("N9-nada", tmp_path / "lab")


def test_cli_listar_e_conferir(tmp_path, capsys):
    assert lab.main(["listar"]) == 0
    assert "N4-conflito" in capsys.readouterr().out
    pasta = tmp_path / "lab"
    assert lab.main(["preparar", "N3-criar-branch", str(pasta)]) == 0
    assert lab.main(["conferir", "N3-criar-branch", str(pasta)]) == 1
    sol_n3a(pasta)
    assert lab.main(["conferir", "N3-criar-branch", str(pasta)]) == 0


def test_configuracao_do_usuario_nao_interfere(tmp_path, monkeypatch):
    """Um alias ou hook na configuração global não muda o que o laboratório prepara."""
    glob = tmp_path / "gitconfig"
    glob.write_text("[core]\n\thooksPath = /caminho/inexistente\n[init]\n\tdefaultBranch = master\n")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(glob))
    pasta = tmp_path / "lab"
    lab.preparar("N3-criar-branch", pasta)
    assert "main" in lab.branches(pasta)


def test_o_laboratorio_nunca_apaga_arquivos():
    """preparar só escreve em pasta vazia ou nova; nenhum caminho do script remove arquivos."""
    fonte = pathlib.Path(lab.__file__).read_text(encoding="utf-8")
    for proibido in ("rmtree", "os.remove", "os.unlink", "rmdir", '"clean"', '"rm"', "_apagar"):
        assert proibido not in fonte, proibido


def test_nivel_5_nao_deixa_clone_auxiliar_na_pasta(tmp_path):
    for cid in ("N5-clonar-e-enviar", "N5-sincronizar"):
        pasta = tmp_path / cid
        lab.preparar(cid, pasta)
        assert sorted(x.name for x in pasta.iterdir()) in (["remoto.git"], ["remoto.git", "trabalho"])


def test_recusa_a_pasta_pessoal_e_a_raiz():
    for pasta in (pathlib.Path.home(), pathlib.Path("/")):
        with pytest.raises(lab.ErroLaboratorio):
            lab.preparar("N1-primeiro-commit", pasta)
