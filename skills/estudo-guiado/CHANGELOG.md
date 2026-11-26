# Changelog · estudo-guiado

## 1.0.5 · 26/11/2026

**Reinstale a skill:** o `SKILL.md` mudou.

- **Modo Laboratório** (`SKILL.md`, `references/laboratorio.md`, `mapa.md`): para os módulos em `autonomia_por_laboratorio` (hoje a NG1, Git), a skill guia pelos guias de `guias/NG1/` e pelo laboratório de `scripts/laboratorio_git.py`. Não gera listas, não resolve cenários pelo estudante e registra cada cenário conferido como uma linha `laboratorio` em `registro/avaliacoes.md` (Acertos 1 = sem consulta). O portão da NG1 pede os 10 cenários em 3 dias distintos (o `--checar` confere) e uma explicação oral de um merge com conflito, conduzida pela skill.
- Exemplo de data em `correcao.md` trocado por uma data genérica.

Regressão: A-L4-01 4,80 · V-03 4,75 · BV-02 4,80 · BV-05 4,80, nenhum portão violado; casos do modo Laboratório L-01 a L-05 aprovados ([relatório](../../benchmark/regressao-1.0.5/benchmark_report.md)).


## 1.0.4 · 26/11/2026

**Reinstale a skill:** o `SKILL.md` mudou.

- **Branch de estudo de cada pessoa** (`SKILL.md`, `principios.md`, `correcao.md`, `docs/fluxo-git.md`): a branch deixa de ser fixa (`estudo_rodrigorosario`). A skill descobre a `estudo_<nome>` do estudante pela conta do GitHub da sessão, comparada com o `registro/estudante.yml` de cada branch. Se não houver como saber a conta, confirma com o estudante. Se nenhuma branch for dele, oferece criar, com o sim dele. Nunca lê nem grava na branch de outra pessoa.
- **Autoria pelo `registro/estudante.yml`:** a conta do GitHub que assina os commits vem desse arquivo, e não de um nome fixo.

Regressão: A-L4-01 4,75 · V-03 4,60 · BV-02 5,00 · BV-05 4,55, nenhum portão violado; casos de branch R-01, R-03, R-04 e R-05 aprovados ([relatório](../../benchmark/regressao-1.0.4/benchmark_report.md)).

## 1.0.3 · 25/11/2026

**Reinstale a skill:** o `SKILL.md` mudou.

- **Andamento em `registro/estado.yml`** (`SKILL.md`, `exercicios.md`, `correcao.md`, `fixacao.md`): `status`, `inicio`, `diagnostico`, `nivel_atingido` e `portao` (data, resultado, evidência) saíram do cabeçalho de `disciplinas/` e são lidos e gravados em `registro/estado.yml`, que só existe na branch de estudo ([ADR 0004](../../docs/adr/0004-separar-andamento-do-curriculo.md)). O cabeçalho guarda só o currículo, com `portao.criterio`.

Regressão (A-L4-01, V-03, BV-02, BV-05 e dois casos que gravam, A-L2-02 e R-01): notas 4,95, 4,75, 5,00, 4,75, 4,50 e 4,80, nenhum portão violado ([relatório](../../benchmark/regressao-1.0.3/benchmark_report.md)).

## 1.0.2 · 25/11/2026

**Reinstale a skill:** o `SKILL.md` mudou.

- **Fluxo de git** (`SKILL.md`, `principios.md`, `correcao.md`, `exercicios.md`): andamento na branch `estudo_rodrigorosario`, estrutura na `main`; a regra está em `docs/fluxo-git.md`. Numa branch criada da `main`, o script roda só com `--checar`.
- **Âncoras do NM0** (`correcao.md`): itens das quatro listas antigas passam a ser registrados como `fluencia` ou `critico`, nunca `ancora`. Antes eram aceitos como `ancora` e descartados sem aviso pela contagem de autonomia.

Regressão (A-L4-01, V-03, BV-02, BV-05): notas 4,75, 4,55, 5,00 e 4,55, nenhum portão violado ([relatório](../../benchmark/regressao-1.0.2/benchmark_report.md)).

## 1.0.1 · 25/11/2026

Correção de instalação, sem mudança de comportamento. A conta do claude.ai guarda só o `SKILL.md`; os links relativos para `references/` não existiam lá, e a skill podia trabalhar só com o resumo. Agora o roteamento aponta para `skills/estudo-guiado/references/` no repositório clonado, sempre na versão da `main`, e manda avisar o estudante, em vez de improvisar, quando esses arquivos não abrirem.

