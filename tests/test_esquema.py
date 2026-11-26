import datetime as dt
import json
import pathlib
import shutil
import time

import pytest

import esquema
from esquema import ESQUEMAS, RAIZ, carregar_esquema, para_json, validar_esquemas

CATALOGO = ["eixos", "unidades", "projetos", "escalas", "aposentados"]

CABECALHO = """---
codigo: XA1
ordem: 1
nome: "Teste"
eixo: "Matemática"
fase: nivelamento
bloco: "A · Teste"
semestre_inicio: 0
semestre_fim: 0
horas_previstas: 10
nivel_alvo: 3
prerequisitos: []
requer_unidades: []
unidades_relacionadas: []
competencias:
  - {id: XA1.c01, nome: "Somar"}
portao:
  criterio: "80% na prova"
---

# XA1 · Teste
"""

GRADUACAO = """---
codigo: XB1
ordem: 2
nome: "Outra"
eixo: "Física"
fase: graduacao
semestre_inicio: 1
semestre_fim: 2
horas_previstas: 100
nivel_alvo: 4
prerequisitos: [XA1]
portao:
  criterio: "Prova"
---
"""


def repo(tmp_path, cabecalhos=(CABECALHO,)):
    """Repositório mínimo: catálogo real copiado e cabeçalhos de disciplina dados."""
    (tmp_path / "catalogo").mkdir()
    for nome in CATALOGO:
        shutil.copy(RAIZ / "catalogo" / f"{nome}.yml", tmp_path / "catalogo" / f"{nome}.yml")
    (tmp_path / "disciplinas").mkdir()
    for i, texto in enumerate(cabecalhos):
        (tmp_path / "disciplinas" / f"X{i}.md").write_text(texto, encoding="utf-8")
    return tmp_path


def trocar(texto, antigo, novo):
    assert antigo in texto
    return texto.replace(antigo, novo)


VERSAO = {"disciplina": "v2"}


