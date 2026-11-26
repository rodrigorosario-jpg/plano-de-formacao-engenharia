# Auditoria do repositório — Knowledge Core (plano-de-estudos)

> **Registro histórico.** Esta é a auditoria de 25/11/2026, aprovada pelo estudante, convertida para Markdown com o texto original e as tabelas reconstruídas. Números, versões e status são os daquela data e não são atualizados aqui. As decisões em vigor estão nas [ADRs](../adr/README.md), e o status atual de cada marco está no [roadmap](roadmap.md).
>
> O documento original tinha dois diagramas que não foram exportados com o texto. O contexto do Knowledge Core está redesenhado, como diagrama C4 de contexto, na [visão](visao.md).

## Resumo e decisões

O repositório não é um acervo de materiais a reorganizar. É um currículo estruturado (86 módulos e disciplinas com pré-requisitos), um motor de estudo (scripts, testes, CI e uma skill) e o início dos registros de um estudante. O Knowledge Core deve formalizar e separar o que existe, sem uma grande migração.

Os cinco achados que mais pesam:

- **Skill instalada desatualizada (resolvido em 25/11/2026).** A cópia ativa na sua conta era a 0.1; agora é a 1.0.1, igual à main.
- **Fonte de verdade dividida.** Unidades do curso, projetos, bibliografia e a escala de domínio só existem no documento Mapa de Formação, fora do Git. Os dois já divergem.
- **Autonomia do NM0.** Âncoras respondidas nas quatro listas atuais não contam para o portão, porque as listas não têm arquivo de verificação.
- **Conhecimento misturado com progresso.** O status do estudante fica no cabeçalho de cada disciplina, e por isso a branch de estudo precisa divergir da main.
- **Regra de branches não escrita.** Ela não está no repositório nem na skill. Uma sessão sem esse contexto pode gravar progresso na main.

Decisões que peço para você aprovar:

| Decisão | Recomendação |
| --- | --- |
| D1. Fonte de verdade | O repositório Git. O Mapa vira referência histórica, exportada e congelada |
| D2. Estrutura | Manter os caminhos atuais e acrescentar catalogo/, schemas/, templates/ e, em docs/, arquitetura/, adr/ e referencia/ |
| D3. Identificadores | Manter os códigos atuais, congelados e nunca reaproveitados |
| D4. Progresso | Separar do currículo no Marco 4, com migração testada |
| D5. Primeiro passo | Só os itens P0 da seção 10 |

## 1. Inventário do repositório

rodrigorosario-jpg/plano-de-estudos (privado) tem 374 arquivos e cerca de 1,1 MB na main, com histórico iniciado em 17/11/2026. São 317 .md, 20 .py, 12 .txt, 11 .json, 8 .csv, 3 .yml, 2 .gitkeep e 1 .gitignore. Não há notebooks, PDFs, imagens nem arquivos de diagrama (há um diagrama Mermaid dentro do NIVELAMENTO.md).

| Área | Arquivos | O que contém |
| --- | --- | --- |
| benchmark/ | 208 | Saídas e avaliações da construção da skill (56% dos arquivos, 54% dos bytes) |
| disciplinas/ | 86 | Cabeçalho YAML e texto curto de cada módulo ou disciplina |
| tests/ | 29 | 77 testes dos scripts e casos de avaliação da skill |
| docs/ | 13 | Design, plano, segurança, manutenção e validação da skill |
| exercicios/ | 9 | 4 listas do NM0, 4 gabaritos e 1 .gitkeep |
| raiz | 8 | README, NIVELAMENTO, AVALIACOES, PROGRESSO, MAPA, plano.yml, dependências |
| scripts/ | 8 | Validação, mapa de deficiências, autonomia, fixação, verificação |
| skills/ | 8 | Skill estudo-guiado 1.0.0 |
| registro/ | 4 | Horas, avaliações, respostas e diagnósticos |
| .github/ | 1 | CI: progresso.py --checar e pytest |

Dependências: PyYAML 6 ou superior e pytest 8 ou superior, sem versões travadas. Python 3.12 no CI.

