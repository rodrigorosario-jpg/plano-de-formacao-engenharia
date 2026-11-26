# Modelo de conhecimento

O que o Knowledge Core guarda, como as entidades se relacionam, como são identificadas e onde mora cada coisa. A origem é a [auditoria de 25/11/2026](auditoria.md), seção 8, e as decisões das [ADRs 0002 a 0005](../adr/README.md).

## Entidades

| Entidade | O que é | ID | Onde mora | Situação |
| --- | --- | --- | --- | --- |
| **Módulo ou disciplina** | Unidade do plano, com tópicos, pré-requisitos, horas, nível-alvo e portão. Módulo é do nivelamento (`NM`, `NF`, `NL`); disciplina é do plano principal | Código: `NM0`, `NL1`, `C8` | `disciplinas/<código>-<nome>.md` | 86 arquivos: 28 de nivelamento, 13 da graduação, 45 depois dela |
| **Competência** | Habilidade avaliável de um módulo; é a unidade do mapa de deficiências | `<código>.cNN`: `NM0.c01` | Campo `competencias` no cabeçalho do módulo | 156, só nos 28 módulos de nivelamento |
| **Lista** | Conjunto de itens de exercício de um módulo, com gabarito e verificação | Caminho do arquivo: `exercicios/NM0/5-ancoras.md` | `exercicios/<código>/` | Só no NM0: 4 listas antigas e 1 de problemas-âncora |
| **Item** | Questão de uma lista, com nível de dificuldade, tipo e competência | Lista + número: `exercicios/NM0/5-ancoras.md`, item 3 | Na lista; resposta em `gabaritos/`; conferência em `verificacao/` | Itens das listas antigas do NM0 não têm verificação |
| **Eixo** | Grande área do plano | Letra: `A` a `H` | [catalogo/eixos.yml](../../catalogo/eixos.yml) | 8 eixos; o nivelamento não pertence a eles |
| **Unidade** | Unidade do curso de Engenharia de Software que uma disciplina requer ou complementa | `U<n>.<m>`: `U2.2` | [catalogo/unidades.yml](../../catalogo/unidades.yml) | 36 unidades, `U1.1` a `U9.4` |
| **Projeto** | Projeto integrador que consolida disciplinas | `PJ<n>`: `PJ1` | [catalogo/projetos.yml](../../catalogo/projetos.yml) | 20 projetos, `PJ1` a `PJ20` |
| **Escala** | Escala de domínio de uma disciplina (`nivel_alvo`, `nivel_atingido`) | Nível: 1 a 7 | [catalogo/escalas.yml](../../catalogo/escalas.yml) | A dificuldade de exercício (1 a 5) é outra escala, em [AVALIACOES.md](../../AVALIACOES.md) |
| **Código aposentado** | Código que saiu de uso e não pode ser reaproveitado | O próprio código: `M0` | `catalogo/aposentados.yml` | [ADR 0003](../adr/0003-codigos-como-identificadores.md) |
| **Conceito** (futuro) | Ideia explicada: o que é, que problema resolve, quando usar, exemplo, limites, referências | A definir | `conceitos/`, criada só com o primeiro conceito | Débito DT-15 em [débitos](debitos.md) |
| **Trilha** (futuro) | Caminho de estudo até uma disciplina ou objetivo | Não tem: é derivada | Gerada a partir do grafo de pré-requisitos, nunca armazenada | Estágio 3 da [visão](visao.md) |

Referência (bibliografia) e termo de glossário também são candidatos a entidade. As referências estão hoje como texto no corpo das disciplinas, sem link; os termos estão no [glossário](glossario.md). Tecnologia, habilidade e avaliação como entidade própria não serão criadas agora.

## Relações

**Explícitas** (gravadas nos arquivos e conferidas por script):

| Relação | De → para | Onde está |
| --- | --- | --- |
| pré-requisito | disciplina → disciplina | `prerequisitos` no cabeçalho; 174 arestas, sem ciclos |
| requer unidade | disciplina → unidade | `requer_unidades` |
| relacionada a unidade | disciplina → unidade | `unidades_relacionadas` |
| pertence ao eixo | disciplina → eixo | `eixo` no cabeçalho e `disciplinas` em `eixos.yml` |
| projeto consolida | projeto → disciplina | `disciplinas` em `projetos.yml` |
| pré-requisito de unidade | unidade → unidade | `prerequisitos` em `unidades.yml` |
| competência de | competência → módulo | `competencias` no cabeçalho |
| item avalia | item → competência | `competencia` no `.yml` de verificação e em `registro/respostas.csv` |
| lista de | lista → módulo | Pasta `exercicios/<código>/` |

**Inferidas** (calculadas, nunca gravadas): "libera" (o inverso de pré-requisito), ancestrais, cadeias críticas e trilhas.

**Futuras:** complementa, contrasta e relacionado só entram junto com os conceitos.

Regras do grafo:

- Ciclos são barrados por `scripts/progresso.py`.
- Pré-requisito redundante por transitividade pode ficar, se for intencional. A auditoria contou 37.
- O diagrama do nivelamento deve passar a ser gerado do YAML, em vez de mantido à mão.

## Identificadores

