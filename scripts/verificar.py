#!/usr/bin/env python3
"""Verificação independente de gabaritos.

Cada lista nova tem um arquivo exercicios/<código>/verificacao/<lista>.yml que diz, item a item,
como recalcular a resposta (calculo), como testar a unicidade (predicado) ou quem revisou um item
não calculável (revisao + nota). O gabarito é sempre lido do arquivo de gabarito da lista.

Uso:
    python scripts/verificar.py exercicios/NM0/verificacao/5-exemplo.yml
"""
import ast
import math
import operator
import os
import pathlib
import re
import signal
import subprocess
import sys
import tempfile
from fractions import Fraction

try:
    import resource  # só existe em POSIX; sem ele, executar_codigo fica sem limites de recurso
except ImportError:
    resource = None

import yaml

from respostas import TIPOS_ITEM

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
       ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow}
CMP = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt, ast.LtE: operator.le,
       ast.Gt: operator.gt, ast.GtE: operator.ge}


def _avaliar_no(no, nomes):
    if isinstance(no, ast.Expression):
        return _avaliar_no(no.body, nomes)
    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)) and not isinstance(no.value, bool):
        return Fraction(str(no.value))
    if isinstance(no, ast.Name) and no.id in nomes:
        return nomes[no.id]
    if isinstance(no, ast.BinOp) and type(no.op) in BIN:
        a, b = _avaliar_no(no.left, nomes), _avaliar_no(no.right, nomes)
        if isinstance(no.op, ast.Pow):
            if b.denominator != 1 or abs(b) > 1000 or abs(a) > 10**6:
                raise ValueError("potência fora do limite (expoente inteiro até 1000, base até 1.000.000)")
            return a ** int(b)
        return Fraction(BIN[type(no.op)](a, b))
    if isinstance(no, ast.UnaryOp) and isinstance(no.op, (ast.USub, ast.UAdd)):
        v = _avaliar_no(no.operand, nomes)
        return -v if isinstance(no.op, ast.USub) else v
    if isinstance(no, ast.UnaryOp) and isinstance(no.op, ast.Not) and "_logico" in nomes:
        return not _avaliar_no(no.operand, nomes)
    if (isinstance(no, ast.Call) and isinstance(no.func, ast.Name) and no.func.id == "F"
            and len(no.args) == 2 and not no.keywords):
        return Fraction(_avaliar_no(no.args[0], nomes)) / Fraction(_avaliar_no(no.args[1], nomes))
    if isinstance(no, ast.Compare) and "_logico" in nomes:
        esq = _avaliar_no(no.left, nomes)
        for op, dir_ in zip(no.ops, no.comparators):
            if type(op) not in CMP:
                raise ValueError("comparação não permitida")
            d = _avaliar_no(dir_, nomes)
            if not CMP[type(op)](esq, d):
                return False
            esq = d
        return True
    if isinstance(no, ast.BoolOp) and "_logico" in nomes:
        vals = (_avaliar_no(v, nomes) for v in no.values)
        return all(vals) if isinstance(no.op, ast.And) else any(vals)
    raise ValueError(f"expressão não permitida: {ast.dump(no)[:60]}")


def avaliar(expr):
    """Avalia aritmética exata (Fraction): números, + - * / // % **, parênteses e F(a, b)."""
    try:
        arvore = ast.parse(str(expr), mode="eval")
    except SyntaxError as e:
        raise ValueError(f"sintaxe inválida: {expr}") from e
    return _avaliar_no(arvore, {})


def normalizar(resposta):
    """Converte respostas numéricas no padrão brasileiro em Fraction; texto vira minúsculas."""
    t = str(resposta).strip().replace("\u2212", "-")
    t = re.sub(r"^R\$\s*", "", t)
    m = re.fullmatch(r"(-?[\d.,]+(?: \d+/\d+)?|-?\d+/\d+)\s*(%|[^\d\s][^\d]*)?", t)
    if m and m.group(2):
        t = m.group(1)
    m = re.fullmatch(r"(-?\d+) (\d+)/(\d+)", t)
    if m:
        inteiro, num, den = (int(g) for g in m.groups())
        return inteiro + (Fraction(num, den) if inteiro >= 0 else -Fraction(num, den))
    num = t.replace(" ", "")
    if "," in num:
        num = num.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", num):
        num = num.replace(".", "")
    try:
        return Fraction(num)
    except (ValueError, ZeroDivisionError):
        return t.lower()


MAX_INTERVALO = 1_000_000


def respostas_validas(predicado, variavel, inicio, fim):
    if fim - inicio > MAX_INTERVALO:
        raise ValueError(f"intervalo maior que {MAX_INTERVALO:,}".replace(",", "."))
    try:
        arvore = ast.parse(predicado, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"predicado com sintaxe inválida: {predicado}") from e
    return [n for n in range(inicio, fim + 1) if _avaliar_no(arvore, {variavel: Fraction(n), "_logico": True})]


