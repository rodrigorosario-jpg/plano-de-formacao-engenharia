# Nível 8 · GitHub e colaboração profissional

[G5](../../disciplinas/G5-git-avancado-e-engenharia-de-versionamento.md) · [guias da G5](README.md) · [árvore](../NG1/README.md)

## 1. Objetivo

Colaborar como numa equipe profissional ou num projeto open source: fork, pull request, revisão, issues, mensagens padronizadas, versões semânticas e releases.

## 2. Conceitos

- **Fork:** sua cópia de um repositório de outra pessoa, para propor mudanças sem acesso de escrita ao original.
- **Pull request (PR):** pedido para integrar uma branch em outra, com diff, discussão, revisão e checks automáticos.
- **Review:** comentários linha a linha e um veredito (aprovar, comentar, pedir mudanças).
- **Issues:** registro de bugs, tarefas e propostas. **Discussions:** conversa aberta, sem ser tarefa.
- **Projects:** quadros que organizam issues e PRs.
- **Tag:** nome fixo para um commit. **Release:** uma tag publicada no GitHub, com notas e artefatos.
- **CODEOWNERS:** quem revisa cada caminho; o GitHub pede a revisão automaticamente.
- **Templates:** modelos de issue e de PR em `.github/`.
- **Conventional Commits:** `tipo(escopo): resumo`, com tipos como `feat`, `fix`, `docs`, `chore`, `refactor`, `test`; `!` ou `BREAKING CHANGE:` marcam quebra de compatibilidade.
- **SemVer:** `MAIOR.MENOR.CORREÇÃO`. Quebra de compatibilidade sobe a maior; funcionalidade nova compatível, a menor; correção, a última.
- **Open source:** licença, código de conduta, guia de contribuição e política de segurança dizem a quem chega como participar.

## 3. Explicação

O PR é a unidade de colaboração: uma branch, um assunto, uma descrição que diz **o quê e por quê**, checks automáticos e uma revisão. PR pequeno é revisado de verdade; PR de 2 000 linhas recebe "LGTM".

Revisar é ler com uma pergunta: isto faz o que diz, sem quebrar o resto, e alguém entende daqui a um ano? Comente sobre o código, não sobre a pessoa, e diferencie o bloqueante ("isto apaga o arquivo do usuário") do gosto ("eu nomearia diferente, sem bloquear").

Mensagens no padrão Conventional Commits permitem gerar changelog e decidir a próxima versão SemVer automaticamente (níveis 10 e 12): `feat` sobe a menor, `fix` a correção, `!` a maior.

Fluxo de contribuição por fork:

```text
fork → clone do fork → git remote add upstream <original> → branch → commits → push no fork → PR para o original
          ↑                                                                                  |
          └──── git fetch upstream && git merge upstream/main (manter atualizado) ←──────────┘
```

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `git remote add upstream <url>` | Liga o fork ao original |
| `git fetch upstream` | Atualiza a cópia do original |
| `git tag -a v1.2.0 -m "..."` | Cria uma tag anotada |
| `git push origin v1.2.0` | Envia a tag |
| `git describe --tags` | Diz a tag mais próxima do commit atual |
| `gh pr create`, `gh pr checkout <n>`, `gh pr review` | PRs pela linha de comando (GitHub CLI) |
| `gh release create v1.2.0 --notes-file NOTAS.md` | Publica uma release |

## 5. Sintaxe

```text
feat(laboratorio): cenário de rebase interativo
fix(publicacao): recusa e-mail que não seja noreply
docs(guias): nível 8 da árvore de Git
refactor(progresso)!: estado passa a viver em registro/estado.yml

BREAKING CHANGE: branches antigas precisam da migração única.
```

```text
.github/CODEOWNERS            * @dono          /scripts/ @dono @revisor
.github/pull_request_template.md
.github/ISSUE_TEMPLATE/*.yml
```

## 6. Exemplos reais

