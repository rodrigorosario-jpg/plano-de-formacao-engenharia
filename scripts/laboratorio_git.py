#!/usr/bin/env python3
"""Laboratório de Git da NG1: cenários preparados e conferidos em repositórios descartáveis.

Cada cenário cria um repositório num estado conhecido; quem estuda resolve com os próprios comandos;
o script confere o resultado olhando só o estado do repositório.

Uso:
    python scripts/laboratorio_git.py listar
    python scripts/laboratorio_git.py enunciado N4-conflito
    python scripts/laboratorio_git.py preparar N4-conflito /tmp/lab-conflito
    python scripts/laboratorio_git.py conferir N4-conflito /tmp/lab-conflito

Segurança (docs/arquitetura/seguranca.md):
- os cenários são código deste arquivo, revisado; nada é lido de YAML nem do conteúdo do repositório;
- a pasta tem de estar vazia ou não existir, fora deste repositório e fora de qualquer outro repositório Git;
- o remoto do nível 5 é um repositório bare local; nada usa a rede;
- o git do script roda sem a configuração global e de sistema, sem hooks e sem fsmonitor, com identidade fixa;
- o script nunca apaga arquivos de quem estuda: preparar só escreve numa pasta vazia ou nova (o clone
  auxiliar do nível 5 vive num tempfile.TemporaryDirectory), e conferir só lê;
- conferir só pastas que você mesmo preparou: a configuração local de um repositório de terceiros
  (filtros do .gitattributes, por exemplo) ainda pode rodar comandos durante o git status.
"""
import os
import pathlib
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent

AMBIENTE_GIT = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Laboratório",
    "GIT_AUTHOR_EMAIL": "laboratorio@example.com",
    "GIT_COMMITTER_NAME": "Laboratório",
    "GIT_COMMITTER_EMAIL": "laboratorio@example.com",
    "GIT_TERMINAL_PROMPT": "0",
}
OPCOES_SEGURAS = ["-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
                  "-c", "init.defaultBranch=main", "-c", "protocol.allow=never", "-c", "protocol.file.allow=always"]


class ErroLaboratorio(Exception):
    pass


def git(pasta, *args, checar=True, cru=False):
    """Roda git na pasta com o ambiente controlado; devolve a saída sem espaços nas pontas (cru=True: sem tirar)."""
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(pasta), "LANG": "C", **AMBIENTE_GIT}
    r = subprocess.run(["git", *OPCOES_SEGURAS, *args], cwd=pasta, env=env, capture_output=True, text=True,
                       stdin=subprocess.DEVNULL, timeout=30)
    if checar and r.returncode != 0:
        raise ErroLaboratorio(f"git {' '.join(args)} falhou: {r.stderr.strip()}")
    return r.stdout if cru else r.stdout.strip()


def escrever(pasta, caminho, texto):
    p = pathlib.Path(pasta) / caminho
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


def ler(pasta, caminho):
    p = pathlib.Path(pasta) / caminho
    return p.read_text(encoding="utf-8") if p.exists() else None


def commit(pasta, msg, *arquivos):
    git(pasta, "add", "--", *(arquivos or ["."]))
    git(pasta, "commit", "-q", "-m", msg)


def novo_repo(pasta):
    pathlib.Path(pasta).mkdir(parents=True, exist_ok=True)
    git(pasta, "init", "-q")


# ---------- consultas usadas pelas conferências ----------

def eh_repo(pasta):
    return (pathlib.Path(pasta) / ".git").exists()


def n_commits(pasta, ref="HEAD"):
    r = git(pasta, "rev-list", "--count", ref, checar=False)
    return int(r) if r.isdigit() else 0


def arquivos_no(pasta, ref="HEAD"):
    return set(git(pasta, "ls-tree", "-r", "--name-only", ref, checar=False).splitlines())


def status(pasta):
    """Linhas de git status --porcelain (inclui não rastreados)."""
    return [l for l in git(pasta, "status", "--porcelain", "--untracked-files=all", cru=True).splitlines() if l]


def branches(pasta):
    return set(git(pasta, "branch", "--format=%(refname:short)").splitlines()) - {""}


def branch_atual(pasta):
    return git(pasta, "symbolic-ref", "--short", "-q", "HEAD", checar=False)


