# Nível 5 · Git remoto

[NG1](../../disciplinas/NG1-git-essencial.md) · competência NG1.c06 · [árvore](README.md)

## 1. Objetivo

Sincronizar com repositórios remotos: buscar o trabalho dos outros, integrar com o seu e enviar, entendendo a diferença entre a sua branch e a cópia local da branch remota.

## 2. Conceitos

- **Remoto:** outro repositório Git com um apelido, geralmente uma URL do GitHub.
- **origin:** o apelido padrão do remoto de onde você clonou.
- **upstream:** por convenção, o repositório original quando você trabalha num fork (`origin` = o seu fork, `upstream` = o original). Também é o nome da relação "esta branch local acompanha aquela remota".
- **Fork:** uma cópia de um repositório na sua conta do GitHub (nível 8).
- **Branch de rastreamento remoto:** `origin/main` é a sua **cópia local** de onde a `main` do remoto estava no último `fetch`. Ela não se atualiza sozinha.
- **Tracking branch:** a sua `main` local configurada para acompanhar `origin/main`; é o que permite `git pull` e `git push` sem argumentos e o "ahead/behind" do `git status`.
- **fetch:** baixa commits e atualiza `origin/*`. Não mexe nas suas branches nem na pasta.
- **pull:** `fetch` + integração (merge, ou rebase se configurado) na branch atual.
- **push:** envia commits da branch local e move a branch no remoto. É recusado se o remoto tem commits que você não tem.

## 3. Explicação

Há três versões da "mesma" `main`: a do GitHub, a `origin/main` no seu computador (a foto do último `fetch`) e a sua `main` local. `git status` diz *"Your branch is behind 'origin/main' by 2 commits"* comparando a segunda com a terceira, não com o GitHub. Por isso o primeiro comando de uma sessão é `git fetch`.

Um push recusado (*rejected, non-fast-forward*) quer dizer: alguém enviou commits que você não tem. A resposta certa é buscar e integrar (`git pull`, ou `git fetch` + `git merge origin/main`), resolver conflitos se houver, testar e enviar de novo. A resposta errada é `git push --force`, que apaga do remoto o trabalho da outra pessoa.

Prefira `fetch` + olhar + integrar a `pull` às cegas: `git log --oneline main..origin/main` mostra o que vem antes de você aceitar.

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `git remote -v` | Lista os remotos e as URLs |
| `git remote add <nome> <url>` | Acrescenta um remoto |
| `git fetch [remoto]` | Atualiza `remoto/*` sem mexer no seu trabalho |
| `git pull` | Busca e integra na branch atual |
| `git push` | Envia a branch atual para a que ela acompanha |
| `git push -u origin <branch>` | Primeiro envio de uma branch nova, já configurando o acompanhamento |
| `git ls-remote <remoto>` | Lista as refs do remoto sem baixar nada |

## 5. Sintaxe

```text
git fetch --prune                     # também remove origin/* de branches apagadas no remoto
git branch -vv                        # mostra qual remota cada branch acompanha e o ahead/behind
git log --oneline main..origin/main   # o que o remoto tem e você não
git log --oneline origin/main..main   # o que você vai enviar
git pull --ff-only                    # só integra se for fast-forward
git pull --rebase                     # integra reaplicando os seus commits por cima (nível 6)
git push origin --delete <branch>     # apaga a branch no remoto
```

## 6. Exemplos reais

```console
$ git push
 ! [rejected]        main -> main (fetch first)
$ git fetch
$ git log --oneline main..origin/main
a1b2c3d changelog, enviado por outra pessoa
$ git merge origin/main
$ git push
```

Neste repositório, cada sessão de estudo começa com `git fetch origin`, `git switch estudo_<nome>` e `git merge origin/main` ([regra 1](../../docs/fluxo-git.md)). Um push recusado por refs `origin/*` velhas se resolve com um `fetch`, nunca com force push.

## 7. Cenários de uso

- Começar o dia sincronizado com o que o grupo enviou.
- Publicar uma branch nova para abrir um pull request (nível 8).
- Conferir se uma branch existe no remoto sem clonar (`git ls-remote`).

## 8. Erros comuns

- **Achar que `origin/main` é o GitHub ao vivo.** É a foto do último fetch.
- **`git pull` com mudanças não commitadas** e cair num conflito misturado com trabalho local.
- **Responder a um push recusado com `--force`.**
- **Esquecer o `-u` no primeiro push** e depois estranhar que `git push` sozinho não sabe para onde ir.

## 9. Riscos

- `git push --force` reescreve a branch no remoto e pode apagar commits de outras pessoas. Se um dia for inevitável numa branch **só sua**, use `--force-with-lease`, que recusa se o remoto mudou desde o seu fetch (nível 6). Neste repositório, nunca.
- Credenciais: autentique com SSH ou com o gerenciador de credenciais do Git, nunca com token escrito na URL do remoto (`git remote -v` mostraria o token).

## 10. Boas práticas

- `git fetch` no começo de cada sessão.
- `git pull --ff-only` como padrão (`git config --global pull.ff only`): se não der para avançar, você decide conscientemente como integrar.
- Envie com frequência, para não acumular divergência.
- Branch local com o mesmo nome da remota que ela acompanha.

## 11. Exercício básico

Sem rede: `git init --bare /tmp/remoto.git`, clone duas vezes (`/tmp/ana` e `/tmp/beto`). Ana commita e envia; Beto faz `fetch` e confere com `git log --oneline --all` que `origin/main` andou e a `main` dele não. Depois Beto integra.

## 12. Exercício intermediário

No mesmo arranjo, Ana e Beto commitam ao mesmo tempo; Ana envia primeiro. Explique, antes de rodar, o que acontece com o push de Beto e por quê. Depois resolva sem `--force`, com `fetch`, merge e push.

## 13. Exercício avançado

Laboratório, sem consulta: `N5-clonar-e-enviar` e `N5-sincronizar`.

## 14. Desafio aplicado ao repositório

1. Só leitura: `git remote -v`, `git branch -vv` e `git ls-remote origin 'refs/heads/estudo_*'`. Quantas branches de estudo existem no remoto? A sua está à frente ou atrás de `origin`?
2. Só leitura: compare `git rev-parse main` com `git rev-parse origin/main` antes e depois de um `git fetch`, e explique a diferença.
3. Na próxima sessão de estudo, faça você mesmo o começo da sessão da [regra 1](../../docs/fluxo-git.md), com `fetch`, `switch` e merge da `main`, lendo cada saída antes do comando seguinte.

## 15. Checklist de validação

- [ ] Explico a diferença entre `main`, `origin/main` e a `main` do GitHub.
- [ ] Uso `fetch` + `log A..B` para ver o que vem e o que vai.
- [ ] Resolvo um push recusado sem força.
- [ ] Publico uma branch nova com `push -u`.
- [ ] Os dois cenários do nível 5 passaram no `conferir`.

## 16. Critério de conclusão

`N5-clonar-e-enviar` e `N5-sincronizar` passam sem consulta. Com os níveis 1 a 4, fecham os 10 cenários do portão da NG1 (em pelo menos 3 dias distintos), mais a explicação oral do nível 4.

## 17. Próximo módulo

Fim da NG1. Na graduação, a [G5](../G5/README.md) começa pelo [nível 6 · Rebase e histórico avançado](../G5/6-rebase-e-historico.md).
