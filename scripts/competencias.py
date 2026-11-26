"""Competências por módulo: IDs estáveis no formato <CÓDIGO>.cNN, declarados no frontmatter."""
import re


def competencias(disc):
    """Mapa id → {"codigo", "nome"} com as competências de todos os módulos."""
    return {
        c["id"]: {"codigo": cod, "nome": c.get("nome", "")}
        for cod, d in disc.items()
        for c in d.get("competencias") or []
    }


def validar_competencias(disc):
    erros, vistos = [], set()
    for cod, d in disc.items():
        padrao = re.compile(rf"^{re.escape(cod)}\.c\d{{2}}$")
        for c in d.get("competencias") or []:
            cid = str(c.get("id", ""))
            if not padrao.match(cid):
                erros.append(f"{cod}: competência '{cid}' fora do formato {cod}.cNN")
            if cid in vistos:
                erros.append(f"{cod}: competência {cid} repetida")
            vistos.add(cid)
            if not str(c.get("nome") or "").strip():
                erros.append(f"{cod}: competência {cid} sem nome")
    return erros