- Este repositório integra estrutura na `main` só por PR, e cada PR diz o que muda e o que foi conferido (`pytest`, `--checar`).
- Pré-lançamento em SemVer: `1.0.0-rc.1` < `1.0.0`. A versão `0.y.z` diz "API instável, pode quebrar a qualquer hora".
- `git describe --tags` em `v1.2.0-5-g1a2b3c4` quer dizer: 5 commits depois da `v1.2.0`, no commit `1a2b3c4`.

## 7. Cenários de uso

- Corrigir um erro de digitação num projeto open source que você usa.
- Trabalho em grupo da faculdade com a `main` protegida e PRs revisados pelo colega.
- Publicar a versão 1.0 de uma biblioteca com notas de release.

## 8. Erros comuns

- **PR que mistura assuntos** (refatoração + funcionalidade + formatação).
- **Descrição vazia** ou "ver commits".
- **Trabalhar na `main` do fork:** o fork diverge do original e todo PR leva lixo. Uma branch por PR.
- **Tag leve para release:** sem autor, data nem mensagem. Use `-a`.
- **Mudar a tag de uma versão já publicada.** Uma versão publicada é imutável; corrija com uma versão nova.

## 9. Riscos

- PRs de forks executam workflows do seu repositório (nível 10): o GitHub limita os segredos, mas `pull_request_target` mal usado dá ao código do fork acesso de escrita.
- Revisão que só aprova sem ler dá uma falsa sensação de controle.
- Apagar ou mover tag publicada quebra quem fixou aquela versão.

## 10. Boas práticas

- PR pequeno, com descrição e checks verdes antes de pedir revisão.
- Conventional Commits nas mensagens, ou pelo menos no título do PR (quando o merge é squash).
- SemVer desde a primeira release; changelog por versão.
- `CONTRIBUTING`, `SECURITY`, código de conduta e licença em todo projeto aberto.

## 11. Exercício básico

Crie um repositório de treino no GitHub. Abra uma issue, crie uma branch que a resolva, abra um PR com `Closes #1` na descrição e mescle. Confira que a issue fechou sozinha.

## 12. Exercício intermediário

Escreva cinco mensagens de commit no padrão Conventional Commits para mudanças reais do seu histórico e diga, para uma sequência delas desde a `v1.3.2`, qual seria a próxima versão SemVer e por quê.

## 13. Exercício avançado

Contribua com um projeto open source de verdade, mesmo que com uma correção de documentação: fork, `upstream`, branch, PR seguindo o `CONTRIBUTING` do projeto, e resposta a pelo menos um comentário de revisão.

## 14. Desafio aplicado ao repositório

Só leitura e escrita fora deste repositório:

1. Leia os PRs mesclados deste repositório (`gh pr list --state merged --limit 10`) e classifique os títulos por tipo Conventional Commits. Algum não segue o padrão?
2. Proponha, por escrito, as releases que este repositório teria tido se usasse SemVer desde o PR #5: quais PRs seriam `MENOR` e quais `MAIOR`? (A migração do estado para `registro/estado.yml` quebrou branches antigas: que parte do SemVer isso aciona?)

> Na versão pública deste repositório o histórico tem um commit por publicação. Se for o seu caso, faça este desafio num projeto seu com histórico (veja [desafios que leem histórico](../NG1/README.md#desafios-que-leem-histórico)).

## 15. Checklist de validação

- [ ] Contribuo por fork mantendo `upstream` atualizado.
- [ ] Escrevo PRs pequenos com descrição útil.
- [ ] Faço revisão diferenciando bloqueante de sugestão.
- [ ] Escrevo mensagens em Conventional Commits.
- [ ] Decido a próxima versão SemVer a partir das mudanças.
- [ ] Crio tag anotada e release com notas.

## 16. Critério de conclusão

Um PR seu foi aceito, ou está em revisão com comentários respondidos, num projeto que não é seu, e o exercício intermediário está respondido.

## 17. Próximo módulo

[Nível 9 · Segurança e governança](9-seguranca-e-governanca.md) e [nível 10 · Automação e CI/CD](10-automacao-e-cicd.md), em qualquer ordem.
