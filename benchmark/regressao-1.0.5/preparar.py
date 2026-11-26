"""Prepara os casos da regressão 1.0.5. Uso: python benchmark/regressao-1.0.5/preparar.py <pasta> [casos...]

Cópia de tests/skill/preparar_caso.py + remoto bare com a main (sem andamento) e estudo_ana (com estudante.yml)."""
import pathlib, subprocess, sys, shutil
RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tests" / "skill")); sys.path.insert(0, str(RAIZ / "scripts"))
import preparar_caso as pc
from estado import carregar_estado, formatar_estado
B = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("/tmp/bench105")
LAB = ["N1-primeiro-commit", "N1-staging-parcial", "N2-restaurar", "N2-versao-antiga", "N3-criar-branch",
       "N3-limpar-branches", "N4-fast-forward", "N4-conflito", "N5-clonar-e-enviar", "N5-sincronizar"]
CASOS = {"A-L4-01": {}, "V-03": {}, "BV-02": {}, "BV-05": {},
         "L-01": {"ng1": True}, "L-02": {"ng1": True, "lab": LAB[:3]}, "L-03": {"ng1": True, "lab": LAB[:6]},
         "L-04": {"ng1": True, "lab": LAB, "dias": 3}, "L-05": {"ng1": True, "lab": LAB[:4]}}
def g(cwd, *a): subprocess.run(["git", "-c", "user.name=bench", "-c", "user.email=bench@local", *a], cwd=cwd, check=True, capture_output=True)
def preparar(caso):
    base = caso if not caso.startswith("L-") else "L"
    d = B / "with_skill" / caso
    pc.preparar(base, "with_skill", d)
    cfg = CASOS[caso]
    estado = (d / "registro/estado.yml").read_text()
    # a main não tem estado.yml (regra do fluxo); a branch de estudo tem
    g(d, "branch", "-M", "main")
    g(d, "rm", "-q", "--cached", "registro/estado.yml"); (d / "registro/estado.yml").unlink()
    g(d, "commit", "-qm", "main sem andamento")
    g(d, "switch", "-qc", "estudo_ana")
    (d / "registro/estado.yml").write_text(estado)
    (d / "registro/estudante.yml").write_text("schema_version: 1\nbranch: estudo_ana\ngithub: rodrigorosario-jpg\n")
    if cfg.get("ng1"):
        mods = dict(carregar_estado(d).get("modulos") or {})
        mods["NG1"] = {"status": "em_andamento", "inicio": __import__("datetime").date(2026, 11, 2)}
        (d / "registro/estado.yml").write_text(formatar_estado(mods))
    lab = cfg.get("lab", [])
    if lab:
        dias = cfg.get("dias", 2)
        av = d / "registro/avaliacoes.md"
        txt = av.read_text().rstrip("\n") + "\n"
        for i, c in enumerate(lab):
            txt += f"| 2026-11-{10 + (i % dias):02d} | NG1 | laboratorio | 1 | 1 | {c} | |\n"
        av.write_text(txt)
    subprocess.run(["python3", "scripts/progresso.py"], cwd=d, capture_output=True)
    g(d, "add", "-A"); g(d, "commit", "-qm", "andamento")
    g(d, "switch", "-q", "main")
    remoto = B / "remotos" / f"{caso}.git"
    if remoto.exists(): shutil.rmtree(remoto)
    g(B, "clone", "-q", "--bare", str(d), str(remoto))
    g(d, "remote", "add", "origin", str(remoto)); g(d, "fetch", "-q", "origin")
    g(d, "branch", "-q", "-u", "origin/main", "main")
    return d
if __name__ == "__main__":
    for c in (sys.argv[2:] or CASOS):
        print(preparar(c))
