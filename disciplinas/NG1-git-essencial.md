---
codigo: NG1
ordem: 4
nome: "Git essencial: histórico, branches, merge e remoto"
eixo: "Programação"
fase: nivelamento
bloco: "V · Versionamento com Git"
semestre_inicio: 0
semestre_fim: 0
horas_previstas: 20
nivel_alvo: 3
prerequisitos: []
requer_unidades: []
unidades_relacionadas: []
competencias:
  - {id: NG1.c01, nome: "Modelo do Git: diretório de trabalho, staging, commit e HEAD"}
  - {id: NG1.c02, nome: "Ler e comparar o histórico"}
  - {id: NG1.c03, nome: "Recuperar arquivos e desfazer mudanças locais"}
  - {id: NG1.c04, nome: "Criar, trocar e apagar branches"}
  - {id: NG1.c05, nome: "Mesclar e resolver conflitos"}
  - {id: NG1.c06, nome: "Sincronizar com um remoto: fetch, pull e push"}

portao:
  criterio: "Os 10 cenários do laboratório de Git (níveis 1 a 5) resolvidos sem consulta, em pelo menos 3 dias distintos, e uma explicação oral de um merge com conflito"
---

# NG1 · Git essencial: histórico, branches, merge e remoto

Nivelamento · bloco V · Versionamento com Git · até 20 h

## Tópicos, na ordem

Fundamentos do Git (nível 1); arquivos e histórico (nível 2); branches (nível 3); merge e conflitos (nível 4); Git remoto (nível 5).

Cada nível tem um guia em [guias/NG1](../guias/NG1/README.md), com teoria, comandos, erros comuns, exercícios e um desafio aplicado a este repositório. Os níveis 6 a 12 (rebase, recuperação, colaboração, segurança, automação, internals e engenharia de versionamento) ficam na [G5](G5-git-avancado-e-engenharia-de-versionamento.md).

## Aplicações

A sua branch de estudo neste repositório ([fluxo de git](../docs/fluxo-git.md)); trabalhos em grupo da graduação; qualquer projeto de software, do primeiro script ao portfólio.

## Laboratório

Os exercícios avançados de cada nível são cenários conferidos por script, cada um num repositório descartável fora deste:

```bash
python scripts/laboratorio_git.py listar
python scripts/laboratorio_git.py preparar N1-primeiro-commit /tmp/lab
# ... resolva o cenário dentro de /tmp/lab ...
python scripts/laboratorio_git.py conferir N1-primeiro-commit /tmp/lab
```

## Como estudar este módulo

Siga o [roteiro comum dos módulos de nivelamento](../docs/roteiro-nivelamento.md), com uma diferença: o estudo guiado e a aplicação usam os guias e o laboratório, não listas numéricas. Comece pelo diagnóstico do [guia do nível 1](../guias/NG1/1-fundamentos.md).

## Referência principal

Scott Chacon e Ben Straub, Pro Git (2ª edição, livre em git-scm.com/book/pt-br); documentação oficial do Git (git-scm.com/docs); MIT Missing Semester, aula de controle de versão.

## Competência ao concluir

Versionar o próprio trabalho sem medo de perder nada: commitar, ler o histórico, desfazer, trabalhar em branches, resolver conflitos e sincronizar com o GitHub.

## Portão de saída

Os 10 cenários do laboratório de Git (níveis 1 a 5) resolvidos sem consulta, em pelo menos 3 dias distintos, e uma explicação oral de um merge com conflito.

A autonomia deste módulo vem do laboratório, não de problemas-âncora de listas: o `plano.yml` registra a exceção em `autonomia_por_laboratorio` ([ADR 0010](../docs/adr/0010-disciplinas-de-git-e-guias.md)). Cada cenário que passa no `conferir` vira uma linha `laboratorio` em `registro/avaliacoes.md`, na branch de estudo: Acertos 1 se foi sem consulta, 0 se houve consulta, e o código do cenário nas Observações (por exemplo `| 2026-12-01 | NG1 | laboratorio | 1 | 1 | N4-conflito | |`). O `MAPA.md` mostra quantos cenários e dias já foram cumpridos, e o `--checar` recusa o portão concluído sem os 10 cenários em 3 dias distintos.

## Anotações
