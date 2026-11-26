# Avaliações

As avaliações servem para medir o domínio, não para cumprir etapas. Valem para o nivelamento e para todo o plano. Os exercícios são pedidos ao Claude conforme os modelos abaixo, e cada resultado vai para [registro/avaliacoes.md](registro/avaliacoes.md).

## Tipos de avaliação

| Tipo | Quando | Formato | Decide |
| --- | --- | --- | --- |
| `diagnostico` | No início de cada bloco do nivelamento | 20 a 30 questões cobrindo todos os módulos do bloco, sem consulta, com tempo marcado | O que estudar em cada módulo |
| `exercicios` | Durante o estudo de um módulo | Listas por nível de dificuldade (tabela abaixo) | Quando pedir a prova de saída |
| `saida` | Ao fim de cada módulo ou disciplina | 15 a 20 questões, sem consulta, com tempo marcado | Se o portão foi cumprido |
| `revisao` | 7, 30 e 90 dias depois do portão | 5 a 10 questões mistas, de 15 a 20 minutos, no almoço | Se o conteúdo continua dominado |
| `laboratorio` | Cada cenário do laboratório de Git (NG1) que passou no `conferir` | Uma linha por cenário: Acertos 1 se foi sem consulta, 0 se houve consulta; o código do cenário (ex.: `N4-conflito`) nas Observações | Se a NG1 tem os cenários e os dias que o portão pede ([ADR 0010](docs/adr/0010-disciplinas-de-git-e-guias.md)) |

## Níveis de exercício

| Nível | Nome | O que treina |
| --- | --- | --- |
| 1 | Fixação (iniciante) | Aplicar a definição ou o procedimento diretamente |
| 2 | Aplicação (básico) | Combinar dois procedimentos ou escolher qual usar |
| 3 | Intermediário | Números maiores, cálculo mental, conferência e estimativa |
| 4 | Contexto (avançado) | Problemas de engenharia, física, computação ou ciência de dados |
| 5 | Desafio (complexo) | Problemas de olimpíada ou de vestibulares exigentes, que pedem ideia própria |

A escala é a mesma das listas do NM0 e do `registro/respostas.csv`.

Além do nível, cada item tem um tipo: `fluencia`, `metodos` (resolver por dois caminhos), `simplificacao`, `armadilha_simplificacao` (quando simplificar demais dá errado), `critico` (estimar antes, dado faltando ou sobrando, achar o erro), `ancora` (problema complexo, sem dicas), `fixacao` (módulos concluídos) e `diagnostico`. A composição das listas e as regras de autonomia estão em [docs/skills/design.md](docs/skills/design.md).

## Regras de decisão

| Resultado | Ação |
| --- | --- |
| Diagnóstico ≥ 85% nas questões de um módulo | Ir direto para a prova de saída; se passar, o módulo fica `dispensada` |
| Diagnóstico entre 60% e 84% | Estudar só os tópicos com erro, depois prova de saída |
| Diagnóstico < 60% | Estudar o módulo inteiro |
| Lista mista de níveis 1 a 3 com ≥ 80%, sem consulta | Pedir a prova de saída |
| Prova de saída ≥ 80% **e** autonomia (5 problemas-âncora diferentes resolvidos sem ajuda, em pelo menos 3 dias distintos; valores em `plano.yml`) | Portão cumprido: `concluida` (ou `dispensada`, se veio direto do diagnóstico). Vale para os módulos do nivelamento com portão a partir de 20/11/2026; o `MAPA.md` mostra quantas âncoras faltam |
| Prova de saída < 80% | Voltar aos tópicos com erro; nova prova, com outras questões, em no mínimo 3 dias |
| Revisão < 70% | Mudar para `em_revisao` e refazer exercícios dos tópicos com erro; nova revisão em 7 dias |
| Aviso `autonomia-em-queda` (2 ou mais das últimas 3 respostas de um módulo feito com erro ou ajuda) | Fazer uma revisão curta do módulo; se ficar abaixo de 70%, mudar para `em_revisao` |
| Aviso `fixacao-vencida` (competência de módulo feito sem prática há mais de 30 dias) | Incluir a competência na próxima lista; o sorteio de fixação (`progresso.py --sortear-fixacao N`) já a favorece |

## Como pedir ao Claude

Copie e ajuste. Peça sempre o gabarito separado, para resolver antes de conferir.

- **Diagnóstico:** "Diagnóstico do bloco A do nivelamento (NM1 a NM5): 25 questões, sem calculadora, indicando a qual módulo cada questão pertence. Gabarito separado."
- **Exercícios:** "Exercícios de NM5, nível 2, 10 questões, com 3 de contexto em computação. Gabarito separado."
- **Prova de saída:** "Prova de saída de NM5: 15 questões, 60 minutos, sem calculadora. Gabarito separado."
- **Revisão espaçada:** "Revisão de NM3 e NM4: 8 questões mistas para 15 minutos."
- **Correção:** "Corrija minhas respostas da prova de saída de NM5: [respostas]. Classifique cada erro como conceito, procedimento ou atenção."
- **Explicação de um erro:** "Na questão 7 eu errei porque [raciocínio]. Onde está a falha?"

A classificação dos erros alimenta o caderno de erros: erro de conceito pede reestudo do tópico; de procedimento, mais exercícios do mesmo tipo; de atenção, revisão do método de conferência.

## Como o diagnóstico muda a previsão

O script estima as horas de cada módulo do nivelamento pelo resultado do diagnóstico e desconta as horas já registradas:

| Diagnóstico do módulo | Horas estimadas |
| --- | --- |
| 85% ou mais | 20% do máximo: prova de saída e uma revisão |
| De 60% a 84% | 50% do máximo: só os tópicos com erro |
| Abaixo de 60%, ou sem diagnóstico | 100% do máximo |

Com essas horas e a média real das últimas quatro semanas do registro semanal (24 h por semana enquanto não houver registro), o PROGRESSO.md mostra a data prevista para terminar o nivelamento.

## Como registrar

1. Acrescente uma linha em `registro/avaliacoes.md`.
2. Depois de um diagnóstico, preencha o campo `diagnostico` de cada módulo do bloco em `registro/estado.yml` com a porcentagem de acertos daquele módulo.
3. Depois de uma prova de saída aprovada, preencha `status` e `portao` (`data`, `resultado`, `evidencia`) do módulo em `registro/estado.yml`.
4. Rode `python scripts/progresso.py`: ele mostra a última avaliação de cada módulo e avisa quando uma revisão espaçada vence ou quando uma revisão abaixo de 70% pede `em_revisao`.
