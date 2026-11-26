import pathlib
import time

import pytest
import yaml

from catalogo import avisos_catalogo, validar_catalogo
from esquema import RAIZ, carregar_cabecalhos
import catalogo

AVALIACOES = """# Avaliações

## Níveis de exercício

| Nível | Nome | O que treina |
| --- | --- | --- |
| 1 | Fácil | Aplicar direto |
| 2 | Difícil | Combinar |

A escala é a mesma.
"""


def disciplina(codigo, eixo="Matemática", fase="graduacao", pre=(), unidades=(), status="nao_iniciada", resultado=None):
    return {"codigo": codigo, "eixo": eixo, "fase": fase, "prerequisitos": list(pre), "requer_unidades": list(unidades),
            "unidades_relacionadas": [], "status": status, "portao": {"criterio": "x", "resultado": resultado},
            "arquivo": f"disciplinas/{codigo}.md"}


def montar(tmp_path, disc=None, corpo=None):
    """Repositório mínimo coerente: XA1 e XA2 no eixo A, XN0 no nivelamento, uma lista com verificação."""
    disc = disc or {
        "XA1": disciplina("XA1", unidades=["U1.1"]),
        "XA2": disciplina("XA2", pre=["XA1"]),
        "XN0": disciplina("XN0", eixo="Física", fase="nivelamento"),
    }
    cat = tmp_path / "catalogo"
    cat.mkdir()
    dados = {
        "eixos": {"schema_version": 1, "eixos": [
            {"codigo": "A", "nome": "Mat", "rotulos_nas_disciplinas": ["Matemática"], "disciplinas": ["XA1", "XA2"], "sem_arquivo": ["XA9", "M0"]},
            {"codigo": "B", "nome": "Fís", "rotulos_nas_disciplinas": ["Física"], "disciplinas": []}]},
        "unidades": {"schema_version": 1, "unidades": [
            {"codigo": "U1.1", "nome": "U", "semestre": 1, "nivel": "Base", "prerequisitos": []},
            {"codigo": "U1.2", "nome": "V", "semestre": 1, "nivel": "Base", "prerequisitos": ["U1.1", "XA1"]}]},
        "projetos": {"schema_version": 1, "projetos": [
            {"codigo": "PJ1", "nome": "P", "disciplinas": ["XA1", "XA9"], "complexidade": "Baixa", "competencia": "c", "momento": "m"}]},
        "escalas": {"schema_version": 1, "dominio": [], "dificuldade_exercicio": [
            {"nivel": 1, "nome": "Fácil", "o_que_treina": "Aplicar direto"},
            {"nivel": 2, "nome": "Difícil", "o_que_treina": "Combinar"}]},
        "aposentados": {"schema_version": 1, "aposentados": [{"codigo": "M0", "motivo": "nivelamento", "ver": "AVALIACOES.md"}]},
        "fora-do-plano": {"schema_version": 1, "fora_do_plano": [{"codigo": "XA9", "motivo": "coberta_pelo_curso", "detalhe": "curso"}]},
    }
    for nome, d in dados.items():
        (cat / f"{nome}.yml").write_text(yaml.safe_dump(d, allow_unicode=True), encoding="utf-8")
    (tmp_path / "disciplinas").mkdir()
    for c in disc:
        texto = (corpo or {}).get(c, f"Disciplina {c}. Consolida no PJ1.\n")
        (tmp_path / "disciplinas" / f"{c}.md").write_text(f"---\ncodigo: {c}\n---\n{texto}", encoding="utf-8")
    (tmp_path / "AVALIACOES.md").write_text(AVALIACOES, encoding="utf-8")
    ex = tmp_path / "exercicios/XA1"
    (ex / "verificacao").mkdir(parents=True)
    (ex / "1-l.md").write_text("1. x\n", encoding="utf-8")
    (ex / "verificacao/1-l.yml").write_text("lista: exercicios/XA1/1-l.md\ngabarito: exercicios/XA1/gabaritos/1-l.md\n", encoding="utf-8")
    return disc


def editar(tmp_path, nome, funcao):
    arq = tmp_path / "catalogo" / f"{nome}.yml"
    d = yaml.safe_load(arq.read_text(encoding="utf-8"))
    funcao(d)
    arq.write_text(yaml.safe_dump(d, allow_unicode=True), encoding="utf-8")


