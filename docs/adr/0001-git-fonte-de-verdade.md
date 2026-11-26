# ADR 0001 · Git é a fonte de verdade

- **Status:** Aceita
- **Data:** 25/11/2026

## Contexto

O plano nasceu no documento *Mapa de Formação — Engenheiro Generalista Polímata*, fora do Git. O repositório trouxe as seções 16 a 18 do Mapa para `disciplinas/`, mas unidades do curso, projetos integradores, bibliografia e a escala de domínio continuaram só no Mapa. A [auditoria de 25/11/2026](../arquitetura/auditoria.md) encontrou as duas fontes divergindo: o Mapa não cita o portão de autonomia, usa 4 níveis de exercício em vez de 5 e manda começar por NM1 e NL1, quando o repositório começa pelo NM0.

O repositório já tem o que o Mapa não tem: validação por script, testes, CI, histórico e consumo por programa (scripts e skill).

## Decisão

1. O repositório Git é a fonte de verdade do plano (decisão D1 da auditoria).
2. O Mapa de Formação foi exportado e congelado em [docs/referencia/mapa-de-formacao-rev74.md](../referencia/mapa-de-formacao-rev74.md), revisão 74, em 25/11/2026. Ele é referência histórica: não se edita.
3. Onde o Mapa divergir de `disciplinas/`, `catalogo/`, `AVALIACOES.md` ou `plano.yml`, valem eles.
4. As entidades que só existiam no Mapa (eixos, unidades, projetos e escala de domínio) passaram para [catalogo/](../../catalogo/README.md).
5. Mudança no plano entra no repositório. Não há sincronização de volta para o Mapa.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Manter o Mapa como canônico | Não é validado pelo CI nem lido pelos scripts e pela skill |
| Dividir por assunto (parte no Mapa, parte no Git) | Exige sincronizar duas fontes, e a divergência já aconteceu |

## Consequências

- Uma origem para cada fato do currículo; o CI confere o que está no Git.
- Editar tabelas em arquivo YAML é menos confortável que num documento.
- A cópia congelada tem divergências conhecidas, listadas no cabeçalho dela. Elas não são corrigidas lá (débito DT-02 em [débitos](../arquitetura/debitos.md)).
- Bibliografia (referências) ainda não está no catálogo; quando entrar, vem para o Git, não para o Mapa.