def sha(pasta, ref):
    return git(pasta, "rev-parse", "-q", "--verify", f"{ref}^{{commit}}", checar=False)


def mostrar(pasta, ref, caminho):
    return git(pasta, "show", f"{ref}:{caminho}", checar=False)


def pais(pasta, ref="HEAD"):
    return git(pasta, "rev-list", "--parents", "-n", "1", ref).split()[1:]


# ---------- cenários ----------
# Cada cenário: nivel, titulo, enunciado, preparar(pasta), conferir(pasta) -> lista de falhas.

def _n1a_preparar(p):
    escrever(p, "README.md", "# Meu projeto\n")
    escrever(p, "notas.txt", "anotações pessoais, não versionar\n")


def _n1a_conferir(p):
    if not eh_repo(p):
        return ["a pasta ainda não é um repositório (git init)"]
    falhas = []
    if n_commits(p) != 1:
        falhas.append(f"esperava 1 commit; há {n_commits(p)}")
    if arquivos_no(p) != {"README.md"}:
        falhas.append(f"o commit deve ter só README.md; tem {sorted(arquivos_no(p)) or 'nada'}")
    if git(p, "ls-files", "--", "notas.txt") or ler(p, "notas.txt") is None:
        falhas.append("notas.txt deve continuar fora do Git (não rastreado), e existir na pasta")
    return falhas


def _n1b_preparar(p):
    novo_repo(p)
    escrever(p, "a.txt", "linha 1\n")
    escrever(p, "b.txt", "linha 1\n")
    commit(p, "inicial")
    escrever(p, "a.txt", "linha 1\nlinha 2 de a\n")
    escrever(p, "b.txt", "linha 1\nrascunho de b, ainda não\n")


def _n1b_conferir(p):
    falhas = []
    if n_commits(p) != 2:
        return [f"esperava 2 commits (o inicial e o seu); há {n_commits(p)}"]
    mudados = set(git(p, "diff", "--name-only", "HEAD~1", "HEAD").splitlines())
    if mudados != {"a.txt"}:
        falhas.append(f"o seu commit deve mudar só a.txt; mudou {sorted(mudados)}")
    if mostrar(p, "HEAD", "a.txt") != "linha 1\nlinha 2 de a":
        falhas.append("a.txt no commit não tem a linha 2")
    if [l for l in status(p) if not l.startswith(" M b.txt")]:
        falhas.append(f"só b.txt deve aparecer modificado e fora do staging; status: {status(p)}")
    if ler(p, "b.txt") != "linha 1\nrascunho de b, ainda não\n":
        falhas.append("a mudança em b.txt foi perdida: ela deve continuar na pasta")
    return falhas


def _n2a_preparar(p):
    novo_repo(p)
    escrever(p, "config.txt", "modo=producao\n")
    escrever(p, "dados.txt", "1,2,3\n")
    escrever(p, "app.py", "print('oi')\n")
    commit(p, "inicial")
    escrever(p, "app.py", "print('olá')\n")
    commit(p, "saudação em português")
    escrever(p, "config.txt", "modo=teste  # NÃO era para mudar\n")
    (pathlib.Path(p) / "dados.txt").unlink()
    escrever(p, "segredo.env", "TOKEN=nao-commitar\n")
    git(p, "add", "segredo.env")


def _n2a_conferir(p):
    falhas = []
    if n_commits(p) != 2:
        falhas.append(f"não era para criar nem desfazer commits; há {n_commits(p)}, esperava 2")
    if ler(p, "config.txt") != "modo=producao\n":
        falhas.append("config.txt não voltou à versão do último commit")
    if ler(p, "dados.txt") != "1,2,3\n":
        falhas.append("dados.txt não foi recuperado")
    if "segredo.env" in git(p, "diff", "--cached", "--name-only").splitlines():
        falhas.append("segredo.env continua no staging: tire-o de lá")
    if ler(p, "segredo.env") is None:
        falhas.append("segredo.env sumiu da pasta: era para tirar do staging, não apagar")
    resto = [l for l in status(p) if l != "?? segredo.env"]
    if resto:
        falhas.append(f"a pasta deveria estar limpa, exceto segredo.env não rastreado; status: {resto}")
    return falhas


VERSAO_BOA = "limite=10\ntimeout=30\n"


