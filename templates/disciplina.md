---
codigo: <código novo, como S4; nunca reaproveite um código>
ordem: <posição na sequência geral, número inteiro>
nome: "<nome da disciplina>"
eixo: "<nome do eixo, como em catalogo/eixos.yml>"
fase: <graduacao ou pos_formatura>
semestre_inicio: <semestre de início>
semestre_fim: <semestre de fim>
horas_previstas: <horas previstas>
nivel_alvo: <1 a 7, escala de domínio de catalogo/escalas.yml>
prerequisitos: [<códigos das disciplinas ou módulos, separados por vírgula; vazio se não houver>]
requer_unidades: [<códigos de unidade de catalogo/unidades.yml, como U5.1; vazio se não houver>]
unidades_relacionadas: [<códigos de unidade; vazio se não houver>]

portao:
  criterio: "<critério do portão, sem ponto final>"
---

# <código> · <nome>

Semestre <semestre_inicio, ou semestre_inicio–semestre_fim se forem diferentes> · <horas_previstas> h previstas · nível-alvo <nivel_alvo>

## Tópicos, na ordem

<tópicos numa frase, separados por vírgula, na ordem de estudo>.

## Referência principal

<autor, título; outras referências separadas por ponto e vírgula>.

## Competência ao concluir

<o que se sabe fazer ao concluir, começando por um verbo>.

## Portão de saída

<o mesmo texto de portao.criterio>. A disciplina só é concluída quando o portão é cumprido sem consulta e no tempo regulamentar.

## Anotações
