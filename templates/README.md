# Modelos

Modelos para criar arquivos novos no formato que o repositório já usa. Cada um copia a estrutura de um arquivo real; os trechos entre `<` e `>` são marcadores que explicam o que escrever ali.

| Modelo | Quando usar | Copie para | Arquivo real de referência |
| --- | --- | --- | --- |
| [disciplina.md](disciplina.md) | Disciplina nova da graduação ou da pós-formatura | `disciplinas/<código>-<nome>.md` | [S4](../disciplinas/S4-arquitetura-de-software.md) |
| [modulo-nivelamento.md](modulo-nivelamento.md) | Módulo novo do nivelamento (NM, NF ou NL) | `disciplinas/<código>-<nome>.md` | [NM1](../disciplinas/NM1-numeros-inteiros-e-operacoes.md) |
| [lista.md](lista.md) | Lista de exercícios de um módulo ou disciplina | `exercicios/<código>/<n>-<nome>.md` | [NM0, lista 5](../exercicios/NM0/5-ancoras.md) |
| [gabarito.md](gabarito.md) | Gabarito de uma lista, sempre junto com ela | `exercicios/<código>/gabaritos/<n>-<nome>.md` | [gabarito da lista 5](../exercicios/NM0/gabaritos/5-ancoras.md) |
| [verificacao.yml](verificacao.yml) | Como conferir cada item da lista, sempre junto com ela | `exercicios/<código>/verificacao/<n>-<nome>.yml` | [verificação da lista 5](../exercicios/NM0/verificacao/5-ancoras.yml) |
| [conceito.md](conceito.md) | Texto de um conceito: o que é, que problema resolve, quando usar, exemplo, limites, referências, origem e revisão | `conceitos/<id>.md` | Ainda não há |

## Regras

- Abra os modelos em modo texto (no editor ou no botão Raw do GitHub): na visualização do GitHub, os marcadores somem.
- Troque todos os marcadores. Antes de validar, procure `<` no arquivo novo; não pode sobrar nenhum.
- Os links dos modelos têm marcadores com espaço, e por isso a checagem de links os ignora. No arquivo novo, cada link precisa apontar para um arquivo que existe.
- Lista, gabarito e verificação andam juntos e têm o mesmo nome. A numeração dos itens é única na lista inteira e igual no gabarito.
- Códigos de disciplina e IDs de competência nunca mudam nem são reaproveitados.
- `portao.criterio` e o texto do "Portão de saída" são o mesmo critério: escreva os dois iguais.
- O cabeçalho guarda só o currículo. O andamento (`status`, `inicio`, `diagnostico`, `nivel_atingido` e `portao` com `data`, `resultado` e `evidencia`) fica em `registro/estado.yml`, na branch de estudo ([fluxo de git](../docs/fluxo-git.md)); o schema recusa esses campos no cabeçalho.
- Módulo de nivelamento não repete o roteiro de estudo: a seção "Como estudar este módulo" aponta para o [roteiro comum](../docs/roteiro-nivelamento.md). O NM0 é a exceção, com roteiro próprio.
- `competencias` é obrigatório em módulo de nivelamento e opcional em disciplina; sem ele, a disciplina não recebe respostas no `registro/respostas.csv`.
- O nível de exercício (1 a 5) segue a tabela de [AVALIACOES.md](../AVALIACOES.md#níveis-de-exercício). Não confunda com `nivel_alvo`, a escala de domínio de 1 a 7 de [catalogo/escalas.yml](../catalogo/escalas.yml).
- `conceitos/` ainda não existe. A pasta só é criada com o primeiro conceito, e o formato do ID é decidido nesse momento.
- Arquivo novo é estrutura e vai para a `main` ([fluxo de git](../docs/fluxo-git.md)).

## Como validar

```bash
python scripts/verificar.py exercicios/<código>/verificacao/<n>-<nome>.yml   # lista nova: tem que dizer "Verificação sem divergências."
python scripts/diagrama.py                                                  # módulo novo de nivelamento: regera o diagrama de NIVELAMENTO.md
python scripts/progresso.py --checar                                        # sempre: links, pré-requisitos, lista x gabarito, verificações
pytest -q                                                                   # se mexeu em scripts/ ou tests/
```

O `--checar` não reescreve `PROGRESSO.md` nem `MAPA.md`. Ao incluir uma lista nova num módulo, acrescente-a também na seção "Listas de exercícios" do módulo, se houver.

## Branch de estudo

`estudante.yml` vai para `registro/estudante.yml` da sua branch de estudo, `estudo_<nome>`. Ele diz qual é a branch e qual conta do GitHub assina os commits ([fluxo de git](../docs/fluxo-git.md)). O schema está em `schemas/estudante.schema.json`.