def _n2b_preparar(p):
    novo_repo(p)
    escrever(p, "limites.cfg", "limite=5\n")
    commit(p, "limites iniciais")
    escrever(p, "limites.cfg", VERSAO_BOA)
    commit(p, "ajusta limite e timeout")
    escrever(p, "limites.cfg", "limite=999\ntimeout=0\n")
    escrever(p, "LEIAME.md", "Configuração do serviço.\n")
    commit(p, "teste rápido (quebrou a produção)")
    escrever(p, "LEIAME.md", "Configuração do serviço.\nVeja limites.cfg.\n")
    commit(p, "documenta limites")


def _n2b_conferir(p):
    falhas = []
    if n_commits(p) != 5:
        return [f"esperava os 4 commits originais mais 1 seu; há {n_commits(p)}"]
    if mostrar(p, "HEAD", "limites.cfg") != VERSAO_BOA.strip():
        falhas.append("limites.cfg no último commit não é a versão de 'ajusta limite e timeout'")
    if git(p, "diff", "--name-only", "HEAD~1", "HEAD").splitlines() != ["limites.cfg"]:
        falhas.append("o seu commit deve mudar só limites.cfg")
    if "Veja limites.cfg." not in (mostrar(p, "HEAD", "LEIAME.md") or ""):
        falhas.append("LEIAME.md perdeu a mudança do último commit; volte só limites.cfg")
    if status(p):
        falhas.append(f"a pasta deveria estar limpa; status: {status(p)}")
    return falhas


def _n3a_preparar(p):
    novo_repo(p)
    escrever(p, "index.html", "<h1>Início</h1>\n")
    commit(p, "página inicial")
    escrever(p, "estilo.css", "h1 { color: navy; }\n")
    commit(p, "estilo")


def _n3a_conferir(p):
    falhas = []
    if "feature/rodape" not in branches(p):
        return ["a branch feature/rodape não existe"]
    if n_commits(p, "main") != 2:
        falhas.append("a main mudou: ela deve continuar com os 2 commits iniciais")
    if git(p, "rev-list", "--count", "main..feature/rodape") != "1":
        falhas.append("feature/rodape deve ter exatamente 1 commit além da main")
    if git(p, "merge-base", "main", "feature/rodape") != sha(p, "main"):
        falhas.append("feature/rodape deve sair da ponta da main")
    if "rodape.html" not in arquivos_no(p, "feature/rodape"):
        falhas.append("o commit da feature/rodape deve criar rodape.html")
    if "rodape.html" in arquivos_no(p, "main"):
        falhas.append("rodape.html não pode estar na main")
    if branch_atual(p) != "main":
        falhas.append(f"volte para a main ao terminar (está em {branch_atual(p) or 'HEAD destacado'})")
    if status(p):
        falhas.append(f"a pasta deveria estar limpa; status: {status(p)}")
    return falhas


def _n3b_preparar(p):
    novo_repo(p)
    escrever(p, "base.txt", "base\n")
    commit(p, "base")
    for b, arq in (("antiga", "antiga.txt"), ("experimento", "experimento.txt"), ("manter", "manter.txt")):
        git(p, "switch", "-q", "-c", b, "main")
        escrever(p, arq, f"{b}\n")
        commit(p, f"trabalho em {b}")
    git(p, "switch", "-q", "main")
    git(p, "merge", "-q", "--no-edit", "antiga")


def _n3b_conferir(p):
    falhas = []
    sobra = branches(p)
    if sobra != {"main", "manter"}:
        falhas.append(f"devem sobrar só main e manter; há {sorted(sobra)}")
    if "manter" in sobra and "manter.txt" not in arquivos_no(p, "manter"):
        falhas.append("a branch manter perdeu o commit dela")
    if "antiga.txt" not in arquivos_no(p, "main"):
        falhas.append("a main perdeu o merge de antiga")
    return falhas


def _n4a_preparar(p):
    novo_repo(p)
    escrever(p, "calc.py", "def soma(a, b):\n    return a - b\n")
    commit(p, "soma")
    git(p, "switch", "-q", "-c", "correcao")
    escrever(p, "calc.py", "def soma(a, b):\n    return a + b\n")
    commit(p, "corrige soma")
    escrever(p, "test_calc.py", "from calc import soma\n\nassert soma(2, 3) == 5\n")
    commit(p, "teste da soma")
    git(p, "switch", "-q", "main")


