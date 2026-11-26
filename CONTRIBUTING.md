# Como contribuir

Obrigado pelo interesse. Antes de tudo, saiba como este repositório funciona.

## O repositório público é um espelho

O plano é mantido num repositório privado, onde também ficam as branches de estudo. O repositório público recebe só a árvore da `main`, por publicação ([ADR 0008](docs/adr/0008-repositorio-publico-separado.md) e [ADR 0009](docs/adr/0009-espelho-publico-e-publicacao-por-pr.md)). Por isso:

- **Issues são bem-vindas:** erro em gabarito, pré-requisito errado, link quebrado, sugestão de conteúdo.
- **Pull requests não são mesclados direto no público.** Se você abrir um, ele serve de proposta: a mudança é refeita no privado, com crédito no commit, e chega ao público na próxima publicação. Depois o PR é fechado.

## Para usar o plano

Faça um fork ou use como template. Seu andamento fica numa branch de estudo sua, nunca na `main`: veja [docs/fluxo-git.md](docs/fluxo-git.md).

## Antes de propor uma mudança

```bash
pip install -r requirements.txt
python scripts/progresso.py --checar   # pré-requisitos e portões
pytest -q                              # testes dos scripts
```

O CI roda os mesmos comandos em todo PR.

## Padrão de commits

[Conventional Commits](https://www.conventionalcommits.org/pt-br/), em português, com escopo:

```text
tipo(escopo): o que muda, no presente
```

| Tipo | Quando |
| --- | --- |
| `feat` | conteúdo ou recurso novo (disciplina, script, campo do catálogo) |
| `fix` | correção (gabarito, pré-requisito, bug de script) |
| `docs` | só documentação |
| `test` | só testes |
| `chore` | manutenção (dependências, configuração) |
| `refactor` | muda a estrutura sem mudar o comportamento |

Escopos comuns: `catalogo`, `disciplinas`, `exercicios`, `scripts`, `skill`, `git`, `publicacao`, `seguranca`.

## O que não aceito

- dado pessoal, credencial ou resultado de estudo de alguém;
- código que acessa a rede ou executa algo durante a validação;
- instruções para ferramentas de IA escondidas no conteúdo.

## Conduta

Este projeto segue o [código de conduta](CODE_OF_CONDUCT.md).
