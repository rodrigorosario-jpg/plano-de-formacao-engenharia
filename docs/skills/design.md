# Design · Skills de estudo guiado

**Versão:** 1.0 (aprovado e implementado na skill estudo-guiado 1.0.0, de 20/11/2026, com status "aprovada com restrições"; a skill está na 1.0.2, veja o [CHANGELOG](../../skills/estudo-guiado/CHANGELOG.md))
**Data:** 19/11/2026
**Base:** [framework-plano-mestre.md](framework-plano-mestre.md) (Skill Engineering Framework: fases 0 a 17, testes L1 a L5, rubrica de 0 a 5, portões e status final), aplicado ao plano de formação deste repositório. Termos como "portão", "L1 a L5", "holdout" e "status final" seguem as definições de lá.

Neste documento, "o estudante" é o dono deste repositório. As decisões que ele tomou aparecem como dele; as decisões tomadas por quem escreveu o design aparecem marcadas como **[decisão do design]**.

---

## 1. Intenção

O estudante está reconstruindo a base de matemática, física e lógica desde o Ensino Fundamental. O objetivo é chegar a um domínio compatível com estudos avançados, uma futura dissertação de mestrado e habilidades técnicas de engenharia. O plano completo (nivelamento, graduação e pós-formatura, com pré-requisitos rígidos) já está neste repositório.

As skills existem para servir a esse estudo. **O propósito declarado é desenvolver o raciocínio para resolver problemas, e não treinar um executor de procedimentos.** Uma skill que ensina a aplicar fórmulas mais rápido, sem formar o julgamento de quando e por que aplicá-las, fracassou, mesmo que todas as respostas estejam corretas.

**Por que agora:** o nivelamento começou (diagnóstico do bloco A zerado, listas do NM0 prontas). Com exercícios pedidos ao Claude sem padrão, acontecem erros como a questão do NM0 com duas respostas válidas (24 e 48), que só foi pega por conferência manual. Correções soltas também não acumulam um retrato do que está fraco.

**Futuro:** tudo isto vai evoluir para uma plataforma de estudo de autoria do estudante. As skills e os dados deste repositório são o protótipo e a especificação dessa plataforma.

## 2. O que é sucesso

Nas palavras do estudante: **resolver problemas complexos de forma autônoma.** Exemplo: no nivelamento de matemática, chegar a resolver sozinho problemas complexos daquele bloco, e assim por diante.

O que ele definiu sobre autonomia:

- No início as skills dão bastante apoio, **para não gerar frustração**.
- Com o tempo o apoio diminui, mas **as avaliações seguem todos os critérios** do começo ao fim.
- Autonomia não é um acerto isolado. É **N problemas resolvidos sem ajuda, de forma continuada, até o fim da trilha**.
- **O aprendizado não termina quando a trilha termina:** perguntas aleatórias de blocos concluídos aparecem durante os blocos seguintes, para garantir a fixação.

## 3. Objetivos, não objetivos e antiobjetivos

**Objetivos**

1. Gerar listas de exercícios corretas, sem ambiguidade e com gabarito verificado de forma independente.
2. Corrigir as respostas do estudante item a item, classificando o tipo de erro e mostrando métodos alternativos.
3. Manter um **mapa de deficiências** cumulativo, calculado a partir de todas as correções.
4. Conduzir **perguntas estruturadas de diagnóstico** que levem o estudante a descobrir sozinho onde está a lacuna.
5. Medir e manter a **autonomia** ao longo do tempo.
6. Programar a **fixação**: questões aleatórias de módulos concluídos, misturadas ao conteúdo novo, pela trilha inteira.
7. Exercitar **várias técnicas para o mesmo resultado**, **simplificação** (fluência, e também os erros de simplificar demais) e **pensamento crítico** em toda a janela de aprendizado, não como etapa final.
8. Aplicar o **rigor completo do framework, por fases** (decisão do estudante).

**Alcance da v1.0** **[decisão do design]**: os 28 módulos do nivelamento (NM0 a NM18, NF1 a NF5, NL1 a NL4). As fases A e B são construídas e testadas no bloco A da matemática, onde o estudante está; as fases C e D estendem a física e a lógica. As disciplinas da graduação e do pós-formatura entram numa versão seguinte, porque precisam de outras formas de verificação (provas formais, projetos).

**Não objetivos (por enquanto)**

