# ADR 0008 · Repositório público separado

- **Status:** Aceita
- **Data:** 26/11/2026

## Contexto

O estudante quer publicar o Knowledge Core como portfólio e para reuso. O repositório atual tem, no histórico, o e-mail pessoal em commits feitos pelo site, commits com autor "Claude" e versões antigas com resultados de estudo; e a branch de estudo ficaria pública junto.

## Decisão

Criar um repositório público novo, que recebe só a árvore da `main`, num histórico próprio e limpo, pela conta do estudante. Este repositório continua privado, com a `main` e as branches de estudo. `scripts/publicar.sh` leva a `main` para o público e recusa publicar dados de estudo. Licenças: MIT no código e CC BY 4.0 no conteúdo ([LICENSE](../../LICENSE), [LICENSE-CONTEUDO.md](../../LICENSE-CONTEUDO.md)).

## Alternativas consideradas

- Reescrever o histórico deste repositório e torná-lo público: exige forçar o envio de todas as branches e tirar a branch de estudo antes.
- Publicar como está: expõe e-mail, resultados e a branch de estudo.

## Consequências

- O público não tem o histórico de desenvolvimento; cada publicação é um commit novo.
- Mudanças de estrutura continuam sendo feitas aqui, por pull request na `main`, e depois publicadas.
