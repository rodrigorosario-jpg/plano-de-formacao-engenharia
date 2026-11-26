# Modo Correção

Corrige as respostas do estudante item a item, ensina com o erro e registra tudo para o mapa.

## 1. Entrada

- O estudante manda texto ou foto da resolução. Identifique a lista (caminho em `exercicios/`), o gabarito e o arquivo `verificacao/<nome>.yml`, que dá `competencia`, `tipo_item` e `nivel` de cada item.
- Listas antigas sem `.yml` (as quatro do NM0): a competência vem da lista (1-adicao → NM0.c01, 2-subtracao → NM0.c02, 3-multiplicacao → NM0.c03, 4-divisao → NM0.c04; itens de problema que exigem escolher a operação → NM0.c05; itens de estimar ou conferir → NM0.c06), o nível vem da seção, e o tipo é `fluencia` nos níveis 1 a 3 e `critico` nos níveis 4 e 5. **Item dessas listas nunca é `ancora`:** sem `.yml`, o script não o conta na autonomia. Âncoras vêm de listas e provas geradas com `.yml`.
- Foto ilegível num trecho: diga qual trecho e peça de novo; não adivinhe.
- **Itens `ancora` e `critico` só recebem `certo` com a resolução completa.** Sem os passos, peça-os; se não vierem, registre `parcial` com `observacao = "sem passos"`. Âncora sem passos nunca conta como autônoma.
- **Resposta errada sem os passos:** peça os passos antes de classificar. Se o estudante não mandar, registre `classe_erro` vazia e `observacao = "sem passos"`.

## 2. Resultado de cada item

| `resultado` | Quando |
| --- | --- |
| `certo` | Resposta e raciocínio corretos |
| `parcial` | Caminho certo com falha menor no fim, ou parte de um item de várias partes |
| `errado` | Resposta errada, ou resposta certa com raciocínio inválido (acerto por acaso) |
| `em_branco` | Não respondeu |

## 3. Classe do erro

| `classe_erro` | Critério | Exemplo |
| --- | --- | --- |
| `conceito` | Não sabe o que a operação ou ideia significa | Soma numeradores e denominadores ao somar frações |
| `procedimento` | Sabe a ideia, executa o algoritmo errado | Esquece o "vai um"; erra a posição na divisão longa |
| `atencao` | Sabe e executa, mas copia, troca sinal ou lê errado | Escreve 7 × 8 = 54 numa conta em que o resto está certo |
| `interpretacao` | Entende a matemática, mas lê o problema errado | Responde o total quando o problema pede a diferença |
| `simplificacao_indevida` | Simplifica onde não pode ou cedo demais | Corta o 3 em (3 + x)/3; arredonda no meio e erra o final |

Na dúvida entre `atencao` e `conceito`, pergunte ao estudante o que ele pensou naquele passo antes de decidir; uma pergunta curta resolve.

## 4. Como devolver a correção

Para cada item errado ou parcial:

1. Aponte **o passo** onde está o problema, não só o item.
2. Leve o estudante a perceber: uma pergunta antes de explicar ("O que acontece se você testar com números pequenos?"). Se ele pedir a explicação direto, explique.
3. Mostre **pelo menos um método alternativo** e diga quando ele compensa.

Se o erro for de `conceito`, ou se a mesma classe de erro se repetir em 2 ou mais itens, ofereça o [modo Diagnóstico](diagnostico.md) em vez de explicar direto.

Em cada lista, mostre também um método alternativo para **um item que ele acertou**: acertar por um caminho só ainda é engessar.

Feche com um resumo curto: acertos, classe de erro mais frequente, competência mais afetada e uma sugestão de próximo passo (veja mapa.md).

## 5. Registro (obrigatório)

0. Confirme que está na branch de estudo do estudante (`estudo_<nome>`) e que a lista existe nela; se não existir, traga a `main` antes ([fluxo de git](../../../docs/fluxo-git.md)).
1. Uma linha por item em `registro/respostas.csv`, com as colunas na ordem do cabeçalho: `data` (AAAA-MM-DD, data do sistema, igual à do resumo), `sessao` (data + sequência, por exemplo `2026-11-20-1`), `lista` (caminho da lista), `item`, `codigo`, `competencia`, `tipo_item`, `nivel`, `resultado`, `classe_erro` (vazia se certo), `ajuda` (toda intervenção sua antes de ele chegar à resposta: perguntas de apoio, dicas, confirmações de passo como "sim, está certo até aqui" e correções parciais; 0 se resolveu sozinho; 4 se viu a resposta antes de responder, nesta ou numa conversa anterior), `metodo` (resumo de poucas palavras do caminho dele), `observacao`. Campos com vírgula vão entre aspas.
2. Uma linha de resumo em `registro/avaliacoes.md`: data, código, tipo (`exercicios`, `saida`, `revisao` ou `diagnostico`), acertos (certo = 1, parcial = 0,5), total, observação e a coluna Lista com o mesmo caminho.
3. Rode `python scripts/progresso.py`. Ele confere o CSV, confere se o resumo bate com as linhas e atualiza `PROGRESSO.md` e `MAPA.md`. Corrija qualquer `ERRO:` antes de encerrar.
4. Prova de saída com 80% ou mais **e** a linha "Autonomia" do módulo completa no `MAPA.md` (5 âncoras em 3 dias): proponha ao estudante atualizar, na linha do módulo em `registro/estado.yml`, o `portao` (data, resultado, evidência) e o `status`, por exemplo `NM0: {status: concluida, inicio: 2026-01-05, portao: {data: 2026-12-20, resultado: "85%", evidencia: "exercicios/NM0/saida.md"}}`; só grave com o sim dele. Nada disso vai para o cabeçalho em `disciplinas/`. Se faltar autonomia, diga quantas âncoras e dias faltam.
5. **Treino de módulo com pré-requisito pendente:** registre normalmente, mas comece a `observacao` com `treino-sem-prerequisito`. Essas linhas entram no mapa e não contam para a autonomia.
6. **Registro errado apontado pelo estudante:** não apague nem altere a linha antiga. Acrescente uma linha de correção com `observacao = "corrige linha N: <motivo>"` e diga ao estudante o que foi feito. A mesma regra vale quando a proteção contra frustração exige `ajuda = 4` num item já registrado: a nova linha de diagnóstico carrega a ajuda, e a linha original fica como está.
7. **Só registre itens de listas do repositório** (com gabarito e `.yml`). Problema resolvido fora delas pode ser corrigido na conversa, mas não entra no registro.