- As outras skills do catálogo do framework (Research, Data Engineering, BI, SQL etc.). Decisão do estudante: no início, o foco é 100% nos estudos. A Research vem depois, para teoria e para o mestrado; as técnicas entram quando a trilha chegar nesses assuntos.
- Construir a plataforma. Aqui só se garante que os dados e as regras estejam prontos para ela.
- Material didático (apostilas, aulas). O plano original já exclui isso.

**Antiobjetivos (é fracasso, mesmo que funcione)**

- A skill entrega a resposta em vez de levar o estudante até ela.
- Frustração no início, por dificuldade sem apoio.
- **Autonomia falsa:** acertos isolados contam como domínio e o conhecimento se perde depois sem que nada perceba.
- Exercício com erro ou ambiguidade no gabarito.
- Ritual mecânico: listas que treinam só repetição de procedimento, sem perguntas de porquê, de estimativa ou de crítica.
- Dados presos ao Claude, que a futura plataforma não consiga ler.

## 4. Restrições

- **Onde roda:** no claude.ai, no projeto "Estudos", com acesso ao repositório `rodrigorosario-jpg/plano-de-estudos` (privado; hoje as branches seguem o [fluxo de git](../fluxo-git.md)). Em sessões novas o repositório precisa ser anexado e clonado antes do uso.
- **Formatos abertos:** markdown com frontmatter YAML, CSV e scripts Python, como o resto do repositório. Nada que só o Claude consiga ler.
- **Regras já existentes continuam valendo:** pré-requisitos rígidos, portões, tipos de avaliação (`diagnostico`, `exercicios`, `saida`, `revisao`), revisões em 7, 30 e 90 dias, `limite_abertas` e validação por `scripts/progresso.py --checar` no CI.
- **Rotina:** estudo nos dias úteis, em janelas curtas (manhã, almoço e noite). Fins de semana não são obrigatórios.
- **Git:** commit e push só quando o estudante pedir.
- **Idioma:** português do Brasil.

## 5. O que o estudante decidiu sobre o "como"

- Usar no claude.ai, gravando no repositório deste plano.
- O ciclo de uma sessão: **lista de exercícios → correção → mapa de deficiências → perguntas estruturadas até a conclusão de onde está a lacuna.**
- Várias técnicas para o mesmo resultado; exercícios de simplificação nas duas leituras (fluência **e** armadilhas de simplificação excessiva); pensamento crítico o tempo todo.
- Apoio decrescente e critérios constantes; autonomia continuada de N problemas; fixação com perguntas aleatórias nos blocos seguintes.
- Rigor completo do framework, aplicado por fases.
- Primeira entrega focada só no ciclo de estudo.

## 6. Arquitetura

### 6.1 Uma skill com cinco modos **[decisão do design]**

Uma skill, `estudo-guiado`, com um `SKILL.md` curto (ativação, princípios, roteamento e segurança) e um arquivo de referência por modo:

| Modo | Arquivo | Faz |
| --- | --- | --- |
| Exercícios | `references/exercicios.md` | Gera listas, problemas-âncora e provas |
| Correção | `references/correcao.md` | Corrige, classifica erros, mostra métodos alternativos, registra |
| Mapa | `references/mapa.md` | Lê e interpreta o mapa de deficiências; propõe o próximo passo |
| Diagnóstico | `references/diagnostico.md` | Conduz as perguntas estruturadas, com apoio graduado |
| Fixação | `references/fixacao.md` | Sorteia e aplica questões de módulos concluídos |

Além disso, `references/principios.md` reúne o que vale em todo modo: pensamento crítico, várias técnicas, simplificação e "não entregar a resposta".

**Por que uma skill e não cinco:** os modos compartilham o mesmo modelo de dados e se encadeiam na mesma sessão (a correção chama o diagnóstico, que alimenta o mapa). Cinco skills disputariam a ativação e duplicariam os princípios. O framework pede para evitar tanto um arquivo gigante quanto uma modularização desnecessária. Os arquivos de referência dão a modularidade sem multiplicar as ativações.

**Onde a skill vive:** a fonte versionada fica em `skills/estudo-guiado/` neste repositório. A instalação na conta do claude.ai é feita pelo cartão de proposta de skill, a partir dessa fonte. **[decisão do design]**

### 6.2 Modelo de dados