TEMPO_CODIGO = 5  # segundos de relógio; o limite de CPU acompanha este valor
LIMITE_MEMORIA = 256 * 1024 * 1024  # bytes de memória virtual (RLIMIT_AS)
LIMITE_ARQUIVO = 1024 * 1024  # bytes por arquivo escrito, inclusive stdout e stderr (RLIMIT_FSIZE)
LIMITE_ARQUIVOS_ABERTOS = 64  # descritores abertos (RLIMIT_NOFILE)
LIMITE_SAIDA = 64 * 1024  # bytes de stdout aceitos como resposta


def _limite(nome, valor, folga=0):
    """Baixa o limite `nome` para `valor` (soft) e `valor + folga` (hard), sem passar do teto que o processo já tem."""
    _, teto = resource.getrlimit(nome)
    duro = valor + folga
    if teto != resource.RLIM_INFINITY:
        valor, duro = min(valor, teto), min(duro, teto)
    resource.setrlimit(nome, (valor, duro))


def _aplicar_limites(cpu):
    """Roda no filho, antes do exec (POSIX)."""
    # Folga de 1 s no hard: o kernel manda SIGXCPU (reconhecido como tempo esgotado) antes do SIGKILL.
    _limite(resource.RLIMIT_CPU, cpu, folga=1)
    _limite(resource.RLIMIT_AS, LIMITE_MEMORIA)
    _limite(resource.RLIMIT_FSIZE, LIMITE_ARQUIVO)
    _limite(resource.RLIMIT_NOFILE, LIMITE_ARQUIVOS_ABERTOS)
    _limite(resource.RLIMIT_CORE, 0)


def _ambiente_minimo():
    """Nenhuma variável herdada. No Windows o Python precisa de SYSTEMROOT para iniciar."""
    if os.name == "nt":
        return {"SYSTEMROOT": os.environ.get("SYSTEMROOT", r"C:\Windows")}
    return {}


