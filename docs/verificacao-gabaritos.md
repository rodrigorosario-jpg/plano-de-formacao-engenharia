# Verificação dos gabaritos

Toda lista nova gerada pela skill tem, ao lado, um arquivo `exercicios/<código>/verificacao/<lista>.yml` que diz como conferir cada item de forma independente do gabarito. O `python scripts/progresso.py --checar` roda todos eles; um item com gabarito errado (`gabarito-divergente`) ou com mais de uma resposta válida (`item-ambiguo`) faz a validação falhar.

```yaml
lista: exercicios/NM2/1-fracoes.md
gabarito: exercicios/NM2/gabaritos/1-fracoes.md
itens:
  - item: 1
    calculo: "F(3,4) + F(1,8)"     # aritmética exata; F(a, b) é a fração a/b
  - item: 2
    predicado: "n % 6 == 0 and n % 8 == 0 and n < 40"
    variavel: n
    intervalo: [1, 200]             # exige exatamente uma resposta válida, igual à do gabarito
  - item: 3
    codigo: |                       # lógica de programação: a saída do programa é comparada ao gabarito
      print(sum(range(1, 11)))
  - item: 4
    revisao: independente           # item não calculável, conferido por outra leitura
    nota: "segunda leitura por subagente em 2026-11-20"
```

## Como o gabarito é lido

- O gabarito vem da tabela `| Nº | Resposta |`.
- O texto depois de ` (`, ` — `, `: ` ou `; ` é tratado como explicação.
- Respostas equivalentes são aceitas: `0,75` e `3/4`; `1.000` é mil; unidades, `%` e `R$` são ignorados na comparação.

## Limites de segurança

- Expressões são avaliadas sem `eval`, só com aritmética exata, e com limite de potência (expoente inteiro até 1000, base até 1.000.000): `9**9**9` é recusado em vez de travar.
- Intervalos de `predicado` têm no máximo 1.000.000 de valores.
- Código roda num processo Python isolado (`python -I`), com tempo máximo de 5 segundos.

## Conferência das listas antigas do NM0 (26/11/2026)

As listas 1 a 4 do NM0 não têm `.yml` ([exceção registrada](../exercicios/sem-verificacao.yml)). Os 440 itens foram conferidos uma vez por quatro agentes independentes, um por lista: cada item foi resolvido pelo enunciado, com as contas em Python, antes da comparação com o gabarito. Nenhuma resposta estava errada. Quatro itens foram ajustados:

- subtração 98 tinha 9 respostas certas e o gabarito dava só uma; agora lista todas;
- multiplicação 96 e 97 e divisão 105 pediam um padrão ou exemplos que o gabarito não mostrava; agora mostra.

