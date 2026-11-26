# Nível 4 · Merge e conflitos

[NG1](../../disciplinas/NG1-git-essencial.md) · competência NG1.c05 · [árvore](README.md)

## 1. Objetivo

Integrar uma branch em outra, prever se o merge será fast-forward ou com commit de merge, e resolver conflitos sem perder o trabalho de nenhum dos lados.

## 2. Conceitos

- **Merge:** junta o histórico de outra branch na branch atual.
- **Fast-forward:** se a branch atual não andou desde que a outra saiu dela, o Git só avança o ponteiro. Nenhum commit novo.
- **Three-way merge:** se as duas andaram, o Git compara três versões: a base comum (o ancestral mais recente das duas) e as duas pontas. O resultado vira um **commit de merge**, com dois pais.
- **Conflito:** as duas pontas mudaram o mesmo trecho de formas diferentes em relação à base. O Git não adivinha qual vale; ele para e pede para você decidir.
- **Marcadores de conflito:** `<<<<<<<`, `=======` e `>>>>>>>` delimitam as duas versões no arquivo.
- **Merge abortado:** `git merge --abort` volta ao estado de antes do merge.
- **Estratégias:** a padrão (`ort`) resolve quase tudo; opções como `-X ours`/`-X theirs` escolhem um lado automaticamente nos trechos em conflito. `--no-ff` força commit de merge; `--ff-only` recusa se não der para avançar.

## 3. Explicação

Antes de mesclar, pergunte: a minha branch tem commits que a outra não tem? `git log --oneline main..correcao` mostra o que vem; `git log --oneline correcao..main` mostra o que a main tem a mais. Se o segundo é vazio, o merge será fast-forward.

Um conflito não é um erro; é o Git sendo honesto. Ao parar, ele deixa o repositório num estado intermediário: os arquivos sem conflito já estão no staging, os com conflito estão marcados como "both modified". Seu trabalho é:

1. Abrir cada arquivo em conflito e decidir o resultado, que pode ser um lado, o outro ou uma combinação nova.
2. Apagar todos os marcadores.
3. `git add` em cada arquivo resolvido (isso diz ao Git "resolvido").
4. `git commit` (ou `git merge --continue`) para criar o commit de merge.

Se ficar perdido no meio, `git merge --abort` desfaz tudo e você recomeça com calma.

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `git merge <branch>` | Integra a branch na atual |
| `git merge --abort` | Desiste do merge em andamento |
| `git merge --continue` | Conclui depois de resolver |
| `git mergetool` | Abre uma ferramenta visual configurada para resolver |
| `git diff` (durante o conflito) | Mostra só os trechos em conflito |
| `git log --merge` | Commits dos dois lados que tocam os arquivos em conflito |

## 5. Sintaxe

```text
git merge --ff-only <branch>     # só se for fast-forward; senão, recusa
git merge --no-ff <branch>       # sempre cria commit de merge
git merge -X theirs <branch>     # nos trechos em conflito, fica com o lado de <branch>
git checkout --ours <arq>        # durante o conflito: pega a versão da branch atual
git checkout --theirs <arq>      # durante o conflito: pega a versão da que entra
git config merge.conflictstyle zdiff3   # mostra também a versão da base
```

## 6. Exemplos reais

```text
<<<<<<< HEAD
# Projeto do grupo
=======
# Projeto Final de Algoritmos
>>>>>>> titulo
```

Com `conflictstyle zdiff3`, aparece também `||||||| base` com o texto original, e fica claro o que cada lado mudou.

Neste repositório, os conflitos entre os PRs #13 a #15 em `docs/arquitetura/debitos.md` foram resolvidos juntando as linhas dos dois lados e tirando as duplicadas: a resolução certa raramente é "um lado inteiro".

O fluxo de git define uma regra de resolução para um caso específico: ao trazer a `main` para a branch de estudo, em `registro/`, `PROGRESSO.md` e `MAPA.md` fica a versão da branch de estudo ([regra 5](../../docs/fluxo-git.md)).

## 7. Cenários de uso

- Integrar uma feature terminada na principal.
- Trazer a principal atualizada para dentro da sua branch longa (como a de estudo), para não divergir demais.
- Dois colegas mexeram no mesmo arquivo do trabalho em grupo.

## 8. Erros comuns

- **Commitar com marcadores no arquivo.** Procure com `git diff --check` ou `grep -n '<<<<<<<'` antes do commit.
- **Resolver escolhendo um lado inteiro sem ler** e apagar o trabalho do colega.
- **Mesclar na direção errada** (a `main` dentro da feature quando queria o contrário). O merge entra na branch **atual**.
- **Entrar em pânico e apagar a pasta.** `git merge --abort` existe para isso.

## 9. Riscos

- `-X ours` e `-X theirs` descartam silenciosamente as mudanças do outro lado nos trechos em conflito.
- Um merge mal resolvido e já enviado não se desfaz apagando: use `git revert -m 1 <merge>` (nível 7).

## 10. Boas práticas

- Mescle cedo e com frequência: conflitos pequenos são fáceis.
- Rode os testes depois de resolver, antes do commit de merge: um merge sem conflito textual ainda pode quebrar o código.
- Ligue `merge.conflictstyle zdiff3`.
- Uma branch, um assunto: menos sobreposição, menos conflito.

## 11. Exercício básico

Monte os dois casos num repositório de brinquedo: um merge fast-forward (a `main` parada) e um three-way sem conflito (cada branch muda um arquivo diferente). Desenhe o grafo antes e confira com `git log --oneline --graph --all`.

## 12. Exercício intermediário

Provoque um conflito: as duas branches mudam a mesma linha. Antes de resolver, responda: qual é a base comum (`git merge-base main outra`)? O que cada lado mudou em relação a ela? Depois aborte com `--abort`, confira que tudo voltou, e refaça o merge resolvendo.

## 13. Exercício avançado

Laboratório, sem consulta: `N4-fast-forward` e `N4-conflito`. O portão da NG1 pede também uma **explicação oral** de um merge com conflito: base, os dois lados, por que o Git parou e como você decidiu.

## 14. Desafio aplicado ao repositório

1. Só leitura: `git log --merges --oneline -10` e `git show --stat <um-merge>`. Os merges têm dois pais (`git log -1 --format=%P <merge>`). Qual pai é a `main` e qual é a branch do PR?
2. Numa cópia descartável: crie duas branches a partir de `origin/main` que mudam a mesma linha de `README.md`, mescle as duas na `main` local, resolva o conflito e rode `python scripts/progresso.py --checar` antes do commit de merge.

> Na versão pública deste repositório o histórico tem um commit por publicação. Se for o seu caso, faça este desafio num projeto seu com histórico (veja [desafios que leem histórico](README.md#desafios-que-leem-histórico)).

## 15. Checklist de validação

- [ ] Prevejo se um merge será fast-forward antes de rodar.
- [ ] Explico base comum e three-way merge.
- [ ] Resolvo um conflito, removo os marcadores e concluo o merge.
- [ ] Sei abortar um merge em andamento.
- [ ] Os dois cenários do nível 4 passaram no `conferir`.

## 16. Critério de conclusão

`N4-fast-forward` e `N4-conflito` passam sem consulta, e a explicação oral de um merge com conflito foi feita.

## 17. Próximo módulo

[Nível 5 · Git remoto](5-remoto.md): trabalhar com o GitHub e com outras pessoas.
