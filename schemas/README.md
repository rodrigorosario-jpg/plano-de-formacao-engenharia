# Schemas

JSON Schema (draft 2020-12) dos arquivos de dados do plano. Eles descrevem o formato que os scripts já supõem. A validação roda em `scripts/esquema.py`, com a biblioteca `jsonschema`.

| Schema | Valida | `$id` |
| --- | --- | --- |
| [disciplina.schema.json](disciplina.schema.json) | Cabeçalho YAML de cada arquivo em `disciplinas/` | `plano-de-estudos/schemas/disciplina/v2` |
| [eixos.schema.json](eixos.schema.json) | `catalogo/eixos.yml` | `plano-de-estudos/schemas/eixos/v1` |
| [unidades.schema.json](unidades.schema.json) | `catalogo/unidades.yml` | `plano-de-estudos/schemas/unidades/v1` |
| [projetos.schema.json](projetos.schema.json) | `catalogo/projetos.yml` | `plano-de-estudos/schemas/projetos/v1` |
| [escalas.schema.json](escalas.schema.json) | `catalogo/escalas.yml` | `plano-de-estudos/schemas/escalas/v1` |
| [aposentados.schema.json](aposentados.schema.json) | `catalogo/aposentados.yml` | `plano-de-estudos/schemas/aposentados/v1` |
| [verificacao.schema.json](verificacao.schema.json) | `exercicios/<código>/verificacao/*.yml` | `plano-de-estudos/schemas/verificacao/v1` |
| [plano.schema.json](plano.schema.json) | `plano.yml` | `plano-de-estudos/schemas/plano/v1` |
| [sem-verificacao.schema.json](sem-verificacao.schema.json) | `exercicios/sem-verificacao.yml` | `plano-de-estudos/schemas/sem-verificacao/v1` |
| [estado.schema.json](estado.schema.json) | `registro/estado.yml`, quando existe (só na branch de estudo) | `plano-de-estudos/schemas/estado/v1` |

Versões antigas ficam em `historico/` para referência e não são usadas na validação: [disciplina.v1.schema.json](historico/disciplina.v1.schema.json), que aceitava os campos de andamento no cabeçalho.

## Cabeçalho de disciplina

- **Obrigatórios:** `codigo`, `nome`, `eixo`, `fase`, `ordem`, `prerequisitos`, `horas_previstas`, `nivel_alvo` e `portao.criterio`.
- **Condicionais:** no nivelamento, `bloco` (no formato `<letra> · <nome>`) e `competencias` são obrigatórios, e `semestre_inicio` e `semestre_fim` também, valendo 0. Fora do nivelamento, `bloco` não existe e `semestre_inicio` e `semestre_fim` são obrigatórios. `competencias` é uma lista de `{id, nome}`, com `id` no formato `<CÓDIGO>.cNN` do próprio arquivo. `requer_unidades` e `unidades_relacionadas` citam códigos de `catalogo/unidades.yml`.
- **Proibidos:** `status`, `inicio`, `diagnostico`, `nivel_atingido`, `portao.data`, `portao.resultado` e `portao.evidencia`. São andamento e ficam em `registro/estado.yml`. A v2 recusa esses campos; a v1 os aceitava como transitórios até o Marco 4.
- Datas são texto ISO (`AAAA-MM-DD`). O YAML as lê como data, e o script as converte em texto antes de validar.
- Campo fora da lista é erro, para pegar erro de digitação como `prerequisito`.

## Andamento

`registro/estado.yml` tem `schema_version: 1` e `modulos`, um mapa do código do módulo para os campos de andamento: `status`, `inicio`, `diagnostico`, `nivel_atingido` e `portao` (`data`, `resultado`, `evidencia`). Campo ausente vale o padrão (`status: nao_iniciada`, demais nulos). Código desconhecido e status fora da lista são conferidos por `scripts/estado.py`, junto com o `--checar`.

## Versões

- Cada schema tem a versão no `$id` (`.../v1`, `.../v2`).
- Os arquivos do catálogo, `exercicios/sem-verificacao.yml` e `registro/estado.yml` têm `schema_version: 1`, e o schema exige esse valor. Cabeçalhos de disciplina, verificações de lista e `plano.yml` não têm campo de versão.
- Campo opcional novo é compatível e não muda a versão. Mudança que quebra arquivos existentes cria a versão seguinte e vem com um script de migração. Foi o caso do cabeçalho de disciplina: a v2 tirou os campos de andamento, e `scripts/migrar_estado.py` faz a migração.

## Mensagens

`scripts/esquema.py` devolve uma linha por problema, no formato `<arquivo>: <caminho do campo>: <mensagem>`, por exemplo `registro/estado.yml: modulos.NM0.inicio: valor '23/11/2026' não é null nem string no formato esperado`. `(raiz)` indica o arquivo inteiro, como num campo obrigatório ausente.

O `scripts/progresso.py` roda o schema dos cabeçalhos antes de tudo: com um cabeçalho inválido, ele lista os erros e para, sem chegar às outras verificações.