Branches: main (16 commits) e estudo_rodrigorosario, 6 commits à frente. docs/readme e skills/fase-a já estão incorporadas à main. As 27 execuções do CI registradas no GitHub passaram.

## 2. Mapa dos conhecimentos e dependências

São 28 módulos de nivelamento (até 790 h), 13 disciplinas durante a graduação (1.840 h) e 45 depois dela (3.320 h).

| Eixo | Nivelamento | Graduação | Pós | Horas |
| --- | --- | --- | --- | --- |
| Matemática | 19 | 6 | 6 | 1.810 |
| Ciência da computação | 0 | 2 | 8 | 1.340 |
| Inteligência artificial | 0 | 0 | 5 | 510 |
| Elétrica e computação | 0 | 2 | 4 | 510 |
| Engenharia de dados | 0 | 0 | 6 | 430 |
| Programação | 4 | 2 | 0 | 415 |
| Física | 5 | 0 | 4 | 405 |
| Infraestrutura | 0 | 1 | 3 | 210 |
| Interdisciplinar | 0 | 0 | 4 | 190 |
| Engenharia de software | 0 | 0 | 5 | 130 |

Estado do material:

- **Estrutura:** as 86 têm tópicos, referência principal e portão de saída.
- **Competências:** 156, somente nos 28 módulos de nivelamento. As outras 58 não podem receber respostas.
- **Exercícios:** só o NM0 (440 itens em 4 listas).
- **Texto explicativo e exemplos de código:** não há. A seção Anotações está vazia em todas.
- **Referências:** nomes de livros e cursos, nenhum link. O próprio Mapa avisa que foram escritas de memória e pede conferir as edições.
- **Grafo:** 174 pré-requisitos, sem ciclos nem destinos inexistentes. 37 são redundantes por transitividade.

Renomear listas ou competências quebra o histórico em registro/. Mover pastas quebra os scripts, o CI e a skill instalada.

## 3. Diagnóstico da estrutura atual

A base é boa: formatos abertos, um arquivo por módulo, códigos estáveis, validação automática, testes e CI. As 58 disciplinas do plano principal batem com o Mapa em pré-requisitos, portões e horas.

Os problemas são de separação e de fonte de verdade:

| Problema | Evidência | Princípio afetado |
| --- | --- | --- |
| Entidades definidas fora do Git | O repositório cita 21 unidades do curso (U1.2 a U9.3) e 8 projetos (PJ1 a PJ17) que só o Mapa define. A escala de nivel_alvo também | Fonte de verdade, validabilidade |
| Progresso dentro do currículo | status, inicio, diagnostico e portao.data ficam no cabeçalho da disciplina, assim como o nível atingido | Baixo acoplamento |
| Dois ramos de vida longa | O arquivo do NM0 já difere entre main e a branch de estudo. PROGRESSO.md e MAPA.md da main pararam em 20/11 | Fonte de verdade |
| Mesmo fato em vários lugares | Pré-requisitos no YAML, na tabela e no diagrama do NIVELAMENTO.md e no Mapa. Limites em AVALIACOES.md, nos módulos, no código e no plano.yml | Fonte de verdade |
| Schema implícito | Os campos obrigatórios só existem como acessos no código. Um campo ausente interrompe o script com erro de Python | Validabilidade |
| Evidência misturada ao produto | benchmark/ é mais da metade do repositório e não é conhecimento de estudo | Modularidade |

O que preservar: o histórico Git; os códigos e IDs de competência; o grafo em disciplinas/; as listas e gabaritos do NM0; os scripts, testes e a skill; o Mapa de Formação. Os registros de estudo (respostas, avaliações, diagnóstico) mais recentes existem apenas na branch estudo_rodrigorosario, que não deve ser apagada nem sobrescrita.

## 4. Avaliação da qualidade

### Afeta o estudo agora

**Skill instalada (resolvido em 25/11/2026).** A cópia de estudo-guiado na conta estava na 0.1 e foi atualizada para a 1.0.1, que lê as regras de cada modo em skills/estudo-guiado/references/ na main. As mudanças da 1.0.2 (fluxo de git e âncoras do NM0) ficam só nesses arquivos e não pedem reinstalação. *(Nota de 25/11/2026: depois da auditoria, o `SKILL.md` também mudou na 1.0.2 e a skill foi reinstalada.)*