O que já existe continua: `disciplinas/*.md`, `registro/avaliacoes.md`, `registro/semanal.md`, `exercicios/<código>/` e `gabaritos/`, `PROGRESSO.md` (gerado).

Novidades **[decisão do design: nomes e colunas finais ficam com o construtor, mantendo o conteúdo]**:

1. **Competências por módulo.** Cada `disciplinas/<código>.md` ganha no frontmatter uma lista `competencias` com IDs estáveis (`NM1.c01`, `NM1.c02`…) e um nome curto. Os tópicos já descritos em cada arquivo são a fonte. O mapa de deficiências é calculado por competência, não por módulo inteiro.
2. **`registro/respostas.csv`:** uma linha por item respondido. É o dado bruto de tudo. Colunas mínimas:
   - `data`, `sessao`, `lista` (caminho do arquivo da lista), `item`, `codigo`, `competencia`;
   - `tipo_item`: `fluencia`, `metodos`, `simplificacao`, `armadilha_simplificacao`, `critico`, `ancora`, `fixacao`;
   - `nivel` (1 a 5), `resultado` (`certo`, `parcial`, `errado`, `em_branco`);
   - `classe_erro` (`conceito`, `procedimento`, `atencao`, `interpretacao`, `simplificacao_indevida` ou vazio);
   - `ajuda` (número de perguntas de apoio usadas, 0 = sozinho), `metodo` (resumo do caminho que o estudante usou);
   - `observacao`.
3. **`MAPA.md` (gerado, como o `PROGRESSO.md`):** por módulo e competência, mostra acertos recentes, classes de erro predominantes, nível de autonomia e situação. As regras da situação consideram as últimas 10 respostas da competência **[decisão do design: limites iniciais, em `plano.yml`]**:
   - `sem_dados`: menos de 3 respostas, e nenhum erro de conceito;
   - `fraca`: algum erro de `conceito` nas 3 últimas respostas ou nas respostas do dia mais recente, ou menos de 60% de acertos;
   - `forte`: pelo menos 5 respostas, 85% ou mais de acertos e 80% ou mais delas com `ajuda = 0`;
   - `em_formacao`: os demais casos;
   - `em_queda`: competência de módulo concluído que se encaixa em `fraca` ou que atende à regra de queda da seção 6.3.

   Tem ainda uma seção "lacunas prováveis em pré-requisitos", que relaciona erros de um módulo a competências dos módulos de que ele depende.
4. **`registro/diagnosticos/AAAA-MM-DD-<código>.md`:** resumo de cada conversa de diagnóstico: a hipótese inicial, as perguntas feitas, a conclusão a que o estudante chegou e o encaminhamento. Fica em texto porque é narrativo; o essencial (competência e ajuda) também vai para o CSV.
5. **`plano.yml`** ganha parâmetros: `autonomia_n` (padrão 5), `autonomia_dias_distintos` (padrão 3), `fixacao_proporcao` (padrão 0,2) e `fixacao_janela` (padrão 3: últimas respostas consideradas para queda). **[decisão do design: valores iniciais]**

O `scripts/progresso.py` (ou um script irmão, `scripts/mapa.py`) passa a:

- validar o CSV (códigos e competências existentes, valores permitidos, data válida, item da lista existente);
- gerar o `MAPA.md`;
- sortear as questões de fixação (`--sortear-fixacao`);
- avisar sobre quedas de autonomia.

O CI continua rodando `--checar`.

### 6.3 Regras de autonomia **[decisão do design, a partir do que o estudante definiu]**

- **Problema-âncora:** problema complexo, de vários passos, que mistura competências do módulo (e de pré-requisitos) e exige montar a estratégia. Cada módulo de nível alvo 3 ou mais tem uma reserva de âncoras.
- **Autônomo:** âncora com `resultado = certo` e `ajuda = 0`.
- **Autonomia de módulo atingida:** `autonomia_n` âncoras diferentes resolvidas de forma autônoma, em pelo menos `autonomia_dias_distintos` dias diferentes.
- Todos os 28 módulos do nivelamento têm `nivel_alvo` 3, então todos têm âncoras.
- **Portão:** os status `concluida` e `dispensada` passam a exigir, além da prova de saída com 80% ou mais, a autonomia atingida. Isso altera o `AVALIACOES.md`, os critérios do portão e o `--checar`.
- **Autonomia mantida:** âncoras e questões de módulos concluídos continuam aparecendo (fixação). Se, nas últimas `fixacao_janela` questões de um módulo concluído, houver duas ou mais com erro ou com ajuda, o módulo fica `em_queda` no mapa e o script avisa para mudar o status para `em_revisao`, como a regra de revisão abaixo de 70% já faz.

