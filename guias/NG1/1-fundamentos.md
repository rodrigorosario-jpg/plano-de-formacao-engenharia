# Nível 1 · Fundamentos do Git

[NG1](../../disciplinas/NG1-git-essencial.md) · competência NG1.c01 · [árvore](README.md)

## Diagnóstico

Responda sem consultar, por escrito, antes de ler o resto. Se acertar as cinco, faça só os exercícios avançados deste nível e siga para o nível 2.

1. Qual a diferença entre Git e GitHub?
2. Depois de `git add a.txt`, o arquivo já está no histórico?
3. O que `HEAD` aponta logo depois de um commit na `main`?
4. Se você apagar a pasta do projeto no seu computador, o que acontece com o repositório no GitHub? E o contrário?
5. O que `git status` mostra que `git log` não mostra?

## 1. Objetivo

Entender as três áreas do Git (diretório de trabalho, staging e repositório), criar commits que contam uma história clara e ler o que o Git está dizendo em `git status`.

## 2. Conceitos

- **Sistema de controle de versão:** guarda versões sucessivas de um conjunto de arquivos e permite comparar, voltar e trabalhar em paralelo.
- **Versionamento distribuído:** cada clone tem o histórico inteiro. Não existe "o servidor" para o Git; o GitHub é um clone a mais, combinado como ponto de encontro.
- **Git x GitHub:** Git é o programa que versiona, e roda sem internet. GitHub é um serviço que hospeda repositórios Git e acrescenta pull requests, issues, Actions e permissões.
- **Repositório:** a pasta `.git`, com todos os commits, branches e configurações.
- **Diretório de trabalho:** os arquivos que você vê e edita.
- **Staging (índice):** o rascunho do próximo commit. Você escolhe o que entra.
- **Commit:** um retrato completo do projeto, com autor, data, mensagem e o commit anterior (pai). É identificado por um hash (SHA).
- **HEAD:** "onde você está". Normalmente aponta para uma branch, que aponta para um commit.
- **Branch:** um nome móvel que aponta para um commit e avança a cada commit novo.
- **Histórico:** a cadeia de commits ligados pelos pais.

## 3. Explicação

Pense em três caixas. Você edita na primeira (diretório de trabalho). `git add` copia a versão atual de um arquivo para a segunda (staging). `git commit` transforma o conteúdo do staging num retrato permanente, na terceira (repositório), e move a branch atual para ele.

Por que existe o staging? Para separar o que você fez do que você quer registrar. Numa tarde você corrige um bug e começa um rascunho; o staging deixa você commitar só a correção, com uma mensagem que diz exatamente isso. Um histórico de commits pequenos e coerentes é o que permite, meses depois, achar quando um bug entrou e desfazer só aquilo.

`git status` é o painel: diz em que branch você está, o que está no staging ("Changes to be committed"), o que mudou e não está no staging ("Changes not staged") e o que o Git não rastreia ("Untracked"). Leia antes de cada `add` e de cada `commit`.

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `git init` | Transforma a pasta atual num repositório (cria `.git`) |
| `git clone <url> [pasta]` | Copia um repositório existente, com todo o histórico |
| `git status` | Mostra o estado das três áreas |
| `git add <arquivo>` | Põe a versão atual do arquivo no staging |
| `git commit -m "mensagem"` | Registra o staging como um commit |
| `git log` | Lista os commits a partir de HEAD |
| `git diff` | Diferença entre diretório de trabalho e staging |
| `git show [commit]` | Mostra um commit: metadados e o que mudou |

## 5. Sintaxe

```text
git add <caminho>...            # um ou mais arquivos ou pastas
git add -p                      # escolhe trecho a trecho (patch)
git commit -m "<resumo>"        # resumo no imperativo, até ~60 caracteres
git commit                      # abre o editor para resumo + corpo
git log --oneline --graph -n 10 # 10 commits, uma linha cada, com o grafo
git show HEAD                   # o último commit
git show HEAD~1                 # o anterior ("um pai atrás")
```

Configuração única, antes do primeiro commit:

```bash
git config --global user.name "seu-usuario"
git config --global user.email "seu-usuario@users.noreply.github.com"   # e-mail privado do GitHub
```

