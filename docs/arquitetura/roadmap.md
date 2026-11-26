# Roadmap do Knowledge Core

Marcos, entregáveis, critérios de aceite e status. A origem é a seção 10 da [auditoria de 25/11/2026](auditoria.md); este arquivo é o que se atualiza quando um marco anda.

## Status em 25/11/2026

| Marco | Status |
| --- | --- |
| 1. Fundação | Concluído |
| 2. Padronização | Entregue neste pull request |
| 3. Qualidade | Entregue neste pull request |
| 4. Consolidação | Entregue neste pull request |
| 5. Aplicação | Só depois de haver conteúdo para consultar |
| 6. Plataforma | Só depois do Marco 5 e de uso real |

O aceite dos Marcos 2 e 3 é conferido pelo CI e por `python scripts/qualidade.py` quando o pull request entra na `main`. O do Marco 4 também pela prova na branch de estudo descrita no próprio marco.

## Marcos

### 1. Fundação

- **Objetivo:** registrar as decisões e fechar os problemas de integridade que afetavam o estudo.
- **Entregáveis:** a auditoria e as decisões D1 a D5; skill instalada atualizada (1.0.1, depois 1.0.2); Mapa exportado para `docs/referencia/`; regra de branches em [docs/fluxo-git.md](../fluxo-git.md) e na skill; âncoras do NM0 (itens das listas antigas nunca contam como âncora; lista de 6 problemas-âncora com verificação); catálogo com eixos, unidades, projetos e escalas; regressão da skill sem portões violados (4,75 · 4,55 · 5,00 · 4,55); [ADRs](../adr/README.md) e [visão](visao.md).
- **Aceite:** decisões registradas; CI verde.
- **Não será feito:** mover arquivos.
- **Status:** concluído. O P0 entrou nos PRs #5 e #6 em 25/11/2026; as ADRs e a visão entram com esta documentação.

### 2. Padronização

- **Objetivo:** dar formato declarado a tudo o que o Core guarda.
- **Entregáveis:** catálogo completo (inclui `catalogo/aposentados.yml`); JSON Schema versionado em `schemas/` ([ADR 0005](../adr/0005-json-schema-versionado.md)); modelos por tipo de conteúdo em `templates/`; escalas únicas (dificuldade 1 a 5, domínio 1 a 7); taxonomia por eixo; documentação de arquitetura ([modelo](modelo.md), [glossário](glossario.md), [débitos](debitos.md)).
- **Depende de:** Marco 1.
- **Risco:** quebrar o formato atual.
- **Aceite:** 100% dos 86 arquivos de `disciplinas/` validam contra o schema.
- **Não será feito:** conteúdo novo em massa.
- **Status:** entregue neste pull request.

### 3. Qualidade

- **Objetivo:** transformar as regras do modelo em validações automáticas.
- **Entregáveis:** novas validações (código de disciplina único, referências a unidades e projetos resolvidas, lista sem verificação só com exceção registrada em `exercicios/sem-verificacao.yml`); testes para cada regra; relatório de qualidade (`python scripts/qualidade.py`); CI mais restrito ([segurança](seguranca.md)); execução do campo `codigo:` com ambiente vazio e limites.
- **Depende de:** Marco 2.
- **Risco:** regras que travem o estudo.
- **Aceite:** cada regra com teste; nenhuma referência solta.
- **Não será feito:** indexador.
- **Status:** entregue neste pull request.

### 4. Consolidação

- **Objetivo:** separar os dados de quem estuda do conhecimento.
- **Entregáveis:** andamento movido dos cabeçalhos de `disciplinas/` para `registro/estado.yml`, só na branch de estudo ([ADR 0004](../adr/0004-separar-andamento-do-curriculo.md)); `scripts/estado.py` e o schema `estado` v1; schema do cabeçalho v2, que recusa campos de andamento (a v1 fica em `schemas/historico/`); script de migração `scripts/migrar_estado.py` com teste; scripts, testes e skill (1.0.3) ajustados; [fluxo de git](../fluxo-git.md) atualizado, com o procedimento único de migração da branch de estudo.
- **Depende de:** Marco 3.
- **Risco:** perda de histórico.
- **Aceite:** o mesmo `MAPA.md` antes e depois da migração; reversível pelo Git.
- **Não será feito:** reorganizar por domínio.
- **Status:** entregue neste pull request. Os 86 cabeçalhos da `main` estão sem campos de andamento (`python scripts/qualidade.py`: progresso separado, Sim). Numa cópia da branch de estudo, a migração seguida do merge deste trabalho gerou `PROGRESSO.md` e `MAPA.md` iguais aos de antes, menos a linha da data de geração, sem conflito no merge; reverter o commit da migração devolve os cabeçalhos como eram.

### 5. Aplicação

- **Objetivo:** consultar o Core sem abrir os arquivos um a um.
- **Entregáveis:** export JSON; navegação, busca e filtros.
- **Depende de:** Marco 4 e conteúdo para consultar.
- **Risco:** construir sem uso.
- **Aceite:** a aplicação lê o Core sem copiá-lo.
- **Não será feito:** contas de usuário; API sem consumidor.
- **Status:** só depois de haver conteúdo e uso real.

### 6. Plataforma

- **Objetivo:** trilhas, avaliações, progresso e IA contextual sobre o Core.
- **Depende de:** Marco 5 e uso real.
- **Risco:** autonomia falsa; custo.
- **Aceite:** definido depois do Marco 5.
- **Não será feito:** nada antes da hora.
- **Status:** só depois do Marco 5 e de uso real.

## Critérios para o Core evoluir além do Marco 4

O Core só passa para a aplicação (Marco 5) quando todos estes critérios estiverem na meta. A coluna do meio é a medição da auditoria; os valores atuais são medidos por `python scripts/qualidade.py`.

| Critério | Na auditoria (25/11/2026) | Meta |
| --- | --- | --- |
| Itens com ID único verificado | IDs existem, unicidade de disciplina não checada | 100% |
| Metadados validados por schema | Nenhum schema | 100% |
| Referências a unidades e projetos resolvidas | Nenhuma no Git | 100% |
| Listas com verificação | 0 de 4 | 100% ou exceção registrada |
| Fatos de currículo com uma só origem | Várias cópias | Uma origem, o resto gerado |
| Progresso separado do conhecimento | Não | Sim |
| Histórico preservado | Sim | Sim, conferido após cada migração |

## Governança

- Mudança de estrutura entra na `main` por pull request, com uma ADR nova quando mudar uma decisão ([ADR 0006](../adr/0006-fluxo-de-git.md)).
- Andamento só na branch de estudo.
- Um marco só muda de status aqui depois que o aceite for conferido.
- Débitos que viram trabalho de um marco saem de [débitos](debitos.md) com a data e o pull request que os resolveu.
