# Nível 2 · Manipulação de arquivos e histórico

[NG1](../../disciplinas/NG1-git-essencial.md) · competências NG1.c02 e NG1.c03 · [árvore](README.md)

## 1. Objetivo

Mover, renomear e remover arquivos pelo Git; comparar qualquer par de versões; desfazer mudanças locais; trazer de volta a versão antiga de um arquivo sem reescrever o histórico.

## 2. Conceitos

- **Ciclo de vida de um arquivo:** não rastreado → rastreado (modificado ↔ no staging ↔ commitado). Um arquivo removido com `git rm` sai do rastreamento no próximo commit.
- **Rastreado x não rastreado:** rastreado é o que já entrou em algum commit ou está no staging. O resto o Git só lista.
- **Comparação:** `git diff` compara duas das três áreas, ou dois commits.
- **Recuperação de arquivo:** pegar o conteúdo de um arquivo de outra área (staging, commit) e escrever por cima.
- **Autoria por linha:** `git blame` diz, para cada linha, o último commit que a mudou.

## 3. Explicação

Há três comparações que você vai usar o tempo todo:

| Você quer ver | Comando |
| --- | --- |
| O que mudou e ainda não está no staging | `git diff` |
| O que vai no próximo commit | `git diff --staged` |
| A diferença entre dois commits | `git diff A B` |

E duas direções de "desfazer" local, com `git restore`:

- `git restore --staged x`: tira `x` do staging; a mudança continua na pasta. Não perde nada.
- `git restore x`: joga fora a mudança de `x` na pasta e volta ao que está no staging (ou no último commit). **Perde a mudança.**

Para trazer a versão de um commit antigo, use `git restore --source=<commit> x`: o arquivo volta ao conteúdo daquele commit, como uma mudança nova, que você commita. O passado não muda; o histórico ganha um commit dizendo "voltei este arquivo".

`git rm` e `git mv` fazem a operação no disco e já põem no staging. O Git não guarda renomeações: ele as deduz comparando conteúdos, por isso `git log --follow` acompanha um arquivo através de renomeações.

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `git rm <arq>` | Apaga o arquivo e registra a remoção no staging |
| `git rm --cached <arq>` | Para de rastrear, mas mantém o arquivo na pasta |
| `git mv <de> <para>` | Renomeia ou move, já no staging |
| `git restore <arq>` | Descarta mudanças locais do arquivo |
| `git restore --staged <arq>` | Tira do staging |
| `git restore --source=<commit> <arq>` | Traz o conteúdo de um commit |
| `git diff`, `git diff --staged` | Comparações (tabela acima) |
| `git log` | Histórico, com filtros |
| `git blame <arq>` | Último commit de cada linha |

## 5. Sintaxe

```text
git log --oneline -- <arquivo>          # só commits que mexeram no arquivo
git log --follow -p -- <arquivo>        # acompanha renomeações e mostra os diffs
git log --grep="<texto>"                # mensagem contém o texto
git log --since="2 weeks ago" --author="<nome>"
git log -S "<texto>"                    # commits que adicionaram ou removeram o texto
git diff HEAD~3 HEAD -- <arquivo>
git show <commit>:<caminho>             # o arquivo inteiro como estava no commit
git blame -L 10,20 <arquivo>            # só as linhas 10 a 20
```

## 6. Exemplos reais

```console
$ git log --oneline -- requirements.txt     # cada commit que mexeu nas dependências
$ git show <sha> -- requirements.txt        # o que exatamente mudou num deles
$ git blame scripts/publicar.sh | head      # quem mexeu em cada linha, e quando
```

Recuperar um arquivo apagado por engano, ainda sem commit: `git restore apagado.txt`. Apagado num commit anterior: ache o commit com `git log --oneline -- apagado.txt` e rode `git restore --source=<commit>~1 apagado.txt` (o `~1` é o commit antes da remoção).

## 7. Cenários de uso

- Descobrir quando um valor de configuração mudou e qual foi a justificativa no commit.
- Desistir de uma tentativa que não deu certo, antes de commitar.
- Tirar do rastreamento um arquivo que deveria estar no `.gitignore` (`git rm --cached`, depois o `.gitignore`).

## 8. Erros comuns

- **Apagar com `rm` e esquecer o `git add`/`git rm`:** o commit não leva a remoção.
- **Confundir `restore` com `restore --staged`:** o primeiro descarta trabalho.
- **Achar que `git rm --cached` remove o segredo do histórico:** remove só dos próximos commits.
- **Ler `git blame` como culpa:** a linha pode ter sido só reformatada. Siga o commit com `git show`.

## 9. Riscos

- `git restore <arq>` (sem `--staged`) e `git checkout -- <arq>` descartam mudança **não commitada**. Ela não vai para o reflog; não há como voltar. Na dúvida, `git stash` antes (nível 7).
- `git restore --source=...` sobrescreve o arquivo na pasta. Commite ou guarde o que estava lá antes.

## 10. Boas práticas

- Renomeie com `git mv` num commit separado do commit que muda o conteúdo: o diff fica legível e o `--follow` funciona melhor.
- Antes de desfazer, leia `git diff` do que vai perder.
- Para desfazer algo já commitado e enviado, nunca reescreva: faça um commit novo (este nível) ou use `git revert` (nível 7).

## 11. Exercício básico

Num repositório de brinquedo com três commits: renomeie um arquivo com `git mv`, apague outro com `git rm`, rode `git status` e `git diff --staged` e explique cada linha. Commite.

## 12. Exercício intermediário

`git log --oneline -- limites.cfg` mostra três commits. Sem mudar nada, descubra qual valor o arquivo tinha em cada um (`git show <sha>:limites.cfg`) e escreva a linha do tempo do valor do timeout.

## 13. Exercício avançado

Laboratório, sem consulta: `N2-restaurar` e `N2-versao-antiga`.

## 14. Desafio aplicado ao repositório

Só leitura:

1. Com `git log --follow --oneline -- docs/referencia/mapa-de-formacao-rev74.md`, liste os commits que mexeram no Mapa congelado e diga, pelas mensagens, por que ele mudou mesmo sendo "congelado".
2. `git log -S "autonomia_n" --oneline`: em que commit esse parâmetro apareceu?
3. `git blame -L '/^## Regras/,+10' docs/fluxo-git.md`: quantos commits diferentes escreveram as regras do fluxo?

> Na versão pública deste repositório o histórico tem um commit por publicação. Se for o seu caso, faça este desafio num projeto seu com histórico (veja [desafios que leem histórico](README.md#desafios-que-leem-histórico)).

## 15. Checklist de validação

- [ ] Escolho entre `diff`, `diff --staged` e `diff A B` sem errar.
- [ ] Sei quais formas de `restore` perdem trabalho.
- [ ] Recupero um arquivo de um commit antigo sem reescrever o histórico.
- [ ] Filtro o `git log` por arquivo, texto e mensagem.
- [ ] Os dois cenários do nível 2 passaram no `conferir`.

## 16. Critério de conclusão

`N2-restaurar` e `N2-versao-antiga` passam sem consulta, e o desafio do repositório está respondido.

## 17. Próximo módulo

[Nível 3 · Branches](3-branches.md): linhas de trabalho paralelas.
