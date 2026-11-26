#!/usr/bin/env python3
"""Junta, sem editar, a saída de um caso executado: resposta ao estudante, arquivos alterados,
diff e resultado do --checar na cópia do repositório.

Uso:
    python tests/skill/coletar.py <bench_dir> <ID> <baseline|with_skill> <destino.md>
"""
import pathlib
import subprocess
import sys


def rodar(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip()


def coletar(bench, caso, grupo):
    bench = pathlib.Path(bench)
    resposta = bench / "out" / grupo / f"{caso}.md"
    repo = bench / grupo / caso
    partes = [f"# {caso} · {grupo}", "", "## Resposta ao estudante", "",
              resposta.read_text(encoding="utf-8") if resposta.exists() else "(nenhuma resposta gravada)"]
    if (repo / ".git").exists():
        partes += ["", "## Arquivos alterados", "", "```", rodar(["git", "status", "--short"], repo) or "(nenhum)", "```",
                   "", "## Diff", "", "```diff", rodar(["git", "diff", "--", ".", ":(exclude)PROGRESSO.md", ":(exclude)MAPA.md"], repo)[:20000], "```",
                   "", "## Arquivos novos", ""]
        novos = rodar(["git", "ls-files", "--others", "--exclude-standard"], repo).splitlines()
        for n in novos[:12]:
            partes += [f"### {n}", "", "```", (repo / n).read_text(encoding="utf-8", errors="replace")[:6000], "```", ""]
        partes += ["## progresso.py --checar", "", "```", rodar(["python", "scripts/progresso.py", "--checar"], repo) or "(sem saída)", "```"]
        partes += ["", "## Commits", "", "```", rodar(["git", "log", "--oneline"], repo), "```"]
    else:
        arquivos = sorted(str(p.relative_to(repo)) for p in repo.rglob("*") if p.is_file() and "skills" not in p.parts)
        partes += ["", "## Arquivos criados na pasta (fora de skills/)", "", "```", "\n".join(arquivos) or "(nenhum)", "```"]
    return "\n".join(partes) + "\n"


if __name__ == "__main__":
    bench, caso, grupo, destino = sys.argv[1:5]
    destino = pathlib.Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(coletar(bench, caso, grupo), encoding="utf-8")
    print(destino)