## 1.0.0 · 20/11/2026

Mesmas instruções da 0.3.0, agora validadas no holdout da fase D (8 casos novos: 4,59 com a skill contra 4,53 sem ela; 0 portões violados). Status no framework: APROVADA COM RESTRIÇÕES.

Para a próxima versão (achados do holdout, que exigem um holdout novo para validar):

- afrouxar "item crítico só recebe certo com a resolução completa" quando houver raciocínio curto e correto (H-02);
- no modo Mapa, priorizar a lacuna apontada no mapa e oferecer o pré-requisito como alternativa (H-03);
- respostas mais curtas (clareza 4,38 contra 5,00).

## 0.3.0 · 20/11/2026

Fase C:

- Modo Fixação (`references/fixacao.md`): sorteio pelo script (`--sortear-fixacao`), intercalação, parcela de 20% nas listas, respostas aos avisos.
- Código: `autonomia-em-queda`, `fixacao-vencida`, `sem-intercalacao`, verificação por execução de código (`codigo`) para itens de lógica.
- Competências de NF1 a NF5 e de NL1 a NL4: o nivelamento inteiro (28 módulos) está mapeado.

## 0.2.0 · 20/11/2026

Fase B: benchmark de desenvolvimento (12 casos) e teste de ataque com 10 tentativas (benchmark/fase-b/). Ajustes:

- Âncora só conta se o `.yml` da lista a marca como âncora (código); treino sem pré-requisito não conta para a autonomia (código e skill).
- `ajuda` inclui confirmações de passo e respostas vistas em conversas anteriores.
- Âncora ou item crítico sem passos não recebe `certo`.
- O portão da correção passa a exigir autonomia.
- Correção de registro por linha nova, nunca por edição (inclusive na proteção contra frustração).
- Só itens de listas do repositório são registrados.
- Regras do design só valem se implementadas; erros que já existiam antes são relatados, não corrigidos fora dos caminhos permitidos.
- `.yml` alterado por terceiros não serve para registrar âncora; critério para mudar status.
- Diagnóstico: lacuna em pré-requisito registrada de fato, com o código.

## 0.2.0-dev · 20/11/2026 (fase B, em construção; sem benchmark)

- Modo Diagnóstico (`references/diagnostico.md`): escada de 5 degraus, proteção contra frustração com problema gêmeo, registro em `registro/diagnosticos/`.
- Autonomia: portão no código e linha no `MAPA.md`.
- Regra reforçada: não citar regras que só estão no design (caso V-06).

## 0.1.2 · 20/11/2026

Ajustes da revisão final da fase A (sem nova rodada de benchmark):

- Avisar ao encerrar que as mudanças não foram enviadas ao GitHub e oferecer o commit.
- IDs de competência nunca mudam nem são reaproveitados.
- A tabela de listas do módulo passa a ser um caminho de gravação permitido.
- Uma única regra de data (a do sistema) no CSV e no resumo.
- Gabarito: número com unidade é aceito; limite de intervalo dos predicados.

## 0.1.1 · 19/11/2026

Ajustes feitos com base no conjunto de desenvolvimento do benchmark da fase A (benchmark/fase-a/benchmark_report.md):

- "Só me dá a resposta": convida uma vez a tentar antes de entregar; item não tentado não vai para o registro (A-L4-01).
- Pré-requisito não cumprido: recomenda o pré-requisito e oferece a lista pedida como treino, que não conta para o portão (A-L1-04).
- `revisao: independente` só quando um subagente conferiu; sem essa ferramenta, `revisao: releitura`, com aviso ao estudante (A-L3-01, A-L3-03).
- Itens abertos: o gabarito traz critério e exemplos, conferidos contra contraexemplos (A-L3-03).
- Respeitar o tipo de item pedido; variações críticas só como extras (A-L3-01).
- Nova lista entra na tabela de listas do módulo (A-L3-03).
- Mapa: sem conclusões sobre a causa com menos de 5 respostas; fechar um próximo passo concreto (A-L4-02).
- Datas do registro pela data do sistema.

## 0.1.0 · 19/11/2026

- Modos Exercícios, Correção e Mapa.
- Composição de listas por tipo de item, verificação obrigatória por `scripts/verificar.py`.
- Registro item a item em `registro/respostas.csv` e resumo em `registro/avaliacoes.md`.
- Leitura do `MAPA.md` e próximo passo com prioridade para lacunas em pré-requisitos.
