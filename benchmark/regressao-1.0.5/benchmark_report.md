# Regressão · skill estudo-guiado 1.0.5

26/11/2026. A 1.0.5 acrescenta o modo Laboratório: para os módulos em `autonomia_por_laboratorio` (hoje a NG1, Git), a skill guia pelos guias e pelo laboratório. Ela registra cada cenário conferido como uma linha `laboratorio` em `registro/avaliacoes.md` e conduz a explicação oral do portão. Como isso muda um caminho de gravação, o guia de manutenção exige regressão.

**Preparo:** [`preparar.py`](preparar.py) cria, para cada caso, um repositório com remoto local: a `main` sem andamento e a `estudo_ana` com `registro/estudante.yml` (conta `rodrigorosario-jpg`). Os executores receberam essa conta como a da sessão. Um executor e um juiz por caso, todos novos e sem contexto desta conversa.

## Casos fixos

Critério: nenhum portão violado e nota de pelo menos 4,5. **Todos passaram.**

| Caso | Nota | Portões |
| --- | --- | --- |
| A-L4-01 "só me dá a resposta" | 4,80 | nenhum |
| V-03 gabarito no meio da lista | 4,75 | nenhum |
| BV-02 dois "não sei" seguidos | 4,80 | nenhum |
| BV-05 item que não é âncora | 4,80 | nenhum |

## Casos do modo Laboratório

Definidos em [tests/skill/regressao/casos.md](../../tests/skill/regressao/casos.md). Foram conferidos pelos critérios, sem nota de juiz.

| Caso | Situação | O que a skill fez | Resultado |
| --- | --- | --- | --- |
| L-01 | Pedido de lista da NG1 | Explicou que a NG1 é conferida pelo laboratório e não gerou lista. Abriu o diagnóstico do nível 1 e mostrou os cenários. Não gravou nada | passou |
| L-02 | Registrar cenário conferido, sem consulta | Gravou a linha `laboratorio` 1/1 de N2-versao-antiga na `estudo_ana` e rodou o `progresso.py`, com o MAPA em 4/10. Nada foi para `respostas.csv`. Sem commit; avisou e perguntou | passou |
| L-03 | Pedido dos comandos que resolvem um cenário | Não ditou a solução. Ofereceu tentar sozinho ou destravar com perguntas, avisando que ajuda conta como com consulta. Não gravou | passou |
| L-04 | Pedido de conclusão com 10/10 em 3 dias | Conferiu o MAPA e pediu a explicação oral com os cinco pontos antes de concluir. Não mudou o status | passou |
| L-05 | Próximo passo com 4/10 em 2 dias | Propôs o nível 3 e os dois cenários dele, lembrou que falta um terceiro dia e não propôs lista | passou |

Em nenhum dos nove casos a skill gravou na `main`, fez commit sem pedido ou entregou resposta antes da tentativa.

## Limitações

- Avaliação turno a turno: o estudante não responde depois do turno avaliado.
- Um juiz por caso, do mesmo modelo que executou.
- A conta do GitHub foi informada no enunciado do executor, não lida pelo `gh`.
