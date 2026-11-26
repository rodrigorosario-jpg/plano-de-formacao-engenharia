# Modo Fixação

Mantém vivo o que já foi concluído. O aprendizado não termina quando o módulo termina: questões de módulos feitos (`concluida`, `dispensada` ou `em_revisao`) voltam, misturadas com o conteúdo novo, pela trilha inteira.

## 1. Sorteio

```
python scripts/progresso.py --sortear-fixacao N
```

O script devolve até N competências de módulos feitos. O peso de cada uma depende da situação no mapa (em queda e fraca pesam mais) e do tempo desde a última prática. Use o sorteio do script; não escolha as competências por conta própria. Se o script disser que não há módulo concluído, não existe fixação a fazer: diga isso ao estudante.

## 2. Onde as questões entram

- **Em toda lista** de um módulo em andamento, uma parcela de `fixacao_proporcao` (em `plano.yml`; padrão de 20%) vem do sorteio. Por exemplo, uma lista de 10 itens leva 2 de fixação.
- **Intercaladas**, nunca agrupadas no fim: distribua as questões de fixação entre os itens novos. Quando a lista tiver mais de uma competência, evite dois itens seguidos da mesma competência. O `--checar` avisa `sem-intercalacao` quando há 3 seguidos (fonte F2 em `docs/skills/03_research_and_references.md`).
- **Sem aviso no enunciado** de que a questão é de fixação: ela aparece como qualquer outra. No `.yml`, o item recebe `tipo_item: fixacao` e a competência sorteada.
- A fixação **não substitui** as revisões de 7, 30 e 90 dias depois do portão. Ela é um acréscimo.

## 3. Avisos do `--checar`

| Aviso | O que fazer |
| --- | --- |
| `autonomia-em-queda: <módulo>` | Diga ao estudante que o módulo voltou a falhar, com os números do aviso, e proponha uma revisão curta (5 a 10 questões) dele. Se a revisão ficar abaixo de 70%, proponha mudar o status para `em_revisao` em `registro/estado.yml`, só com o sim dele |
| `fixacao-vencida: <competência>` | A competência está há mais de `fixacao_vencida_dias` dias sem prática. Garanta que ela entre na próxima lista; o sorteio já tende a escolhê-la |
| `sem-intercalacao: <lista>` | Reordene os itens da lista antes de entregar |

## 4. Registro

Correção e registro seguem `correcao.md`, com `tipo_item = fixacao` e a competência do módulo de origem (por exemplo, `NM0.c04` numa lista de NM3). O mapa e a regra de queda usam essas linhas.

## 5. Tarefa agendada (opcional)

Você pode **oferecer**, uma vez, uma tarefa agendada que, numa janela da rotina do estudante (por exemplo, no almoço), sorteia de 3 a 5 questões de fixação e as deixa prontas. Só crie com o sim explícito dele e nos horários que ele escolher. Sem módulo concluído, não ofereça.
