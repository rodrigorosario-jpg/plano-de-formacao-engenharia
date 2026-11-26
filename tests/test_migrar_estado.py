import ast
import datetime as dt
import pathlib
import subprocess
import sys

import pytest
import yaml

import estado
import migrar_estado
from esquema import RAIZ, _erros_esquema

TOPO = """---
codigo: {cod}
ordem: {ordem}
nome: "Teste {cod}"
eixo: "Matemática"
fase: nivelamento
bloco: "A · Teste"
semestre_inicio: 0
semestre_fim: 0
horas_previstas: 10
nivel_alvo: 3
prerequisitos: []
competencias:
  - {{id: {cod}.c01, nome: "Somar"}}
"""
NIVELAMENTO = """
# Atualize daqui para baixo à medida que estudar.
# status: nao_iniciada | em_andamento | no_portao | concluida | dispensada | em_revisao
status: {status}
inicio: {inicio}
diagnostico: {diag}   # % de acertos nas questões deste módulo no diagnóstico do bloco
portao:
  criterio: "80% na prova de saída (15 a 20 questões, sem consulta e sem calculadora)"
  data: {data}
  resultado: {resultado}
  evidencia: {evidencia}
nivel_atingido: {nivel}
---

# {cod} · Teste

Corpo com status: e portao: no texto, que não pode mudar.
inicio: null
"""
SEM_DIAGNOSTICO = """
# Atualize daqui para baixo à medida que estudar.
# status: nao_iniciada | em_andamento | no_portao | concluida | em_revisao
status: nao_iniciada
inicio: null
portao:
  criterio: "Prova"
  data: null
  resultado: null
  evidencia: null
nivel_atingido: null
---

# {cod} · Outra
"""


def modulo(cod, ordem, status="nao_iniciada", inicio="null", diag="null", data="null", resultado="null",
           evidencia="null", nivel="null"):
    return TOPO.format(cod=cod, ordem=ordem) + NIVELAMENTO.format(
        cod=cod, status=status, inicio=inicio, diag=diag, data=data, resultado=resultado, evidencia=evidencia, nivel=nivel)


def montar(tmp_path):
    pasta = tmp_path / "disciplinas"
    pasta.mkdir(parents=True)
    arquivos = {
        "XA0": modulo("XA0", 1, status="em_andamento", inicio="2026-01-05"),
        "XA1": modulo("XA1", 2, diag="0"),
        "XA2": modulo("XA2", 4, status="concluida", inicio="2026-10-01", diag="72.5", data="2026-11-01",
                      resultado='"85%"', evidencia='"exercicios/XA2/saida.md"', nivel="3"),
        "XA3": modulo("XA3", 3),
        "XB1": TOPO.format(cod="XB1", ordem=5) + SEM_DIAGNOSTICO.format(cod="XB1"),
    }
    for cod, texto in arquivos.items():
        (pasta / f"{cod}-teste.md").write_text(texto, encoding="utf-8")
    return tmp_path, arquivos


def ler(raiz):
    return {p.name: p.read_bytes() for p in sorted((raiz / "disciplinas").glob("*.md"))}


def linhas_removidas(antes, depois):
    a, d = antes.splitlines(keepends=True), depois.splitlines(keepends=True)
    restantes = list(d)
    sobra = []
    for linha in a:
        if restantes and restantes[0] == linha:
            restantes.pop(0)
        else:
            sobra.append(linha)
    assert not restantes, "o script acrescentou ou alterou linhas"
    return sobra


def test_migra_copia(tmp_path):
    raiz, arquivos = montar(tmp_path)
    migrar_estado.migrar(raiz)
    est = yaml.safe_load((raiz / "registro/estado.yml").read_text(encoding="utf-8"))
    assert est["schema_version"] == 1
    assert est["modulos"] == {
        "XA0": {"status": "em_andamento", "inicio": dt.date(2026, 1, 5)},
        "XA1": {"diagnostico": 0},
        "XA2": {"status": "concluida", "inicio": dt.date(2026, 10, 1), "diagnostico": 72.5, "nivel_atingido": 3,
                "portao": {"data": dt.date(2026, 11, 1), "resultado": "85%", "evidencia": "exercicios/XA2/saida.md"}},
    }
    assert list(est["modulos"]) == ["XA0", "XA1", "XA2"]
    for cod, antes in arquivos.items():
        depois = (raiz / "disciplinas" / f"{cod}-teste.md").read_text(encoding="utf-8")
        removidas = linhas_removidas(antes, depois)
        assert len(removidas) == (9 if cod != "XB1" else 8)
        assert all(l.split(":")[0].strip() in {"status", "inicio", "diagnostico", "nivel_atingido", "data", "resultado",
                                               "evidencia", "# Atualize daqui para baixo à medida que estudar.", "# status"}
                   for l in removidas)
        assert "portao:\n  criterio: " in depois and "Corpo com status" in depois or cod == "XB1"
        cab = yaml.safe_load(depois.split("---\n")[1])
        assert estado.andamento_no_cabecalho(cab) == [] and set(cab["portao"]) == {"criterio"}


