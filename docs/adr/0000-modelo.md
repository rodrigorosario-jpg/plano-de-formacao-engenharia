# ADR NNNN · Título curto da decisão

Copie este arquivo para `NNNN-titulo-em-kebab-case.md`, com o próximo número livre, e preencha as seções. Números de ADR não são reaproveitados.

- **Status:** Proposta | Aceita | Substituída por ADR NNNN | Descontinuada
- **Data:** DD/MM/AAAA

## Contexto

Que problema ou força pede uma decisão. Fatos, com a origem (auditoria, arquivo, commit). Sem a decisão ainda.

## Decisão

O que foi decidido, em frases curtas e afirmativas. Se a decisão tem regras, liste-as.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Opção A | Motivo |
| Opção B | Motivo |

## Consequências

- O que fica mais fácil.
- O que fica mais difícil ou custa mais.
- O que precisa mudar em outros arquivos, e quando.

## Regras para manter as ADRs

- Uma decisão por arquivo.
- ADR aceita não é reescrita. Se a decisão mudar, crie uma ADR nova e marque a antiga como "Substituída por ADR NNNN".
- Mudança de estrutura que altera uma decisão entra na `main` por pull request junto com a ADR ([fluxo de git](../fluxo-git.md)).
