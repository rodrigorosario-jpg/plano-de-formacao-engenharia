"""Limites de executar_codigo: ambiente vazio, stdin fechado, tempo, memória, arquivo e saída."""
import signal
import subprocess
import sys

import pytest

import verificar
from verificar import executar_codigo

try:
    import resource
except ImportError:
    resource = None

com_limites = pytest.mark.skipif(resource is None, reason="sem o módulo resource")


def test_codigo_valido_continua_funcionando():
    assert executar_codigo("x = 0\nfor i in range(4):\n    x += i\nprint(x)") == "6"


def test_saida_com_acento_volta_em_utf8():
    assert executar_codigo("print('ação')") == "ação"


def test_variavel_do_processo_pai_nao_aparece(monkeypatch):
    monkeypatch.setenv("SEGREDO_DO_PAI", "nao-deve-vazar")
    saida = executar_codigo("import os\nprint(os.environ.get('SEGREDO_DO_PAI', 'ausente'))\nprint(sorted(os.environ))")
    assert saida.splitlines()[0] == "ausente"
    assert "HOME" not in saida and "PATH" not in saida


def test_stdin_vem_vazio():
    assert executar_codigo("import sys\nprint(repr(sys.stdin.read()))") == "''"


def test_laco_infinito_termina_por_tempo(monkeypatch):
    monkeypatch.setattr(verificar, "TEMPO_CODIGO", 0.3)
    with pytest.raises(ValueError, match="tempo"):
        executar_codigo("while True: pass")


@pytest.mark.skipif(resource is None or not sys.platform.startswith("linux"),
                    reason="RLIMIT_AS só é respeitado no Linux")
def test_estouro_de_memoria_termina_com_erro():
    with pytest.raises(ValueError, match="MemoryError"):
        executar_codigo("x = bytearray(512 * 1024 * 1024)\nprint(len(x))")


@com_limites
def test_arquivo_grande_e_barrado():
    with pytest.raises(ValueError, match="File too large"):
        executar_codigo("open('f', 'wb').write(b'x' * (2 * 1024 * 1024))")


@com_limites
def test_arquivos_abertos_sao_limitados():
    with pytest.raises(ValueError, match="Too many open files"):
        executar_codigo("fs = [open('f%d' % i, 'w') for i in range(1000)]")


def test_saida_grande_e_barrada():
    with pytest.raises(ValueError, match="saída"):
        executar_codigo("print('x' * 200_000)")


@pytest.mark.skipif(verificar.resource is None or sys.platform == "darwin", reason="limites de CPU só em Linux")
def test_limite_de_cpu_chega_como_sigxcpu_antes_do_sigkill():
    # Com soft == hard o kernel pode mandar SIGKILL direto, e o erro saía como "sinal 9" (falha no CI).
    proc = subprocess.run([sys.executable, "-I", "-c", "while True: pass"], preexec_fn=lambda: verificar._aplicar_limites(1),
                          capture_output=True, timeout=10)
    assert proc.returncode == -signal.SIGXCPU


def test_gabarito_fora_do_repositorio_nao_e_lido(tmp_path):
    fora = tmp_path / "fora.md"
    fora.write_text("| 1 | SEGREDO |\n", encoding="utf-8")
    raiz = tmp_path / "repo"
    (raiz / "exercicios/XA1/verificacao").mkdir(parents=True)
    yml = raiz / "exercicios/XA1/verificacao/L.yml"
    yml.write_text(f"gabarito: {fora}\nitens:\n  - {{item: 1, calculo: '1'}}\n", encoding="utf-8")
    msgs = verificar.verificar(yml, raiz)
    assert msgs and "fora do repositório" in msgs[0] and "SEGREDO" not in " ".join(msgs)


@pytest.mark.skipif(verificar.resource is None, reason="grupo de processos só em POSIX")
def test_processo_neto_nao_sobrevive_ao_fim_do_codigo(tmp_path):
    marca = tmp_path / "neto.txt"
    neto = f"import time; time.sleep(1); open({str(marca)!r}, 'w').write('vivo')"
    codigo = f"import subprocess, sys\nsubprocess.Popen([sys.executable, '-c', {neto!r}])\nprint(42)"
    assert executar_codigo(codigo) == "42"
    import time
    time.sleep(1.5)
    assert not marca.exists()
