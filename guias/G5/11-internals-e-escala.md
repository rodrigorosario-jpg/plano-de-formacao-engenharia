# Nível 11 · Git avançado e arquitetura: internals e repositórios grandes

[G5](../../disciplinas/G5-git-avancado-e-engenharia-de-versionamento.md) · [guias da G5](README.md) · [árvore](../NG1/README.md)

## 1. Objetivo

Entender o Git como um banco de objetos endereçados por conteúdo, e usar esse modelo para explicar o comportamento dos comandos e para lidar com repositórios grandes: arquivos pesados, muitos projetos, histórico longo.

## 2. Conceitos

- **Objetos:** quatro tipos, guardados em `.git/objects`.
  - **Blob:** conteúdo de um arquivo.
  - **Tree:** uma pasta (nome, modo e hash de cada blob ou tree).
  - **Commit:** uma tree raiz, pai(s), autor, committer e mensagem.
  - **Tag anotada:** aponta para um objeto, com autor e mensagem.
- **SHA:** hash do conteúdo do objeto (SHA-1 por padrão; SHA-256 disponível). Mesmo conteúdo, mesmo hash: por isso arquivos iguais são guardados uma vez só.
- **Refs:** nomes que apontam para hashes (`refs/heads/main`, `refs/tags/v1.0`). HEAD é uma ref simbólica.
- **Packfiles:** muitos objetos comprimidos num arquivo, com deltas entre versões parecidas.
- **Garbage collection:** empacota objetos e remove os inalcançáveis vencidos.
- **Git LFS:** guarda arquivos grandes num servidor à parte; o repositório guarda um ponteiro.
- **Sparse checkout:** só parte das pastas no diretório de trabalho.
- **Clone parcial e raso:** `--filter=blob:none` baixa blobs sob demanda; `--depth` baixa só os últimos commits.
- **Submodules:** um repositório dentro de outro, fixado num commit.
- **Monorepo:** muitos projetos num repositório só.
- **Worktrees:** vários diretórios de trabalho ligados ao mesmo `.git`, cada um numa branch.

## 3. Explicação

Um commit não guarda diferenças; guarda uma tree completa. Isso parece caro, mas como blobs e trees idênticos têm o mesmo hash, um commit que muda um arquivo cria só um blob novo e as trees no caminho até ele. As diferenças que você vê no `git diff` são calculadas na hora, comparando trees. Os deltas existem, mas só como compressão dentro dos packfiles.

Esse modelo explica o resto da árvore: uma branch é um arquivo com um hash (nível 3); um rebase cria commits novos porque o pai muda e, com ele, o hash (nível 6); o reflog recupera commits porque os objetos ainda estão lá até o gc (nível 7); e um segredo commitado persiste porque o blob continua alcançável pelo histórico (nível 9).

Repositório grande tem três formas de dor, com remédios diferentes:

| Dor | Remédio |
| --- | --- |
| Arquivos binários grandes que mudam | Git LFS, ou não versionar (artefatos fora do Git) |
| Muitos arquivos ou projetos, você só usa uma parte | Sparse checkout com clone parcial |
| Histórico enorme | Clone parcial (`--filter=blob:none`) ou raso, só na CI |

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `git cat-file -t/-p <obj>` | Tipo e conteúdo de um objeto |
| `git rev-parse <ref>` | Resolve um nome para hash |
| `git hash-object <arq>` | Calcula o hash que um arquivo teria |
| `git ls-tree <tree-ish>` | Lista uma tree |
| `git count-objects -vH` | Tamanho do repositório |
| `git gc` | Empacota e limpa |
| `git worktree add/list/remove` | Diretórios de trabalho extras |
| `git sparse-checkout set <pastas>` | Restringe a pasta de trabalho |
| `git submodule add/update --init` | Repositórios aninhados |
| `git lfs track "<padrão>"` | Passa um tipo de arquivo para o LFS |

## 5. Sintaxe

```text
git cat-file -p HEAD                 # o objeto commit: tree, parent, author, mensagem
git cat-file -p HEAD^{tree}          # a tree raiz
git rev-parse HEAD~2 main@{yesterday} :/texto
git clone --filter=blob:none --sparse <url> && git sparse-checkout set disciplinas docs
git worktree add ../pe-revisao origin/main    # outra branch, outra pasta, mesmo repositório
git worktree remove ../pe-revisao
git submodule update --init --recursive
```

