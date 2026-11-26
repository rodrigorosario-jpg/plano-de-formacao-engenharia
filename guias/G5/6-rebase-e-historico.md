# Nível 6 · Rebase e histórico avançado

[G5](../../disciplinas/G5-git-avancado-e-engenharia-de-versionamento.md) · [guias da G5](README.md) · [árvore](../NG1/README.md)

> Todos os exercícios deste nível reescrevem histórico. Faça numa cópia descartável sem remoto ([segurança dos exercícios](README.md#segurança-dos-exercícios)).

## 1. Objetivo

Reorganizar commits de uma branch **sua, ainda não compartilhada** (reordenar, juntar, corrigir mensagens e reaplicar sobre outra base), e saber quando isso é proibido.

## 2. Conceitos

- **Rebase:** pega os commits da sua branch que não estão na base, e os reaplica um a um em cima da nova base. O resultado são **commits novos**, com outros SHAs.
- **Rebase interativo:** o mesmo, com uma lista editável: para cada commit, `pick`, `reword`, `edit`, `squash`, `fixup` ou `drop`, e na ordem que você quiser.
- **Squash e fixup:** juntam um commit ao anterior; `squash` combina as mensagens, `fixup` descarta a do commit absorvido.
- **Amend:** substitui o último commit por um novo.
- **Cherry-pick:** cria na branch atual um commit com as mesmas mudanças de outro commit.
- **Merge x rebase:** o merge preserva o que aconteceu (duas linhas que se juntam); o rebase reescreve como se tivesse sido em linha reta.
- **Reescrita de histórico:** qualquer operação que troca commits existentes por outros. Para quem já tinha os antigos, a branch "divergiu".

## 3. Explicação

A regra que decide tudo: **não reescreva commits que outra pessoa já tem.** Se você fez rebase de uma branch que um colega já baixou, os commits dele apontam para pais que não existem mais no seu histórico; o próximo pull dele duplica commits ou gera conflitos sem sentido. Numa branch só sua, antes do PR, reescrever é higiene: dez commits "wip", "conserta", "agora vai" viram três commits que contam a história.

Durante um rebase, cada commit reaplicado pode conflitar. O Git para, você resolve como no nível 4, `git add` e `git rebase --continue`. `git rebase --abort` volta tudo ao estado de antes.

Merge ou rebase para trazer a principal para a sua branch? Os dois funcionam. Rebase deixa o histórico linear, mas só numa branch não compartilhada. Merge é sempre seguro. Neste repositório, a branch de estudo recebe a `main` por **merge**: ela é compartilhada com o próprio GitHub e com a skill de estudo ([fluxo de git](../../docs/fluxo-git.md)).

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `git rebase <base>` | Reaplica os commits da branch atual sobre `<base>` |
| `git rebase -i <base>` | Rebase interativo |
| `git rebase --continue`, `--abort`, `--skip` | Controle durante um rebase |
| `git commit --amend` | Refaz o último commit |
| `git cherry-pick <commit>` | Copia um commit para a branch atual |
| `git push --force-with-lease` | Envia uma branch reescrita, mas recusa se o remoto mudou desde o seu fetch |

## 5. Sintaxe

```text
git rebase -i HEAD~5                     # edita os últimos 5 commits
git rebase --onto <nova> <velha> <branch> # transplanta <branch> de <velha> para <nova>
git commit --fixup=<sha>                 # cria um commit marcado para juntar a <sha>
git rebase -i --autosquash <base>        # já arruma os fixup! na lista
git commit --amend --no-edit             # inclui o staging no último commit, mesma mensagem
git cherry-pick -x <sha>                 # registra na mensagem de onde veio
git cherry-pick A..B                     # uma faixa (exclui A)
```

Lista do rebase interativo:

```text
pick   1a2b3c4 cria o parser
fixup  5d6e7f8 conserta typo no parser
reword 9a8b7c6 testes
drop   0f1e2d3 print de depuração
```

## 6. Exemplos reais

- Antes de abrir um PR, `git rebase -i origin/main` com `fixup` e `reword` transforma `wip`, `wip 2` e `ajusta` em `feat(laboratorio): cenários do nível 5`.
- Uma correção urgente feita na `main` precisa ir também para a branch de release `v1.2`: `git switch release/1.2 && git cherry-pick -x <sha>` (nível 12).
- Esqueceu um arquivo no último commit, ainda não enviado: `git add esquecido.txt && git commit --amend --no-edit`.

## 7. Cenários de uso

- Limpar a branch de feature antes da revisão.
- Atualizar uma branch de feature sua com a `main` mantendo histórico linear.
- Levar uma correção específica para outra linha de versão.
- Separar um commit grande em dois (`edit` no rebase interativo, depois `git reset HEAD~` e commits menores).

## 8. Erros comuns

- **Rebase de branch compartilhada** e depois `push --force`.
- **Amend de commit já enviado.**
- **Resolver o mesmo conflito várias vezes** num rebase longo. Ligue `git config rerere.enabled true`, que lembra resoluções.
- **Cherry-pick em vez de merge** para trazer uma branch inteira: duplica commits com SHAs diferentes e confunde merges futuros.

## 9. Riscos

- Rebase, amend e `drop` geram commits novos; os antigos ficam acessíveis **só pelo reflog local** por cerca de 90 dias (nível 7). Antes de um rebase grande, `git branch backup/<nome>` é um seguro de graça.
- `git push --force` sobrescreve o remoto sem conferir nada. Se precisar enviar uma branch sua reescrita, use `--force-with-lease`. Numa branch protegida (nível 9), o GitHub recusa os dois.

## 10. Boas práticas

- Reescreva só o que ainda não saiu da sua máquina, ou o que está numa branch só sua de PR.
- `--force-with-lease`, nunca `--force`.
- Cada commit do resultado deve compilar e passar nos testes: `git rebase -i --exec "pytest -q" <base>` confere commit a commit.
- No time, combine se a branch principal aceita merge commits ou só histórico linear (nível 12).

## 11. Exercício básico

Na cópia descartável, crie uma branch com quatro commits (dois deles "wip"). Com `git rebase -i`, junte os "wip" ao commit certo e reescreva uma mensagem. Compare `git log --oneline` antes e depois e anote quais SHAs mudaram. Por que mudaram até os que você não tocou?

## 12. Exercício intermediário

Crie duas branches a partir do mesmo commit, A e B, e avance a `main` com um commit que conflita com A. Integre A por rebase e B por merge. Desenhe o grafo resultante e escreva quando você escolheria cada forma numa equipe.

## 13. Exercício avançado

Simule o problema: num remoto bare local, Ana e Beto clonam; Ana faz rebase da branch compartilhada e envia com `--force`. Mostre o que acontece no próximo `pull` de Beto. Repita com `--force-with-lease` e explique por que o envio de Ana é recusado quando Beto enviou antes.

## 14. Desafio aplicado ao repositório

Na cópia descartável **sem remoto**: crie `curriculo/treino-rebase` a partir de `main` com três commits pequenos em `## Anotações` de três disciplinas, um deles com mensagem ruim. Arrume com `rebase -i` para dois commits no padrão `docs(disciplinas): ...`, rode `python scripts/progresso.py --checar` em cada commit com `--exec` e mostre o `git log --oneline` final.

## 15. Checklist de validação

- [ ] Explico por que rebase gera commits novos.
- [ ] Uso `pick`, `reword`, `squash`, `fixup` e `drop` no rebase interativo.
- [ ] Sei abortar e continuar um rebase com conflito.
- [ ] Sei dizer quando reescrever é proibido.
- [ ] Uso `--force-with-lease` e sei o que ele protege.
- [ ] Faço cherry-pick com `-x`.

## 16. Critério de conclusão

O exercício avançado está feito, com a explicação escrita do que aconteceu com Beto, e o desafio do repositório produziu um histórico limpo que passa no `--checar` commit a commit.

## 17. Próximo módulo

[Nível 7 · Recuperação e troubleshooting](7-recuperacao.md): o reflog e como desfazer quase tudo.
