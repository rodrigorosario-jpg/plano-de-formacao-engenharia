# G5 · Git avançado e engenharia de versionamento: guias

Níveis 6 a 12 da [árvore de estudos de Git](../NG1/README.md). Disciplina: [G5](../../disciplinas/G5-git-avancado-e-engenharia-de-versionamento.md). Pré-requisitos: [NG1](../../disciplinas/NG1-git-essencial.md) (níveis 1 a 5) e G1 (Linux e shell).

| Nível | Guia | O que você passa a fazer |
| --- | --- | --- |
| 6 | [Rebase e histórico avançado](6-rebase-e-historico.md) | Limpar o histórico de uma branch sua antes do PR, sem afetar ninguém |
| 7 | [Recuperação e troubleshooting](7-recuperacao.md) | Recuperar o que parecia perdido e desfazer o que já foi enviado |
| 8 | [GitHub e colaboração](8-colaboracao-github.md) | Contribuir por fork e PR, revisar, versionar e publicar releases |
| 9 | [Segurança e governança](9-seguranca-e-governanca.md) | Proteger credenciais, a branch principal e a cadeia de dependências |
| 10 | [GitOps, automação e CI/CD](10-automacao-e-cicd.md) | Automatizar validação, release e implantação a partir do Git |
| 11 | [Internals e repositórios grandes](11-internals-e-escala.md) | Entender os objetos do Git e lidar com repositórios grandes |
| 12 | [Engenharia de versionamento](12-engenharia-de-versionamento.md) | Escolher e defender a estratégia de branching e de releases de uma equipe |

## Como a G5 é conferida

Os níveis 6 a 12 não têm laboratório por script: as situações são abertas demais para um `conferir`. Cada guia tem uma checklist, e o portão da G5 é um **projeto**: um repositório seu com ruleset, CI, releases versionadas e changelog, mais uma recuperação de histórico demonstrada ao vivo. O projeto é defendido numa explicação oral.

## Segurança dos exercícios

Os níveis 6 e 7 ensinam comandos que **reescrevem ou descartam** histórico (`rebase`, `commit --amend`, `reset --hard`, `push --force-with-lease`). Todos os exercícios e desafios deles rodam numa cópia descartável:

```bash
git clone ~/caminho/plano-de-estudos /tmp/pe-g5     # clone local; nada vai para o GitHub
cd /tmp/pe-g5
git remote remove origin                            # sem remoto, nenhum push acidental
```

Nunca na `main`, nunca na sua branch de estudo, e nunca com push para o GitHub deste repositório.
