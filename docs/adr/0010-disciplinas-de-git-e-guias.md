# ADR 0010 · Git no plano: NG1, G5, guias e laboratório

- **Status:** Aceita
- **Data:** 26/11/2026

## Contexto

O Mapa rev74 não tem Git em nenhuma disciplina, e o próprio plano depende dele: o andamento vive numa branch de estudo, a estrutura entra por pull request e a publicação passa por um script. O estudante pediu uma árvore de estudos de Git em 12 níveis, do básico à engenharia de versionamento, com exercícios e desafios aplicados a este repositório.

Duas coisas não cabem no formato dos outros módulos de nivelamento:

- **Listas numéricas:** os exercícios de Git são estados de repositório, não contas. Um gabarito de texto não confere se um conflito foi resolvido.
- **Problemas-âncora:** a regra de autonomia (`autonomia_n` âncoras em `autonomia_dias_distintos` dias) depende dessas listas.

## Decisão

- **NG1 · Git essencial**, no nivelamento (bloco V), com os níveis 1 a 5 e seis competências. Decisão do estudante em 26/11/2026, entre três opções: NG1 + G5, só uma disciplina na graduação, ou só um guia fora da trilha.
- **G5 · Git avançado e engenharia de versionamento**, na graduação (eixo Infraestrutura, semestre 3, depois de NG1 e G1), com os níveis 6 a 12. O portão é um projeto defendido oralmente.
- **Guias em `guias/NG1/` e `guias/G5/`**, um por nível, todos com as mesmas 17 seções, mais o roteiro geral e o glossário. Ficam fora de `docs/`, porque são conteúdo de estudo, não documentação do repositório.
- **Laboratório (`scripts/laboratorio_git.py`):** 10 cenários dos níveis 1 a 5, cada um preparado num repositório descartável e conferido pelo estado final. Os cenários são código revisado do script, nada é lido do conteúdo. O script recusa pastas dentro de repositórios e pastas não vazias, roda o git sem configuração global, hooks ou rede, e não apaga arquivos de quem estuda.
- **Autonomia pelo laboratório:** `plano.yml` lista a NG1 em `autonomia_por_laboratorio`. O `--checar` dispensa as âncoras só para os módulos listados, e recusa código que não seja de um módulo do nivelamento. O portão da NG1 pede os 10 cenários resolvidos sem consulta em pelo menos 3 dias distintos, a mesma exigência de espaçamento das âncoras, com as datas anotadas na evidência do portão.
- **Exercícios que reescrevem histórico** (níveis 6 e 7) rodam só numa cópia descartável, sem remoto. Nunca na `main`, na branch de estudo ou com push para o GitHub deste repositório.

## Alternativas consideradas

- **Uma disciplina só, na graduação:** deixaria o estudante usando a branch de estudo durante todo o nivelamento sem saber o que um merge faz.
- **Guia fora da trilha, sem portão:** nada garantiria que o conteúdo fosse estudado nem conferido.
- **Listas numéricas com perguntas sobre comandos:** conferem memória, não a habilidade de deixar um repositório no estado certo.
- **Guias em `docs/git/`:** misturaria material de estudo com a documentação do repositório.

## Consequências

- A `ordem` das disciplinas depois da NG1 e da G5 aumentou em 1 ou 2. Os códigos não mudam ([ADR 0003](0003-codigos-como-identificadores.md)).
- A skill de estudo guiado não gera listas para a NG1: o estudo usa os guias e o laboratório. Ela continua registrando o portão e o andamento.
- Os níveis 6 a 12 não têm conferência por script. A G5 é conferida pelo projeto e pela checklist de cada guia.
- O laboratório executa git na máquina de quem estuda. O risco está no [modelo de segurança](../arquitetura/seguranca.md), junto com o de `verificar.py`.
