# Nível 12 · Engenharia de versionamento

[G5](../../disciplinas/G5-git-avancado-e-engenharia-de-versionamento.md) · [guias da G5](README.md) · [árvore](../NG1/README.md)

## 1. Objetivo

Escolher, documentar e defender a estratégia de versionamento de uma equipe: como o trabalho flui até a principal, como versões são numeradas e publicadas, como hotfixes entram e como mudanças são governadas.

## 2. Conceitos

- **Estratégia de branching:** quais branches existem, quanto vivem e como o trabalho volta à principal.
- **Trunk-based development:** branches de horas ou poucos dias, integradas na principal várias vezes por dia; o que não está pronto fica atrás de *feature flags*.
- **GitHub Flow:** principal sempre implantável, uma branch por mudança, PR e merge; implanta depois do merge.
- **Git Flow:** `main` (versões publicadas), `develop` (integração), `feature/*`, `release/*` e `hotfix/*`.
- **Release branches:** linhas mantidas por versão (`release/1.x`), com correções levadas por cherry-pick.
- **Conventional Commits e SemVer:** a mensagem diz o tipo de mudança; a versão diz o impacto para quem usa (nível 8).
- **Release management:** quando e como uma versão sai, quem aprova, o que acompanha (notas, artefatos, migração).
- **Changelog:** registro legível por versão: adicionado, mudado, corrigido, removido.
- **Hotfix:** correção urgente de uma versão em produção, com caminho curto e rastreável.
- **Governança de mudanças:** quem pode mudar o quê, com que revisão, e como decisões ficam registradas (ADRs).

## 3. Explicação

Não existe estratégia melhor; existe a que combina com o **ritmo de entrega** e com o **número de versões mantidas ao mesmo tempo**.

| Situação | Estratégia que costuma servir | Por quê |
| --- | --- | --- |
| Serviço web implantado várias vezes por dia, CI forte | Trunk-based | Integração contínua de verdade; pouca divergência, conflitos pequenos |
| Equipe pequena, implantação depois de cada PR | GitHub Flow | Simples: principal + branches curtas + PR |
| Produto instalado pelo cliente, com várias versões em suporte | Git Flow ou release branches | Precisa corrigir a 1.x enquanto a 2.0 avança |
| Biblioteca pública | GitHub Flow + tags SemVer + release branches para versões antigas | Usuários dependem do número da versão |

O custo do Git Flow é a divergência: `develop` e `main` se afastam, releases viram eventos, e merges grandes trazem conflitos grandes. O custo do trunk-based é a disciplina: testes rápidos e confiáveis, feature flags e revisão rápida. Sem isso, a principal quebra.

**Hotfix**, em qualquer estratégia: branch a partir da tag em produção, correção mínima com teste, revisão, release de correção (`1.4.1`) e a mesma correção levada para a principal (merge ou cherry-pick `-x`), para o bug não voltar na próxima versão.

A governança se registra no próprio repositório: regras no `CONTRIBUTING`, proteções nas configurações (nível 9), decisões em ADRs. Este repositório tem um exemplo real de estratégia não convencional, com motivo escrito: **branches de longa duração por estudante, nunca mescladas na principal** ([ADR 0006](../../docs/adr/0006-fluxo-de-git.md)), e um **repositório público que é só espelho**, alimentado por um script ([ADR 0008](../../docs/adr/0008-repositorio-publico-separado.md)).

## 4. Comandos

| Comando ou recurso | Para quê |
| --- | --- |
| `git tag -a vX.Y.Z` | Marca a versão |
| `git log --oneline vA..vB` | Commits entre duas versões (base do changelog) |
| `git switch -c hotfix/X.Y.Z+1 vX.Y.Z` | Hotfix a partir da versão em produção |
| `git cherry-pick -x <sha>` | Leva uma correção para outra linha |
| `gh release create` | Publica a release |
| Ferramentas de release (release-please, semantic-release) | Versão e changelog a partir de Conventional Commits |

## 5. Sintaxe

```markdown
## [1.5.0] - 2026-12-01
### Adicionado
- Laboratório de Git com 10 cenários conferidos por script.
### Corrigido
- `status` do laboratório perdia o espaço inicial do porcelain.

## [1.4.1] - 2026-11-20
### Corrigido
- Hotfix: a importação de CSV quebrava com campos vazios.
```