def test_esquemas_sao_validos_e_versionados():
    for nome in ESQUEMAS:
        esq = carregar_esquema(nome)
        assert esq["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert esq["$id"] == f"plano-de-estudos/schemas/{nome}/{VERSAO.get(nome, 'v1')}"


def test_v1_do_cabecalho_fica_como_historico():
    from jsonschema import Draft202012Validator
    v1 = json.loads((RAIZ / "schemas/historico/disciplina.v1.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(v1)
    assert v1["$id"] == "plano-de-estudos/schemas/disciplina/v1" and "status" in v1["properties"]


def test_para_json_converte_datas_em_qualquer_nivel():
    d = {"a": dt.date(2026, 11, 23), "b": [{"c": dt.date(2026, 1, 2)}], "n": None}
    assert para_json(d) == {"a": "2026-11-23", "b": [{"c": "2026-01-02"}], "n": None}
    json.dumps(para_json(d))


def test_cabecalhos_validos_sem_erro(tmp_path):
    assert validar_esquemas(repo(tmp_path, [CABECALHO, GRADUACAO])) == []


def test_obrigatorio_ausente(tmp_path):
    raiz = repo(tmp_path, [trocar(CABECALHO, "horas_previstas: 10\n", "")])
    msgs = validar_esquemas(raiz)
    assert len(msgs) == 1 and msgs[0].startswith("disciplinas/X0.md: (raiz): ") and "horas_previstas" in msgs[0]


def test_criterio_do_portao_obrigatorio(tmp_path):
    raiz = repo(tmp_path, [trocar(GRADUACAO, 'portao:\n  criterio: "Prova"\n', 'portao: {}\n')])
    msgs = validar_esquemas(raiz)
    assert len(msgs) == 1 and msgs[0].startswith("disciplinas/X0.md: portao: ") and "criterio" in msgs[0]


def test_v2_proibe_andamento_no_cabecalho(tmp_path):
    texto = trocar(CABECALHO, 'portao:\n  criterio: "80% na prova"\n',
                   'status: nao_iniciada\ninicio: null\nportao:\n  criterio: "80% na prova"\n  data: null\n')
    msgs = validar_esquemas(repo(tmp_path, [texto]))
    assert {m.split(": ")[1] for m in msgs} == {"status", "inicio", "portao.data"}
    assert all("registro/estado.yml" in m for m in msgs)


def escrever_estado(raiz, texto):
    (raiz / "registro").mkdir(exist_ok=True)
    (raiz / "registro/estado.yml").write_text(texto, encoding="utf-8")


def test_estado_valido_e_ausente(tmp_path):
    raiz = repo(tmp_path)
    assert validar_esquemas(raiz) == []
    escrever_estado(raiz, "schema_version: 1\nmodulos:\n  XA1: {status: em_andamento, inicio: 2026-11-23}\n"
                          "  XB1: {diagnostico: 0, portao: {data: 2026-11-30, resultado: \"85%\", evidencia: null}}\n")
    assert validar_esquemas(raiz) == []
    escrever_estado(raiz, "schema_version: 1\nmodulos: {}\n")
    assert validar_esquemas(raiz) == []


def test_estado_invalido(tmp_path):
    raiz = repo(tmp_path)
    escrever_estado(raiz, "schema_version: 1\nmodulos:\n  XA1: {status: pausada, inicio: \"23/11/2026\", outro: 1}\n"
                          "  xa2: {nivel_atingido: 9, portao: {criterio: x}}\n")
    caminhos = {m.split(": ")[1] for m in validar_esquemas(raiz)}
    assert {"modulos.XA1.status", "modulos.XA1.inicio", "modulos.XA1", "modulos.xa2.nivel_atingido",
            "modulos.xa2.portao", "modulos"} <= caminhos
    assert all(m.startswith("registro/estado.yml: ") for m in validar_esquemas(raiz))


def test_campo_desconhecido(tmp_path):
    raiz = repo(tmp_path, [trocar(GRADUACAO, "prerequisitos: [XA1]", "prerequisito: [XA1]")])
    msgs = validar_esquemas(raiz)
    assert any("prerequisito'" in m for m in msgs) and any("prerequisitos" in m for m in msgs)


def test_nivelamento_exige_bloco_e_semestre_zero(tmp_path):
    raiz = repo(tmp_path, [trocar(trocar(CABECALHO, 'bloco: "A · Teste"\n', ""), "semestre_fim: 0", "semestre_fim: 1")])
    msgs = validar_esquemas(raiz)
    assert any("(raiz)" in m and "bloco" in m for m in msgs)
    assert any(": semestre_fim: " in m for m in msgs)


def test_fora_do_nivelamento_exige_semestres_e_proibe_bloco(tmp_path):
    texto = trocar(GRADUACAO, "semestre_inicio: 1\n", 'bloco: "A"\n')
    msgs = validar_esquemas(repo(tmp_path, [texto]))
    assert any("semestre_inicio" in m for m in msgs) and any(": bloco: " in m for m in msgs)


def test_competencia_com_codigo_de_outro_modulo(tmp_path):
    raiz = repo(tmp_path, [trocar(CABECALHO, "id: XA1.c01", "id: XA2.c01")])
    msgs = validar_esquemas(raiz)
    assert msgs == ["disciplinas/X0.md: competencias.0.id: 'XA2.c01' não está no formato XA1.cNN"]


def test_competencia_fora_do_formato(tmp_path):
    raiz = repo(tmp_path, [trocar(CABECALHO, "id: XA1.c01", "id: XA1.1")])
    msgs = validar_esquemas(raiz)
    assert msgs and all(m.startswith("disciplinas/X0.md: competencias.0.id: ") for m in msgs)


def test_cabecalho_ausente_e_yaml_invalido(tmp_path):
    raiz = repo(tmp_path, ["# sem cabeçalho\n", "---\ncodigo: [\n---\n"])
    msgs = validar_esquemas(raiz)
    assert any(m.startswith("disciplinas/X0.md: (raiz): ") and "cabeçalho" in m for m in msgs)
    assert any(m.startswith("disciplinas/X1.md: (raiz): ") and "YAML" in m for m in msgs)


def test_catalogo_sem_versao_e_arquivo_ausente(tmp_path):
    raiz = repo(tmp_path)
    arq = raiz / "catalogo/unidades.yml"
    arq.write_text(arq.read_text(encoding="utf-8").replace("schema_version: 1\n", ""), encoding="utf-8")
    (raiz / "catalogo/projetos.yml").unlink()
    msgs = validar_esquemas(raiz)
    assert any(m.startswith("catalogo/unidades.yml: (raiz): ") and "schema_version" in m for m in msgs)
    assert any(m.startswith("catalogo/projetos.yml: (raiz): ") and "ausente" in m for m in msgs)


def test_versao_errada_no_catalogo(tmp_path):
    raiz = repo(tmp_path)
    arq = raiz / "catalogo/eixos.yml"
    arq.write_text(arq.read_text(encoding="utf-8").replace("schema_version: 1", "schema_version: 2"), encoding="utf-8")
    msgs = validar_esquemas(raiz)
    assert len(msgs) == 1 and msgs[0].startswith("catalogo/eixos.yml: schema_version: ")


def escrever_verificacao(raiz, texto):
    arq = raiz / "exercicios/XA1/verificacao/1-l.yml"
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text(texto, encoding="utf-8")


VERIF = """lista: exercicios/XA1/1-l.md
gabarito: exercicios/XA1/gabaritos/1-l.md
itens:
  - {item: 1, competencia: XA1.c01, tipo_item: ancora, nivel: 4, calculo: "2 + 2"}
  - {item: 2, competencia: XA1.c01, tipo_item: critico, nivel: 3, revisao: releitura, nota: "Claude, 25/11/2026"}
  - {item: 3, competencia: XA1.c01, tipo_item: fluencia, nivel: 1, predicado: "n == 3", variavel: n, intervalo: [0, 10]}
"""


def test_verificacao_valida(tmp_path):
    raiz = repo(tmp_path)
    escrever_verificacao(raiz, VERIF)
    assert validar_esquemas(raiz) == []


def test_verificacao_invalida(tmp_path):
    raiz = repo(tmp_path)
    texto = (VERIF.replace("tipo_item: ancora", "tipo_item: outro")
             .replace("nivel: 3", "nivel: 7")
             .replace(', nota: "Claude, 25/11/2026"', "")
             .replace(", intervalo: [0, 10]", ""))
    escrever_verificacao(raiz, texto + "  - {item: 4, competencia: XA1.c01, tipo_item: fluencia, nivel: 1}\n")
    msgs = validar_esquemas(raiz)
    caminhos = {m.split(": ")[1] for m in msgs}
    assert {"itens.0.tipo_item", "itens.1.nivel", "itens.1", "itens.2", "itens.3"} <= caminhos
    assert any("calculo, predicado, codigo ou revisao" in m for m in msgs)


def test_plano_yml(tmp_path):
    raiz = repo(tmp_path)
    (raiz / "plano.yml").write_text("semestre_atual: 0\nlimite_abertas: 2\n", encoding="utf-8")
    assert validar_esquemas(raiz) == []
    (raiz / "plano.yml").write_text("semestre_atual: -1\nlimite: 2\n", encoding="utf-8")
    caminhos = {m.split(": ")[1] for m in validar_esquemas(raiz)}
    assert caminhos == {"semestre_atual", "(raiz)"}


def test_sem_verificacao(tmp_path):
    raiz = repo(tmp_path)
    arq = raiz / "exercicios/sem-verificacao.yml"
    arq.parent.mkdir()
    arq.write_text("schema_version: 1\nlistas:\n  - {lista: exercicios/XA1/1-l.md, motivo: antiga}\n", encoding="utf-8")
    assert validar_esquemas(raiz) == []
    arq.write_text("schema_version: 1\nlistas:\n  - {lista: XA1/1-l.md}\n", encoding="utf-8")
    caminhos = {m.split(": ")[1] for m in validar_esquemas(raiz)}
    assert caminhos == {"listas.0", "listas.0.lista"}


def test_valores_iguais_aos_do_codigo():
    from config import PADROES
    from progresso import STATUS_VALIDOS
    from respostas import TIPOS_ITEM
    import yaml

    import estado

    andamento = carregar_esquema("estado")["$defs"]["andamento"]["properties"]
    assert set(andamento["status"]["enum"]) == STATUS_VALIDOS == estado.STATUS_VALIDOS
    assert list(andamento) == estado.CAMPOS + ["portao"]
    assert list(andamento["portao"]["properties"]) == estado.CAMPOS_PORTAO
    disc = carregar_esquema("disciplina")["properties"]
    item = carregar_esquema("verificacao")["properties"]["itens"]["items"]["properties"]
    assert set(item["tipo_item"]["enum"]) == TIPOS_ITEM
    assert set(carregar_esquema("plano")["properties"]) == set(PADROES)
    escala = yaml.safe_load((RAIZ / "catalogo/escalas.yml").read_text(encoding="utf-8"))
    niveis = [e["nivel"] for e in escala["dominio"]]
    for esq in (disc["nivel_alvo"], andamento["nivel_atingido"]):
        esq = next((s for s in esq.get("anyOf", [esq]) if s.get("type") == "integer"), esq)
        assert (esq["minimum"], esq["maximum"]) == (min(niveis), max(niveis))


def test_repositorio_real_valida():
    inicio = time.perf_counter()
    assert validar_esquemas(RAIZ) == []
    assert time.perf_counter() - inicio < 0.5


def test_varios_campos_ausentes_aparecem_cada_um_pelo_nome(tmp_path):
    import shutil
    raiz = pathlib.Path(__file__).resolve().parents[1]
    dest = tmp_path / "r"
    shutil.copytree(raiz, dest, ignore=shutil.ignore_patterns(".git", "__pycache__", "benchmark", "tests"))
    arq = next((dest / "disciplinas").glob("NM13-*.md"))
    t = arq.read_text(encoding="utf-8")
    t = "\n".join(l for l in t.split("\n") if not l.startswith(("nome:", "eixo:", "horas_previstas:")))
    arq.write_text(t, encoding="utf-8")
    msgs = [m for m in esquema.validar_esquemas(dest) if "NM13" in m]
    for campo in ("nome", "eixo", "horas_previstas"):
        assert any(f"'{campo}'" in m for m in msgs), msgs


def test_estudante_valido_ausente_e_invalido(tmp_path):
    raiz = repo(tmp_path)
    arq = raiz / "registro" / "estudante.yml"
    arq.parent.mkdir(parents=True, exist_ok=True)
    assert validar_esquemas(raiz) == []
    arq.write_text("schema_version: 1\nbranch: estudo_ana\ngithub: ana-dev\n", encoding="utf-8")
    assert validar_esquemas(raiz) == []
    arq.write_text("schema_version: 1\nbranch: main\ngithub: 'ana dev'\nemail: x\n", encoding="utf-8")
    caminhos = {m.split(": ")[1] for m in validar_esquemas(raiz)}
    assert {"branch", "github", "(raiz)"} <= caminhos
    assert all(m.startswith("registro/estudante.yml: ") for m in validar_esquemas(raiz))