**Âncoras do NM0.** autonomia.py só conta uma âncora se o .yml de verificação da lista a marca como tal. A pasta exercicios/NM0/verificacao/ está vazia. A regra de correção, porém, manda registrar itens dessas listas como âncora. Eles entram no mapa e ficam fora da autonomia, sem aviso. A branch de estudo ainda não tem âncoras registradas, então nada se perdeu. Para fechar o NM0 são necessárias 5 âncoras em 3 dias, vindas de listas novas ou de um .yml criado para as antigas. O texto do módulo não menciona essa exigência.

### Inconsistências

- **Nível de exercício:** AVALIACOES.md usa 5 níveis; o Mapa usa 4. Os 27 módulos com o roteiro padrão ainda pedem “problemas de nível 3” ligados a aplicações, que na escala nova são o nível 4.
- **Duas escalas chamadas “nível”:** dificuldade do exercício (1 a 5) e domínio da disciplina (nivel_alvo, 1 a 7, definido só no Mapa).
- **Portão do NM0:** o módulo exige metas nas quatro listas e prova de saída; o Mapa exige só a prova.
- **Portão do NL1:** pede programas escritos, embora o módulo seja de lógica proposicional. O texto é igual para NL1 a NL4 e vem do Mapa.
- **Mapa desatualizado:** não cita o portão de autonomia; manda abrir NM1 e NL1 (hoje o começo é o NM0).
- **Diagrama do nivelamento:** omite NM3 → NF1 e NM6 → NF5 (implícitas por outros caminhos).
- **Documento de design:** ainda diz “rascunho para aprovação”, com a skill já em 1.0.0.

### Validações que faltam

- Código de disciplina repetido não é detectado: o segundo arquivo substitui o primeiro em silêncio.
- requer_unidades não é conferido.
- Portão concluído exige um resultado preenchido, mas o script não confere se ele atinge 80%.

### Duplicidades e fragmentos

- O roteiro “Como estudar este módulo” é idêntico em 27 arquivos.
- As disciplinas do plano principal são fichas curtas, o que é adequado para currículo e ainda não é material de estudo.

### O que passou

- Nenhum link interno quebrado fora de benchmark/ (lá há 85, pasta que a checagem ignora de propósito).
- Conferi por aritmética 241 dos 440 gabaritos do NM0, sem divergência. Os outros 199, em geral problemas em texto, não foram conferidos.
- Nenhum segredo ou e-mail encontrado no conteúdo dos arquivos pelos padrões pesquisados.

## 5. Lacunas

| Lacuna | Quando importa |
| --- | --- |
| Verificação e mapa de itens das listas do NM0 | Agora |
| Regra de branches documentada | Agora |
| Catálogo de unidades, projetos, referências, eixos e escalas | Marco 2 |
| Schemas com versão | Marco 2 |
| Modelos (templates) por tipo de conteúdo | Marco 2 |
| ADRs, visão, modelo de dados, glossário, registro de débitos | Marcos 1 e 2 |
| Licença | Antes de abrir o repositório como portfólio |
| Conceitos como entidade, com relações entre si | Quando houver o primeiro texto explicativo |
| Competências nas 58 disciplinas do plano principal | Antes de estudar cada uma |
| Verificação de provas formais e projetos | Antes da graduação usar a skill |
| Teste da skill com estudante real | A própria validação recomenda um mês de uso |

Não proponho preencher conteúdo em massa. Texto gerado antes de ser estudado criaria volume sem validação.

## 6. Riscos

### Riscos do produto

| Risco | Impacto | Mitigação |
| --- | --- | --- |
| Mapa e repositório continuarem divergindo | Alto | D1: uma fonte só, com exportação do Mapa |
| Perda de registros numa fusão de branches | Alto | Regra escrita; depois, separar o progresso |
| Reorganização quebrar histórico e skill | Alto | Manter caminhos; migrar com teste |
| Arquitetura crescer mais que o estudo | Médio | Entrar só o que tiver uso; P0 pequeno |

