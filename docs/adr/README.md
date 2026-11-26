# Registros de decisão de arquitetura (ADRs)

Cada arquivo registra uma decisão: o contexto, o que foi decidido, as alternativas e as consequências. O formato está em [0000-modelo.md](0000-modelo.md).

| ADR | Decisão | Status | Data |
| --- | --- | --- | --- |
| [0001](0001-git-fonte-de-verdade.md) | Git é a fonte de verdade; o Mapa fica congelado em `docs/referencia/` | Aceita | 25/11/2026 |
| [0002](0002-markdown-e-yaml-sem-banco.md) | Markdown e YAML, sem banco de dados; estrutura de pastas | Aceita | 25/11/2026 |
| [0003](0003-codigos-como-identificadores.md) | Códigos atuais como identificadores, nunca reaproveitados | Aceita | 25/11/2026 |
| [0004](0004-separar-andamento-do-curriculo.md) | Separar o andamento do currículo em `registro/estado.yml` | Aceita, implementada | 25/11/2026 |
| [0005](0005-json-schema-versionado.md) | JSON Schema com `jsonschema`, schemas versionados em `schemas/` | Aceita | 25/11/2026 |
| [0006](0006-fluxo-de-git.md) | Andamento na branch de estudo de cada pessoa, estrutura na `main` por pull request | Aceita | 25/11/2026 |
| [0007](0007-autoria-dos-commits.md) | Commits pela conta do estudante, sem assinatura do Claude | Aceita | 25/11/2026 |
| [0008](0008-repositorio-publico-separado.md) | Repositório público separado, só com a árvore da `main`; MIT no código e CC BY 4.0 no conteúdo | Aceita | 26/11/2026 |
| [0009](0009-espelho-publico-e-publicacao-por-pr.md) | O público é só espelho; Dependabot só no privado; publicação por PR com ruleset na `main` pública | Aceita | 26/11/2026 |
| [0010](0010-disciplinas-de-git-e-guias.md) | Git no plano: NG1 no nivelamento, G5 na graduação, guias por nível e laboratório conferido por script | Aceita | 26/11/2026 |

## Origem

As ADRs 0001 a 0005 registram as decisões D1 a D5 da [auditoria de 25/11/2026](../arquitetura/auditoria.md), aprovadas pelo estudante. A auditoria usa o rótulo D5 duas vezes: na seção 8 é o JSON Schema (ADR 0005); na tabela do resumo é "primeiro passo: só os itens P0", uma escolha de sequência e não de arquitetura, que por isso não tem ADR. As ADRs 0006 e 0007 registram regras do [fluxo de git](../fluxo-git.md). A ADR 0009 vem da auditoria de hardening de 26/11/2026, registrada em [segurança](../arquitetura/seguranca.md). A ADR 0010 registra a escolha do estudante sobre onde o Git entra no plano.

## Como propor uma decisão

1. Copie [0000-modelo.md](0000-modelo.md) para o próximo número livre, com um título curto em kebab-case.
2. Preencha com status "Proposta" e abra um pull request para a `main` ([fluxo de git](../fluxo-git.md)).
3. Com a aprovação do estudante, mude o status para "Aceita" e acrescente a linha nesta tabela.
4. Para mudar uma decisão aceita, crie uma ADR nova e marque a antiga como "Substituída por ADR NNNN". Números não são reaproveitados.

Veja também a [documentação de arquitetura](../arquitetura/README.md).