## 6. Exemplos reais

```console
$ git cat-file -p HEAD
tree 4b825dc...
parent 2d834a5...
author rodrigorosario-jpg <...@users.noreply.github.com> ...
$ echo 'olá' | git hash-object --stdin       # o mesmo hash em qualquer máquina
```

Trabalho em paralelo com worktrees: `git worktree add ../pe-ci ci/ajuste` e `git worktree add ../pe-docs docs/guia` deixam duas frentes abertas em duas pastas, cada uma na sua branch, sem clonar de novo.

## 7. Cenários de uso

- Revisar um PR numa worktree sem largar o que você estava fazendo.
- Clonar só a pasta do serviço que você mantém num monorepo.
- Versionar modelos ou datasets grandes com LFS, ou decidir não versioná-los.
- Explicar a um colega por que o rebase mudou os hashes.

## 8. Erros comuns

- **Commitar binários grandes** sem LFS: o repositório cresce para sempre, mesmo que você apague o arquivo depois.
- **Submodule em estado "detached"** e commits perdidos dentro dele.
- **Apagar a pasta de uma worktree na mão** em vez de `git worktree remove` (resolva com `git worktree prune`).
- **`git gc --prune=now` em repositório com algo a recuperar.**

## 9. Riscos

- `git gc --prune=now` e `git reflog expire --expire=now --all` destroem a rede de segurança do nível 7.
- Submodules apontam para outro repositório: se ele sumir ou for reescrito, o seu deixa de clonar.
- Monorepo sem CODEOWNERS e sem CI por caminho vira um gargalo de revisão.

## 10. Boas práticas

- Artefatos de build e dados grandes fora do Git.
- LFS decidido antes do primeiro binário, não depois.
- Worktrees para trabalho paralelo; `git worktree list` para não esquecer nenhuma.
- Prefira gerenciador de pacotes a submodule, quando der.

## 11. Exercício básico

Num repositório de brinquedo com dois commits, percorra só com `cat-file -p`: do commit à tree, da tree a um blob, e do commit ao pai. Desenhe o grafo de objetos.

## 12. Exercício intermediário

Prove, com `hash-object` e `count-objects`, que dois arquivos de conteúdo idêntico em pastas diferentes ocupam um blob só. Depois faça um rebase e mostre, com `cat-file`, que os commits novos apontam para as **mesmas trees** dos antigos quando não houve conflito.

## 13. Exercício avançado

Monte um mini-monorepo com três projetos e um CODEOWNERS. Clone com `--filter=blob:none --sparse`, trabalhe só num projeto, e compare tamanho e tempo com um clone completo. Use uma worktree para revisar uma segunda branch em paralelo.

## 14. Desafio aplicado ao repositório

Só leitura, no seu clone:

1. `git count-objects -vH`: quanto o repositório ocupa? Qual pasta tem mais arquivos (`git ls-tree -r --name-only HEAD | cut -d/ -f1 | sort | uniq -c`)?
2. Ache o blob de `plano.yml` no commit atual com `git rev-parse HEAD:plano.yml` e mostre com `cat-file -p`.
3. Crie uma worktree de `origin/main` em `/tmp/pe-main`, compare com a sua branch de estudo com `diff -r --brief` e remova a worktree com `git worktree remove`.

## 15. Checklist de validação

- [ ] Explico os quatro tipos de objeto e como se ligam.
- [ ] Navego no banco de objetos com `cat-file` e `rev-parse`.
- [ ] Explico por que commit guarda retratos e mesmo assim o repositório é pequeno.
- [ ] Escolho entre LFS, sparse checkout e clone parcial para cada dor.
- [ ] Uso worktrees e sei removê-las.

## 16. Critério de conclusão

O exercício intermediário está feito e explicado por escrito, e o desafio do repositório foi concluído com a worktree removida.

## 17. Próximo módulo

[Nível 12 · Engenharia de versionamento](12-engenharia-de-versionamento.md).