### Threat model (STRIDE)

| Ameaça | Onde | Mitigação atual e proposta | Risco residual |
| --- | --- | --- | --- |
| Adulteração: inflar autonomia | .yml e CSV editáveis | Regras da skill, filtro de âncoras, histórico Git | Aceitável para uso pessoal |
| Elevação de privilégio: código arbitrário | verificar.py executa o campo codigo: | Processo python -I com 5 s, que não é sandbox: pode ler arquivos, usar rede e herdar variáveis. Roda no CI a cada push ou PR. Isolar antes de aceitar contribuições | Alto se houver terceiros |
| Cadeia de suprimentos | CI e dependências | Travar versões, fixar actions por commit, limitar permissions | Baixo hoje |
| Exposição de informação | Publicação do repositório | Registros de estudo, rotina e um e-mail pessoal em 3 commits iriam junto | Decidir antes de publicar |
| Repúdio e falsificação de autoria | Commits | Histórico Git; assinatura de commits é opcional | Baixo |
| Negação de serviço | Intervalos e expressões | Limites já implementados | Muito baixo |

### IA

A skill já trata o conteúdo como dado, e o teste de ataque de 20/11 corrigiu, na versão do repositório, as brechas achadas (resistiu a 7 de 10 tentativas antes da correção). Para o futuro, o Knowledge Core deve seguir quatro regras: material nunca concede permissão; consumidor de IA lê, mas não executa exemplos; cada trecho carrega origem e status de revisão; dados do estudante ficam fora do índice de conhecimento.

### Exemplos de código (quando existirem)

Cada um declara contexto, ambiente, dependências, requisitos, como executar, riscos e limitações. Nada é executado automaticamente sem isolamento.

## 7. Potencial de evolução

O potencial é alto porque o difícil de reconstruir já existe: um grafo de pré-requisitos validado, portões mensuráveis e um modelo de respostas item a item.

| Estágio | Já aproveitável | O que falta |
| --- | --- | --- |
| 1. Knowledge Core | Grafo, códigos, validação, CI | Schema, catálogo, separação do progresso |
| 2. Aplicação de consulta | YAML e CSV legíveis por qualquer tecnologia | Conteúdo para consultar e um export JSON |
| 3. Plataforma de aprendizagem | Autonomia, fixação, mapa de deficiências, revisão espaçada | Separar dados pessoais; interface; mais de um estudante só se houver demanda |

O motor de estudo já antecipa recursos do estágio 3. Mantenha-o, mas trate-o como consumidor do Core, não como parte dele.

## 8. Proposta inicial de arquitetura

Três contextos separados: o conhecimento, o motor que o usa e os dados de quem estuda.

### Decisões e alternativas

| Decisão | Por quê | Alternativas descartadas | Custo ou risco |
| --- | --- | --- | --- |
| D1. Git é a fonte de verdade | Validação, histórico e consumo por programa já existem lá | Manter o Mapa como canônico (não é validado pelo CI); dividir por assunto (exige sincronizar) | Editar tabelas em arquivo é menos confortável |
| D2. Arquivos Markdown e YAML, sem banco de dados | 86 itens cabem folgadamente | Banco relacional ou de grafos: infraestrutura sem necessidade | Consultas ricas ficam para o export |
| D3. Códigos atuais como ID | Legíveis e já usados no histórico | UUID (ilegível, exige migrar); slug do título (muda com o nome) | O prefixo sugere a área; reclassificar não renomeia |
| D4. Separar progresso do currículo | Reduz a divergência entre branches | Manter como está e só documentar | Mexe em scripts, testes e skill |
| D5. JSON Schema | Escreve o schema que o código já supõe; independe de linguagem | Pydantic (preso a Python); só checagens manuais | Nova dependência (jsonschema) |

### Modelo de conhecimento

