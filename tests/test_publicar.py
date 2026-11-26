"""Testes de scripts/publicar.sh com repositórios locais descartáveis (sem rede)."""
import os
import pathlib
import shutil
import subprocess

import pytest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "scripts" / "publicar.sh"
NOREPLY = "fulano@users.noreply.github.com"

pytestmark = pytest.mark.skipif(shutil.which("bash") is None, reason="precisa de bash")


def _git(cwd, *args, email=NOREPLY):
    env = {**os.environ, "GIT_AUTHOR_NAME": "Fulano", "GIT_AUTHOR_EMAIL": email,
           "GIT_COMMITTER_NAME": "Fulano", "GIT_COMMITTER_EMAIL": email,
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
    return subprocess.run(["git", *args], cwd=cwd, env=env, capture_output=True, text=True, check=True).stdout.strip()


def _escrever(raiz, caminho, texto):
    p = raiz / caminho
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


@pytest.fixture
def repos(tmp_path):
    """Um privado (origin, bare), um público (bare, vazio) e um clone de trabalho com os dois remotos."""
    origin = tmp_path / "privado.git"
    publico = tmp_path / "publico.git"
    for bare in (origin, publico):
        _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(bare))
    work = tmp_path / "work"
    _git(tmp_path, "init", "-q", "-b", "main", str(work))
    _escrever(work, "README.md", "# Plano\n")
    _escrever(work, ".github/dependabot.yml", "version: 2\n")
    _escrever(work, "registro/avaliacoes.md", "| Data | Nota |\n| --- | --- |\n")
    _escrever(work, "registro/respostas.csv", "data,exercicio,resposta\n")
    _git(work, "add", "-A")
    _git(work, "commit", "-q", "-m", "inicial")
    _git(work, "remote", "add", "origin", str(origin))
    _git(work, "remote", "add", "publico", str(publico))
    _git(work, "push", "-q", "origin", "main")
    return work, publico


def _publicar(work, *args, email=NOREPLY, path="/usr/bin:/bin"):
    env = {**os.environ, "GIT_COMMITTER_NAME": "Fulano", "GIT_COMMITTER_EMAIL": email,
           "GIT_AUTHOR_NAME": "Fulano", "GIT_AUTHOR_EMAIL": email,
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "PATH": path}
    return subprocess.run(["bash", str(SCRIPT), "publico", *args], cwd=work, env=env,
                          capture_output=True, text=True)


def _mudar_main(work, caminho, texto, msg="muda"):
    _escrever(work, caminho, texto)
    _git(work, "add", "-A")
    _git(work, "commit", "-q", "-m", msg)
    _git(work, "push", "-q", "origin", "main")


def test_primeira_publicacao_vai_para_main_sem_dependabot(repos):
    work, publico = repos
    r = _publicar(work, "--enviar")
    assert r.returncode == 0, r.stderr
    arquivos = _git(publico, "ls-tree", "-r", "--name-only", "main").splitlines()
    assert "README.md" in arquivos
    assert ".github/dependabot.yml" not in arquivos
    assert _git(publico, "log", "-1", "--format=%ae %s", "main").startswith(NOREPLY + " Publica a main privada")


def test_simulacao_nao_envia(repos):
    work, publico = repos
    r = _publicar(work)
    assert r.returncode == 0, r.stderr
    assert "simulação" in r.stdout
    assert _git(publico, "branch", "--list") == ""


def test_publicacao_seguinte_vai_para_branch_de_pr(repos):
    work, publico = repos
    assert _publicar(work, "--enviar").returncode == 0
    _mudar_main(work, "README.md", "# Plano\n\nNovo.\n")
    r = _publicar(work, "--enviar")
    assert r.returncode == 0, r.stderr
    branches = _git(publico, "branch", "--format=%(refname:short)").splitlines()
    assert any(b.startswith("publicacao/") for b in branches)
    assert _git(publico, "show", "main:README.md") == "# Plano"  # a main não foi tocada


def test_nada_a_publicar(repos):
    work, _ = repos
    assert _publicar(work, "--enviar").returncode == 0
    r = _publicar(work)
    assert r.returncode == 0
    assert "Nada a publicar" in r.stdout


def test_recusa_espelho_divergente(repos, tmp_path):
    work, publico = repos
    assert _publicar(work, "--enviar").returncode == 0
    # Alguém muda o público direto (ex.: um PR do Dependabot mesclado lá).
    outro = tmp_path / "outro"
    _git(tmp_path, "clone", "-q", str(publico), str(outro))
    _escrever(outro, "requirements.txt", "pyyaml==9\n")
    _git(outro, "add", "-A")
    _git(outro, "commit", "-q", "-m", "Bump pyyaml")
    _git(outro, "push", "-q", "origin", "main")
    _mudar_main(work, "README.md", "# Plano\n\nNovo.\n")
    r = _publicar(work, "--enviar")
    assert r.returncode != 0
    assert "não vieram de uma publicação" in r.stderr


# Montado em partes para que o próprio arquivo não tenha um endereço pessoal: o publicar.sh
# varre a árvore da main inteira, inclusive tests/, e recusaria publicar por causa dele.
EMAIL_PESSOAL = "alguem" + "@" + "hotmail.com"


def test_recusa_email_pessoal_na_arvore(repos):
    work, _ = repos
    _mudar_main(work, "docs/contato.md", f"Fale comigo: {EMAIL_PESSOAL}\n")
    r = _publicar(work)
    assert r.returncode != 0
    assert "e-mail" in r.stderr
    assert "hotmail" not in r.stderr  # o erro não repete o endereço


def test_aceita_emails_de_exemplo(repos):
    work, _ = repos
    _mudar_main(work, "docs/contato.md", "Use fulano@example.com ou x@users.noreply.github.com\n")
    assert _publicar(work).returncode == 0


def test_recusa_identidade_que_nao_e_noreply(repos):
    work, _ = repos
    r = _publicar(work, email=EMAIL_PESSOAL)
    assert r.returncode != 0
    assert "noreply" in r.stderr


def test_recusa_dado_de_estudo(repos):
    work, _ = repos
    _mudar_main(work, "registro/estado.yml", "schema_version: 1\n")
    r = _publicar(work)
    assert r.returncode != 0
    assert "dado de estudo" in r.stderr


def test_remoto_local_nunca_chama_gh(repos, tmp_path):
    """Com um gh falso no PATH, um remoto que não é do GitHub não pode acionar o gh."""
    work, publico = repos
    falso = tmp_path / "bin"
    falso.mkdir()
    marca = tmp_path / "gh-chamado"
    (falso / "gh").write_text(f"#!/bin/sh\ntouch {marca}\nexit 1\n")
    (falso / "gh").chmod(0o755)
    assert _publicar(work, "--enviar").returncode == 0
    _mudar_main(work, "README.md", "# Plano\n\nNovo.\n")
    r = _publicar(work, "--enviar", path=f"{falso}:/usr/bin:/bin")
    assert r.returncode == 0, r.stderr
    assert not marca.exists()
    assert "Abra o pull request" in r.stdout


def test_publico_recriado_vazio_nao_conta_como_divergencia(repos, tmp_path):
    """Se o público foi apagado e recriado vazio, a ref antiga publico/main não pode bloquear a publicação."""
    work, publico = repos
    assert _publicar(work, "--enviar").returncode == 0
    _git(work, "fetch", "-q", "publico")
    shutil.rmtree(publico)
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(publico))
    r = _publicar(work, "--enviar")
    assert r.returncode == 0, r.stderr
    assert "Primeira publicação" in r.stdout
