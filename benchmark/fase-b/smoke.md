# Teste de fumaça · fase B (modo Diagnóstico)

Executado em 20/11/2026 numa cópia limpa do repositório (com a skill 0.2.0), seguindo `skills/estudo-guiado/references/diagnostico.md`. Quem conduziu foi o Claude da sessão principal; o estudante foi simulado.

| Passo | O que foi feito | Resultado | Situação |
| --- | --- | --- | --- |
| Estado inicial | Item 1 da lista de frações registrado como errado (`conceito`) | NM2.c03 🔴 fraca | ✅ |
| Escada | Degrau 0 ("não sei"), degrau 1 ("juntar tudo") e degrau 2 (pergunta de conceito sobre o denominador) | O estudante formulou a lacuna no degrau 2 | ✅ |
| Formulação | Citada literalmente, sem ser reescrita pelo assistente | "não dá pra somar pedaço de tamanho diferente, primeiro tem que deixar do mesmo tamanho…" | ✅ |
| Registro | `registro/diagnosticos/2026-11-20-NM2.md` (hipótese, perguntas, degraus, formulação, encaminhamento) e uma linha no CSV (`tipo_item = diagnostico`, `ajuda = 2`, `resultado = certo`) | `progresso.py --checar` com código 0 | ✅ |
| Mapa | Regenerado | NM2.c03 segue 🔴 fraca (1/2): o erro de conceito do mesmo dia continua recente, o que é correto até o problema gêmeo ser resolvido. Autonomia do NM2: 0/5 | ✅ |

**Observação:** a linha de diagnóstico não altera a linha original do item, como manda a regra da v0.2.0.
