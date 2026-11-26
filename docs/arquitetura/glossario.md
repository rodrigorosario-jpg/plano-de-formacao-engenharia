# Glossário

Termos do projeto, em ordem alfabética. A coluna "Onde é definido" aponta a definição que vale; se este glossário divergir dela, vale a fonte.

| Termo | Definição curta | Onde é definido |
| --- | --- | --- |
| **ADR** | Registro de uma decisão de arquitetura: contexto, decisão, alternativas e consequências | [docs/adr/](../adr/README.md) |
| **Ajuda** | Número de intervenções antes de o estudante chegar à resposta: perguntas de apoio, dicas, confirmações de passo, correções parciais. 0 = sozinho; 4 = viu a resposta antes | [correcao.md](../../skills/estudo-guiado/references/correcao.md), coluna `ajuda` de `registro/respostas.csv` |
| **Andamento** | Tudo o que registra o estudo de uma pessoa: `registro/`, inclusive `registro/estado.yml` com `status`, `inicio`, `diagnostico`, `nivel_atingido` e os dados do portão. Oposto de estrutura | [Fluxo de git](../fluxo-git.md), [ADR 0004](../adr/0004-separar-andamento-do-curriculo.md) |
| **Âncora** (problema-âncora) | Problema complexo, de vários passos, que mistura competências e exige montar a estratégia, sem dicas. Só conta se o `.yml` de verificação da lista o marca como `ancora`; itens das listas antigas do NM0 nunca contam | [Design, seção 6.3](../skills/design.md), [AVALIACOES.md](../../AVALIACOES.md), [CHANGELOG da skill](../../skills/estudo-guiado/CHANGELOG.md) |
| **Autonomia** | 5 âncoras diferentes resolvidas certo e com `ajuda` 0, em pelo menos 3 dias distintos. Exigida no portão dos módulos de nivelamento com portão a partir de 20/11/2026 | [AVALIACOES.md](../../AVALIACOES.md), [plano.yml](../../plano.yml) (`autonomia_n`, `autonomia_dias_distintos`), [scripts/autonomia.py](../../scripts/autonomia.py) |
| **Autonomia em queda** | Aviso: 2 ou mais das últimas 3 respostas de um módulo concluído com erro ou ajuda | [AVALIACOES.md](../../AVALIACOES.md), [plano.yml](../../plano.yml) (`fixacao_janela`) |
| **Benchmark** | Saídas, avaliações cegas e relatórios da construção e da regressão da skill. É evidência, não conhecimento de estudo | [Guia de manutenção](../skills/08_maintenance_guide.md) |
| **Bloco** | Grupo de módulos do nivelamento (A a E de matemática, L de lógica, F de física), com um diagnóstico no início | [NIVELAMENTO.md](../../NIVELAMENTO.md), campo `bloco` |
| **Branch de estudo** | `estudo_<nome>`, uma por pessoa, com `registro/estudante.yml`: onde o andamento é lido e gravado. Nunca é mesclada na `main` | [Fluxo de git](../fluxo-git.md), [ADR 0006](../adr/0006-fluxo-de-git.md) |
| **Catálogo** | Registros de referência que as disciplinas citam por código: eixos, unidades, projetos, escalas e códigos aposentados | [catalogo/README.md](../../catalogo/README.md) |
| **Classe de erro** | Por que um item foi errado: `conceito`, `procedimento`, `atencao`, `interpretacao` ou `simplificacao_indevida` | [Design, seção 6.2](../skills/design.md), [correcao.md](../../skills/estudo-guiado/references/correcao.md) |
| **Código** | Identificador de uma entidade do Core (`NM0`, `C8`, `U2.2`, `PJ1`). Nunca muda nem é reaproveitado | [ADR 0003](../adr/0003-codigos-como-identificadores.md) |
| **Código aposentado** | Código que saiu de uso, registrado para não ser reaproveitado. `M0` é o primeiro | [ADR 0003](../adr/0003-codigos-como-identificadores.md), `catalogo/aposentados.yml` |
| **Competência** | Habilidade avaliável de um módulo, com ID estável (`NM0.c01`). O mapa de deficiências é calculado por competência | Campo `competencias` em `disciplinas/`, [modelo](modelo.md) |
| **Dados de quem estuda** | Um dos três contextos: respostas, avaliações, horas, diagnósticos e andamento. Ficam fora do índice de conhecimento | [Visão](visao.md) |
| **Débito** | Problema conhecido, registrado com impacto, proposta e quando tratar | [Débitos](debitos.md) |
| **Diagnóstico** | Dois sentidos: (1) avaliação no início de um bloco, que decide o que estudar em cada módulo; (2) modo da skill que faz perguntas, uma por vez, até o estudante achar a própria lacuna | (1) [AVALIACOES.md](../../AVALIACOES.md); (2) [diagnostico.md](../../skills/estudo-guiado/references/diagnostico.md) |
| **Dispensada** | Status de um módulo que o estudante pulou porque o diagnóstico e a prova de saída mostraram o domínio | [AVALIACOES.md](../../AVALIACOES.md), [README](../../README.md) |
| **Eixo** | Grande área do plano, de `A` a `H`. Os módulos de nivelamento não pertencem a eixos | [catalogo/eixos.yml](../../catalogo/eixos.yml) |
| **Em revisão** (`em_revisao`) | Status de um módulo concluído cuja revisão ficou abaixo de 70% | [AVALIACOES.md](../../AVALIACOES.md) |
| **Estrutura** | Tudo o que não é andamento: listas, gabaritos, verificações, texto e demais campos das disciplinas, catálogo, scripts, testes, skill e documentação. Vai para a `main` | [Fluxo de git](../fluxo-git.md) |
| **Fase** | Etapa do plano a que uma disciplina pertence: `nivelamento`, `graduacao` ou `pos_formatura` | Campo `fase` em `disciplinas/`, [modelo](modelo.md) |
| **Fixação** | Questões de módulos já concluídos que voltam sempre nas listas (`fixacao_proporcao`, 20%), sorteadas pelo script. Não confundir com o nível 1 da dificuldade de exercício, também chamado "Fixação" | [AVALIACOES.md](../../AVALIACOES.md), [fixacao.md](../../skills/estudo-guiado/references/fixacao.md), [plano.yml](../../plano.yml) |
| **Fixação vencida** | Aviso: competência de módulo concluído sem prática há mais de 30 dias | [AVALIACOES.md](../../AVALIACOES.md), [plano.yml](../../plano.yml) (`fixacao_vencida_dias`) |
| **Gabarito** | Respostas de uma lista, em arquivo separado (`gabaritos/`), numa tabela `Nº`, `Resposta`. Só é mostrado depois da tentativa | [Verificação dos gabaritos](../verificacao-gabaritos.md), [SKILL.md](../../skills/estudo-guiado/SKILL.md) |
| **Intercalação** | Alternar competências numa lista. O aviso `sem-intercalacao` sai com 3 itens seguidos da mesma competência | [README](../../README.md), [fixacao.md](../../skills/estudo-guiado/references/fixacao.md) |
| **Item** | Questão de uma lista, com nível de dificuldade, tipo e competência | [Modelo](modelo.md) |
| **Knowledge Core** | A parte do repositório que descreve o que se estuda e é a fonte de verdade do plano | [Visão](visao.md) |
| **Lista** | Conjunto de itens de exercício de um módulo, com gabarito e verificação, em `exercicios/<código>/`. Identificada pelo caminho | [Modelo](modelo.md), [exercicios.md](../../skills/estudo-guiado/references/exercicios.md) |
| **Mapa de deficiências** | `MAPA.md`, gerado pelo script: situação de cada competência (fraca, em formação, forte, em queda, sem dados), linha de autonomia e lacunas prováveis em pré-requisitos | [README](../../README.md), [Design, seção 6.2](../skills/design.md), [mapa.md](../../skills/estudo-guiado/references/mapa.md) |
| **Mapa de Formação** | Documento de origem do plano. A revisão 74 está congelada no repositório e não é mais fonte de verdade | [Cópia congelada](../referencia/mapa-de-formacao-rev74.md), [ADR 0001](../adr/0001-git-fonte-de-verdade.md) |
| **Motor de estudo** | Um dos três contextos: scripts, testes e a skill, que leem o conhecimento e os dados de quem estuda | [Visão](visao.md) |
| **Nível de dificuldade** | Escala de 1 a 5 dos itens de exercício: Fixação, Aplicação, Intermediário, Contexto, Desafio. Campo `nivel` das listas e do CSV | [AVALIACOES.md](../../AVALIACOES.md) |
| **Nível de domínio** | Escala de 1 a 7 de uma disciplina: Reconhecimento, Compreensão, Aplicação, Implementação, Análise, Projeto, Pesquisa. Campos `nivel_alvo` e `nivel_atingido`. Não é a mesma escala do nível de dificuldade | [catalogo/escalas.yml](../../catalogo/escalas.yml) |
| **Nivelamento** | Fase 0: 28 módulos (`NM`, `NF`, `NL`), até 790 h, que reconstroem a base de matemática, física e lógica antes do plano principal | [NIVELAMENTO.md](../../NIVELAMENTO.md) |
| **Portão** (de saída) | Critério que comprova o domínio de um módulo ou disciplina (`portao.criterio`). No nivelamento: 80% na prova de saída e autonomia | [AVALIACOES.md](../../AVALIACOES.md), campo `portao` em `disciplinas/` |
| **Pré-requisito** | Disciplina que precisa estar `concluida`, `dispensada` ou `em_revisao` antes de outra sair de `nao_iniciada` | Campo `prerequisitos`, [README](../../README.md) |
| **Problema gêmeo** | Problema com a mesma estrutura e outros números, entregue depois de uma explicação para o estudante tentar sozinho | [Design, seção 6.4](../skills/design.md) |
| **Projeto integrador** | Projeto que consolida várias disciplinas (`PJ1` a `PJ20`) | [catalogo/projetos.yml](../../catalogo/projetos.yml) |
| **Prova de saída** | Avaliação de 15 a 20 questões, sem consulta e com tempo marcado, que decide o portão | [AVALIACOES.md](../../AVALIACOES.md) |
| **Regressão** | Casos de avaliação da skill (A-L4-01, V-03, BV-02, BV-05) rodados de novo a cada mudança em regra invariável: nota mínima 4,5 e nenhum portão violado | [Guia de manutenção](../skills/08_maintenance_guide.md) |
| **Revisão espaçada** | Avaliação curta 7, 30 e 90 dias depois do portão | [AVALIACOES.md](../../AVALIACOES.md) |
| **Schema** | Descrição em JSON Schema do formato de um tipo de arquivo, com versão no `$id`. Os dados do catálogo dizem sua versão em `schema_version` | [ADR 0005](../adr/0005-json-schema-versionado.md), `schemas/` |
| **Tipo de item** | Papel do item na lista: `fluencia`, `metodos`, `simplificacao`, `armadilha_simplificacao`, `critico`, `ancora`, `fixacao`, `diagnostico` | [AVALIACOES.md](../../AVALIACOES.md), [Design, seção 6.5](../skills/design.md) |
| **Treino** | Lista feita sem o pré-requisito cumprido. Não conta para o portão nem para a autonomia | [SKILL.md](../../skills/estudo-guiado/SKILL.md) |
| **Unidade** | Unidade do curso de Engenharia de Software (`U1.2` a `U9.4`) que uma disciplina requer ou complementa | [catalogo/unidades.yml](../../catalogo/unidades.yml) |
| **Verificação** | Arquivo `.yml` ao lado de cada lista que diz como conferir cada item sem o gabarito (`calculo`, `predicado`, `codigo` ou `revisao`). Também marca as âncoras | [Verificação dos gabaritos](../verificacao-gabaritos.md) |
