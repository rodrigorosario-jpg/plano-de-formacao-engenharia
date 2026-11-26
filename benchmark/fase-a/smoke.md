# Teste de fumaça · fase A

Roteiro da seção "Como validar" do [design](../../docs/skills/design.md), executado em 19/11/2026 numa cópia limpa do repositório (com a skill), seguindo `skills/estudo-guiado/` pelo próprio Claude da sessão principal. O estudante foi simulado.

| Passo | O que foi feito | Resultado | Situação |
| --- | --- | --- | --- |
| 1. "Lista de NM0, divisão, 12 itens" | Lista `exercicios/NM0/5-divisao-guiada.md`, com gabarito e `verificacao/5-divisao-guiada.yml`. Composição: 5 de fluência, 1 de métodos, 2 de simplificação, 1 armadilha, 2 críticos e 1 âncora | `verificar.py`: "Verificação sem divergências."; `--checar` com código 0 | ✅ |
| 2. Respostas com erros plantados (conceito no item 3, atenção no 12, simplificação indevida no 8) | 12 linhas em `registro/respostas.csv`; resumo 9/12 em `avaliacoes.md`, com a coluna Lista | Classes registradas conforme o plantado; `--checar` com código 0 | ✅ |
| 3. `progresso.py --checar` e `MAPA.md` | Mapa gerado | NM0.c04 aparece 🔴 fraca (6/9, conceito) | ✅ depois de correção (abaixo) |
| 4. "Qual meu próximo passo?" | Leitura do mapa conforme `references/mapa.md` | Próximo passo: lista focada em divisão (NM0.c04), com itens de métodos e críticos; NM0.c05 e NM0.c06 seguem `sem_dados`, com poucas respostas | ✅ |
| Caso de erro: linha com `NM0.c99` e `ajuda = -1` | Linha acrescentada à mão | `ERRO: csv-invalido: linha 14, coluna competencia...` e `...coluna ajuda...`; código 1 | ✅ |
| Extra: resumo com acertos errados (10/12) | Linha de `avaliacoes.md` alterada | `ERRO: resumo-divergente: ... avaliações 10/12, respostas 9/12`; código 1 | ✅ |

## Defeito encontrado e corrigido

Na primeira execução do passo 3, NM0.c04 apareceu 🟡 em_formacao. O erro de conceito era o item 3 e, pela regra "conceito nas 3 últimas respostas", a ordem dos itens dentro da mesma lista escondia o erro. A regra passou a considerar as 3 últimas respostas **ou** todas as respostas do dia mais recente. O teste `test_conceito_na_mesma_sessao_conta_como_recente` falhou antes da correção e passou depois. O design (6.2) e o `references/mapa.md` foram atualizados.
