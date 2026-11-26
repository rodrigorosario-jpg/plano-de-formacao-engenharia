# Publicação

Este repositório é privado: guarda a `main` e as branches de estudo. A versão pública é um repositório separado e é **só espelho**: recebe a árvore da `main`, sem o histórico privado e sem `.github/dependabot.yml` ([ADR 0008](adr/0008-repositorio-publico-separado.md), [ADR 0009](adr/0009-espelho-publico-e-publicacao-por-pr.md)).

## Publicar

```bash
git remote add publico https://github.com/<usuário>/<repositório-público>.git   # uma vez
scripts/publicar.sh publico            # mostra o que seria publicado
scripts/publicar.sh publico --enviar   # publica
```

- **Primeira publicação** (público vazio): o commit vai direto para a `main`. Em seguida, aplique o ruleset (abaixo).
- **Publicações seguintes:** o commit vai para a branch `publicacao/<sha>` e o script abre um pull request. Espere o CI passar e mescle com **Rebase and merge**, que mantém o histórico linear e o autor noreply.

Publicar é decisão do dono do repositório: a skill não publica sozinha.

## O script recusa publicar quando

| Situação | O que fazer |
| --- | --- |
| A `main` tem `registro/estado.yml`, `registro/estudante.yml` ou resultados em `registro/` | Dado de estudo fica na branch de estudo; tire da `main` por PR |
| A árvore tem um e-mail que não é noreply nem de exemplo | Procure com `git grep -nE '[A-Za-z0-9._%+-]+@'` e remova por PR |
| A identidade do git local não é noreply | `git config user.email <id>+<usuário>@users.noreply.github.com` |
| O público tem mudanças que não vieram de uma publicação | Traga a mudança para a `main` privada por PR; depois publique |

## Configuração do repositório público

Estas proteções vivem no GitHub, não em arquivos. O estado de cada uma (aplicada, verificada ou só recomendada) fica no checklist de [segurança](arquitetura/seguranca.md#configuração-do-github).

**Ruleset `main`** (Settings → Rules → Rulesets), alvo: branch padrão:

- exigir pull request, com 0 aprovações;
- exigir o check `validar`;
- bloquear force push e exclusão;
- bypass: papel *Repository admin* (o dono), para emergências.

**Settings → General:** só *Allow rebase merging*; *Automatically delete head branches* ligado; Wiki e Projects desligados.

**Settings → Code security:** *Private vulnerability reporting*, *Dependabot alerts*, *Secret scanning* com *Push protection* e *CodeQL* (default setup) ligados. *Dependabot security updates* fica desligado: as atualizações entram pelo privado.

**Settings → Actions → General:** *Workflow permissions* em *Read repository contents*; aprovação obrigatória para workflows de PRs de fora (*Require approval for all external contributors*).

**Na sua conta** (Settings → Emails): *Keep my email addresses private* e *Block command line pushes that expose my email*. Sem isso, um merge feito pelo site sai com o e-mail principal da conta.

## Quem faz fork

O `CODEOWNERS` e o link de relato de vulnerabilidade em `.github/ISSUE_TEMPLATE/config.yml` apontam para o dono original; ajuste os dois no seu fork.