| Entidade | Situação |
| --- | --- |
| Módulo ou disciplina, competência, lista, item | Já existem |
| Eixo, unidade do curso, projeto, referência, escala | Formalizar no catálogo |
| Conceito, termo de glossário | Quando houver texto |
| Trilha | Derivada do grafo, não armazenada |
| Tecnologia, habilidade, avaliação como entidade própria | Não criar agora |

Relações explícitas: pré-requisito, requer unidade, unidade cobre disciplina, projeto consolida disciplina. Inferidas: “libera”, ancestrais e cadeias críticas. Complementa, contrasta e relacionado só entram com os conceitos. Pré-requisito redundante por transitividade pode ficar, se for intencional; o diagrama passa a ser gerado do YAML. Ciclos continuam barrados pelo script.

IDs: nunca mudam nem são reaproveitados. Códigos aposentados (como M0) entram numa lista no catálogo.

### Metadados

| Classe | Campos |
| --- | --- |
| Obrigatórios | codigo, nome, eixo, fase, ordem, prerequisitos, horas_previstas, nivel_alvo, portao.criterio |
| Condicionais | bloco (nivelamento), competencias (para receber respostas), semestre_inicio e semestre_fim (fora do nivelamento), unidades_relacionadas, requer_unidades |
| Transitórios (saem no Marco 4) | status, inicio, nivel_atingido, diagnostico, portao.data, portao.resultado, portao.evidencia. O schema do Marco 2 os aceita |
| Opcionais | referências, projetos, tags |
| Futuros | tecnologias, público-alvo, tempo por conceito |
| Fora do arquivo | datas, autor e versão (vêm do Git); idioma (um só, no repositório) |

O schema leva schema_version. Campo opcional novo é compatível; mudança que quebra exige script de migração.

### Padrão de conteúdo

| Tipo | Obrigatório |
| --- | --- |
| Disciplina | identificação, tópicos, referência, competência final, portão |
| Módulo de nivelamento | o anterior, aplicações e competências; o roteiro comum vira um documento único |
| Lista | instruções, itens com nível, gabarito, verificação |
| Conceito (futuro) | o que é, que problema resolve, quando usar, exemplo, limites, referências |

### Validação e automação

Estender o que existe, sem ferramenta nova além do jsonschema: schema, código único, referências a unidades e projetos, diagrama gerado e lista sem verificação. Cada regra nasce com teste. O CI do GitHub Actions já bloqueia o que falhar.

## 9. Estrutura recomendada

Recomendo a organização híbrida: pastas por tipo de artefato, arquivos planos nomeados por ID e domínio como metadado.

| Organização | Benefício | Limitação | Custo de migrar |
| --- | --- | --- | --- |
| Por domínio | Navegação intuitiva | Itens interdisciplinares e reclassificações movem arquivos | Alto |
| Por tecnologia | Boa para material de ferramentas | Não serve a um currículo de fundamentos | Alto |
| Por tipo de material | Validação simples | Pouca visão por assunto | Baixo (é quase o atual) |
| Híbrida (recomendada) | Caminhos estáveis; visões por assunto geradas | Depende de índices gerados | Baixo, só acréscimos |

Proposta, ainda não implementada:

```
plano-de-estudos/
  disciplinas/     mantém
  exercicios/      mantém
  registro/        mantém (estado.yml entra no Marco 4)
  catalogo/        novo: eixos, unidades, projetos, referencias, escalas
  schemas/         novo (Marco 2)
  templates/       novo (Marco 2)
  docs/
    arquitetura/   novo: visao, auditoria, modelo, seguranca, roadmap, debitos
    adr/           novo: uma decisão por arquivo
    referencia/    novo: exportação do Mapa de Formação
    skills/        mantém
  scripts/ tests/ skills/ benchmark/ plano.yml    mantêm
```

conceitos/ só é criada com o primeiro conceito. benchmark/ fica onde está, identificado como evidência, porque vários documentos apontam para ele. Um C4 de contexto pode acompanhar a visão; diagramas de contêiner e componente ainda não agregam.

## 10. Roadmap preliminar

O P0 tem cinco itens pequenos e não move nenhum arquivo.

