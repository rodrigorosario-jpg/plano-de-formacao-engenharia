# Relatório de benchmark · fase C (modo Fixação)

Skill `estudo-guiado` 0.3.0. Executada em 20/11/2026 com a mesma metodologia das fases anteriores: cópias isoladas, executores novos e juízes cegos. Os casos estão em [tests/skill/fase-c/casos.md](../../tests/skill/fase-c/casos.md).

## Desenvolvimento (6 casos)

| Caso | Baseline | Com skill |
| --- | --- | --- |
| C-01 lista com fixação intercalada | 4,35 | 4,75 |
| C-02 queda de autonomia | 4,71 | 4,71 |
| C-03 sem módulo concluído | 4,76 | 4,76 |
| C-04 fixação vencida | 4,76 | 4,76 |
| C-05 tarefa agendada | 4,06 | 4,63 |
| C-06 itens de lógica verificados por código | 4,80 | 4,60 |
| **Média** | **4,57** | **4,70** (+0,13) |

## Validação (3 casos novos, uma única execução)

| Caso | Baseline | Com skill |
| --- | --- | --- |
| CV-01 lista com fixação vencida | 4,80 | 4,75 |
| CV-02 pergunta direta sobre o NM0 | 4,80 | 4,80 |
| CV-03 fixação de módulo não concluído | 5,00 | 5,00 |
| **Média** | **4,87** | **4,85** (−0,02) |

## Regressão (casos das fases A e B com a 0.3.0)

Critério: nenhum portão violado e nota de pelo menos 4,5. Todos passaram.

| Caso | Nota | Portões |
| --- | --- | --- |
| A-L4-01 "só me dá a resposta" | 4,80 | nenhum |
| V-03 gabarito no meio da lista | 4,80 | nenhum |
| BV-02 dois "não sei" seguidos | 5,00 | nenhum |
| BV-05 item que não é âncora | 4,60 | nenhum |

## Leitura

- **A fixação vem quase toda do repositório.** Os avisos `autonomia-em-queda`, `fixacao-vencida` e `sem-intercalacao` e o sorteio `--sortear-fixacao` estão no código. O baseline, que roda os scripts e lê o `AVALIACOES.md`, chega aos mesmos resultados. Por isso houve empate na maioria dos casos e na validação.
- **Onde a skill ainda ganha:** na disciplina de oferecer a tarefa agendada sem criá-la (C-05) e na intercalação da fixação dentro da lista (C-01).
- **Nenhum portão foi violado em nenhum grupo**, e as versões novas não regrediram nos casos antigos.

## Limitações

- A amostra é pequena (6 + 3 casos), com um juiz por caso.
- O NM0 aparece como concluído em todos os casos de fixação, então não houve casos com vários módulos concluídos competindo no sorteio.
- A tarefa agendada só foi testada como oferta, porque o ambiente de teste não permitia criá-la.
