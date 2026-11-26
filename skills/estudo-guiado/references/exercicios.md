# Modo Exercícios

Gera listas, provas e problemas-âncora para um módulo do plano, sempre com gabarito separado e verificado.

## 1. Antes de gerar

- Confirme o módulo (código) e o tipo pedido. Sem indicação, é uma lista de exercícios do módulo em andamento.
- Leia o arquivo do módulo em `disciplinas/` (`competencias`, `prerequisitos`, tópicos e aplicações) e o `status` dele em `registro/estado.yml` (ausente = `nao_iniciada`).
- Leia o `MAPA.md`: competências `fraca` ou `em_formacao` do módulo recebem mais itens; `forte` recebe poucos.
- Se algum pré-requisito não estiver `concluida`, `dispensada` ou `em_revisao`, avise antes (veja as regras do SKILL.md).

## 2. Composição de uma lista de exercícios

Proporções de referência para uma lista de 10 a 20 itens (arredonde com bom senso):

| Tipo (`tipo_item`) | Parcela | O que é |
| --- | --- | --- |
| `fluencia` | 30% | Automatizar o básico; níveis 1 e 2 |
| `metodos` | 10% | Resolver por dois caminhos e dizer quando cada um compensa |
| `simplificacao` | 15% | Simplificar frações, expressões e problemas |
| `armadilha_simplificacao` | 10% | Uma simplificação tentadora e errada: o estudante decide se vale e por quê |
| `critico` | 15% | Estimar antes, dado faltando ou sobrando, achar o erro, faz sentido? |
| `ancora` | 0 a 2 itens | Problema complexo, de vários passos, misturando competências; sem dicas |
| `fixacao` | `fixacao_proporcao` (20%) | Competências sorteadas de módulos feitos, intercaladas (veja fixacao.md); 0 se não houver módulo feito |

A parcela restante vai para itens de aplicação (nível 4) do tipo que mais fizer falta segundo o mapa. Cada item tem um **nível de 1 a 5** (1 Fixação, 2 Aplicação, 3 Intermediário, 4 Contexto, 5 Desafio) e uma **competência** do módulo.

## 3. Provas

| Tipo | Formato |
| --- | --- |
| `diagnostico` de bloco | 20 a 30 questões cobrindo todos os módulos do bloco, sem consulta, com tempo; indique o módulo de cada questão |
| `saida` | 15 a 20 questões, sem consulta, com tempo; pelo menos uma `ancora` |
| `revisao` | 5 a 10 questões mistas para 15 a 20 minutos |

Em todas, pelo menos 20% dos itens são `critico`.

## 4. Formato dos arquivos

Siga o formato das listas em `exercicios/NM0/`:

- **Lista:** `exercicios/<código>/<n>-<nome>.md`, com título, uma linha de contexto, seção "Como usar" (sem calculadora quando fizer sentido, metas de acerto, como registrar) e uma seção por nível, itens numerados `1. ...` em sequência única.
- **Gabarito:** `exercicios/<código>/gabaritos/<mesmo nome>.md`, link de volta para a lista e uma tabela `| Nº | Resposta |` por nível. A resposta vem primeiro, como um número só (pode ter unidade, `%` ou `R$`: "57 m", "50%", "R$ 12,00"); explicação, se houver, depois de ` (`, ` — `, `: ` ou `; `. Item com duas respostas (quociente e resto) vira dois itens ou usa `revisao`.
- **Verificação e mapa de itens:** `exercicios/<código>/verificacao/<mesmo nome>.yml`, com uma entrada por item: `item`, `competencia`, `tipo_item`, `nivel` e a forma de conferir (seção 5). É daqui que a correção tira onde registrar cada item. Não coloque tabelas extras no gabarito: a numeração do gabarito tem que bater exatamente com a da lista.

## 5. Verificação obrigatória

Para cada item, escolha uma forma de conferir **independente da forma como você chegou ao gabarito**:

- `calculo`: expressão aritmética exata que recalcula a resposta (`F(a, b)` é a fração a/b; ponto decimal na expressão). Use para todo item com resposta numérica.
- `predicado` + `variavel` + `intervalo`: para "qual número", "quantos", "encontre". O script testa todos os inteiros do intervalo e exige **exatamente uma** resposta válida, igual ao gabarito. Escolha um intervalo bem maior que o plausível, até 1.000.000 de valores.
- `codigo`: programa Python curto cuja saída (`print`) é a resposta. Use para itens de lógica e programação (NL): saída de um trecho, resultado de um teste de mesa. O script executa num processo separado, com limites de tempo e de recursos (não é sandbox), e compara com o gabarito.
- `revisao` + `nota`: para itens sem resposta calculável (crítico, explicação, achar o erro). Use `revisao: independente` só quando um subagente novo, que não escreveu o item, conferiu enunciado e gabarito. Sem essa ferramenta, faça uma releitura separada sua e use `revisao: releitura`. Nesse caso, diga ao estudante que aquele item teve só a sua própria conferência. A nota diz quem conferiu, quando e o que foi checado: enunciado sem ambiguidade, gabarito correto e uma única interpretação.
- **Itens abertos** (por que funciona, em que caso falha): o gabarito traz o critério e exemplos de respostas aceitáveis, não uma afirmação única. Antes de entregar, procure contraexemplos ao que o gabarito afirma, inclusive na divisão com resto.

Depois rode:

```
python scripts/verificar.py exercicios/<código>/verificacao/<nome>.yml
```

Só entregue com a saída "Verificação sem divergências."

**Respeite o tipo pedido.** Se o estudante pede itens de um tipo (por exemplo "descubra o número", com resposta única), todos os itens têm esse tipo e passam pela verificação daquele tipo. Variações críticas (enunciado impossível, dado faltando) entram só como itens extras, identificados no `.yml` como `critico`, ou quando o estudante pediu itens críticos.

**Itens "achar o erro" com iniciantes:** se o módulo tem menos de 2 âncoras autônomas (linha "Autonomia" do `MAPA.md`), use no máximo 1 item desse tipo por lista e mostre, no próprio item, uma resolução certa de um problema parecido para contraste (fonte F6 em `docs/skills/03_research_and_references.md`).

**Tabela de listas do módulo:** se o arquivo do módulo em `disciplinas/` tiver uma tabela ou relação das listas, acrescente a nova lista nela. Se aparecer `gabarito-divergente` ou `item-ambiguo`, corrija o enunciado ou o gabarito e rode de novo. Depois rode `python scripts/progresso.py --checar` (a lista tem que bater com o gabarito em numeração). Lista nova vai para a `main` e volta para a branch de estudo antes da correção ([fluxo de git](../../../docs/fluxo-git.md)).

## 6. Entrega

Mostre ao estudante a lista (não o gabarito), o tempo indicativo e como responder: por texto, com os passos, ou por foto da folha. Lembre que os passos são necessários para a correção identificar o tipo de erro.