## 6. Exemplos reais

```console
$ git status
On branch main
Changes to be committed:
        modified:   README.md
Changes not staged for commit:
        modified:   notas.txt
Untracked files:
        rascunho.md
```

Leitura: o próximo commit leva só `README.md`. `notas.txt` mudou, mas a mudança não vai junto. `rascunho.md` o Git nem conhece.

Neste repositório, `git log --oneline -5` mostra mensagens no padrão `tipo(escopo): resumo`, como `docs: ...` e `fix(seguranca): ...`, o Conventional Commits do nível 8.

## 7. Cenários de uso

- Começar a versionar um trabalho da faculdade que hoje vive em `final_v3_agora_vai.docx`.
- Clonar um projeto de um colega para rodar na sua máquina.
- Antes de pedir ajuda, mandar o `git status` e o `git log --oneline -5`: quem ajuda entende o estado em segundos.

## 8. Erros comuns

- **Commitar tudo com `git add .`** e levar junto `.env`, caches ou o rascunho. Use `git status` antes e um `.gitignore`.
- **Mensagem "update" ou "ajustes":** daqui a um mês ela não diz nada. Diga o que muda e por quê.
- **Rodar `git init` dentro de outro repositório.** Isso cria um repositório aninhado; `git status` na pasta de cima passa a mostrar a pasta como um bloco estranho.
- **Achar que `git add` salva.** Só o commit registra no histórico.

## 9. Riscos

- **Segredo commitado fica no histórico** mesmo que você apague o arquivo no commit seguinte. Se uma senha ou token entrar num commit enviado, considere o segredo vazado: revogue e gere outro (nível 9).
- **E-mail pessoal:** o e-mail do `user.email` vai em cada commit e fica público junto com o repositório. Use o noreply do GitHub.

## 10. Boas práticas

- Um commit, uma ideia. Se a mensagem precisa de "e", talvez sejam dois commits.
- `git status` antes de `add`, `git diff --staged` antes de `commit`.
- `.gitignore` desde o primeiro commit (veja o deste repositório).
- Resumo no imperativo: "corrige o cálculo do desconto", não "corrigido" nem "corrigindo".

## 11. Exercício básico

Numa pasta nova fora de qualquer repositório: `git init`, crie `a.txt`, faça o primeiro commit. Edite `a.txt` e crie `b.txt`. Antes de cada comando, escreva o que espera que `git status` mostre; depois confira. Faça um commit só com `a.txt`.

## 12. Exercício intermediário

Você recebe este `git status`:

```text
Changes to be committed:   new file: config.env
Changes not staged:        modified: app.py
```

Explique em três frases o que um `git commit -m "app"` faria, por que isso é um problema e o que você faria antes de commitar. (Pista: o nível 2 tem o comando para tirar do staging.)

## 13. Exercício avançado

Laboratório, sem consulta: `N1-primeiro-commit` e `N1-staging-parcial`.

## 14. Desafio aplicado ao repositório

Só leitura, no repositório verdadeiro:

1. `git log --oneline --graph -n 20`: quantos commits de merge aparecem? Como você os reconheceu?
2. Escolha um commit `docs:` e rode `git show <sha> --stat`. Quais arquivos mudaram?
3. Leia o `.gitignore` e escreva, para três linhas dele, o que aconteceria se elas não existissem.

> Na versão pública deste repositório o histórico tem um commit por publicação. Se for o seu caso, faça este desafio num projeto seu com histórico (veja [desafios que leem histórico](README.md#desafios-que-leem-histórico)).

## 15. Checklist de validação

- [ ] Explico diretório de trabalho, staging e repositório sem olhar.
- [ ] Prevejo a saída de `git status` antes de rodar.
- [ ] Faço um commit com só parte das mudanças.
- [ ] Minha identidade do git usa o e-mail noreply.
- [ ] Os dois cenários do nível 1 passaram no `conferir`.

## 16. Critério de conclusão

Os dois cenários do nível 1 passam no `conferir` sem consulta, e o exercício intermediário está respondido por escrito.

## 17. Próximo módulo

[Nível 2 · Arquivos e histórico](2-arquivos-e-historico.md): remover, renomear, desfazer e ler o passado.
