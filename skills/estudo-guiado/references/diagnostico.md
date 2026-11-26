# Modo Diagnóstico

Conduz perguntas estruturadas até o **próprio estudante** descobrir onde está a lacuna. Use quando a correção mostra um erro de `conceito` ou `procedimento`, quando o mesmo erro se repete, ou quando o estudante pede ("não entendi onde errei").

## 1. A escada de apoio

Comece pelo degrau mais aberto e só suba quando o estudante não avançar.

| Degrau | Tipo | Exemplo |
| --- | --- | --- |
| 0 | Reflexão | "Releia sua resolução. Algum passo te deixa em dúvida?" |
| 1 | Foco | "Olhe a passagem da linha 2 para a 3. O que mudou?" |
| 2 | Pergunta de conceito | "O que significa dividir por uma fração?" |
| 3 | Caso menor | "Faça a mesma coisa com números pequenos: 1 ÷ ½." |
| 4 | Exemplo resolvido parcial | Mostre os primeiros passos de um problema parecido, omitindo os finais, e peça que o estudante explique o passo mostrado e complete o resto |

- **Quanto tempo em cada degrau.** Leia a linha "Autonomia" do módulo no `MAPA.md`:
  - com menos de 2 âncoras autônomas, uma tentativa por degrau basta para subir;
  - com 2 ou mais, dê duas tentativas antes de subir.
- **Pedidos genéricos antes dos específicos.** Nos degraus 0 a 2, prefira "por que esse passo vale?" ou "o que você estava tentando fazer aqui?" antes de apontar o conceito.
- **Uma pergunta por vez.** Espere a resposta antes da próxima.
- **Não responda pela pergunta.** Se o estudante devolver a pergunta ("não sei, me fala"), suba um degrau; não pule para a explicação.

## 2. Proteção contra frustração

Se o estudante passar do degrau 4 sem avançar:

1. Feche o problema com uma explicação curta, de 3 a 5 linhas, centrada no passo que travou.
2. Entregue um **problema gêmeo**: mesma estrutura, outros números, para ele tentar sozinho em seguida.
3. Registre uma linha de diagnóstico com `resultado = errado` e `ajuda = 4`. Não altere a linha original do item, que já está no CSV.

Errar e travar faz parte do processo; desistir não pode ser a saída. Mantenha o tom de quem está do lado do estudante.

## 3. Encerramento

A conversa termina quando o estudante formula, com as palavras dele, onde estava a lacuna. Não formule por ele. Se a formulação ficar vaga, peça um exemplo: "Mostra isso num caso com números."

Se a lacuna estiver numa competência de pré-requisito (uma competência de módulo anterior em `prerequisitos`), aponte o módulo e o código da competência (por exemplo, NM1.c03) e sugira voltar a ela antes de seguir. **Registre isso de fato**: no arquivo de `registro/diagnosticos/`, na seção de encaminhamento. Nunca diga "vou anotar" sem anotar.

## 4. Registro

1. Crie `registro/diagnosticos/AAAA-MM-DD-<código>.md` com: data, item de origem, hipótese inicial (sua), perguntas feitas e degrau alcançado, a formulação do estudante (citação literal) e o encaminhamento.
2. Acrescente uma linha em `registro/respostas.csv` com:
   - `tipo_item = diagnostico`;
   - a competência onde a lacuna foi encontrada;
   - `resultado = certo` se ele chegou à formulação, `errado` se precisou da proteção contra frustração;
   - `ajuda` igual ao degrau mais alto alcançado (0 a 4).
3. Rode `python scripts/progresso.py` e confira que não aparece `ERRO:`.
