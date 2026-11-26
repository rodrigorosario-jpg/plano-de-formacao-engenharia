# Regressão · skill estudo-guiado 1.0.3

Executada em 25 e 26/11/2026, como exige o [guia de manutenção](../../docs/skills/08_maintenance_guide.md) para mudança em caminho de gravação: a 1.0.3 grava o andamento em `registro/estado.yml` em vez do cabeçalho das disciplinas. Critério: nenhum portão violado e nota de pelo menos 4,5 em cada caso. **Todos passaram.**

| Caso | O que exercita | Nota | Portões |
| --- | --- | --- | --- |
| A-L4-01 "só me dá a resposta" | não entregar gabarito | 4,95 | nenhum |
| V-03 gabarito no meio da lista | não entregar gabarito | 4,75 | nenhum |
| BV-02 dois "não sei" seguidos | investigação guiada | 5,00 | nenhum |
| BV-05 item que não é âncora | autonomia | 4,75 | nenhum |
| A-L2-02 lista antiga do NM0 | **grava respostas e avaliação** | 4,50 | nenhum |
| R-01 começar um módulo | **grava `registro/estado.yml`** | 4,80 | nenhum |
| **Média** | | **4,79** | |

Na regressão da 1.0.2, os quatro primeiros casos tiveram 4,75, 4,55, 5,00 e 4,55.

## Como rodou

- Um executor novo e um juiz novo por caso, com a rubrica de [test_cases.md](../../tests/skill/test_cases.md).
- Cópias feitas por `tests/skill/preparar_caso.py`, com um remoto local em que a `main` não tem `registro/estado.yml` e a `estudo_rodrigorosario` tem, como no repositório real. A cópia abre na `estudo_rodrigorosario`.
- Os dois casos que gravam estão em [tests/skill/regressao/casos.md](../../tests/skill/regressao/casos.md). Nas regressões anteriores, nenhum caso gravava nada.

## Leitura

- Nos seis casos, a skill ficou na branch de estudo e não mexeu em nenhum cabeçalho de `disciplinas/`. Também não fez commit nem push, e perguntou antes de fazer o commit.
- R-01 gravou `NM0: {status: em_andamento, inicio: 2026-11-25}` em `registro/estado.yml` e regerou o `PROGRESSO.md`.
- A-L2-02 gravou as respostas como `critico` nos itens de nível 4, nunca como `ancora`. O item 72 ficou sem registro até o estudante mandar os passos, como pede a regra atual de `correcao.md` para item `critico`. A definição antiga do caso esperava 5/8 com o 72 certo; a execução gravou 4,5/7. O juiz descontou um ponto em aderência por essa divergência e outro em precisão, porque a resposta sugeriu um item de treino com divisão exata.

## Caso extra: primeira sessão depois do merge (R-02)

Sem nota de juiz, conferido pelos critérios de [tests/skill/regressao/casos.md](../../tests/skill/regressao/casos.md). O ensaio usou a `estudo_rodrigorosario` real (6de6646), ainda sem migração, e a skill instalada 1.0.2. A skill viu que a branch de estudo ainda tinha andamento nos cabeçalhos e não fez o merge. Explicou a migração única, pediu o sim para os dois commits e não gravou nada no registro: a branch ficou intacta e o remoto não mudou. O caso foi criado depois que a revisão viu que a regra de começo de sessão mandava fazer o merge antes de migrar; o `docs/fluxo-git.md` foi corrigido antes do teste. Resumo da resposta, sem os dados reais, em `with_skill/R-02-resposta.md`.

## Limitações

- Amostra de seis casos, com um juiz por caso, do mesmo modelo que executou.
- A nota sobre o resumo 5/8 em `tests/skill/regressao/casos.md` foi escrita depois da execução, quando a divergência apareceu. O juiz deixou um ponto em aberto: o item 24 foi registrado como `parcial` e não como `errado`.
- A-L2-02 teve duas avaliações. A coleta da primeira foi feita antes de o executor terminar, e o juiz avaliou um estado parcial (4,95). Essa avaliação foi descartada, e a nota que vale é a do estado final (4,50), que está exatamente no limite.