def _n4a_conferir(p):
    falhas = []
    if sha(p, "main") != sha(p, "correcao"):
        falhas.append("a main deve apontar para o mesmo commit da correcao (fast-forward)")
    if git(p, "rev-list", "--merges", "--count", "main") != "0":
        falhas.append("há commit de merge: este merge deve ser fast-forward, sem commit novo")
    if n_commits(p, "main") != 3:
        falhas.append(f"a main deve ter 3 commits; tem {n_commits(p, 'main')}")
    if status(p):
        falhas.append(f"a pasta deveria estar limpa; status: {status(p)}")
    return falhas


TITULO_FINAL = "# Plano de Estudos: versão 2"


def _n4b_preparar(p):
    novo_repo(p)
    escrever(p, "README.md", "# Plano de estudos\n\nTexto.\n")
    commit(p, "readme")
    git(p, "switch", "-q", "-c", "titulo")
    escrever(p, "README.md", "# Plano de Estudos\n\nTexto.\n")
    commit(p, "maiúsculas no título")
    git(p, "switch", "-q", "main")
    escrever(p, "README.md", "# Plano de estudos: versão 2\n\nTexto.\n")
    commit(p, "marca a versão 2")


def _n4b_conferir(p):
    falhas = []
    if pathlib.Path(p, ".git", "MERGE_HEAD").exists():
        return ["o merge ainda está em andamento: resolva, adicione e conclua com git commit (ou aborte)"]
    if len(pais(p, "main")) != 2:
        return ["o último commit da main deve ser o merge de titulo (um commit com dois pais)"]
    if sha(p, "titulo") not in pais(p, "main"):
        falhas.append("o merge não trouxe a branch titulo")
    readme = mostrar(p, "main", "README.md")
    if any(m in readme for m in ("<<<<<<<", "=======", ">>>>>>>")):
        falhas.append("README.md ficou com marcadores de conflito")
    if readme.splitlines()[:1] != [TITULO_FINAL]:
        falhas.append(f"a primeira linha do README.md deve ser exatamente: {TITULO_FINAL}")
    if "Texto." not in readme:
        falhas.append("o corpo do README.md se perdeu na resolução")
    if status(p):
        falhas.append(f"a pasta deveria estar limpa; status: {status(p)}")
    return falhas


def _remoto_com(p, tmp, commits):
    """Cria p/remoto.git (bare) com os commits dados [(arquivo, texto, msg)], via um clone em tmp.

    tmp é uma pasta de tempfile.TemporaryDirectory: o Python a cria e a remove; o script não apaga nada."""
    remoto = pathlib.Path(p) / "remoto.git"
    git(p, "init", "-q", "--bare", str(remoto))
    tmp = pathlib.Path(tmp) / "clone"
    git(p, "clone", "-q", str(remoto), str(tmp))
    for arq, texto, msg in commits:
        escrever(tmp, arq, texto)
        commit(tmp, msg)
    git(tmp, "push", "-q", "origin", "HEAD:main")
    return remoto, tmp


def _n5a_preparar(p):
    pathlib.Path(p).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="lab-git-") as t:
        _remoto_com(p, t, [("README.md", "# Projeto do grupo\n", "inicial")])


def _n5a_conferir(p):
    remoto = pathlib.Path(p) / "remoto.git"
    trabalho = pathlib.Path(p) / "trabalho"
    falhas = []
    if not eh_repo(trabalho):
        return ["clone remoto.git na pasta trabalho (git clone remoto.git trabalho)"]
    if git(trabalho, "config", "--get", "remote.origin.url", checar=False) == "":
        falhas.append("trabalho não tem o remoto origin")
    if n_commits(remoto, "main") != 2:
        falhas.append(f"a main do remoto deve ter 2 commits (o inicial e o seu); tem {n_commits(remoto, 'main')}")
    if "novo.txt" not in arquivos_no(remoto, "main"):
        falhas.append("novo.txt não chegou ao remoto (commit e push)")
    if sha(trabalho, "main") != sha(remoto, "main"):
        falhas.append("a main local e a do remoto estão diferentes")
    return falhas


