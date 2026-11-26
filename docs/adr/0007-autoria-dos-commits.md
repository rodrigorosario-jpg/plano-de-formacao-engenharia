# ADR 0007 · Commits pela conta do estudante, sem assinatura do Claude

- **Status:** Aceita
- **Data:** 25/11/2026

## Contexto

Boa parte das mudanças do repositório é feita numa sessão do Claude, a pedido do estudante. O repositório é o registro da formação do estudante e deve servir de portfólio. Quatro commits do PR #5 saíram com autor "Claude". O ambiente de execução também pode acrescentar, por padrão, linhas de coautoria às mensagens de commit e um rodapé de "Generated with Claude Code" aos pull requests.

## Decisão

1. Todo commit sai pela conta do estudante (`rodrigorosario-jpg`), com o e-mail `noreply` do GitHub.
2. Mensagens de commit não levam linhas `Co-Authored-By` nem `Claude-Session`. Pull requests não levam rodapé de "Generated with Claude Code".
3. Commit e push só quando o estudante pedir.
4. A regra completa, com os comandos de configuração, é a regra 7 de [docs/fluxo-git.md](../fluxo-git.md).
5. Os quatro commits do PR #5 com autor "Claude" ficam como estão, por decisão do estudante. O histórico publicado não é reescrito.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Commits com coautoria do Claude | O estudante preferiu que o histórico fique só na conta dele |
| Reescrever os commits antigos | Exige force push em branch publicada e pode quebrar referências de PRs |

## Consequências

- O histórico novo fica uniforme na conta do estudante.
- O uso do Claude continua documentado na skill, nos documentos de `docs/skills/` e nos benchmarks, não na autoria.
- Ficam dois débitos: os commits antigos com autor "Claude" e o rodapé que o ambiente acrescenta aos pull requests, que precisa ser retirado à mão (DT-11 e DT-12 em [débitos](../arquitetura/debitos.md)).
