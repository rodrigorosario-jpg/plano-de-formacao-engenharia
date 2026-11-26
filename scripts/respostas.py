"""registro/respostas.csv: uma linha por item respondido (dado bruto do mapa de deficiências)."""
import csv
import datetime as dt

COLUNAS = ["data", "sessao", "lista", "item", "codigo", "competencia", "tipo_item", "nivel",
           "resultado", "classe_erro", "ajuda", "metodo", "observacao"]
TIPOS_ITEM = {"fluencia", "metodos", "simplificacao", "armadilha_simplificacao", "critico",
              "ancora", "fixacao", "diagnostico"}
RESULTADOS = {"certo", "parcial", "errado", "em_branco"}
CLASSES_ERRO = {"conceito", "procedimento", "atencao", "interpretacao", "simplificacao_indevida"}


def _inteiro(v):
    try:
        return int(str(v).strip())
    except ValueError:
        return v


def _data(v):
    try:
        return dt.date.fromisoformat(str(v).strip())
    except ValueError:
        return v


def carregar_respostas(caminho):
    """Lê o CSV (tolera BOM e \\r\\n). Converte data, item, nivel e ajuda quando válidos.
    Cabeçalho diferente de COLUNAS devolve [{"_cabecalho_invalido": True}]."""
    if not caminho.exists():
        return []
    try:
        with caminho.open(encoding="utf-8-sig", newline="") as f:
            leitor = csv.DictReader(f)
            if leitor.fieldnames != COLUNAS:
                return [{"_cabecalho_invalido": True, "_linha": 1}]
            linhas = []
            for l in leitor:
                n = leitor.line_num
                problema = None
                if None in l:
                    problema = "colunas a mais (campo com vírgula precisa estar entre aspas)"
                elif None in l.values():
                    problema = "colunas a menos"
                elif any("\n" in (v or "") for v in l.values()):
                    problema = "aspa não fechada: o campo engoliu a linha seguinte"
                l = {k: (v or "").strip() if isinstance(v, (str, type(None))) else v for k, v in l.items() if k is not None}
                l.update(_linha=n, _problema=problema, data=_data(l.get("data", "")), item=_inteiro(l.get("item", "")),
                         nivel=_inteiro(l.get("nivel", "")), ajuda=_inteiro(l.get("ajuda", "")))
                linhas.append(l)
            return linhas
    except UnicodeDecodeError:
        return [{"_codificacao_invalida": True, "_linha": 1}]


def validar_respostas(linhas, comps, raiz):
    if linhas and linhas[0].get("_codificacao_invalida"):
        return ["csv-invalido: arquivo não está em UTF-8; salve como CSV UTF-8"]
    if linhas and linhas[0].get("_cabecalho_invalido"):
        return ["csv-invalido: cabeçalho difere de " + ",".join(COLUNAS)]
    erros = []
    codigos = {c["codigo"] for c in comps.values()}
    for l in linhas:
        def erro(col, motivo):
            erros.append(f"csv-invalido: linha {l['_linha']}, coluna {col}: {motivo}")
        if l.get("_problema"):
            erros.append(f"csv-invalido: linha {l['_linha']}: {l['_problema']}")
            continue
        if not isinstance(l["item"], int) or l["item"] < 1:
            erro("item", f"'{l['item']}' deve ser inteiro ≥ 1")
        if not isinstance(l["data"], dt.date):
            erro("data", f"'{l['data']}' não é uma data AAAA-MM-DD")
        if l["codigo"] not in codigos:
            erro("codigo", f"código '{l['codigo']}' sem competências declaradas")
        comp = comps.get(l["competencia"])
        if comp is None:
            erro("competencia", f"competência '{l['competencia']}' não existe")
        elif comp["codigo"] != l["codigo"]:
            erro("competencia", f"competência '{l['competencia']}' não pertence a {l['codigo']}")
        if l["tipo_item"] not in TIPOS_ITEM:
            erro("tipo_item", f"'{l['tipo_item']}' inválido")
        if l["resultado"] not in RESULTADOS:
            erro("resultado", f"'{l['resultado']}' inválido")
        if l["classe_erro"] and l["classe_erro"] not in CLASSES_ERRO:
            erro("classe_erro", f"'{l['classe_erro']}' inválida")
        if l["classe_erro"] and l["resultado"] == "certo":
            erro("classe_erro", "deve ficar vazia quando o resultado é certo")
        if not isinstance(l["nivel"], int) or not 1 <= l["nivel"] <= 5:
            erro("nivel", f"'{l['nivel']}' fora de 1 a 5")
        if not isinstance(l["ajuda"], int) or l["ajuda"] < 0:
            erro("ajuda", f"'{l['ajuda']}' deve ser inteiro ≥ 0")
        if l["lista"] and not (raiz / l["lista"]).exists():
            erro("lista", f"'{l['lista']}' não existe")
    return erros


PESO = {"certo": 1.0, "parcial": 0.5}


def conferir_resumos(avs, linhas):
    """Compara as avaliações com coluna Lista contra as linhas do CSV da mesma data e lista.
    Resumos da mesma lista no mesmo dia (correção em partes) são somados."""
    msgs, grupos = [], {}
    for a in avs:
        if a.get("lista"):
            g = grupos.setdefault((a["data"], a["lista"]), [0.0, 0.0])
            g[0] += float(a["acertos"])
            g[1] += float(a["total"])
    for (data, lista), (ac_av, tot_av) in grupos.items():
        doc = [l for l in linhas if l.get("lista") == lista and l.get("data") == data]
        acertos = sum(PESO.get(l["resultado"], 0.0) for l in doc)
        if (acertos, float(len(doc))) != (ac_av, tot_av):
            msgs.append(f"resumo-divergente: {data} {lista}: avaliações {ac_av:g}/{tot_av:g}, "
                        f"respostas {acertos:g}/{len(doc)}")
    return msgs