| Prioridade | Iniciativas |
| --- | --- |
| P0 integridade | Feito em 25/11/2026 nos PRs #5 e #6, mesclados na main e trazidos para a branch de estudo: skill 1.0.2 · D1 aprovada e Mapa exportado para docs/referencia/ · regra de branches em docs/fluxo-git.md e na skill · itens das listas antigas do NM0 nunca contam como âncora, e lista de 6 problemas-âncora · catalogo/ com eixos, unidades, projetos e escalas · regressão da skill sem portões violados (4,75 · 4,55 · 5,00 · 4,55). |
| P1 consolidação | Documentos de arquitetura e ADRs · schemas · templates · alinhar escalas e textos divergentes |
| P2 automação | Novas validações · diagrama gerado · separar progresso · endurecer CI e execução de código |
| P3 futuro | Export JSON, aplicação, plataforma, IA |

### Marcos

| Marco | Objetivo, escopo e entregáveis | Depende de | Risco | Aceite | Não será feito |
| --- | --- | --- | --- | --- | --- |
| 1. Fundação | Esta auditoria, D1 a D5, ADRs, visão, Mapa exportado, regra de branches, âncoras do NM0, skill instalada atualizada. Feito em 25/11/2026: skill, Mapa, regra de branches, âncoras, catálogo e regressão; faltam ADRs e visão. | Sua aprovação | Documentar demais | Decisões registradas; CI verde | Mover arquivos |
| 2. Padronização | Catálogo, schemas, templates, escalas únicas, taxonomia por eixo | 1 | Quebrar o formato atual | 100% dos 86 arquivos validam | Conteúdo novo em massa |
| 3. Qualidade | Validações, testes, relatório de qualidade, CI mais restrito | 2 | Regras que travam o estudo | Cada regra com teste; nenhuma referência solta | Indexador |
| 4. Consolidação | Separar progresso, migrar registros, ajustar scripts e skill | 3 | Perda de histórico | Mesmos números no mapa antes e depois; reversível por Git | Reorganizar por domínio |
| 5. Aplicação | Export JSON, navegação, busca, filtros | 4 e conteúdo para consultar | Construir sem uso | Lê o Core sem copiá-lo | Contas, API sem consumidor |
| 6. Plataforma | Trilhas, avaliações, progresso, IA contextual | 5 e uso real | Autonomia falsa; custo | Definido após o Marco 5 | Nada antes da hora |

### Critérios para o Core evoluir além do Marco 4

| Critério | Hoje | Meta |
| --- | --- | --- |
| Itens com ID único verificado | IDs existem, unicidade de disciplina não checada | 100% |
| Metadados validados por schema | Nenhum schema | 100% |
| Referências a unidades e projetos resolvidas | Nenhuma no Git | 100% |
| Listas com verificação | 0 de 4 | 100% ou exceção registrada |
| Fatos de currículo com uma só origem | Várias cópias | Uma origem, o resto gerado |
| Progresso separado do conhecimento | Não | Sim |
| Histórico preservado | Sim | Sim, conferido após cada migração |

Governança proposta: mudança de estrutura por pull request para a main, com ADR quando mudar uma decisão; andamento só na branch de estudo.

## Método, limites e aprovação

Nada foi alterado no repositório nem no Mapa, e não houve commit. Não executei scripts nem testes do repositório; fiz checagens estáticas com código próprio. O resultado do CI vem do histórico do GitHub.

Limites desta auditoria:

- Li a documentação central, os scripts principais e a skill; das disciplinas, uma amostra, mais a análise dos 86 cabeçalhos e seções. Dos benchmarks, só relatórios por amostragem.
- No Mapa (revisão 74), não li a seção 8.2. Li por alto os capítulos 9, 10 e 13; o cotejo com o repositório se concentrou nos capítulos 16 a 18.
- Não testei o comportamento da skill.

Próxima etapa: você aprova, ajusta ou recusa D1 a D5. Com a aprovação, executo um item do P0 por vez, mostro o que mudou e valido antes de seguir.

Fontes: repositório plano-de-estudos (main em 54bb3ec, branch de estudo em 97aaffd) e Mapa de Formação.