### 6.4 Apoio graduado no diagnóstico

O diagnóstico funciona como uma escada de perguntas, do mais aberto ao mais conduzido:

| Degrau | Exemplo |
| --- | --- |
| 0 · Reflexão | "Releia sua resolução. Algum passo te deixa em dúvida?" |
| 1 · Foco | "Olhe a passagem da linha 2 para a 3. O que mudou?" |
| 2 · Pergunta de conceito | "O que significa dividir por uma fração?" |
| 3 · Caso menor | "Faça a mesma coisa com números pequenos: 1 ÷ ½." |
| 4 · Exemplo resolvido parcial | Mostra o primeiro passo de um problema parecido e pede o resto |

- No início da trilha (ou de um bloco), a escada sobe rápido: menos tentativas por degrau. Com a autonomia crescendo, ela sobe devagar e começa nos degraus de cima mais tarde.
- **Proteção contra frustração:** se o estudante passar do degrau 4 sem avançar, a skill fecha o problema com uma explicação curta, registra o item no CSV com `resultado = errado`, a classe de erro e a `ajuda` usada (o mapa então marca a competência como `fraca` pelas regras da seção 6.2) e entrega um **problema gêmeo** (mesma estrutura, outros números) para ele tentar sozinho em seguida.
- A conversa termina com o estudante formulando, com as palavras dele, onde estava a lacuna. A skill não formula por ele. Se a lacuna estiver num pré-requisito, a skill aponta o módulo e sugere voltar, seguindo a regra de não avançar sem base.

### 6.5 Composição das listas

Toda lista gerada pela skill mistura tipos de item **[decisão do design: proporções iniciais, ajustáveis]**:

| Tipo | Papel | Parcela típica |
| --- | --- | --- |
| `fluencia` | Automatizar o básico (níveis 1 e 2) | 30% |
| `metodos` | Resolver por dois caminhos; comparar quando cada um compensa | 10% |
| `simplificacao` | Fluência em simplificar expressões, frações e problemas | 15% |
| `armadilha_simplificacao` | Mostrar quando simplificar demais dá errado (cortes indevidos, arredondar cedo) | 10% |
| `critico` | Estimar antes de calcular, dado faltando ou sobrando, achar o erro numa resolução, "faz sentido?" | 15% |
| `ancora` | Problema complexo, sem dicas | 0 a 2 itens |
| `fixacao` | Módulos concluídos, sorteados | `fixacao_proporcao` (0 enquanto não houver módulo concluído) |

Os itens têm sempre um contexto de aplicação quando o módulo pede (computação, física, finanças pessoais, engenharia), como os arquivos de disciplina já descrevem.

### 6.6 Verificação dos exercícios

O tipo de verificação depende da área **[decisão do design]**:

- **Itens com resposta calculável** (matemática, e física com unidades conferidas pelo script): a skill gera o gabarito e um script Python independente (com `fractions` e, se preciso, `sympy`) recalcula a resposta. Divergência impede a entrega da lista.
- **Unicidade:** para itens de "encontre o número", "quantos" ou "qual", o script testa todas as respostas candidatas no intervalo do enunciado. Mais de uma válida impede a entrega (caso 24/48).
- **Itens não calculáveis** (crítico, interpretação): uma segunda leitura independente confere enunciado e gabarito. Pode ser um subagente, quando a plataforma permitir; senão, uma revisão separada. O resultado é registrado.
- **Lógica e programação (NL1 a NL4):** tabelas-verdade conferidas por script; programas e testes de mesa conferidos executando o código de referência com casos de teste.
- As listas vão para `exercicios/<código>/` com gabarito separado em `gabaritos/`, no formato das listas do NM0, para que `listas_sem_gabarito()` continue funcionando.

### 6.7 Fixação