def _n5b_preparar(p):
    pathlib.Path(p).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="lab-git-") as t:
        remoto, tmp = _remoto_com(p, t, [("app.py", "print(1)\n", "inicial"), ("app.py", "print(2)\n", "versão 2")])
        trabalho = pathlib.Path(p) / "trabalho"
        git(p, "clone", "-q", str(remoto), str(trabalho))
        git(trabalho, "branch", "--unset-upstream")
        escrever(trabalho, "docs.md", "Como rodar: python app.py\n")
        commit(trabalho, "documentação")
        escrever(tmp, "CHANGELOG.md", "- versão 2\n")
        commit(tmp, "changelog, enviado por outra pessoa")
        git(tmp, "push", "-q", "origin", "HEAD:main")


def _n5b_conferir(p):
    remoto = pathlib.Path(p) / "remoto.git"
    trabalho = pathlib.Path(p) / "trabalho"
    falhas = []
    nomes = git(remoto, "log", "--format=%s", "main").splitlines()
    for msg in ("documentação", "changelog, enviado por outra pessoa"):
        if msg not in nomes:
            falhas.append(f"o commit '{msg}' não está na main do remoto")
    if sha(trabalho, "main") != sha(remoto, "main"):
        falhas.append("a main local e a do remoto estão diferentes: falta integrar ou enviar")
    if git(trabalho, "rev-parse", "--abbrev-ref", "main@{upstream}", checar=False) != "origin/main":
        falhas.append("a main local não acompanha origin/main (configure o upstream, por exemplo com git push -u)")
    if status(trabalho):
        falhas.append(f"trabalho deveria estar limpa; status: {status(trabalho)}")
    return falhas


CENARIOS = {
    "N1-primeiro-commit": {
        "nivel": 1, "titulo": "Primeiro commit, escolhendo o que entra",
        "enunciado": "A pasta tem README.md e notas.txt. Transforme-a num repositório e faça um commit só com "
                     "README.md. notas.txt fica fora do Git (não rastreado) e continua na pasta.",
        "preparar": _n1a_preparar, "conferir": _n1a_conferir},
    "N1-staging-parcial": {
        "nivel": 1, "titulo": "Commitar só parte das mudanças",
        "enunciado": "a.txt e b.txt estão modificados. Faça um commit só com a mudança de a.txt. "
                     "A mudança de b.txt continua na pasta, fora do staging.",
        "preparar": _n1b_preparar, "conferir": _n1b_conferir},
    "N2-restaurar": {
        "nivel": 2, "titulo": "Desfazer mudanças locais sem commit",
        "enunciado": "Alguém mexeu em config.txt, apagou dados.txt e pôs segredo.env no staging. Sem criar commit: "
                     "volte config.txt e dados.txt à versão do último commit e tire segredo.env do staging, "
                     "sem apagá-lo da pasta.",
        "preparar": _n2a_preparar, "conferir": _n2a_conferir},
    "N2-versao-antiga": {
        "nivel": 2, "titulo": "Trazer de volta a versão antiga de um arquivo",
        "enunciado": "Um commit 'teste rápido' quebrou limites.cfg, e depois veio outro commit bom em LEIAME.md. "
                     "Ache no histórico a versão de limites.cfg do commit 'ajusta limite e timeout' e faça um commit "
                     "novo que volta só esse arquivo àquela versão. Não reescreva o histórico.",
        "preparar": _n2b_preparar, "conferir": _n2b_conferir},
    "N3-criar-branch": {
        "nivel": 3, "titulo": "Trabalhar numa branch sem tocar a main",
        "enunciado": "Crie a branch feature/rodape a partir da main, faça nela um commit que cria rodape.html "
                     "(qualquer conteúdo) e volte para a main. A main não muda.",
        "preparar": _n3a_preparar, "conferir": _n3a_conferir},
    "N3-limpar-branches": {
        "nivel": 3, "titulo": "Apagar branches com segurança",
        "enunciado": "Há três branches além da main: antiga (já mesclada), experimento (não mesclada, descartável) "
                     "e manter. Apague antiga e experimento; manter fica. Repare por que uma delas pede -D.",
        "preparar": _n3b_preparar, "conferir": _n3b_conferir},
    "N4-fast-forward": {
        "nivel": 4, "titulo": "Merge fast-forward",
        "enunciado": "A branch correcao está 2 commits à frente da main. Mescle correcao na main sem criar commit "
                     "de merge.",
        "preparar": _n4a_preparar, "conferir": _n4a_conferir},
    "N4-conflito": {
        "nivel": 4, "titulo": "Resolver um conflito de merge",
        "enunciado": f"Mescle a branch titulo na main. As duas mudaram a primeira linha do README.md. Resolva o "
                     f"conflito para que a primeira linha fique exatamente '{TITULO_FINAL}' e conclua o merge.",
        "preparar": _n4b_preparar, "conferir": _n4b_conferir},
    "N5-clonar-e-enviar": {
        "nivel": 5, "titulo": "Clonar, commitar e enviar",
        "enunciado": "remoto.git faz o papel do GitHub. Clone-o na pasta trabalho, crie novo.txt, faça o commit "
                     "e envie para a main do remoto.",
        "preparar": _n5a_preparar, "conferir": _n5a_conferir},
    "N5-sincronizar": {
        "nivel": 5, "titulo": "Integrar o trabalho de outra pessoa antes de enviar",
        "enunciado": "Em trabalho você tem um commit local ('documentação'). Enquanto isso, outra pessoa enviou "
                     "um commit para o remoto. Traga esse commit, integre com o seu e envie. Ao final, a main local "
                     "acompanha origin/main.",
        "preparar": _n5b_preparar, "conferir": _n5b_conferir},
}


