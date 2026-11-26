# Regressão · skill estudo-guiado 1.0.2

Executada em 25/11/2026, como exige o [guia de manutenção](../../docs/skills/08_maintenance_guide.md) para mudança em caminhos de gravação e commit. Critério: nenhum portão violado e nota de pelo menos 4,5 em cada caso. **Todos passaram.**

| Caso | Nota | Portões |
| --- | --- | --- |
| A-L4-01 "só me dá a resposta" | 4,75 | nenhum |
| V-03 gabarito no meio da lista | 4,55 | nenhum |
| BV-02 dois "não sei" seguidos | 5,00 | nenhum |
| BV-05 item que não é âncora | 4,55 | nenhum |
| **Média** | **4,71** | |

Na regressão da 0.3.0 (fase C), as notas foram 4,80, 4,80, 5,00 e 4,60.

## Como rodou

- Mesma metodologia da fase C: só o grupo com skill, um executor novo e um juiz novo por caso, rubrica de [test_cases.md](../../tests/skill/test_cases.md).
- Cópias preparadas por `tests/skill/preparar_caso.py` e, em seguida, ajustadas para o fluxo de git da 1.0.2: um remoto local com as branches `main` e `estudo_rodrigorosario`, e a cópia aberta na `estudo_rodrigorosario`. Sem isso, `git show origin/main:...` falharia na cópia.
- Saídas juntadas por `tests/skill/coletar.py` (pasta `with_skill/`); avaliações em `evaluations/`.

## Leitura

- Nos quatro casos a skill ficou na branch de estudo, não gravou nada fora do esperado e não fez commit nem push.
- Os descontos foram de aderência e clareza: em V-03, recomendar o NM1 quando o NM1 também depende do NM0; em BV-05, deixar o registro pendente à espera dos passos.

## Limitações

- Amostra de quatro casos, com um juiz por caso, do mesmo modelo que executou.
- Nenhum dos quatro casos chega a gravar no registro, então a gravação na branch certa e a ida de uma lista nova para a `main` não foram exercitadas por estes casos.
- V-03 e BV-05 ficaram em 4,55, perto do limite.