- Toda lista de um módulo em andamento recebe uma parcela de questões de módulos concluídos (`fixacao_proporcao`). O sorteio pesa a situação no mapa (mais peso para `em_formacao` e `em_queda`) e o tempo desde a última vez que a competência apareceu.
- As revisões de 7, 30 e 90 dias continuam como estão. A fixação é adicional e não tem dia marcado.
- A fixação continua depois que a trilha termina: módulos do nivelamento aparecem na graduação, e assim por diante.
- **Tarefa agendada opcional** **[decisão do design: fase C, opcional]**: uma tarefa programada no claude.ai que, numa janela da rotina (por exemplo no almoço), sorteia de 3 a 5 questões de fixação e as deixa prontas para o estudante. Só é criada se o estudante quiser, quando chegar a fase C.

### 6.8 Convivência com o que já existe **[decisão do design]**

- **Dois níveis de registro.** O `registro/respostas.csv` guarda cada item. O `registro/avaliacoes.md` continua com uma linha por avaliação (o resumo), porque as regras de decisão e a previsão do `progresso.py` leem esse arquivo. A skill escreve nos dois na mesma correção, e o `--checar` confere se os acertos e o total do resumo batem com as linhas do CSV daquela lista.
- **Escala de níveis única, de 1 a 5:** 1 Fixação (iniciante), 2 Aplicação (básico), 3 Intermediário, 4 Contexto (avançado), 5 Desafio (complexo). As listas do NM0 já usam essa escala. O `AVALIACOES.md` passa de 4 para 5 níveis, e o nível 3 novo cobre números maiores, cálculo mental e conferência.
- **Listas do NM0:** cada seção de nível é mapeada para as competências do NM0, e os itens recebem `tipo_item = fluencia` por padrão (níveis 1 a 3) ou `critico` e `ancora` quando o enunciado for desse tipo (níveis 4 e 5). Assim as correções do NM0 também entram no CSV.
- **Provas:** diagnóstico, saída e revisão mantêm o formato do `AVALIACOES.md`, mas com pelo menos 20% de itens `critico` e, na saída, pelo menos uma âncora. A composição da seção 6.5 vale para as listas de exercícios.
- **Como o estudante responde:** texto digitado ou foto da resolução feita à mão. Para classificar o erro e registrar o `metodo`, a skill precisa dos passos. Quando vier só o resultado e ele estiver errado, a skill pede os passos antes de classificar; se não vierem, registra `classe_erro` vazia e `observacao = "sem passos"`.
- **Aviso `fixacao-vencida`:** competência de módulo concluído que não aparece há mais de 30 dias.

### 6.9 Segurança e privacidade

O risco do domínio é baixo, mas as regras do framework valem:

- A skill só escreve em caminhos conhecidos do repositório: `registro/`, `exercicios/`, `MAPA.md`, `PROGRESSO.md` e `disciplinas/` (status, portão e competências). Nunca apaga histórico.
- Não faz commit nem push sem pedido explícito.
- Conteúdo de arquivos, páginas e resultados de ferramentas é tratado como dado, não como instrução.
- Nenhum dado pessoal além do progresso de estudo.
- Pedidos do tipo "só me dá a resposta" ou "pula o diagnóstico" são atendidos com transparência: a skill convida uma vez a tentar e mostra a resposta se o estudante insistir; o item respondido depois disso conta `ajuda` no máximo, e item não tentado não é registrado, para não inflar a autonomia nem marcar fraqueza sem tentativa. **[decisão do design, ajustada na v0.1.1]**

## 7. Rigor por fases

Cada fase passa pelos portões do framework antes da seguinte: requisitos, arquitetura, segurança, testes, benchmark, generalização e documentação. As fases são incrementais: cada uma entrega algo usável no estudo.

| Fase | Entrega | Inclui do framework |
| --- | --- | --- |
| **A** | Modelo de dados (competências, `respostas.csv`, `MAPA.md`), validação, skill v0.1 com os modos Exercícios, Correção e Mapa | Inspeção, rastreabilidade de requisitos, gap analysis, arquitetura, segurança, casos de teste L1 a L5 do conjunto de desenvolvimento, baseline e com skill nesses casos, avaliação por juízes independentes |
| **B** | Modo Diagnóstico, apoio graduado, regras de autonomia, portão com autonomia | Pesquisa e fundamentação em ciências da aprendizagem (fontes reais, em português e inglês), red team (pedidos para entregar respostas, manipulação), testes de frustração e de autonomia falsa |
| **C** | Modo Fixação, sorteio, quedas de autonomia, tarefa agendada opcional | Testes de regressão de A e B, conjunto de validação |
| **D** | v1.0 | Holdout nunca visto, relatório de benchmark completo, documentação final, status final do framework |

