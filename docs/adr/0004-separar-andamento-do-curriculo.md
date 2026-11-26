# ADR 0004 · Separar o andamento do currículo

- **Status:** Aceita, implementada
- **Data:** 25/11/2026

## Contexto

O cabeçalho de cada arquivo em `disciplinas/` mistura duas coisas: o plano (pré-requisitos, horas, nível-alvo, competências, critério do portão) e o andamento de quem estuda (`status`, `inicio`, `diagnostico`, `nivel_atingido`, `portao.data`, `portao.resultado`, `portao.evidencia`). Por isso a branch de estudo precisa divergir da `main` nos mesmos arquivos. A [auditoria de 25/11/2026](../arquitetura/auditoria.md) encontrou o arquivo do NM0 já diferente entre as duas branches, e apontou a perda de registros numa fusão de branches como risco alto.

Hoje a regra de branches do [fluxo de git](../fluxo-git.md) contém o risco ([ADR 0006](0006-fluxo-de-git.md)), mas não o remove.

## Decisão

1. O andamento sai dos cabeçalhos de `disciplinas/` e vai para `registro/estado.yml` (decisão D4 da auditoria).
2. `registro/estado.yml` só existe na branch de estudo (`estudo_<nome>`).
3. A `main` não tem esse arquivo. Os scripts tratam a ausência como todos os módulos `nao_iniciada`.
4. A migração é feita por script, com teste. O aceite é o mesmo `MAPA.md` antes e depois da migração, e a mudança é reversível pelo Git.
5. Até o Marco 4, os campos de andamento continuam no cabeçalho e são aceitos pelo schema como transitórios ([modelo](../arquitetura/modelo.md)).

## Implementação

Feita no Marco 4, em 25/11/2026:

- `scripts/estado.py` lê `registro/estado.yml` e aplica o andamento às disciplinas; os outros scripts continuam lendo `status` e `portao` como antes. O formato está em [schemas/estado.schema.json](../../schemas/estado.schema.json).
- O schema do cabeçalho passou à v2, que recusa os campos de andamento; a v1 fica em [schemas/historico/](../../schemas/historico/disciplina.v1.schema.json).
- `scripts/migrar_estado.py` migra os cabeçalhos linha a linha. Na `main` rodou com `--nao-gravar-estado`; na branch de estudo roda uma vez, antes de trazer a `main` ([fluxo de git](../fluxo-git.md)).
- O aceite foi conferido numa cópia da branch de estudo: `PROGRESSO.md` e `MAPA.md` iguais antes e depois, menos a linha da data de geração.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Manter como está e só documentar | A regra de branches reduz o risco, mas os mesmos arquivos continuam divergindo entre as branches |
| Andamento num arquivo por disciplina dentro de `registro/` | Multiplica arquivos sem ganho; um arquivo só basta para 86 itens |
| Andamento na `main` | Mistura os dados de quem estuda com o conhecimento, que é o que esta decisão quer evitar |

## Consequências

- Os arquivos de `disciplinas/` ficam iguais nas duas branches; trazer a `main` para a branch de estudo deixa de gerar conflito no andamento.
- Mexe em scripts (`progresso.py`, `autonomia.py` e outros que leem `status`), testes e na skill, que hoje grava esses campos no cabeçalho. A skill precisa de nova versão e regressão.
- O [fluxo de git](../fluxo-git.md) e o `README.md` precisam ser atualizados na mesma mudança.
- Enquanto o Marco 4 não chega, a separação dos dados de quem estuda fica incompleta (débito DT-07 em [débitos](../arquitetura/debitos.md)).