## 6. Exemplos reais

- Um serviço de uma equipe de 8 pessoas: trunk-based, PRs de menos de 300 linhas, CI de 6 minutos, feature flags, implantação contínua com rollback por revert.
- Um aplicativo desktop com suporte de 18 meses por versão: release branches `release/3.x` e `release/4.x`, correções na principal levadas por cherry-pick, tags SemVer.
- Este repositório: PR para toda estrutura na `main`, uma branch de estudo por pessoa e publicação controlada por script. Sem releases versionadas até aqui. A skill de estudo, porém, tem versão (`1.0.4`) e roda testes de regressão a cada versão.

## 7. Cenários de uso

- Propor a estratégia de um projeto novo de equipe.
- Migrar uma equipe de Git Flow para trunk-based, ou o contrário, com justificativa.
- Organizar a primeira release de um projeto e o primeiro hotfix.

## 8. Erros comuns

- **Copiar o Git Flow** para um serviço com implantação contínua: branches e cerimônias que ninguém precisa.
- **Trunk-based sem testes confiáveis:** a principal quebra todo dia.
- **Hotfix que não volta para a principal:** o bug reaparece na versão seguinte.
- **Changelog gerado só da lista de commits**, ilegível para o usuário.
- **Estratégia na cabeça de uma pessoa**, sem estar escrita.

## 9. Riscos

- Branches de vida longa acumulam divergência; o merge final vira um projeto.
- Release automatizada sem revisão pode publicar versão maior por um `!` acidental.
- Mudar a estratégia no meio de um ciclo de release confunde quem já tinha trabalho em andamento.

## 10. Boas práticas

- Estratégia escrita num ADR, com o motivo e a alternativa descartada.
- Branches curtas por padrão; vida longa só com motivo (como a branch de estudo).
- SemVer + Conventional Commits + changelog por versão.
- Caminho de hotfix ensaiado antes da primeira emergência.
- Revisão da estratégia quando o ritmo de entrega mudar.

## 11. Exercício básico

Para cada um dos quatro cenários da tabela da explicação, desenhe o grafo de branches de uma semana típica, com pelo menos uma feature, uma release e um hotfix.

## 12. Exercício intermediário

No repositório do projeto da G5, publique `v1.0.0`, `v1.1.0` (uma funcionalidade) e `v1.1.1` (um hotfix feito a partir da tag `v1.1.0` e levado de volta para a principal). Escreva o changelog das três versões.

## 13. Exercício avançado

Escreva um ADR para uma equipe fictícia de sua escolha (tamanho, produto, ritmo de entrega), escolhendo a estratégia de branching e de releases, com as alternativas consideradas e os motivos da escolha. Defenda o ADR oralmente contra as objeções de quem preferiria a outra estratégia.

## 14. Desafio aplicado ao repositório

Leia os ADRs [0006](../../docs/adr/0006-fluxo-de-git.md), [0008](../../docs/adr/0008-repositorio-publico-separado.md) e [0010](../../docs/adr/0010-disciplinas-de-git-e-guias.md). Escreva uma página respondendo:

1. Que estratégia de branching este repositório usa, nos termos deste nível?
2. Por que as branches de estudo não seguem a regra "branches curtas"? O motivo se sustenta?
3. Se o repositório passasse a ter releases versionadas, o que seria `MAIOR`, `MENOR` e `CORREÇÃO`? Proponha o primeiro changelog.

Se você achar uma melhoria, ela entra como proposta de ADR, por PR.

## 15. Checklist de validação

- [ ] Comparo trunk-based, GitHub Flow, Git Flow e release branches pelos custos.
- [ ] Escolho a estratégia a partir do ritmo de entrega e das versões em suporte.
- [ ] Executo um hotfix completo, inclusive levando a correção à principal.
- [ ] Escrevo um changelog útil para o usuário.
- [ ] Registro uma decisão de versionamento num ADR.

## 16. Critério de conclusão

O exercício intermediário fecha o projeto do portão da G5 (repositório com ruleset, CI, releases versionadas e changelog). O ADR do exercício avançado foi defendido oralmente.

## 17. Próximo módulo

Fim da árvore de Git. O que vem depois é usar: G3 (cloud e infraestrutura como código) aplica GitOps de verdade, e S5 (entrega e operação) aplica release management a um sistema em produção.