def executar_codigo(codigo):
    """Roda um programa Python curto num subprocesso com limites e devolve a saída (stdout).

    O filho roda com `python -I -X utf8`, numa pasta temporária vazia, com ambiente vazio
    (o filho não herda variáveis do processo pai) e stdin em DEVNULL. Há limite de
    tempo de relógio (TEMPO_CODIGO) e de tamanho da saída (LIMITE_SAIDA). Em POSIX, com o
    módulo `resource`, também limita CPU, memória, tamanho de arquivo escrito e número de
    arquivos abertos, e o filho ganha um grupo de processos próprio, morto inteiro no tempo
    limite. Sem `resource` (Windows), valem só o tempo, o ambiente vazio e o corte da saída.
    Ao terminar, o grupo de processos inteiro é morto, para não deixar netos vivos. Não é sandbox:
    o filho roda com o mesmo usuário, então pode ler o ambiente do pai em /proc, ler e gravar
    arquivos do usuário, usar a rede e escapar do grupo com setsid.

    Isto NÃO é sandbox: o código ainda pode usar a rede, ler qualquer arquivo que o usuário
    do processo lê (inclusive o repositório) e criar processos. Só rode `codigo:` de fonte
    confiável.
    """
    tempo = TEMPO_CODIGO
    extras = {}
    if resource is not None:
        cpu = max(1, math.ceil(tempo))
        extras = {"preexec_fn": lambda: _aplicar_limites(cpu), "start_new_session": True}
    cmd = [sys.executable, "-I", "-X", "utf8", "-c", codigo]
    with tempfile.TemporaryDirectory() as pasta, tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        proc = subprocess.Popen(cmd, cwd=pasta, env=_ambiente_minimo(), stdin=subprocess.DEVNULL,
                                stdout=out, stderr=err, **extras)
        try:
            proc.wait(timeout=tempo)
        except subprocess.TimeoutExpired:
            if resource is not None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                proc.kill()
            proc.wait()
            raise ValueError(f"código passou do tempo limite de {tempo} s")
        finally:
            if resource is not None:
                try:  # mata também netos que o código deixou vivos no mesmo grupo
                    os.killpg(proc.pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
        out.seek(0)
        saida = out.read(LIMITE_SAIDA + 1)
        err.seek(0)
        erro = err.read(LIMITE_SAIDA).decode("utf-8", errors="replace")
    if resource is not None and proc.returncode == -signal.SIGXCPU:
        raise ValueError(f"código passou do tempo limite de {tempo} s (CPU)")
    if proc.returncode != 0:
        motivo = (erro.strip().splitlines() or [""])[-1]
        if not motivo and proc.returncode < 0:
            motivo = f"encerrado pelo sinal {-proc.returncode}"
        raise ValueError("código terminou com erro: " + motivo)
    if len(saida) > LIMITE_SAIDA:
        raise ValueError(f"saída do código passou de {LIMITE_SAIDA // 1024} KiB")
    return saida.decode("utf-8", errors="replace").strip()


def avisos_intercalacao(spec):
    """Aviso quando uma lista com 3+ competências tem 3 itens seguidos da mesma competência (fonte F2)."""
    itens = [it for it in spec.get("itens") or [] if it.get("competencia")]
    if len({it["competencia"] for it in itens}) < 3:
        return []
    for a, b, c in zip(itens, itens[1:], itens[2:]):
        if a["competencia"] == b["competencia"] == c["competencia"]:
            return [f"sem-intercalacao: {spec.get('lista')}: itens {a['item']} a {c['item']} são todos de {a['competencia']}"]
    return []


def ler_gabarito(caminho):
    """Linhas '| N | resposta |' (ou 'N. resposta'); a resposta vai até ' (', ' — ', ': ' ou '; '."""
    gab = {}
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| (\d+) \| (.*?) \|\s*$", linha) or re.match(r"^(\d+)\. (.*)$", linha)
        if m:
            gab[int(m.group(1))] = re.split(r" \(| — |: |; ", m.group(2).strip())[0].strip()
    return gab


def verificar(arquivo, raiz=RAIZ):
    try:
        spec = yaml.safe_load(pathlib.Path(arquivo).read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"gabarito-divergente: {arquivo}: YAML inválido ({e.__class__.__name__})"]
    if not isinstance(spec, dict) or not spec.get("gabarito"):
        return [f"gabarito-divergente: {arquivo}: falta a chave 'gabarito'"]
    nome = spec.get("lista", str(arquivo))
    msgs = []
    raiz_real = pathlib.Path(raiz).resolve()
    caminho_gab = (raiz_real / str(spec["gabarito"])).resolve()
    if pathlib.PurePath(str(spec["gabarito"])).is_absolute() or not caminho_gab.is_relative_to(raiz_real):
        return [f"gabarito-divergente: {nome}: gabarito {spec['gabarito']} fora do repositório"]
    if not caminho_gab.exists():
        return [f"gabarito-divergente: {nome}: gabarito {spec['gabarito']} não existe"]
    gab = ler_gabarito(caminho_gab)
    for it in spec.get("itens") or []:
        n = it.get("item")
        if n not in gab:
            msgs.append(f"gabarito-divergente: {nome} item {n}: sem resposta no gabarito")
            continue
        if "nivel" in it and it["nivel"] not in range(1, 6):
            msgs.append(f"gabarito-divergente: {nome} item {n}: nivel {it['nivel']} fora de 1 a 5")
        if "tipo_item" in it and it["tipo_item"] not in TIPOS_ITEM:
            msgs.append(f"gabarito-divergente: {nome} item {n}: tipo_item '{it['tipo_item']}' inválido")
        esperado = normalizar(gab[n])
        try:
            if "calculo" in it:
                calculado = avaliar(it["calculo"])
                if calculado != esperado:
                    msgs.append(f"gabarito-divergente: {nome} item {n}: gabarito {gab[n]}, verificação {calculado}")
            elif "predicado" in it:
                ini, fim = it["intervalo"]
                validas = respostas_validas(it["predicado"], it.get("variavel", "n"), ini, fim)
                if len(validas) != 1:
                    msgs.append(f"item-ambiguo: {nome} item {n}: {len(validas)} respostas válidas "
                                f"em [{ini}, {fim}]: {', '.join(map(str, validas[:10]))}")
                elif validas[0] != esperado:
                    msgs.append(f"gabarito-divergente: {nome} item {n}: gabarito {gab[n]}, verificação {validas[0]}")
            elif "codigo" in it:
                saida = executar_codigo(it["codigo"])
                if normalizar(saida) != esperado:
                    msgs.append(f"gabarito-divergente: {nome} item {n}: gabarito {gab[n]}, saída do programa {saida}")
            elif "revisao" in it:
                if not str(it.get("nota") or "").strip():
                    msgs.append(f"gabarito-divergente: {nome} item {n}: revisão sem nota de quem conferiu e quando")
            else:
                msgs.append(f"gabarito-divergente: {nome} item {n}: sem calculo, predicado, codigo ou revisao")
        except (ValueError, ZeroDivisionError, KeyError, TypeError) as e:
            msgs.append(f"gabarito-divergente: {nome} item {n}: verificação inválida ({e})")
    return msgs


def main():
    msgs = [m for arq in sys.argv[1:] for m in verificar(pathlib.Path(arq))]
    for m in msgs:
        print("ERRO:", m)
    if not msgs:
        print("Verificação sem divergências.")
    sys.exit(1 if msgs else 0)


if __name__ == "__main__":
    main()
