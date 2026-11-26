"""Configuração do plano: plano.yml sobre os valores padrão."""
import yaml

PADROES = {
    "semestre_atual": 0,
    "limite_abertas": 2,
    "autonomia_n": 5,
    "autonomia_dias_distintos": 3,
    "autonomia_por_laboratorio": [],
    "fixacao_proporcao": 0.2,
    "fixacao_janela": 3,
    "mapa_janela": 10,
    "mapa_min_forte": 5,
    "mapa_pct_forte": 85,
    "mapa_pct_sem_ajuda_forte": 80,
    "mapa_pct_fraca": 60,
    "fixacao_vencida_dias": 30,
}


def carregar_config(caminho):
    dados = yaml.safe_load(caminho.read_text(encoding="utf-8")) if caminho.exists() else None
    return {**PADROES, **(dados or {})}