def um(msgs, prefixo):
    achados = [m for m in msgs if m.startswith(prefixo)]
    assert len(achados) == 1, msgs
    return achados[0]


def test_repositorio_minimo_sem_erro(tmp_path):
    disc = montar(tmp_path)
    assert validar_catalogo(disc, tmp_path) == []


def test_codigo_repetido_entre_arquivos(tmp_path):
    disc = montar(tmp_path)
    (tmp_path / "disciplinas/XA1-copia.md").write_text('---\ncodigo: "XA1"\n---\n', encoding="utf-8")
    m = um(validar_catalogo(disc, tmp_path), "codigo-repetido:")
    assert "XA1" in m and "disciplinas/XA1-copia.md" in m and "disciplinas/XA1.md" in m


def test_unidade_desconhecida(tmp_path):
    disc = montar(tmp_path)
    disc["XA2"]["unidades_relacionadas"] = ["U7.7"]
    disc["XA1"]["requer_unidades"] = ["U8.8"]
    msgs = validar_catalogo(disc, tmp_path)
    assert any("XA2" in m and "U7.7" in m for m in msgs) and any("XA1" in m and "U8.8" in m for m in msgs)


def test_prerequisito_de_unidade_desconhecido(tmp_path):
    disc = montar(tmp_path)
    editar(tmp_path, "unidades", lambda d: d["unidades"][1]["prerequisitos"].extend(["U5.5", "ZZ1"]))
    msgs = validar_catalogo(disc, tmp_path)
    assert any("U1.2" in m and "U5.5" in m for m in msgs) and any("U1.2" in m and "ZZ1" in m for m in msgs)


def test_projeto_citado_inexistente(tmp_path):
    disc = montar(tmp_path)
    (tmp_path / "disciplinas/XA2.md").write_text("---\ncodigo: XA2\n---\nVer PJ1 e PJ42.\n", encoding="utf-8")
    m = um(validar_catalogo(disc, tmp_path), "projeto-desconhecido:")
    assert "PJ42" in m and "disciplinas/XA2.md" in m


def test_eixo_da_disciplina_diverge_do_catalogo(tmp_path):
    disc = montar(tmp_path)
    disc["XA2"]["eixo"] = "Física"
    m = um(validar_catalogo(disc, tmp_path), "eixo-divergente:")
    assert "XA2" in m and "Física" in m


def test_disciplina_fora_de_eixo(tmp_path):
    disc = montar(tmp_path)
    disc["XC1"] = disciplina("XC1")
    (tmp_path / "disciplinas/XC1.md").write_text("---\ncodigo: XC1\n---\n", encoding="utf-8")
    assert "XC1" in um(validar_catalogo(disc, tmp_path), "eixo-ausente:")


def test_rotulo_do_nivelamento_precisa_existir(tmp_path):
    disc = montar(tmp_path)
    disc["XN0"]["eixo"] = "Astrologia"
    assert "Astrologia" in um(validar_catalogo(disc, tmp_path), "eixo-desconhecido:")


def test_disciplina_do_eixo_sem_arquivo(tmp_path):
    disc = montar(tmp_path)
    editar(tmp_path, "eixos", lambda d: d["eixos"][0]["disciplinas"].append("XA3"))
    assert "XA3" in um(validar_catalogo(disc, tmp_path), "disciplina-sem-arquivo:")


def test_sem_arquivo_que_tem_arquivo(tmp_path):
    disc = montar(tmp_path)
    editar(tmp_path, "eixos", lambda d: d["eixos"][0]["sem_arquivo"].append("XA2"))
    assert "XA2" in um(validar_catalogo(disc, tmp_path), "sem-arquivo-com-arquivo:")


def test_disciplina_de_projeto_inexistente(tmp_path):
    disc = montar(tmp_path)
    editar(tmp_path, "projetos", lambda d: d["projetos"][0]["disciplinas"].append("XZ5"))
    m = um(validar_catalogo(disc, tmp_path), "projeto-disciplina-desconhecida:")
    assert "PJ1" in m and "XZ5" in m


