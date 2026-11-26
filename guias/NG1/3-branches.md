# Nível 3 · Branches

[NG1](../../disciplinas/NG1-git-essencial.md) · competência NG1.c04 · [árvore](README.md)

## 1. Objetivo

Criar, trocar, listar e apagar branches com segurança, e saber escolher o tipo de branch para cada trabalho.

## 2. Conceitos

- **Branch:** um ponteiro para um commit. Criar uma branch é barato: o Git escreve um arquivo de 41 bytes.
- **Branch principal:** a de onde sai o que está "pronto" (`main`). Neste repositório, a `main` é o currículo limpo e reutilizável.
- **Branch de feature:** um trabalho novo, com começo e fim (`feature/rodape`, `curriculo/git`).
- **Branch de correção:** conserta algo que já está na principal (`fix/...`, `hotfix/...`).
- **Branch de release:** estabiliza uma versão enquanto a principal segue (nível 12).
- **Branch temporária:** experimento descartável.
- **Branch de longa duração:** vive em paralelo à principal por muito tempo, como a sua `estudo_<nome>`.
- **Estratégia de branching:** a regra combinada de quais branches existem e como o trabalho volta à principal (nível 12).
- **Ciclo de vida:** criar a partir da principal → commits → integrar (nível 4) → apagar.

## 3. Explicação

Quando você faz um commit, a branch em que HEAD está avança para ele; as outras ficam paradas. Por isso duas branches que saem do mesmo commit podem receber trabalhos diferentes sem um ver o outro, até o merge.

Trocar de branch (`git switch`) faz três coisas: move HEAD, atualiza o staging e reescreve o diretório de trabalho para o retrato daquela branch. Se você tem mudanças não commitadas que entrariam em conflito com isso, o Git recusa a troca. Ele está protegendo o seu trabalho: commite, guarde com `git stash` (nível 7) ou descarte antes.

Apagar uma branch apaga só o nome. Os commits continuam lá. `git branch -d` só apaga se os commits já estiverem integrados em outra branch; `-D` apaga mesmo assim, e os commits ficam órfãos (recuperáveis pelo reflog por um tempo, nível 7).

Este repositório usa branches de longa duração por estudante: o andamento vive em `estudo_<nome>` e nunca é mesclado na `main`. Isso mantém a `main` reutilizável por outras pessoas ([fluxo de git](../../docs/fluxo-git.md), [ADR 0006](../../docs/adr/0006-fluxo-de-git.md)).

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `git branch` | Lista as branches locais (`*` marca a atual) |
| `git branch <nome>` | Cria, sem trocar |
| `git switch <nome>` | Troca de branch |
| `git switch -c <nome>` | Cria e troca |
| `git checkout <nome>` | Forma antiga de trocar (também restaura arquivos; prefira `switch` e `restore`) |
| `git branch -d <nome>` | Apaga se já integrada |
| `git branch -D <nome>` | Apaga mesmo sem integrar |

## 5. Sintaxe

```text
git switch -c <nova> <ponto-de-partida>    # cria a partir de outra branch ou commit
git branch -v                              # último commit de cada branch
git branch --merged main                   # já integradas na main (seguras para -d)
git branch --no-merged main                # com trabalho que a main não tem
git branch -m <velho> <novo>               # renomeia
git switch -                               # volta para a branch anterior
```

## 6. Exemplos reais

```console
$ git switch -c curriculo/git origin/main
Switched to a new branch 'curriculo/git'
$ git branch --no-merged main
  curriculo/git
$ git branch -d curriculo/git
error: the branch 'curriculo/git' is not fully merged.
```

O erro é proteção, não falha: a branch tem commits que a `main` não tem.

## 7. Cenários de uso

- Começar um trabalho sem quebrar o que já funciona na `main`.
- Interromper um trabalho para corrigir algo urgente: commite na branch atual, `git switch main`, `git switch -c fix/...`.
- Testar uma ideia maluca numa branch temporária e apagá-la com `-D` se não der certo.

## 8. Erros comuns

- **Commitar na branch errada.** Olhe a primeira linha do `git status`, ou ponha a branch no prompt do terminal.
- **Criar a branch a partir de outra feature, sem querer**, em vez da `main` atualizada. Use `git switch -c nova origin/main` depois de um `git fetch`.
- **Usar `-D` por hábito** e perder trabalho não integrado.
- **Nomes vagos** (`teste2`, `nova`): ninguém sabe o que a branch faz.

## 9. Riscos

- `git branch -D` descarta o nome de commits não integrados. Antes, rode `git log main..<branch>` para ver o que se perderia.
- `git checkout <arquivo>` (sem branch) descarta mudanças: é um dos motivos para usar `switch` e `restore`, que separam as duas funções.

## 10. Boas práticas

- Branch curta, com um objetivo; apague depois de integrar.
- Prefixos combinados: `feature/`, `fix/`, `docs/`, ou os deste repositório (`core/`, `curriculo/`).
- Sempre parta da principal atualizada.
- Branch de estudo é só sua: nunca grave na de outra pessoa.

## 11. Exercício básico

Num repositório de brinquedo: crie `exp` a partir da `main`, faça dois commits nela, volte para a `main` e confirme com `ls` e `git log --oneline --all --graph` que os arquivos da `exp` "sumiram" da pasta, mas não do repositório.

## 12. Exercício intermediário

Você está na `main` com `notas.txt` modificado e não commitado, e `git switch exp` responde *"Your local changes would be overwritten"*. Explique por que o Git recusou e liste três saídas, dizendo o que cada uma faz com a sua mudança.

## 13. Exercício avançado

Laboratório, sem consulta: `N3-criar-branch` e `N3-limpar-branches`.

## 14. Desafio aplicado ao repositório

1. Só leitura: `git branch -r` e `git log --oneline origin/main..origin/estudo_<nome>`. O que a sua branch de estudo tem que a `main` não tem? Por que isso nunca deve ir para a `main`?
2. Numa cópia descartável (`git clone <repo> /tmp/pe-treino`): crie `curriculo/minha-anotacao` a partir de `origin/main`, acrescente uma linha em `## Anotações` da NG1, commite, volte para a `main` e apague a branch. Precisou de `-d` ou `-D`? Por quê?

## 15. Checklist de validação

- [ ] Explico por que criar branch é barato.
- [ ] Sei o que `switch` faz com HEAD, staging e pasta.
- [ ] Uso `--merged` e `--no-merged` antes de apagar.
- [ ] Explico a branch de estudo deste repositório e por que ela não vai para a `main`.
- [ ] Os dois cenários do nível 3 passaram no `conferir`.

## 16. Critério de conclusão

`N3-criar-branch` e `N3-limpar-branches` passam sem consulta, e o exercício intermediário está respondido por escrito.

## 17. Próximo módulo

[Nível 4 · Merge e conflitos](4-merge-e-conflitos.md): juntar o trabalho de duas branches.
