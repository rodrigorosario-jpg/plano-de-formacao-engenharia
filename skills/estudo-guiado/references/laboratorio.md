# Modo Laboratório (NG1 e outros módulos de laboratório)

Vale para os módulos listados em `autonomia_por_laboratorio` no `plano.yml`; hoje, só a NG1 (Git essencial). Neles o estudo usa os guias e o laboratório de Git, **não listas numéricas** ([ADR 0010](../../../docs/adr/0010-disciplinas-de-git-e-guias.md)).

## 1. O que não fazer

- **Não gere lista de exercícios nem prova de saída** para esses módulos, e não use `scripts/verificar.py`. Se o estudante pedir "uma lista da NG1", explique em uma frase que o módulo é conferido pelo laboratório e ofereça o próximo passo do guia.
- **Não resolva um cenário do laboratório** pelo estudante, nem dite a sequência de comandos que o resolve. Uma dica é ajuda: o cenário passa a contar como **com consulta**.
- **Não rode, na máquina do estudante, comandos que alterem a `main`, a branch de estudo ou o remoto** como exercício. Exercício que escreve no Git roda numa cópia descartável (seção "Regra de ouro" de `guias/NG1/README.md`).
- **Não grave nada em `registro/respostas.csv`** para esses módulos: elas não têm itens de lista.

## 2. Estudo

Leia o guia do nível pela `main`: `git show origin/main:guias/NG1/README.md` e `git show origin/main:guias/NG1/<n>-<nome>.md`.

- **Começo do módulo:** o diagnóstico do guia do nível 1 (cinco perguntas, sem consulta). Corrija as respostas uma a uma, como no modo Diagnóstico. Se o estudante acertar as cinco, ele pode ir direto aos cenários do nível 1.
- **Em cada nível,** siga as seções do guia: explique os conceitos e proponha os exercícios básico e intermediário. Os princípios de `principios.md` valem: pergunte antes de explicar e peça a previsão antes do comando ("o que você espera que o `git status` mostre?").
- **O exercício avançado de cada nível é o laboratório.** Indique os dois cenários do nível (`python scripts/laboratorio_git.py listar`) e os comandos `preparar` e `conferir`, que rodam na máquina dele.

## 3. Conferir um cenário

O estudante roda `conferir` na máquina dele e cola a saída.

- **Se a sua sessão tem um shell na mesma máquina e a pasta do cenário,** você pode rodar o `conferir` você mesmo. `conferir` só lê.
- **Passou** quando a saída termina com `Cenário <código> resolvido.` Qualquer outra saída é "ainda não": comente as falhas listadas sem dar a solução.
- **Pergunte, uma vez:** "Resolveu sem consultar guia, colega ou IA?" Se ele consultou, ou se você deu dica sobre esse cenário nesta conversa, conta como com consulta.

## 4. Registrar

Uma linha por cenário que passou, em `registro/avaliacoes.md`, na branch de estudo, com a data do sistema:

```text
| 2026-12-01 | NG1 | laboratorio | 1 | 1 | N4-conflito | |
| 2026-12-01 | NG1 | laboratorio | 0 | 1 | N4-conflito; com consulta | |
```

- Acertos: 1 se foi sem consulta, 0 se houve consulta.
- Total: sempre 1.
- Observações: começam pelo código do cenário.
- Lista: fica vazia.

Depois rode `python scripts/progresso.py`. A linha "Laboratório" do módulo no `MAPA.md` mostra quantos cenários distintos foram resolvidos sem consulta e em quantos dias. Para o portão, valem os 10 cenários em pelo menos 3 dias distintos.

Se o estudante começar o módulo nesta conversa, marque `status: em_andamento` e `inicio` em `registro/estado.yml`, como nos outros módulos e com o sim dele.

## 5. Portão

Quando a linha "Laboratório" do `MAPA.md` estiver completa, falta a explicação oral de um merge com conflito, pedida pelo portão da NG1.

1. **Peça a explicação** de um merge com conflito que ele fez. Ela deve dizer:
   - qual era a base comum;
   - o que cada lado mudou;
   - por que o Git parou;
   - como ele decidiu o resultado;
   - como concluiu ou como abortaria o merge.
2. **Faça no máximo duas perguntas de aprofundamento,** sem ensinar durante a avaliação.
3. **Avalie.** Aprovada quando os cinco pontos estão corretos. Se faltar algum, diga qual e combine a revisão do guia do nível 4.
4. **Com a aprovação,** proponha atualizar a linha do módulo em `registro/estado.yml`, por exemplo `NG1: {status: concluida, inicio: 2026-12-01, portao: {data: 2026-12-10, resultado: "10/10 cenários; explicação oral aprovada", evidencia: "registro/avaliacoes.md (laboratorio)"}}`. Grave só com o sim dele. O `--checar` recusa o portão se faltar cenário ou dia.

## 6. Próximo passo

No modo Mapa, para esses módulos, o próximo passo segue a linha "Laboratório", nesta ordem:

1. Nível com cenário pendente: o guia daquele nível e os cenários que faltam.
2. Cenários completos, mas em menos de 3 dias: refazer, em outro dia, os cenários que ele achou mais difíceis, numa pasta nova.
3. Linha completa: a explicação oral do portão.

## 7. G5

Os níveis 6 a 12 são a G5, disciplina da graduação, conferida por projeto, sem laboratório. Se o estudante pedir esses níveis durante o nivelamento, aponte o guia (`guias/G5/`) e lembre que a G5 depende da NG1 e da G1.