def test_codigo_aposentado_com_arquivo_e_como_prerequisito(tmp_path):
    disc = montar(tmp_path)
    disc["XA2"]["prerequisitos"].append("M0")
    disc["M0"] = disciplina("M0")
    msgs = validar_catalogo(disc, tmp_path)
    assert "M0" in um(msgs, "aposentado-com-arquivo:")
    assert "XA2" in um(msgs, "aposentado-como-prerequisito:")


def test_aposentado_com_ver_quebrado(tmp_path):
    disc = montar(tmp_path)
    editar(tmp_path, "aposentados", lambda d: d["aposentados"][0].update(ver="NADA.md"))
    assert "NADA.md" in um(validar_catalogo(disc, tmp_path), "aposentado-sem-referencia:")


def test_lista_sem_verificacao_e_excecao(tmp_path):
    disc = montar(tmp_path)
    (tmp_path / "exercicios/XA1/2-antiga.md").write_text("1. x\n", encoding="utf-8")
    assert "exercicios/XA1/2-antiga.md" in um(validar_catalogo(disc, tmp_path), "lista-sem-verificacao:")
    (tmp_path / "exercicios/sem-verificacao.yml").write_text(
        "schema_version: 1\nlistas:\n  - {lista: exercicios/XA1/2-antiga.md, motivo: antiga}\n", encoding="utf-8")
    assert validar_catalogo(disc, tmp_path) == []


def test_excecao_desnecessaria_ou_sem_lista(tmp_path):
    disc = montar(tmp_path)
    (tmp_path / "exercicios/sem-verificacao.yml").write_text(
        "schema_version: 1\nlistas:\n  - {lista: exercicios/XA1/1-l.md, motivo: a}\n"
        "  - {lista: exercicios/XA1/9-sumiu.md, motivo: b}\n", encoding="utf-8")
    msgs = validar_catalogo(disc, tmp_path)
    assert "1-l.md" in um(msgs, "excecao-desnecessaria:")
    assert "9-sumiu.md" in um(msgs, "excecao-sem-lista:")


def test_tabela_de_avaliacoes_diverge_da_escala(tmp_path):
    disc = montar(tmp_path)
    (tmp_path / "AVALIACOES.md").write_text(AVALIACOES.replace("| Difícil |", "| Médio |"), encoding="utf-8")
    m = um(validar_catalogo(disc, tmp_path), "escala-divergente:")
    assert "nível 2" in m
    (tmp_path / "AVALIACOES.md").write_text(AVALIACOES.replace("| 2 | Difícil | Combinar |\n", ""), encoding="utf-8")
    assert "escala-divergente:" in " ".join(validar_catalogo(disc, tmp_path))


def test_arquivo_de_catalogo_ausente_nao_gera_ruido(tmp_path):
    disc = montar(tmp_path)
    (tmp_path / "catalogo/eixos.yml").unlink()
    (tmp_path / "catalogo/projetos.yml").unlink()
    assert validar_catalogo(disc, tmp_path) == []  # a ausência é erro de scripts/esquema.py


@pytest.mark.parametrize("status,resultado,avisa", [
    ("concluida", "75%", True),
    ("dispensada", 70, True),
    ("em_revisao", "79,5 %", True),
    ("concluida", "80%", False),
    ("concluida", "17 de 20", False),
    ("em_andamento", "50%", False),
    ("concluida", None, False),
])
def test_aviso_portao_abaixo_de_80(status, resultado, avisa):
    disc = {"XN0": disciplina("XN0", fase="nivelamento", status=status, resultado=resultado),
            "XA1": disciplina("XA1", status="concluida", resultado="50%")}
    avisos = avisos_catalogo(disc)
    assert bool(avisos) == avisa
    if avisa:
        assert avisos[0].startswith("portao-abaixo-de-80: XN0:")


def test_repositorio_real_sem_erro():
    disc = {d["codigo"]: {**d, "arquivo": a} for a, d, e in carregar_cabecalhos(RAIZ)}
    inicio = time.perf_counter()
    assert validar_catalogo(disc, RAIZ) == []
    assert avisos_catalogo(disc) == []
    assert time.perf_counter() - inicio < 0.5


