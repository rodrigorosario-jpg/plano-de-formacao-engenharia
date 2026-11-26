# ADR 0005 · JSON Schema versionado

- **Status:** Aceita
- **Data:** 25/11/2026

## Contexto

Os campos obrigatórios de uma disciplina só existiam como acessos no código: um campo ausente interrompia o script com erro de Python, em vez de uma mensagem clara. O catálogo e as verificações também não tinham formato declarado. A [auditoria de 25/11/2026](../arquitetura/auditoria.md) listou "schemas com versão" como lacuna do Marco 2.

Esta ADR registra a decisão D5 **da seção 8** da auditoria (JSON Schema). A tabela do resumo da auditoria usa o mesmo rótulo, D5, para outra coisa: "primeiro passo: só os itens P0". Essa foi uma escolha de sequência, não de arquitetura, e não tem ADR.

## Decisão

1. A estrutura dos arquivos do Core é descrita em JSON Schema e validada com a biblioteca `jsonschema`.
2. Os schemas ficam em `schemas/`, versionados: o `$id` de cada schema inclui a versão.
3. Os arquivos de dados do catálogo levam o campo `schema_version`, que diz contra qual versão foram escritos.
4. Campo opcional novo é mudança compatível. Mudança incompatível (campo removido, renomeado ou que vira obrigatório) exige nova versão do schema e um script de migração, com teste.
5. A validação roda junto com `python scripts/progresso.py --checar` e, portanto, no CI.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Pydantic | Prende o formato a Python; um consumidor em outra linguagem não reaproveita o schema |
| Só checagens manuais no código | É o que existia: regras espalhadas, sem formato declarado e com erro de Python como mensagem |

## Consequências

- O schema escreve o que o código já supunha, e independe de linguagem.
- Nova dependência: `jsonschema`, com versão exata em `requirements.txt` ([segurança](../arquitetura/seguranca.md)).
- Os campos de andamento são aceitos como transitórios até o Marco 4 ([ADR 0004](0004-separar-andamento-do-curriculo.md)).
- As classes de metadados e o versionamento estão no [modelo](../arquitetura/modelo.md).
