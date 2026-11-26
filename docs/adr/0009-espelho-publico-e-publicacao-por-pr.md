# ADR 0009 · O repositório público é só espelho, e a publicação entra por pull request

- **Status:** Aceita
- **Data:** 26/11/2026

## Contexto

A primeira publicação ([ADR 0008](0008-repositorio-publico-separado.md)) foi seguida, no mesmo dia, de um PR do Dependabot aberto e mesclado direto no repositório público (`pyyaml` 6.0.3 → 6.0.4). A auditoria de hardening de 26/11/2026 achou três consequências:

- o público passou a ter um commit que o privado não tinha, e a publicação seguinte desfaria o bump sem avisar, porque `publicar.sh` gravava a árvore da `main` privada por cima da pública;
- o merge feito pelo site saiu com o e-mail pessoal da conta, que ficou público;
- como `.github/dependabot.yml` ia junto na publicação, o Dependabot continuaria abrindo PRs no espelho.

Também faltava proteção na `main` pública: aceitava force push, exclusão e push direto.

## Decisão

1. **O público é só espelho.** Toda mudança nasce no repositório privado, por PR na `main`, e chega ao público por `scripts/publicar.sh`. PRs abertos no público servem de proposta: a mudança é refeita no privado e o PR é fechado ([CONTRIBUTING](../../CONTRIBUTING.md)).
2. **O Dependabot roda só no privado.** `publicar.sh` tira `.github/dependabot.yml` da árvore publicada.
3. **O script recusa publicar se o espelho divergiu:** a `main` pública tem de ter a mesma árvore da última publicação. O que divergiu é trazido ao privado por PR antes.
4. **O script recusa publicar** se a árvore tiver um e-mail que não seja noreply ou de exemplo, ou se a identidade do git local não for noreply.
5. **A publicação entra por pull request.** A primeira vai direto para a `main` do repositório vazio. As seguintes vão para a branch `publicacao/<sha>` e abrem um PR; o dono mescla com **Rebase and merge** depois do CI passar.
6. **Ruleset na `main` pública:** exige PR (sem aprovação obrigatória, porque o mantenedor é um só e não pode aprovar o próprio PR), exige o check `validar`, bloqueia force push e exclusão. O dono fica na lista de bypass para emergências. Não exige commits assinados: os commits feitos por sessões do Claude não carregam a chave do dono.
7. **Remediação do vazamento:** o repositório público foi apagado e recriado vazio, depois de ligar "Keep my email addresses private" e "Block command line pushes that expose my email". Um force push não bastaria: a referência `refs/pull/1/head` do PR do Dependabot continuaria apontando para o primeiro commit, e o GitHub não deixa apagar referências de PR.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Aceitar PRs no público e trazê-los de volta antes de cada publicação | Duas fontes de verdade; cada publicação depende de lembrar de sincronizar |
| Push direto na `main` pública, com ruleset só contra force push | Escolha do dono: quer que toda mudança pública passe pelo CI num PR |
| Exigir uma aprovação no PR | Tranca o mantenedor único para fora |
| Force push para limpar o histórico público | Deixa os commits antigos acessíveis pelo SHA via `refs/pull/1/head` |

## Consequências

- O público continua com histórico próprio e linear: um commit por publicação.
- Publicar ficou em dois passos: rodar o script e mesclar o PR no site.
- Mudanças feitas direto no público bloqueiam a publicação até serem trazidas ao privado.
- As configurações do GitHub (ruleset, relato privado de vulnerabilidade, alertas) não vivem em arquivos. O estado delas está no checklist de [docs/arquitetura/seguranca.md](../arquitetura/seguranca.md), que distingue o que foi verificado do que só está documentado.