def test_validacoes_juntas_em_menos_de_1s():
    from esquema import validar_esquemas
    inicio = time.perf_counter()
    disc = {d["codigo"]: {**d, "arquivo": a} for a, d, e in carregar_cabecalhos(RAIZ)}
    validar_esquemas(RAIZ)
    validar_catalogo(disc, RAIZ)
    assert time.perf_counter() - inicio < 0.5


# --- correções da revisão dos Marcos 1 a 3 ---

def _repo_copia(tmp_path):
    import shutil
    raiz = pathlib.Path(__file__).resolve().parents[1]
    dest = tmp_path / "r"
    shutil.copytree(raiz, dest, ignore=shutil.ignore_patterns(".git", "__pycache__", "benchmark", "tests"))
    return dest


def _disc_de(raiz):
    import progresso
    antigo = progresso.DIR_DISC
    progresso.DIR_DISC = raiz / "disciplinas"
    try:
        return progresso.carregar_disciplinas()
    finally:
        progresso.DIR_DISC = antigo


def test_verificacao_com_lista_de_outro_arquivo_e_erro(tmp_path):
    raiz = _repo_copia(tmp_path)
    yml = raiz / "exercicios/NM0/verificacao/5-ancoras.yml"
    yml.write_text(yml.read_text(encoding="utf-8").replace("lista: exercicios/NM0/5-ancoras.md",
                                                           "lista: exercicios/NM0/1-adicao.md"), encoding="utf-8")
    erros = catalogo.validar_catalogo(_disc_de(raiz), raiz)
    assert any(e.startswith("verificacao-fora-do-lugar") and "lista" in e for e in erros)


def test_ver_fora_da_raiz_ou_inexistente_e_erro(tmp_path):
    raiz = _repo_copia(tmp_path)
    ap = raiz / "catalogo/aposentados.yml"
    ap.write_text(ap.read_text(encoding="utf-8").replace("ver: NIVELAMENTO.md", "ver: ../../etc/passwd"), encoding="utf-8")
    sv = raiz / "exercicios/sem-verificacao.yml"
    t = sv.read_text(encoding="utf-8")
    sv.write_text(t.replace("ver: skills/estudo-guiado/references/correcao.md", "ver: nao/existe.md", 1), encoding="utf-8")
    erros = catalogo.validar_catalogo(_disc_de(raiz), raiz)
    assert any(e.startswith("aposentado-sem-referencia") for e in erros)
    assert any(e.startswith("excecao-sem-referencia") for e in erros)


def test_projeto_nao_pode_citar_codigo_aposentado(tmp_path):
    raiz = _repo_copia(tmp_path)
    pj = raiz / "catalogo/projetos.yml"
    pj.write_text(pj.read_text(encoding="utf-8").replace("  disciplinas:\n  - P1\n", "  disciplinas:\n  - M0\n  - P1\n", 1),
                  encoding="utf-8")
    erros = catalogo.validar_catalogo(_disc_de(raiz), raiz)
    assert any(e.startswith("aposentado-em-projeto") for e in erros)


def test_porcentagem_usa_o_menor_valor_e_aceita_fracao():
    assert catalogo.porcentagem("níveis 1-2: 95%; prova de saída: 70%") == 70.0
    assert catalogo.porcentagem("14/20") == 70.0


# --- disciplinas do Mapa fora do plano (DT-03) ---

def test_sem_arquivo_precisa_de_motivo_em_fora_do_plano(tmp_path):
    disc = montar(tmp_path)
    editar(tmp_path, "fora-do-plano", lambda d: d.update(fora_do_plano=[]))
    assert um(validar_catalogo(disc, tmp_path), "sem-arquivo-sem-motivo")


def test_fora_do_plano_nao_pode_ter_arquivo_nem_faltar_em_sem_arquivo(tmp_path):
    disc = montar(tmp_path)
    editar(tmp_path, "fora-do-plano", lambda d: d["fora_do_plano"].extend([
        {"codigo": "XA1", "motivo": "fora_do_plano", "detalhe": "x"},
        {"codigo": "XZ7", "motivo": "fora_do_plano", "detalhe": "x"}]))
    msgs = validar_catalogo(disc, tmp_path)
    assert any(m.startswith("fora-do-plano-com-arquivo") and "XA1" in m for m in msgs)
    assert any(m.startswith("fora-do-plano-fora-dos-eixos") and "XZ7" in m for m in msgs)
