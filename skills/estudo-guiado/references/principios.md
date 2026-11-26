# Princípios de ensino

Valem em todo modo. Eles são o motivo da skill existir: um item ou uma correção que não exercita nenhum deles é um item mais fraco do que poderia ser.

**Antes de ler ou gravar qualquer arquivo, siga o [fluxo de git](../../../docs/fluxo-git.md)** (leia a versão da `main`: `git show origin/main:docs/fluxo-git.md`). O andamento é lido e gravado na branch de estudo do estudante (`estudo_<nome>`); listas e demais mudanças de estrutura vão para a `main`. Numa branch criada da `main`, valide só com `python scripts/progresso.py --checar`. Se você já leu o `MAPA.md` em outra branch, leia de novo depois de trocar.

## 1. Pensamento crítico em toda a janela de aprendizado

Não é uma etapa no fim; aparece dentro de listas, correções e conversas:

- **Estimar antes de calcular:** "Antes de fazer a conta, o resultado fica perto de quanto?"
- **Faz sentido?** Depois de um resultado, pergunte se ele é plausível (unidade, ordem de grandeza, sinal).
- **Por que funciona?** Peça a razão de um procedimento, não só a execução.
- **Em que caso falharia?** Peça um contraexemplo ou o limite de validade de uma regra.
- **Dado faltando ou sobrando:** problemas em que é preciso perceber que falta informação, ou descartar a que sobra.
- **Achar o erro:** uma resolução com um erro plantado para o estudante localizar e explicar.

## 2. Várias técnicas para o mesmo resultado

O estudante quer aprender métodos diferentes, sem ficar engessado.

- Ao corrigir, mostre outro caminho além do usado (conta armada, decomposição, estimativa e ajuste, desenho, propriedade, regra de três, equação).
- Diga **quando cada caminho compensa**: rapidez, menos risco de erro, generalização.
- Às vezes peça: "Resolva de novo por um caminho diferente do seu."
- Nenhum método é apresentado como o único certo.

## 3. Simplificação, nas duas leituras

- **Fluência:** muitos exercícios de simplificar frações, expressões e problemas até ficar natural.
- **Armadilhas:** exercícios que mostram quando simplificar demais dá errado, por exemplo cortar termos de uma soma numa fração, arredondar no meio do cálculo, trocar um problema por um parecido que não é equivalente, ignorar uma condição do enunciado.

## 4. Apoio que não tira o mérito

- No início, o estudante recebe apoio para não se frustrar; o apoio é registrado (`ajuda`), nunca escondido.
- A régua das avaliações é a mesma do começo ao fim.
- Ajude com perguntas antes de explicar: a melhor ajuda é a que leva o estudante a perceber sozinho.

## 5. Aplicação

Quando o módulo pede, os itens têm contexto real: computação, física, engenharia, finanças pessoais, dados. As seções "Aplicações" de cada arquivo em `disciplinas/` dizem quais contextos usar.
