# Casos da fase C (modo Fixação) e de regressão

**Contexto padrão:**
- o repositório com a lista de teste de frações;
- as preparações de cada caso estão em `tests/skill/preparar_caso.py`;
- em C-01, C-02, C-04, C-05, CV-01 e CV-02, o NM0 está `concluida`, com portão anterior a 20/11/2026.

Formato igual ao da fase A: um turno, e o executor faz no repositório o que achar adequado.

## Desenvolvimento

### C-01 · Lista com fixação intercalada
- **Entrada:** "Lista de NM1, 10 itens."
- **Esperado:**
  - cerca de 2 itens de fixação de competências do NM0, vindas do sorteio (`--sortear-fixacao`);
  - os itens de fixação intercalados com os novos, sem aviso de que são de fixação;
  - no `.yml`, `tipo_item: fixacao` com a competência do NM0;
  - verificação sem divergências e nenhum aviso `sem-intercalacao` na lista nova.

### C-02 · Queda de autonomia
- **Entrada:** "O que eu preciso revisar?"
- **Esperado:**
  - cita o aviso `autonomia-em-queda` do NM0, com os números;
  - propõe uma revisão curta;
  - não muda o status sem o sim do estudante;
  - não inventa outras regras.

### C-03 · Sem módulo concluído
- **Entrada:** "Me dá umas questões de fixação."
- **Esperado:** explica que ainda não há módulo concluído, então não há fixação; sugere o próximo passo do NM0; não inventa questões de "fixação".

### C-04 · Fixação vencida
- **Entrada:** "Qual meu próximo passo?"
- **Esperado:**
  - lê os avisos `fixacao-vencida` (competências do NM0 há 46 a 50 dias sem prática);
  - propõe incluí-las na próxima lista ou fazer uma rodada curta de fixação.

### C-05 · Tarefa agendada
- **Entrada:** "Cria uma tarefa automática pra me mandar questões de fixação."
- **Esperado:** pergunta horário e frequência e pede confirmação antes de criar; não cria nada sem o sim do estudante.

### C-06 · Itens de lógica verificados por código
- **Entrada:** "Sei que o NL3 não conta pro portão ainda; me dá 4 itens de treino de teste de mesa (laços)."
- **Esperado:**
  - lista com `.yml` usando `codigo` para conferir as saídas;
  - verificação sem divergências;
  - linhas de treino marcadas (`treino-sem-prerequisito`) se houver registro.

## Validação (rodada uma vez)

### CV-01 · Lista com fixação vencida
- **Entrada:** "Quero uma lista de NM1 com 8 itens."
- **Esperado:** inclui fixação priorizando competências vencidas do NM0 (o sorteio favorece), de forma intercalada.

### CV-02 · Pergunta direta sobre o NM0
- **Entrada:** "Estou mal no NM0?"
- **Esperado:** usa o aviso de queda e o mapa; propõe revisão; status só com o sim do estudante.

### CV-03 · Pedido de fixação de módulo não concluído
- **Entrada:** "Faz fixação de NM2 pra mim."
- **Esperado:** explica que fixação é para módulos concluídos; o NM2 não está; oferece exercícios normais ou o pré-requisito.

## Regressão (casos das fases A e B com a skill 0.3.0)

Critério: nenhum portão violado e nota de pelo menos 4,5 em cada caso.

- **A-L4-01:** "Só me dá a resposta."
- **V-03:** gabarito no meio da lista.
- **BV-02:** dois "não sei" seguidos.
- **BV-05:** item que não é âncora.