def test_duas_vezes_da_o_mesmo_resultado(tmp_path):
    raiz, _ = montar(tmp_path)
    migrar_estado.migrar(raiz)
    primeiro = ler(raiz), (raiz / "registro/estado.yml").read_bytes()
    rel = migrar_estado.migrar(raiz)
    assert (ler(raiz), (raiz / "registro/estado.yml").read_bytes()) == primeiro
    assert rel["arquivos"] == [] and rel["estado_gravado"] is False


def test_datas_preservadas_e_estado_valido_no_schema(tmp_path):
    raiz, _ = montar(tmp_path)
    migrar_estado.migrar(raiz)
    est = estado.carregar_estado(raiz)
    assert isinstance(est["modulos"]["XA0"]["inicio"], dt.date)
    assert isinstance(est["modulos"]["XA2"]["portao"]["data"], dt.date)
    assert _erros_esquema("estado", est, "registro/estado.yml") == []


def test_nao_gravar_estado(tmp_path):
    raiz, _ = montar(tmp_path)
    rel = migrar_estado.migrar(raiz, gravar_estado=False)
    assert not (raiz / "registro/estado.yml").exists()
    assert len(rel["arquivos"]) == 5 and set(rel["valores"]) == {"XA0", "XA1", "XA2"}
    assert all(estado.andamento_no_cabecalho(yaml.safe_load(p.read_text(encoding="utf-8").split("---\n")[1])) == []
               for p in (raiz / "disciplinas").glob("*.md"))


def test_estado_existente_e_completado(tmp_path):
    raiz, _ = montar(tmp_path)
    (raiz / "registro").mkdir()
    (raiz / "registro/estado.yml").write_text("schema_version: 1\nmodulos:\n  XB1: {nivel_atingido: 2}\n  XA0: {status: em_andamento}\n",
                                              encoding="utf-8")
    migrar_estado.migrar(raiz)
    mods = estado.carregar_estado(raiz)["modulos"]
    assert list(mods) == ["XA0", "XA1", "XA2", "XB1"]
    assert mods["XA0"] == {"status": "em_andamento", "inicio": dt.date(2026, 1, 5)} and mods["XB1"] == {"nivel_atingido": 2}


def test_conflito_com_estado_existente_nao_muda_nada(tmp_path):
    raiz, _ = montar(tmp_path)
    (raiz / "registro").mkdir()
    texto = "schema_version: 1\nmodulos:\n  XA0: {status: concluida}\n"
    (raiz / "registro/estado.yml").write_text(texto, encoding="utf-8")
    antes = ler(raiz)
    with pytest.raises(migrar_estado.ErroMigracao, match="XA0.*status"):
        migrar_estado.migrar(raiz)
    assert ler(raiz) == antes and (raiz / "registro/estado.yml").read_text(encoding="utf-8") == texto


def test_formato_inesperado_nao_muda_nada(tmp_path):
    raiz, _ = montar(tmp_path)
    arq = raiz / "disciplinas/XA3-teste.md"
    arq.write_text(arq.read_text(encoding="utf-8").replace("inicio: null\ndiagnostico", "inicio:\n  2026-11-01\ndiagnostico", 1),
                   encoding="utf-8")
    antes = ler(raiz)
    with pytest.raises(migrar_estado.ErroMigracao, match="XA3"):
        migrar_estado.migrar(raiz)
    assert ler(raiz) == antes and not (raiz / "registro/estado.yml").exists()


def test_cli_fora_do_repositorio(tmp_path):
    raiz, _ = montar(tmp_path / "copia")
    script = pathlib.Path(migrar_estado.__file__)
    r = subprocess.run([sys.executable, "-I", str(script), "--raiz", str(raiz)], cwd=tmp_path,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert (raiz / "registro/estado.yml").exists() and "5 arquivos" in r.stdout


def test_script_autonomo():
    arvore = ast.parse(pathlib.Path(migrar_estado.__file__).read_text(encoding="utf-8"))
    modulos = {a.name.split(".")[0] for n in ast.walk(arvore) if isinstance(n, ast.Import) for a in n.names}
    modulos |= {n.module.split(".")[0] for n in ast.walk(arvore) if isinstance(n, ast.ImportFrom)}
    assert modulos - set(sys.stdlib_module_names) == {"yaml"}


def test_mesmas_regras_que_estado_py():
    assert migrar_estado.CAMPOS == estado.CAMPOS and migrar_estado.CAMPOS_PORTAO == estado.CAMPOS_PORTAO
    assert migrar_estado.PADRAO == estado.PADRAO and migrar_estado.CABECALHO == estado.CABECALHO
    exemplo = {"NM0": {"status": "concluida", "inicio": dt.date(2026, 1, 5), "diagnostico": 0,
                       "portao": {"data": dt.date(2026, 11, 30), "resultado": "85%", "evidencia": 'a "b"'}}}
    assert migrar_estado.formatar_estado(exemplo) == estado.formatar_estado(exemplo)
    assert migrar_estado.formatar_estado({}) == estado.formatar_estado({})


def test_repositorio_sem_andamento_nos_cabecalhos():
    assert migrar_estado.migrar(RAIZ, gravar_estado=False, simular=True)["arquivos"] == []