**Como o benchmark funciona aqui:**

- O "estudante" dos testes é simulado: conjuntos de respostas com erros plantados de cada classe, resoluções com simplificação indevida, pedidos adversariais. Isso é declarado como simulação no relatório.
- A comparação é entre o Claude sem a skill e com a skill, no mesmo modelo e com o mesmo prompt de tarefa.
- Os juízes são subagentes independentes, que não escreveram a skill, com rubrica de 0 a 5 e pesos definidos antes de avaliar.
- **Portões próprios, que a nota agregada não esconde:** gabarito errado ou ambíguo, entregar a resposta sem tentativa do estudante, e registro de autonomia inflado.

## 8. O que fica para o construtor

- Nomes finais de arquivos e colunas, desde que o conteúdo da seção 6.2 se mantenha.
- Se a lógica de dados fica em `progresso.py` ou num `mapa.py` separado.
- A redação das instruções da skill e dos arquivos de referência.
- O número exato de casos de teste por fase, desde que cubra L1 a L5 e todas as categorias de teste do framework que se aplicam.
- A lista inicial de competências de cada módulo, a partir dos tópicos já descritos. Começar pelo bloco A, que é onde o estudante está.

## Observabilidade

Não existe serviço rodando em produção: a skill roda em conversas e o estado vive em arquivos. Por isso não há monitor de log de runtime (**dispensado**: não há runtime para monitorar). O que faz esse papel:

**Eventos (registros e avisos com chave estável):**

| Chave | Onde aparece | Nível | Campos (sem dado pessoal) |
| --- | --- | --- | --- |
| `resposta-registrada` | Linha em `registro/respostas.csv` | INFO | data, sessão, código, competência, tipo_item, resultado, classe_erro, ajuda |
| `gabarito-divergente` | Bloqueio na geração; nota na sessão | ERROR | lista, item, resposta do gerador, resposta da verificação |
| `item-ambiguo` | Bloqueio na geração | ERROR | lista, item, respostas válidas encontradas |
| `csv-invalido` | `progresso.py --checar` | ERROR | linha, coluna, motivo |
| `autonomia-em-queda` | Aviso do `--checar` e seção no `MAPA.md` | WARN | código, competência, últimas N respostas |
| `fixacao-vencida` | Aviso do `--checar` | WARN | código, dias desde a última questão de fixação |
| `portao-sem-autonomia` | Erro do `--checar` | ERROR | código, âncoras autônomas, mínimo exigido |

**Monitor:** o workflow `.github/workflows/validar.yml` já roda `progresso.py --checar` a cada push. Ele passa a cobrir o CSV, o mapa e os portões com autonomia. Falha bloqueia: o push fica vermelho no GitHub. Responsável: o próprio estudante.

## Como validar

**Ambiente:** uma sessão nova do claude.ai, no projeto "Estudos", com o repositório clonado e a skill instalada.

**Roteiro de teste de fumaça (fase A):**

1. Pedir: "Lista de NM0, divisão, 12 itens." Esperado: a lista sai com a composição da seção 6.5, gabarito separado e verificação registrada; o arquivo aparece em `exercicios/NM0/` e o gabarito em `gabaritos/`.
2. Mandar respostas com erros plantados: um de conceito, um de atenção e uma simplificação indevida. Esperado: correção item a item com a classe certa de cada erro, pelo menos um método alternativo mostrado e as linhas novas em `registro/respostas.csv`.
3. Rodar `python scripts/progresso.py --checar`. Esperado: passa, e o `MAPA.md` mostra a competência do erro de conceito como `fraca`.
4. Pedir: "Qual meu próximo passo?" Esperado: a skill lê o mapa e propõe o próximo passo, sem inventar dados.

**Caso de erro:** colocar à mão no CSV uma linha com competência inexistente (`NM0.c99`) e `ajuda` negativa. Esperado: `--checar` falha com `csv-invalido` nas duas colunas, e o CI fica vermelho.

As fases B e C acrescentam ao roteiro: uma conversa de diagnóstico que termina com o estudante formulando a lacuna, e uma lista com questões de fixação sorteadas de um módulo concluído.
