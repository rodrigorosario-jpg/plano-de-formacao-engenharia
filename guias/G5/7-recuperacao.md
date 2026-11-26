# Nível 7 · Recuperação e troubleshooting

[G5](../../disciplinas/G5-git-avancado-e-engenharia-de-versionamento.md) · [guias da G5](README.md) · [árvore](../NG1/README.md)

> Este nível usa comandos que descartam trabalho. Faça tudo numa cópia descartável sem remoto ([segurança dos exercícios](README.md#segurança-dos-exercícios)).

## 1. Objetivo

Diagnosticar estados estranhos do repositório e recuperar commits, branches e mudanças que pareciam perdidos, escolhendo sempre a operação menos destrutiva.

## 2. Conceitos

- **Reflog:** diário local de cada posição de HEAD e de cada branch, com data. Não vai para o remoto, e as entradas expiram (90 dias por padrão; 30 para commits inalcançáveis).
- **Detached HEAD:** HEAD apontando para um commit, não para uma branch. Commits feitos assim não têm nome que os segure.
- **Reset:** move a branch atual para outro commit. `--soft` mantém staging e pasta; `--mixed` (padrão) limpa o staging e mantém a pasta; `--hard` descarta staging **e pasta**.
- **Restore:** traz conteúdo de arquivos sem mover branch (nível 2).
- **Revert:** commit novo com o inverso de um commit anterior. Não reescreve nada.
- **Stash:** pilha de mudanças não commitadas guardadas à parte.
- **Objeto órfão (inalcançável):** commit que nenhuma ref nem o reflog alcança; o `gc` remove.
- **Destrutivo x não destrutivo:** destrutivo perde trabalho que não está em nenhum commit, ou reescreve histórico compartilhado.

## 3. Explicação

Quase nada que foi **commitado** se perde no Git: o reflog guarda para onde a branch apontava antes do rebase, do reset ou do amend. O que se perde de verdade é trabalho **nunca commitado** descartado por `reset --hard`, `restore`, `checkout -- arquivo` ou `clean -f`. Por isso, ao recuperar, a primeira pergunta é: estava num commit?

Escolha da ferramenta para desfazer:

| Situação | Ferramenta | Destrutivo? |
| --- | --- | --- |
| Mudança na pasta, sem commit | `git restore` ou `git stash` | `restore` sim; `stash` não |
| Último commit, não enviado | `git reset --soft HEAD~1` | Não (as mudanças voltam ao staging) |
| Commit já enviado | `git revert <sha>` | Não |
| Branch apagada ou rebase que deu errado | `git reflog` + `git branch <nome> <sha>` | Não |
| Merge enviado com problema | `git revert -m 1 <merge>` | Não |

Para diagnosticar, leia nesta ordem: `git status` (estado atual e operação em andamento), `git log --oneline --graph --all -20` (onde estão as branches) e `git reflog -20` (o que aconteceu).

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `git reflog [branch]` | Histórico de posições |
| `git reset --soft/--mixed/--hard <commit>` | Move a branch atual |
| `git revert <commit>` | Desfaz com um commit novo |
| `git restore` | Recupera arquivos (nível 2) |
| `git fsck --lost-found` | Lista objetos inalcançáveis, inclusive stashes descartados |
| `git stash` | Guarda e recupera mudanças não commitadas |

## 5. Sintaxe

```text
git reflog --date=relative               # quando cada movimento aconteceu
git branch resgate HEAD@{3}              # cria branch na posição de 3 movimentos atrás
git reset --hard ORIG_HEAD               # volta ao estado antes do último merge, rebase ou reset
git revert --no-edit <sha>
git revert -m 1 <merge>                  # desfaz um merge, mantendo o lado do pai 1
git stash push -m "<descrição>" [--include-untracked]
git stash list ; git stash show -p stash@{0}
git stash pop                            # aplica e remove; em conflito, mantém na pilha
git switch -c resgate                    # em detached HEAD: dá nome aos commits feitos ali
git fsck --unreachable --no-reflogs | grep commit
```

## 6. Exemplos reais

```console
$ git rebase -i HEAD~4          # ...e o resultado ficou errado
$ git reflog -5
e3f... HEAD@{0}: rebase -i (finish): returning to refs/heads/feature
...
a1b... HEAD@{4}: commit: último commit antes do rebase
$ git reset --hard HEAD@{4}     # numa branch só sua, volta a antes do rebase
```

```console
$ git switch --detach v1.0      # olhando uma versão antiga
$ git commit -am "experimento"  # commit sem branch
$ git switch main               # o Git avisa: commit deixado para trás
$ git branch experimento <sha>  # o sha do aviso, ou do reflog
```

## 7. Cenários de uso

- "Apaguei a branch errada com `-D`."
- "O rebase bagunçou tudo."
- "Fiz `reset --hard` e sumiu meu commit."
- "Um commit enviado ontem quebrou a produção": `revert`, nunca reset.
- "Preciso trocar de branch no meio de um trabalho": `stash`.

## 8. Erros comuns

- **`reset --hard` para "limpar"** com mudanças não commitadas que importavam.
- **Reset em branch compartilhada** para desfazer algo já enviado. Use revert.
- **Esquecer stashes** por meses. `git stash list` regularmente, e mensagens com `-m`.
- **Rodar `git gc --prune=now`** logo depois de perder algo: apaga o que o reflog ainda guardava.

## 9. Riscos

Comandos que **descartam trabalho não commitado**, sem volta:

- `git reset --hard`
- `git restore <arq>` e `git checkout -- <arq>`
- `git clean -f` e `git clean -fd`, que apagam arquivos não rastreados (use `-n` antes para ver)
- `git stash drop` e `git stash clear`, recuperáveis só com `fsck` e por pouco tempo

Comandos que **reescrevem histórico**: `reset` para trás numa branch já enviada, `commit --amend`, `rebase` e `push --force`.

## 10. Boas práticas

- Antes de qualquer operação arriscada: `git branch backup/<data>` e `git stash` se houver mudança local.
- Desfazer o que foi enviado é sempre com `revert`.
- Leia o reflog antes de entrar em pânico.
- `git clean -n` antes de `-f`.

## 11. Exercício básico

Na cópia descartável, faça três commits, `git reset --hard HEAD~2` e recupere os dois commits pelo reflog criando uma branch. Depois faça o mesmo com `--soft` e com `--mixed` e descreva, para cada um, onde as mudanças foram parar.

## 12. Exercício intermediário

Apague com `-D` uma branch com dois commits não integrados, troque de branch duas vezes e recupere-a. Depois faça um commit em detached HEAD, saia dele e recupere-o. Explique por que, num clone novo, nenhuma das duas recuperações seria possível.

## 13. Exercício avançado

Num remoto bare local, envie um merge que "quebra" um arquivo. Desfaça com `git revert -m 1`, envie, e depois tente mesclar de novo a mesma branch corrigida. Explique por que as mudanças não voltam e como resolver (revertendo o revert).

## 14. Desafio aplicado ao repositório

Na cópia descartável sem remoto, peça a alguém (ou a você mesmo, de olhos fechados para o comando) para rodar uma destas: `rebase -i` com `drop`, `reset --hard HEAD~3` ou `branch -D` de uma branch com trabalho. Só com `status`, `log --all --graph` e `reflog`, diagnostique o que foi feito e recupere o estado anterior. É esse o "recuperar histórico ao vivo" do portão da G5.

## 15. Checklist de validação

- [ ] Explico `--soft`, `--mixed` e `--hard` pelo efeito nas três áreas.
- [ ] Recupero branch apagada, rebase errado e commit em detached HEAD.
- [ ] Desfaço um commit enviado com revert, inclusive de merge.
- [ ] Sei quais comandos perdem trabalho sem volta.
- [ ] Uso stash com mensagem e sei recuperar um stash descartado.

## 16. Critério de conclusão

O desafio do repositório foi feito diante de outra pessoa ou gravado: diagnóstico falado e recuperação completa, sem consulta.

## 17. Próximo módulo

[Nível 8 · GitHub e colaboração](8-colaboracao-github.md).
