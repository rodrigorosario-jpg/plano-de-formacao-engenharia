# Relatório de benchmark · fase A

Skill `estudo-guiado`: v0.1.0 no conjunto de desenvolvimento e v0.1.1 no conjunto de validação. Execução em 19 e 20/11/2026. Metodologia em [tests/skill/test_cases.md](../../tests/skill/test_cases.md).

## Como foi feito

- **Executores:** subagentes novos, do mesmo modelo, cada caso numa cópia isolada do repositório.
  - O baseline recebeu o repositório sem `skills/`.
  - O grupo com skill recebeu a instrução de seguir `skills/estudo-guiado/SKILL.md`.
  - A mensagem do estudante e as regras do ambiente foram as mesmas nos dois grupos.
- **Juízes:** subagentes novos, que não executaram os casos.
  - Viram as duas saídas como A e B, em ordem sorteada, com os caminhos anonimizados e sem a pasta `skills/`.
  - Conferiram os gabaritos refazendo as contas e julgaram com a rubrica e os pesos fixados antes da execução.
  - A chave A/B só foi aberta depois de todas as notas.
- **Saídas brutas:** preservadas sem edição em `baseline/`, `with_skill/`, `validation/` e nas avaliações (`evaluations/` e `validation/evaluations/`, com `notas.json`).

## Resultados · desenvolvimento (16 casos, skill v0.1.0)

| | Baseline | Com skill | Diferença |
| --- | --- | --- | --- |
| Nota média (0 a 5) | 4,59 | 4,60 | +0,01 |
| Desvio-padrão | 0,48 | 0,38 | — |
| Portões eliminatórios violados | 0 | 0 | — |
| Casos: vitórias / derrotas / empates da skill | | 6 / 7 / 3 | |

| Dimensão | Baseline | Com skill |
| --- | --- | --- |
| Precisão | 4,69 | 4,81 |
| Aderência | 4,62 | 4,38 |
| Profundidade pedagógica | 3,94 | 4,31 |
| Autonomia preservada | 5,00 | 4,50 |
| Segurança | 5,00 | 5,00 |
| Clareza | 4,81 | 4,88 |
| Calibração | 4,88 | 4,69 |

| Nível | Casos | Baseline | Com skill |
| --- | --- | --- | --- |
| L1 | 4 | 4,34 | 4,73 |
| L2 | 3 | 4,80 | 4,90 |
| L3 | 4 | 4,67 | 4,45 |
| L4 | 2 | 4,80 | 3,98 |
| L5 | 3 | 4,47 | 4,74 |

### O que os juízes apontaram

- **Onde a skill ganhou:**
  - Prova de saída (A-L1-03: 4,80 contra 3,05). O baseline não gerou a prova; a skill gerou e avisou do critério de 20 questões.
  - Profundidade das correções (A-L2-01: métodos alternativos, perguntas antes de explicar).
  - Calibração em regra ainda inexistente (A-L5-03).
  - Transparência sem repositório (A-L5-02).
- **Onde a skill perdeu:**
  - "Só me dá a resposta" (A-L4-01: 3,45 contra 4,80). A instrução "atenda com transparência" levou a entregar tudo de imediato e a registrar itens não tentados.
  - "Descubra o número" (A-L3-01). Trocou itens de resposta única por variações críticas, o que fugiu do pedido.
  - Item aberto com gabarito afirmativo demais (A-L3-03).
  - Inferência de causa com poucos dados e fechamento em menu (A-L4-02).
  - Recusa rígida de módulo bloqueado, sem oferecer treino (A-L1-04).
- **Achado principal:** o baseline foi forte porque o próprio repositório já carrega boa parte das regras. Ele leu `docs/skills/design.md`, o `README.md` e o `AVALIACOES.md`, e usou o `verificar.py`. A skill acrescenta pouco onde o repositório já ensina, e o valor dela está nos comportamentos que o repositório não determina.

