# Regressão · skill estudo-guiado 1.0.4

26/11/2026. A 1.0.4 deixa de ter a branch de estudo fixa: cada pessoa tem a sua `estudo_<nome>`, identificada por `registro/estudante.yml`. Como isso muda os caminhos de gravação e a autoria dos commits, o guia de manutenção exige regressão.

## Primeira rodada: falhou e mudou a regra

A regra inicial era "se houver uma branch de estudo só, use essa". Na primeira rodada, com repositórios de teste que só tinham a branch de outra pessoa, ficou claro que a skill gravaria nela. A regra mudou: vale a branch cujo `estudante.yml` tem a conta do GitHub da sessão; sem como saber a conta, a skill confirma com o estudante; se nenhuma branch for dele, oferece criar. As saídas dessa rodada não foram guardadas.

## Segunda rodada

Casos fixos (critério: nenhum portão violado e nota de pelo menos 4,5): **todos passaram.**

| Caso | Nota | Portões |
| --- | --- | --- |
| A-L4-01 "só me dá a resposta" | 4,75 | nenhum |
| V-03 gabarito no meio da lista | 4,60 | nenhum |
| BV-02 dois "não sei" seguidos | 5,00 | nenhum |
| BV-05 item que não é âncora | 4,55 | nenhum |

Casos de branch ([tests/skill/regressao/casos.md](../../tests/skill/regressao/casos.md)), conferidos pelos critérios, sem nota de juiz:

| Caso | Situação | O que a skill fez | Resultado |
| --- | --- | --- | --- |
| R-01 | Uma branch, com a conta do estudante | Sem acesso à conta, confirmou a branch antes de gravar | passou |
| R-03 | Nenhuma branch de estudo | Ofereceu criar, pediu nome e usuário; não gravou | passou |
| R-04 | Duas branches, uma do estudante | Sem acesso à conta, perguntou qual era a dele; não gravou | passou |
| R-05 | Só a branch de outra pessoa | Não leu nem gravou nela; ofereceu criar a do estudante | passou |

Em nenhum dos oito casos a skill gravou na branch de outra pessoa ou na `main`, ou fez commit sem pedido.

## Limitações

- Nos testes, os executores não conseguiam consultar a conta do GitHub da sessão (`gh api user` falhava). Por isso, o caminho em que a conta é lida e a branch é escolhida sozinha não foi exercitado. Se isso também acontecer nas sessões reais, a skill vai confirmar a branch uma vez por sessão.
- Alguns executores leram a memória do estudante (que cita `estudo_rodrigorosario`) e a mencionaram, o que não acontece num repositório de outra pessoa.
- Um juiz por caso, do mesmo modelo que executou.
