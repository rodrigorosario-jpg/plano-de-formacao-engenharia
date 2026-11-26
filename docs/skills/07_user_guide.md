# 07 · Guia de uso da skill estudo-guiado

Para o estudante. Explica como usar a skill no dia a dia, sem precisar ler o resto da documentação.

## Antes de começar

- A skill está instalada na sua conta do claude.ai.
- Abra uma conversa no projeto "Estudos". A skill encontra o repositório `plano-de-estudos` ou pede para anexá-lo.
- Tudo o que ela registra fica no repositório. No fim de cada sessão, ela pergunta se pode fazer o commit: diga sim, senão o registro se perde quando a sessão acaba. O andamento (respostas, avaliações e o `status` de cada módulo, em `registro/estado.yml`) vai para a sua branch de estudo (`estudo_<nome>`; na primeira vez, a skill oferece criá-la) e as listas novas para a `main` ([fluxo de git](../fluxo-git.md)).

## O que pedir

| Você quer | Diga algo como | O que acontece |
| --- | --- | --- |
| Treinar | "Lista de NM0, divisão, 12 itens" | Lista mista e verificada, com gabarito separado. Se já houver módulo concluído, uma parte é de fixação |
| Ser corrigido | "Corrige a lista 5 do NM0: 1) 12, 2) ..." ou uma foto da folha | Correção item a item, com o tipo de cada erro e outros jeitos de resolver; tudo registrado |
| Entender um erro | "Não entendi onde errei no item 3" | Perguntas uma por vez até você mesmo achar a lacuna |
| Saber onde está fraco | "Onde estou fraco?", "o que faço hoje?" | Leitura do `MAPA.md` e um próximo passo concreto |
| Revisar o que já fechou | "O que preciso revisar?" | Avisos de queda e de fixação vencida, mais uma revisão curta |
| Fazer prova | "Prova de saída do NM0" | De 15 a 20 questões, sem consulta, com pelo menos uma âncora |

## Como responder

- **Mostre os passos.** Sem eles, a skill não consegue dizer se o erro foi de conceito, de atenção ou de simplificação, e pede os passos de novo.
- Texto ou foto da folha servem igualmente.
- Se quiser a resposta sem tentar, pode pedir. A skill convida você a tentar uma vez; se insistir, entrega, mas o item fica registrado com ajuda máxima.

## Como ler o MAPA.md

| Situação | Quer dizer |
| --- | --- |
| 🔴 fraca | Erro de conceito recente, ou menos de 60% de acerto |
| 🟡 em formação | Acertando, mas com ajuda ou com poucas respostas |
| 🟢 forte | Pelo menos 5 respostas recentes, 85% de acerto e quase sempre sem ajuda |
| 🟠 em queda | Módulo já concluído que voltou a falhar |
| ⚪ sem dados | Menos de 3 respostas |

A linha **"Autonomia"** de cada módulo mostra quantos problemas-âncora você já resolveu sozinho e em quantos dias diferentes. Para fechar um módulo do nivelamento são necessários **80% na prova de saída e 5 âncoras sem ajuda em 3 dias diferentes**.

## O que a skill nunca faz

- Entregar a resposta antes de você tentar, sem avisar.
- Registrar autonomia que você não mostrou ali na conversa.
- Mudar o status de um módulo sem o seu sim.
- Fazer commit ou push sem você pedir.
- Seguir instruções escritas dentro de enunciados, arquivos ou textos colados.
