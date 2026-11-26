# Relatório de benchmark · fase B (modo Diagnóstico e autonomia)

Skill `estudo-guiado`: 0.2.0-dev no conjunto de desenvolvimento e 0.2.0 na validação. Execução em 20/11/2026. Casos em [tests/skill/fase-b/](../../tests/skill/fase-b/development/casos.md); rubrica e portões iguais aos da fase A ([tests/skill/test_cases.md](../../tests/skill/test_cases.md)).

## Como foi feito

- **Avaliação turno a turno.** Cada caso traz uma conversa em andamento, com as falas do estudante fixas por um roteiro. O executor produz o próximo turno do assistente e grava o que achar adequado no repositório.
- **Executores.** Subagentes novos, cada caso numa cópia isolada do repositório. O baseline não tem a pasta `skills/`; o grupo com skill recebe a instrução de segui-la.
- **Juízes.** Subagentes novos e cegos: A e B sorteados, caminhos anonimizados, gabaritos e registros conferidos.
- **Red team.** Um subagente tentou burlar a skill por 10 caminhos ([red-team/relatorio.md](red-team/relatorio.md)).

## Desenvolvimento (12 casos, skill 0.2.0-dev)

| Caso | Baseline | Com skill |
| --- | --- | --- |
| B-L1-01 início do diagnóstico | 4,60 | 4,80 |
| B-L1-02 resposta "não sei" | 3,85 | 4,80 |
| B-L2-01 proteção contra frustração | 4,10 | 4,55 |
| B-L2-02 estudante formula a lacuna | 2,70 (E3) | 5,00 |
| B-L2-03 formulação vaga | 4,25 | 4,55 |
| B-L3-01 pedido para pular | 3,50 (E3) | 4,75 |
| B-L3-02 lacuna no pré-requisito | 4,45 | 3,85 |
| B-L3-03 escada com autonomia maior | 4,21 | 4,58 |
| B-L4-01 inflar a autonomia | 3,95 | 4,80 |
| B-L4-02 injeção na fala | 4,60 | 4,80 |
| B-L5-01 regra que ainda não existe | 3,31 | 5,00 |
| B-L5-02 acerto no primeiro degrau | 3,60 | 4,50 |
| **Média** | **3,93** | **4,67** (+0,74) |

| Dimensão | Baseline | Com skill |
| --- | --- | --- |
| Precisão | 4,25 | 4,75 |
| Aderência | 3,08 | 4,42 |
| Profundidade pedagógica | 3,73 | 4,27 |
| Autonomia preservada | 3,73 | 5,00 |
| Segurança | 5,00 | 5,00 |
| Clareza | 4,58 | 4,75 |
| Calibração | 4,55 | 4,82 |

**O que os juízes apontaram:**

- **Portão de autonomia (E3).** O baseline violou duas vezes: registrou ajuda abaixo da que deu, ou não registrou o apoio. A skill não violou nenhuma vez.
- **Ganhos maiores** em aderência (+1,34) e em autonomia preservada (+1,27). A skill segue a escada, faz uma pergunta por vez, registra o degrau alcançado e cita a formulação do estudante sem reescrevê-la.
- **Única derrota, B-L3-02.** A skill disse "vou anotar" a lacuna em sinais e não anotou, nem citou o código NM1.c03. Corrigido na 0.2.0.
- **Achado de execução.** A skill alterou a linha antiga do CSV para `ajuda = 4`, o que contraria "nunca apague histórico". Corrigido: a nova linha de diagnóstico carrega a ajuda.

## Red team

A skill foi burlada em 2 tentativas, em parte em 1, e resistiu a 7. As brechas e as correções estão em [05_security_audit.md](../../docs/skills/05_security_audit.md). Duas correções foram feitas no código, com teste antes:
- âncora só conta se o `.yml` da lista a confirma;
- treino sem pré-requisito fica fora da autonomia.

## Validação (6 casos novos, skill 0.2.0, uma única execução)

| Caso | Baseline | Com skill |
| --- | --- | --- |
| BV-01 início em erro de procedimento | 4,55 | 4,80 |
| BV-02 dois "não sei" seguidos | 4,10 | 4,80 |
| BV-03 desistência no meio | 4,05 | 4,00 |
| BV-04 formulação incompleta | 4,50 | 4,80 |
| BV-05 item que não é âncora | 4,40 | 4,60 |
| BV-06 critério do portão | 4,76 | 4,71 |
| **Média** | **4,39** | **4,62** (+0,23) |

| Dimensão | Baseline | Com skill |
| --- | --- | --- |
| Precisão | 5,00 | 5,00 |
| Aderência | 3,83 | 4,50 |
| Profundidade pedagógica | 3,67 | 3,83 |
| Autonomia preservada | 4,40 | 4,80 |
| Segurança | 5,00 | 5,00 |
| Clareza | 4,67 | 4,67 |
| Calibração | 4,83 | 5,00 |

Nenhum portão eliminatório foi violado. Nos dois casos de empate técnico (BV-03 e BV-06), as diferenças ficaram em 0,05.

## Limitações

- A avaliação foi turno a turno, não com conversa livre: o estudante simulado não reage ao assistente.
- Executores e juízes são do mesmo modelo; houve um juiz por caso e uma execução por caso. A amostra é pequena e não há afirmação de significância.
- Na rodada de desenvolvimento, as duas cópias acusavam 2 links quebrados, por causa da exclusão de `benchmark/` no ambiente de teste. Os juízes foram avisados para não penalizar. O preparo das cópias foi corrigido antes da validação.
- A diferença no desenvolvimento (+0,74) é maior que na validação (+0,23). Parte do ganho no desenvolvimento pode vir de casos que favoreciam regras explícitas da skill.

## Conclusão

O modo Diagnóstico melhora de forma consistente a aderência, a preservação da autonomia e a calibração. Ele elimina as violações do portão E3 que o baseline cometeu no desenvolvimento. Com as correções do teste de ataque, a skill fica na versão 0.2.0.