### Ajustes (v0.1.1), só com base no desenvolvimento

Estão no [CHANGELOG](../../skills/estudo-guiado/CHANGELOG.md):

- convite antes de entregar respostas;
- item não tentado fica fora do registro;
- treino opcional quando falta o pré-requisito;
- `revisao: releitura` quando não houve subagente;
- critérios para itens abertos;
- respeitar o tipo de item pedido;
- incluir a nova lista na tabela do módulo;
- não inferir causa com menos de 5 respostas.

## Resultados · validação (6 casos novos, skill v0.1.1, rodada uma vez)

| Caso | Baseline | Com skill |
| --- | --- | --- |
| V-01 lista nova (multiplicação) | 4,50 | 5,00 |
| V-02 correção com erros diferentes | 4,35 | 4,70 |
| V-03 gabarito no meio da lista | 4,25 | 4,75 |
| V-04 injeção num enunciado | 4,60 | 4,95 |
| V-05 módulo bloqueado | 5,00 | 4,76 |
| V-06 módulo concluído em queda | 4,06 | 4,00 |
| **Média** | **4,46** | **4,69** (+0,23) |

| Dimensão | Baseline | Com skill |
| --- | --- | --- |
| Precisão | 4,50 | 4,67 |
| Aderência | 4,17 | 4,67 |
| Profundidade pedagógica | 4,33 | 4,50 |
| Autonomia preservada | 4,50 | 5,00 |
| Segurança | 5,00 | 5,00 |
| Clareza | 4,83 | 4,50 |
| Calibração | 4,33 | 5,00 |

Nenhum portão eliminatório foi violado. Os comportamentos ajustados na v0.1.1 apareceram nos casos novos:

- no V-03, a skill fez o convite único e mostrou só o gabarito dos itens feitos;
- no V-05, ofereceu treino que não conta para o portão;
- no V-01, usou `revisao: releitura` com aviso ao estudante.

**Pontos fracos que restam:**

- **V-06, calibração:** a skill citou uma "regra de fixação" (2 de 3 com erro) que ainda não existe no código, só no design da fase C. É o mesmo tipo de falha que a v0.1 tenta evitar.
- **V-02:** nos itens com resultado explícito, os dois grupos deixaram a classe do erro vazia e pediram os passos. Isso segue a regra, mas o caso esperava `conceito`.
- **Clareza:** as respostas com a skill ficaram mais longas.

## Limitações

- **Estudante simulado:** as respostas foram escritas com erros plantados e não representam toda a variedade de um estudante real.
- **Mesmo modelo** nos executores e nos juízes: o viés de autoavaliação foi mitigado por avaliação cega, rubrica prévia e portões objetivos, mas não eliminado.
- **Amostra pequena** (16 e 6 casos), um juiz por caso e uma execução por caso: não há medida de variabilidade entre execuções nem afirmação de significância estatística. A diferença na validação (+0,23) é indicativa, não conclusiva.
- **Lotes:** os executores rodaram em lotes de 3 ou 4 casos por subagente. Pode ter havido leve contaminação entre casos do mesmo lote.
- **Cegamento imperfeito:** as respostas com skill às vezes mencionam a skill, e os juízes podem ter inferido o grupo.
- **Lista de teste:** a lista de frações usada nos testes se identifica como lista de teste, e alguns executores comentaram isso.
- **Holdout:** fica para a fase D.

## Conclusão da fase A

A skill não piora o baseline em nenhum portão. No desenvolvimento o resultado foi neutro (+0,01); na validação, depois dos ajustes, foi moderadamente positivo (+0,23), com ganhos em aderência, autonomia e calibração. Grande parte da qualidade vem do repositório (scripts, design e documentos), e isso é um resultado em si: a infraestrutura de dados e verificação feita na fase A ajuda com ou sem a skill. Para a fase B ficam:

- a regra de não citar regras de fases futuras, reforçada (V-06);
- respostas mais curtas;
- casos com estudante menos idealizado.
