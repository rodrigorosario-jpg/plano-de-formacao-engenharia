# ADR 0003 · Códigos atuais como identificadores

- **Status:** Aceita
- **Data:** 25/11/2026

## Contexto

Módulos e disciplinas já têm códigos curtos (`NM0`, `NL1`, `C8`), e as competências têm IDs derivados deles (`NM0.c01`). O catálogo usa códigos para eixos (`A` a `H`), unidades (`U1.2`), projetos (`PJ1`) e níveis da escala (1 a 7). `registro/respostas.csv`, os pré-requisitos, as verificações e a skill se referem a esses códigos. Um código já saiu de uso: `M0`, substituído pelo nivelamento.

## Decisão

1. Os códigos atuais são os identificadores das entidades do Core (decisão D3 da auditoria).
2. Um código nunca muda e nunca é reaproveitado, mesmo que a entidade seja renomeada, reclassificada ou removida.
3. Uma competência que precisar sair continua no cabeçalho; uma nova recebe o próximo número livre.
4. Códigos aposentados ficam registrados em `catalogo/aposentados.yml`, com o motivo. `M0` é o primeiro.
5. Reclassificar uma disciplina de eixo muda o metadado `eixo`, não o código. O prefixo sugere a área, mas não a define.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| UUID | Ilegível para quem estuda e exige migrar todo o histórico |
| Slug do título | Muda quando o nome muda |

## Consequências

- O histórico de respostas continua válido sem migração.
- O prefixo pode ficar enganoso depois de uma reclassificação; isso é aceito.
- A unicidade dos códigos de disciplina precisa ser conferida por script: a auditoria encontrou que um código repetido fazia o segundo arquivo substituir o primeiro em silêncio.
- Códigos do Mapa sem arquivo em `disciplinas/` (`M13`, `S3`, `H3`, `H4`) não são aposentados nem reaproveitados (débito DT-03 em [débitos](../arquitetura/debitos.md)).