- O código é o ID ([ADR 0003](../adr/0003-codigos-como-identificadores.md)). Nunca muda nem é reaproveitado.
- O prefixo sugere a área (`NM` matemática do nivelamento, `C` ciência da computação), mas reclassificar muda o metadado `eixo`, não o código.
- IDs de competência seguem a mesma regra: uma competência que sai fica no cabeçalho; uma nova recebe o próximo número livre. O histórico de `registro/respostas.csv` depende deles.
- Listas são identificadas pelo caminho. Renomear uma lista quebra o histórico em `registro/`.

## Metadados de uma disciplina

| Classe | Campos | Regra |
| --- | --- | --- |
| **Obrigatórios** | `codigo`, `nome`, `eixo`, `fase`, `ordem`, `prerequisitos`, `horas_previstas`, `nivel_alvo`, `portao.criterio` | Todo arquivo tem |
| **Condicionais** | `bloco` (nivelamento); `competencias` (para receber respostas); `semestre_inicio` e `semestre_fim` (fora do nivelamento; hoje os 86 arquivos têm, com 0 no nivelamento); `unidades_relacionadas`; `requer_unidades` | Exigidos conforme a fase ou o uso |
| **Proibidos** (desde o Marco 4) | `status`, `inicio`, `nivel_atingido`, `diagnostico`, `portao.data`, `portao.resultado`, `portao.evidencia` | Andamento de quem estuda: fica em `registro/estado.yml`, na branch de estudo ([ADR 0004](../adr/0004-separar-andamento-do-curriculo.md)). O schema v2 do cabeçalho recusa esses campos |
| **Opcionais** | referências, projetos, tags | Podem faltar |
| **Futuros** | tecnologias, público-alvo, tempo por conceito | Ainda não existem |
| **Fora do arquivo** | datas de criação e alteração, autor e versão (vêm do Git); idioma (um só, no repositório) | Não se gravam no cabeçalho |

Valores de `fase` hoje: `nivelamento`, `graduacao` e `pos_formatura`. Os valores de `status` estão no [README](../../README.md) e em [schemas/estado.schema.json](../../schemas/estado.schema.json).

## Andamento

`registro/estado.yml` guarda o andamento de quem estuda, uma linha por módulo com algum valor fora do padrão:

```yaml
schema_version: 1
modulos:
  NM0: {status: em_andamento, inicio: 2026-11-23}
  NM1: {diagnostico: 0}
```

- Campos: `status`, `inicio`, `diagnostico`, `nivel_atingido` e `portao` (`data`, `resultado`, `evidencia`). Campo ausente vale o padrão: `status: nao_iniciada`, demais nulos.
- O arquivo só existe na branch de estudo. Sem ele, como na `main`, todos os módulos estão no padrão.
- `scripts/estado.py` carrega o arquivo e aplica os valores às disciplinas lidas por `scripts/progresso.py`; o resto dos scripts lê o andamento como antes. A validação acusa código desconhecido, status inválido, chave desconhecida e campo de andamento que tenha ficado num cabeçalho.
- A migração dos cabeçalhos para o arquivo é feita por `scripts/migrar_estado.py`, uma vez, como descreve o [fluxo de git](../fluxo-git.md).

## Padrão de conteúdo

| Tipo | Obrigatório |
| --- | --- |
| Disciplina | identificação, tópicos, referência, competência final, portão |
| Módulo de nivelamento | o da disciplina, mais aplicações e competências; o roteiro comum vira um documento único |
| Lista | instruções, itens com nível, gabarito, verificação |
| Conceito (futuro) | o que é, que problema resolve, quando usar, exemplo, limites, referências |

Os modelos de cada tipo ficam em `templates/`.

## Onde mora cada coisa

| Pasta | Contexto | O que guarda |
| --- | --- | --- |
| `disciplinas/` | Conhecimento | Um arquivo por módulo ou disciplina: cabeçalho YAML e corpo em Markdown (exemplo: [NM0](../../disciplinas/NM0-operacoes-fundamentais.md)) |
| [catalogo/](../../catalogo/README.md) | Conhecimento | Eixos, unidades, projetos, escalas e códigos aposentados |
| `exercicios/` | Conhecimento | Por código: listas, `gabaritos/` e `verificacao/` ([como verificar](../verificacao-gabaritos.md)) |
| `schemas/` | Conhecimento | JSON Schema de cada tipo de arquivo, com versão ([ADR 0005](../adr/0005-json-schema-versionado.md)) |
| `templates/` | Conhecimento | Modelo de cada tipo de conteúdo |
| `registro/` | Dados de quem estuda | `respostas.csv`, `avaliacoes.md`, `semanal.md`, `diagnosticos/` e `estado.yml` (andamento de cada módulo). Só na branch de estudo |
| `scripts/`, `tests/`, `skills/`, `plano.yml` | Motor de estudo | Validação, mapa, autonomia, fixação, verificação, a skill e seus parâmetros |
| `docs/referencia/` | Histórico | [Cópia congelada do Mapa de Formação](../referencia/mapa-de-formacao-rev74.md) |
| `benchmark/` | Evidência | Saídas e avaliações da construção da skill; não é conhecimento de estudo |

## Versionamento de schema

- Cada schema em `schemas/` tem `$id` com a versão.
- Os arquivos de dados do catálogo levam `schema_version`.
- Campo opcional novo é compatível e não muda a versão do schema.
- Mudança incompatível (campo removido, renomeado ou que passa a ser obrigatório) cria uma versão nova do schema e exige um script de migração, com teste, que leve os arquivos de uma versão à outra.
- O Git guarda as versões anteriores; a migração precisa ser reversível por ele.
