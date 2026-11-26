# Catálogo

Registros de referência que as disciplinas citam por código.

| Arquivo | O que define | Códigos |
| --- | --- | --- |
| [eixos.yml](eixos.yml) | Eixos do plano e as disciplinas de cada um | A a H |
| [unidades.yml](unidades.yml) | Unidades do curso de Engenharia de Software | `U1.1` a `U9.4` |
| [projetos.yml](projetos.yml) | Projetos integradores | `PJ1` a `PJ20` |
| [fora-do-plano.yml](fora-do-plano.yml) | Disciplinas do Mapa fora do plano, com o motivo | `M13`, `S3`, `H3`, `H4` |
| [escalas.yml](escalas.yml) | Escala de domínio (`nivel_alvo`, `nivel_atingido`) e dificuldade de exercício (`nivel` dos itens) | 1 a 7 e 1 a 5 |
| [aposentados.yml](aposentados.yml) | Códigos que deixaram de existir e não são reaproveitados | `M0` |

A tabela "Níveis de exercício" de [AVALIACOES.md](../AVALIACOES.md) repete a escala de dificuldade. A fonte é `escalas.yml`; se as duas divergirem, a validação falha.

## Regras

- Os códigos são identificadores: não mudam e não são reaproveitados.
- Estes arquivos vieram da revisão 74 do [Mapa de Formação](../docs/referencia/mapa-de-formacao-rev74.md) e agora são a fonte de verdade. Em caso de divergência, valem eles.
- `M13`, `S3`, `H3` e `H4` estão no Mapa sem arquivo em `disciplinas/`. O motivo de cada uma está em [fora-do-plano.yml](fora-do-plano.yml): S3 e H4 são cobertas pelo curso, H3 em parte, e M13 só entra no plano de 10 anos. `M0` foi substituída pelo [nivelamento](../NIVELAMENTO.md).
- Todo arquivo tem `schema_version: 1` e segue o schema de mesmo nome em [schemas/](../schemas/README.md).

## Validação

- `scripts/esquema.py` confere cada arquivo contra o seu schema.
- `scripts/catalogo.py` confere as referências cruzadas: código de disciplina único, unidades e projetos citados existem, o `eixo` de cada disciplina está nos rótulos do eixo que a lista, códigos de `sem_arquivo` e aposentados não têm arquivo, toda lista de exercícios tem verificação ou está em [exercicios/sem-verificacao.yml](../exercicios/sem-verificacao.yml), e a escala de dificuldade bate com AVALIACOES.md.
- `scripts/qualidade.py` imprime o relatório de qualidade.
- O `scripts/progresso.py --checar` roda essas validações, e o CI falha se alguma não passar.
