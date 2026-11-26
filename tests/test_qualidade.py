import time

from esquema import RAIZ
from qualidade import gerar_relatorio, medir

from test_catalogo import montar


def linha(relatorio, criterio):
    achadas = [l for l in relatorio.splitlines() if l.startswith(f"| {criterio}")]
    assert len(achadas) == 1, relatorio
    return [c.strip() for c in achadas[0].strip("|").split("|")]


def cabecalho(codigo, andamento=True, comps=0, fase="graduacao", eixo="Matemática"):
    extra = "status: nao_iniciada\ninicio: null\n" if andamento else ""
    sem = "semestre_inicio: 1\nsemestre_fim: 1\n" if fase != "nivelamento" else 'bloco: "A"\nsemestre_inicio: 0\nsemestre_fim: 0\n'
    lista = "".join(f"  - {{id: {codigo}.c0{i}, nome: c}}\n" for i in range(1, comps + 1))
    return (f"---\ncodigo: {codigo}\nordem: 1\nnome: N\neixo: {eixo}\nfase: {fase}\n{sem}horas_previstas: 10\n"
            f"nivel_alvo: 3\nprerequisitos: []\nrequer_unidades: [U1.1]\n"
            + (f"competencias:\n{lista}" if comps else "")
            + f"{extra}portao:\n  criterio: x\n---\nVer PJ1.\n")


def preparar(tmp_path, andamento=True):
    montar(tmp_path)
    (tmp_path / "disciplinas/XA1.md").write_text(cabecalho("XA1", andamento), encoding="utf-8")
    (tmp_path / "disciplinas/XA2.md").write_text(cabecalho("XA2", andamento), encoding="utf-8")
    (tmp_path / "disciplinas/XN0.md").write_text(cabecalho("XN0", andamento, 2, "nivelamento", "Física"), encoding="utf-8")
    return tmp_path


def test_relatorio_de_repositorio_coerente(tmp_path):
    rel = gerar_relatorio(preparar(tmp_path, andamento=False))
    assert rel.startswith("# Relatório de qualidade")
    assert linha(rel, "Itens com ID único verificado")[1].startswith("100%")
    assert linha(rel, "Progresso separado do conhecimento")[1] == "Sim"
    assert linha(rel, "Listas com verificação")[1].startswith("100%")
    assert linha(rel, "Referências a unidades e projetos resolvidas")[1].startswith("100%")
    comp = linha(rel, "Competências por fase")[1]
    assert "nivelamento: 1 de 1 arquivos com competências (2 no total)" in comp and "graduação: 0 de 2" in comp


def test_relatorio_mostra_falhas(tmp_path):
    raiz = preparar(tmp_path)
    (raiz / "disciplinas/XA1-copia.md").write_text(cabecalho("XA1").replace("ordem: 1\n", ""), encoding="utf-8")
    (raiz / "disciplinas/XA2.md").write_text(cabecalho("XA2").replace("PJ1", "PJ9"), encoding="utf-8")
    (raiz / "exercicios/XA1/2-antiga.md").write_text("1. x\n", encoding="utf-8")
    rel = gerar_relatorio(raiz)
    assert not linha(rel, "Itens com ID único verificado")[1].startswith("100%")
    assert linha(rel, "Metadados validados por schema")[1] != "100%"
    assert not linha(rel, "Referências a unidades e projetos resolvidas")[1].startswith("100%")
    assert linha(rel, "Listas com verificação")[1].startswith("50%")
    assert linha(rel, "Progresso separado do conhecimento")[1].startswith("Não")


def test_medir_sem_efeitos_colaterais(tmp_path):
    raiz = preparar(tmp_path)
    antes = {p: p.read_bytes() for p in raiz.rglob("*") if p.is_file()}
    m = medir(raiz)
    assert {p: p.read_bytes() for p in raiz.rglob("*") if p.is_file()} == antes
    assert m["progresso_separado"] is False


def test_repositorio_real():
    inicio = time.perf_counter()
    rel = gerar_relatorio(RAIZ)
    assert time.perf_counter() - inicio < 0.5
    assert linha(rel, "Metadados validados por schema")[1].startswith("100%")
    assert linha(rel, "Itens com ID único verificado")[1].startswith("100%")
    assert linha(rel, "Referências a unidades e projetos resolvidas")[1].startswith("100%")
    assert linha(rel, "Listas com verificação")[1].startswith("100%")
    assert linha(rel, "Progresso separado do conhecimento")[1] == "Sim"