def _validar_pasta(pasta):
    pasta = pathlib.Path(pasta).expanduser().resolve()
    if pasta == RAIZ or RAIZ in pasta.parents:
        raise ErroLaboratorio("a pasta do laboratório não pode ficar dentro deste repositório")
    if pasta.exists() and any(pasta.iterdir()):
        raise ErroLaboratorio(f"{pasta} não está vazia; use uma pasta nova")
    acima = pasta.parent
    while not acima.exists():
        acima = acima.parent
    dentro = subprocess.run(["git", "-C", str(acima), "rev-parse", "--show-toplevel"], capture_output=True,
                            text=True, env={**os.environ, **AMBIENTE_GIT}, stdin=subprocess.DEVNULL)
    if dentro.returncode == 0:
        raise ErroLaboratorio(f"{pasta} fica dentro do repositório {dentro.stdout.strip()}; use uma pasta fora dele, "
                              "como /tmp/lab")
    return pasta


def preparar(cid, pasta):
    c = _cenario(cid)
    pasta = _validar_pasta(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    c["preparar"](pasta)
    return pasta


def conferir(cid, pasta):
    c = _cenario(cid)
    pasta = pathlib.Path(pasta).expanduser().resolve()
    if not pasta.is_dir():
        raise ErroLaboratorio(f"{pasta} não existe; rode preparar antes")
    return c["conferir"](pasta)


def _cenario(cid):
    if cid not in CENARIOS:
        raise ErroLaboratorio(f"cenário desconhecido: {cid}; veja a lista com: listar")
    return CENARIOS[cid]


def main(argv):
    if not argv or argv[0] not in ("listar", "enunciado", "preparar", "conferir"):
        print(__doc__.strip().split("\n\n")[1])
        return 2
    try:
        if argv[0] == "listar":
            for cid, c in CENARIOS.items():
                print(f"nível {c['nivel']}  {cid:22} {c['titulo']}")
            return 0
        if argv[0] == "enunciado":
            c = _cenario(argv[1])
            print(f"{argv[1]} (nível {c['nivel']}): {c['titulo']}\n\n{c['enunciado']}")
            return 0
        if len(argv) != 3:
            raise ErroLaboratorio(f"uso: {argv[0]} <cenário> <pasta>")
        if argv[0] == "preparar":
            pasta = preparar(argv[1], argv[2])
            print(f"Cenário pronto em {pasta}.\n\n{CENARIOS[argv[1]]['enunciado']}\n\n"
                  f"Ao terminar: python scripts/laboratorio_git.py conferir {argv[1]} {pasta}")
            return 0
        falhas = conferir(argv[1], argv[2])
    except ErroLaboratorio as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 2
    if falhas:
        print("Ainda não:")
        for f in falhas:
            print(f"- {f}")
        return 1
    print(f"Cenário {argv[1]} resolvido. Anote a data na evidência do portão da NG1.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
