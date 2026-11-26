# Casos de validação · fase B

Mesmo formato e mesmo contexto padrão dos casos de desenvolvimento. Estes casos não são usados para ajustar a skill.

## BV-01 · Início em erro de procedimento
- **Entrada:** "Errei o item 7 (2/3 ÷ 4/5 = 8/15). Me ajuda a ver onde errei?"
- **Esperado:** inicia o diagnóstico com uma pergunta aberta; não explica de cara a regra de inverter e multiplicar.

## BV-02 · Dois "não sei" seguidos
- **Conversa adicional:**
  > **Assistente:** Releia sua resolução. Algum passo te deixa em dúvida?
  > **Estudante:** não sei
  > **Assistente:** Olhe a passagem de 1/2 + 1/3 para (1+1)/(2+3). O que você fez com os denominadores?
  > **Estudante:** somei. não sei se pode
- **Esperado:** degrau 2, com uma pergunta de conceito (o que o denominador representa); uma pergunta só.

## BV-03 · Desistência no meio da escada
- **Conversa adicional:** no degrau 2, o estudante responde "cansei, para".
- **Esperado:** respeita a vontade; oferece encerrar com uma explicação curta e um gêmeo, ou retomar depois; registra o que aconteceu, com a ajuda no degrau alcançado.

## BV-04 · Formulação certa, mas incompleta
- **Conversa adicional:**
  > **Estudante:** entendi, tem que ter o mesmo denominador
- **Esperado:** pede que ele aplique a ideia no item original, ou que diga por que é assim, antes de encerrar.

## BV-05 · Pedido de registro de âncora em sessão
- **Entrada:** "Fiz o item 6 sozinho e acertei 3/8. Conta como âncora?"
- **Esperado:**
  - consulta o `.yml`: o item 6 é do tipo `critico`, não `ancora`;
  - explica que ele não conta para a autonomia;
  - registra o acerto com o tipo certo, sem inflar.

## BV-06 · Pergunta sobre o critério do portão
- **Entrada:** "Quantas âncoras faltam pra eu fechar o NM0?"
- **Esperado:** lê o `MAPA.md` (Autonomia: 0/5 em 0/3 dias); explica o critério vigente (prova de saída com 80% ou mais e 5 âncoras em 3 dias); não inventa.
