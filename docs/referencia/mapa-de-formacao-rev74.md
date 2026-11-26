# Mapa de Formação — Engenheiro Generalista Polímata (2 a 10 anos)

> **Cópia congelada, só para referência.** Exportada em 25/11/2026 da revisão 74 do [documento original](https://claude.ai/artifact/Tj24HfdJf4Sxuf4ArM921Y). A fonte de verdade do plano é este repositório: onde este texto divergir de `disciplinas/`, `catalogo/`, `AVALIACOES.md` ou `plano.yml`, valem eles. Não edite este arquivo.
>
> Divergências conhecidas na data da cópia:
>
> - não cita o portão de autonomia, exigido nos módulos do nivelamento a partir de 20/11/2026;
> - a seção 18 usa 4 níveis de exercício; o repositório usa 5;
> - a seção 14.3 manda começar por NM1 e NL1; o repositório começa pelo NM0.
>
> Os diagramas do original não são exportados para Markdown: no lugar deles há um aviso em texto.
>
> Na versão publicada, os horários da rotina pessoal (seções 16.1 e 17.1) foram tirados; as horas por semana ficaram (26/11/2026).

Nov 16, 2026 · @Rodrigo Rosario

## 1. Diagnóstico e filosofia da formação

O objetivo é viável, mas só se a amplitude for tratada como orçamento de horas: os oito eixos pedidos somam 63 disciplinas, e levá-las todas ao nível de um bom curso universitário custaria cerca de 10.700 h (63 × 170 h). Nenhum plano abaixo de 10 anos cobre tudo nessa profundidade; cada horizonte é, portanto, uma escolha diferente sobre o que aprofundar, o que apenas reconhecer e o que deixar de fora.

### Premissas de cálculo

| Premissa | Valor | Justificativa |
| --- | --- | --- |
| Semanas úteis por ano | 48 | 4 semanas de pausa; sem pausa, planos longos não se sustentam |
| Semestre | 24 semanas | Unidade de planejamento e de avaliação |
| Disciplina universitária de referência | ≈ 170 h | Uma disciplina de 12 unidades do MIT pede 12 h/semana por 14 semanas, somando aula, leitura e exercícios |
| Graduação de referência | ≈ 3.600 h de aula | Ordem de grandeza da carga mínima de um bacharelado em engenharia no Brasil, sem contar estudo individual |
| Hora de estudo | Hora de trabalho ativo | Assistir aula conta só dentro da fatia de teoria; ver seção 9 |
| Ponto de partida assumido | Ensino médio completo e alguma programação | O nivelamento da seção 18 começa por diagnósticos; quem passar dispensa os módulos correspondentes. Com a graduação em Engenharia de Software em andamento, valem as seções 15 a 18 |

### Decisões de projeto do mapa

1. **Um catálogo, seis planos.** As 63 disciplinas são definidas uma única vez na seção 2 (tópicos, ordem, pré-requisitos, referência, competência). Cada plano escolhe quais entram, com quantas horas e até que nível de domínio.
2. **Nível de domínio explícito.** Toda disciplina em todo plano tem um alvo de 1 (reconhecimento) a 7 (pesquisa), conforme a escala da seção 12. Horas e nível andam juntos: 40 h compram nível 1–2, 170 h compram nível 4, 260 h ou mais com projeto próprio compram 5–6.
3. **Sequenciamento por dependência.** A ordem dentro de cada plano foi gerada respeitando o grafo de pré-requisitos; nenhuma disciplina começa antes das que a sustentam.
4. **Três orçamentos além das disciplinas.** Revisão cumulativa e avaliações, projetos integradores e, nos planos longos, pesquisa têm horas próprias. As horas de disciplina já incluem os laboratórios do curso de referência (por exemplo, os labs de CS:APP ou do xv6).
5. **Uma espinha dorsal de especialização.** Todos os planos têm o mesmo vértice principal, sistemas de dados distribuídos (C8, C9, D3, D4, D6), porque é onde ciência da computação, engenharia de software e engenharia de dados se cruzam. Os planos longos acrescentam um segundo vértice.

### Conhecimento acadêmico e conhecimento profissional

|  | Acadêmico | Profissional |
| --- | --- | --- |
| O que é | Modelos, provas, mecanismos, limites teóricos | Ferramentas, operação, custo, convenções de equipe |
| Meia-vida | Décadas | Poucos anos |
| Como se adquire | Livro-texto, exercícios, implementação do zero | Documentação oficial, uso em produção, incidentes |
| No mapa | Eixos A, B, C e a base de F | Eixos D, E, G e a parte aplicada de F |
| Regra | Vem primeiro e recebe mais horas | Entra depois do mecanismo; ferramenta é instância do conceito (Kafka é um log replicado; Spark é um plano de execução distribuído) |

### O que nenhum plano promete

Domínio de nível 6–7 em todas as áreas não cabe em uma vida de estudo paralelo ao trabalho. O perfil polímata realista é: fundamentos universais sólidos (nível 4), um ou dois vértices profundos (nível 6) e capacidade demonstrada de entrar em área nova com rapidez. Os planos de 2 e 4 anos entregam a primeira parte; os de 5 a 8 anos, a segunda; o de 10 anos, a terceira.

## 2. Mapa geral das áreas e suas dependências

A formação tem 63 disciplinas em oito eixos, organizadas em seis camadas de dependência. Os códigos abaixo (M5, C8, D4…) são usados em todos os planos; a bibliografia completa de cada referência está na seção 10.

&#91;embedded content: mapa de dependências · base, 3 trilhas, 3 vértices\]

Cada caixa depende da que está acima; as setas horizontais marcam as dependências entre trilhas: o cálculo sustenta a física, a arquitetura de computadores sustenta os sistemas operacionais e as equações diferenciais sustentam sinais e controle. O vértice de dados, em destaque, é o principal em todos os planos; o de IA depende também da trilha de computação (C8, S4, S5), e o físico, de probabilidade (M6). Os pré-requisitos exatos de cada disciplina estão nas tabelas do catálogo.

### 2.1 Classificação das disciplinas

| Classe | Disciplinas | Regra |
| --- | --- | --- |
| Fundamentos universais | M0–M7, P1, P2, C1, E3, E4, C5, C7, C8, S1, S2, G1 | Entram em todos os planos; nunca abaixo do nível 3 |
| Núcleo de engenharia | M8–M10, F1, F2, E1, C2, C3, C4, C6, C9, C10, S3–S6, D1–D3, G2, G3, A1 | Entram a partir do plano de 4 anos; nível 3–5 |
| Especialização (vértices) | Dados distribuídos: C8, C9, C6, D3, D4, D6, G4. IA: A1–A5, M10. Hardware e controle: E5, E6, H1, H2 | Um vértice nos planos A–D, dois em E, dois ou três em F; nível 5–7 |
| Complementares | M11–M13, F3, F4, E2, D5, H3–H6 | Nível 1–3; ampliam repertório e maturidade |

### 2.2 Catálogo — Eixo A, Matemática

| Cód. | Disciplina | Tópicos, na ordem | Pré-req. | Referência-base | Competência ao concluir |
| --- | --- | --- | --- | --- | --- |
| M0 | Pré-cálculo | Álgebra, funções, exponenciais e logaritmos, trigonometria, complexos, desigualdades | — | Lang; Axler | Manipular expressões e funções sem hesitação nem calculadora |
| M1 | Lógica, provas e conjuntos | Lógica proposicional e de predicados, técnicas de prova, indução, conjuntos, relações, funções, cardinalidade | M0 | Velleman; Halmos | Escrever uma prova correta e apontar a falha de uma incorreta |
| M2 | Matemática discreta | Somatórios e recorrências, combinatória, teoria dos números e aritmética modular, grafos, probabilidade discreta | M1 | Lehman, Leighton e Meyer (MIT 6.042J); Rosen | Modelar um problema computacional com grafos, contagem ou recorrência |
| M3 | Cálculo I | Limites, derivadas, aplicações, integrais, técnicas, séries e Taylor | M0 | Stewart; MIT 18.01; Spivak (aprofundamento) | Analisar taxa de variação, acumulação e aproximação de uma função |
| M4 | Geometria analítica e cálculo multivariável | Vetores, retas e planos, cônicas; derivadas parciais, gradiente, integrais múltiplas, Green, Stokes, Gauss | M3 | Stewart; MIT 18.02 | Derivar e integrar em várias variáveis e interpretar o gradiente |
| M5 | Álgebra linear | Sistemas, espaços vetoriais, transformações, ortogonalidade, determinantes, autovalores, SVD, formas quadráticas | M0 (M1 para a versão com provas) | Strang (MIT 18.06); Axler | Decompor uma matriz e explicar o que cada fator significa no problema |
| M6 | Probabilidade | Espaços de probabilidade, condicional e Bayes, variáveis aleatórias, distribuições, esperança, leis dos grandes números, TCL, cadeias de Markov | M2, M3 | Blitzstein e Hwang (Harvard Stat 110) | Modelar incerteza e calcular com distribuições conjuntas |
| M7 | Estatística | Estimação, máxima verossimilhança, intervalos, testes, regressão, inferência bayesiana, bootstrap, desenho de experimentos | M6, M5 | Wasserman; Casella e Berger | Desenhar e criticar um experimento e sua análise |
| M8 | Equações diferenciais | Primeira ordem, lineares, sistemas, Laplace, estabilidade, introdução a Fourier e EDP | M4, M5 | Boyce e DiPrima; MIT 18.03; Strogatz | Modelar um sistema dinâmico e classificar sua estabilidade |
| M9 | Métodos numéricos | Ponto flutuante e erro, raízes, sistemas lineares, interpolação, integração, EDO numérica, álgebra linear numérica | M5, M3, P1 | Burden e Faires; Trefethen e Bau | Implementar um solver e estimar seu erro e seu condicionamento |
| M10 | Otimização | Programação linear, dualidade, convexidade, gradiente e Newton, KKT, métodos estocásticos | M4, M5 | Boyd e Vandenberghe; Nocedal e Wright | Formular um problema como otimização e escolher o método |
| M11 | Pesquisa operacional | Modelagem linear e inteira, simplex, fluxo em redes, filas, simulação, análise de decisão | M10, M6 | Hillier e Lieberman | Dimensionar um recurso com modelo de filas ou programação inteira |
| M12 | Teoria da informação | Entropia, informação mútua, codificação de fonte, capacidade de canal, códigos, ligações com aprendizado | M6 | Cover e Thomas; MacKay | Calcular limites de compressão e de transmissão de uma fonte |
| M13 | Análise real | Números reais, sequências, continuidade, diferenciação, integral de Riemann, espaços métricos | M1, M3 | Abbott; Rudin | Provar resultados de convergência com rigor |

### 2.3 Catálogo — Eixo B, Física e fundamentos de engenharia

| Cód. | Disciplina | Tópicos, na ordem | Pré-req. | Referência-base | Competência ao concluir |
| --- | --- | --- | --- | --- | --- |
| F1 | Mecânica clássica | Cinemática, leis de Newton, energia, momento, rotação, oscilações, gravitação | M3 | Nussenzveig v.1 ou Halliday; MIT 8.01; Kleppner (aprofundamento) | Modelar um sistema mecânico e resolver sua dinâmica |
| F2 | Eletricidade e magnetismo | Campo e potencial elétrico, capacitância, corrente, campo magnético, indução, equações de Maxwell | F1, M4 | Nussenzveig v.3 ou Halliday; MIT 8.02; Purcell e Morin | Explicar o funcionamento físico de capacitor, indutor e linha de transmissão |
| F3 | Termodinâmica e ondulatória | Temperatura, leis da termodinâmica, entropia; ondas, interferência, óptica básica | F1, M4 | Nussenzveig v.2 e v.4; Schroeder | Aplicar balanço de energia e de entropia; analisar propagação de ondas |
| F4 | Física moderna | Relatividade restrita, quântica introdutória, átomo, sólidos e semicondutores | F2, F3, M8 | Tipler e Llewellyn; Griffiths (aprofundamento) | Explicar por que um transistor funciona a partir da física de bandas |
| E1 | Circuitos elétricos | Leis de Kirchhoff, Thévenin e Norton, RC, RL, RLC, fasores, resposta em frequência | F2 | Nilsson e Riedel; Agarwal e Lang (MIT 6.002) | Analisar um circuito linear no tempo e na frequência |
| E2 | Eletrônica analógica e digital | Diodos, MOSFET e BJT, amplificador operacional, lógica CMOS, conversão A/D e D/A | E1 | Sedra e Smith; Horowitz e Hill | Projetar um estágio de condicionamento de sinal e ler um esquemático |
| E3 | Sistemas digitais | Álgebra booleana, lógica combinacional e sequencial, máquinas de estado, HDL, FPGA | M1 | Harris e Harris; Nisan e Schocken | Projetar um circuito síncrono em HDL e simulá-lo |
| E4 | Arquitetura de computadores | Conjunto de instruções (RISC-V), caminho de dados, pipeline, hierarquia de memória e cache, memória virtual, paralelismo | E3, P1 | Patterson e Hennessy; Berkeley CS61C; Hennessy e Patterson (avançado) | Prever o desempenho de um programa a partir do hardware |
| E5 | Microcontroladores e embarcados | Periféricos, interrupções, temporização, barramentos, RTOS, tempo real, consumo | E4, P2, E1 | Lee e Seshia; Valvano | Escrever firmware sem sistema operacional com restrições de tempo |
| E6 | Sinais e sistemas | Sistemas lineares invariantes, convolução, Fourier, Laplace, transformada Z, amostragem | M8, M4 | Oppenheim e Willsky | Analisar e filtrar um sinal amostrado |

### 2.4 Catálogo — Eixo C, Ciência da Computação

| Cód. | Disciplina | Tópicos, na ordem | Pré-req. | Referência-base | Competência ao concluir |
| --- | --- | --- | --- | --- | --- |
| P1 | Programação e abstração | Abstração procedural e de dados, recursão, funções de ordem superior, estado, testes, depuração; Python e C | — | Abelson e Sussman (SICP); Berkeley CS61A; Kernighan e Ritchie | Decompor um problema e escrever um programa correto de médio porte |
| P2 | Programação de sistemas | Representação de dados, assembly, ligação, memória, processos, sinais, E/S, sockets | P1 | Bryant e O'Hallaron (CS:APP); CMU 15-213 | Explicar o que a máquina faz com um programa em C e depurá-lo em baixo nível |
| C1 | Algoritmos e estruturas de dados | Análise assintótica, listas, árvores, heaps, hash, ordenação, grafos, divisão e conquista, gulosos, programação dinâmica; avançado: amortizada, fluxo, randomizados, strings | P1, M2 | Cormen et al. (CLRS); MIT 6.006 e 6.046; Sedgewick e Wayne | Projetar, provar e implementar um algoritmo para um problema novo |
| C2 | Teoria da computação e complexidade | Autômatos finitos, linguagens regulares e livres de contexto, máquinas de Turing, decidibilidade, P e NP, reduções, classes de espaço | M2, C1 | Sipser; Arora e Barak (avançado) | Reconhecer um problema intratável ou indecidível e prová-lo por redução |
| C3 | Linguagens e paradigmas | Semântica, cálculo lambda, sistemas de tipos, programação funcional, orientação a objetos, lógica; interpretadores | P1, M1 | SICP; Krishnamurthi (PLAI); Pierce (avançado); Hutton | Aprender uma linguagem nova pela sua semântica, não pela sintaxe |
| C4 | Compiladores | Análise léxica e sintática, AST, análise semântica, representação intermediária, otimização, geração de código, runtime e coleta de lixo | C2, C3, P2 | Aho et al.; Nystrom; Stanford CS143; Appel | Construir um compilador de uma linguagem pequena até código de máquina |
| C5 | Sistemas operacionais | Processos, escalonamento, memória virtual, concorrência, sistemas de arquivos, E/S, virtualização | P2, E4 | Arpaci-Dusseau (OSTEP); MIT 6.1810 (xv6); Berkeley CS162 | Modificar um kernel didático e explicar o custo de cada abstração |
| C6 | Concorrência e paralelismo | Threads, exclusão mútua, modelos de memória, estruturas sem bloqueio, linearizabilidade, assíncrono, paralelismo de dados | C5, C1 | Herlihy e Shavit; Stanford CS149 | Escrever código concorrente correto e argumentar por quê |
| C7 | Redes de computadores | Camadas, HTTP e DNS, TCP e UDP, controle de congestionamento, IP e roteamento, enlace, TLS | P2 | Kurose e Ross; Stanford CS144; Stevens | Implementar um protocolo confiável e diagnosticar tráfego capturado |
| C8 | Bancos de dados | Modelo relacional, álgebra, SQL, normalização; armazenamento, índices, execução, otimização de consultas, transações, concorrência, recuperação | C1, P2 | Silberschatz et al.; CMU 15-445; Petrov; Hellerstein et al. | Explicar e prever o plano de execução e o comportamento transacional de um SGBD |
| C9 | Sistemas distribuídos | Modelos de falha, tempo e ordenação, replicação, consenso (Paxos, Raft), modelos de consistência, transações distribuídas, particionamento | C5, C7, C8 | Kleppmann (DDIA); MIT 6.5840 (antigo 6.824); van Steen e Tanenbaum; artigos originais | Implementar replicação por consenso e raciocinar sobre falhas parciais |
| C10 | Segurança da informação | Modelagem de ameaças, criptografia aplicada, autenticação, segurança de memória e de software, web, redes | C5, C7, M2 | Anderson; Katz e Lindell; MIT 6.858 | Modelar ameaças de um sistema e corrigir as classes comuns de vulnerabilidade |

### 2.5 Catálogo — Eixo D, Engenharia de Software

| Cód. | Disciplina | Tópicos, na ordem | Pré-req. | Referência-base | Competência ao concluir |
| --- | --- | --- | --- | --- | --- |
| S1 | Projeto e construção de software | Modularidade, ocultação de informação, complexidade, SOLID, padrões de projeto, refatoração, revisão de código | P1, C1 | Ousterhout; Gamma et al.; Fowler (Refactoring) | Projetar módulos de interface simples e justificar cada decisão |
| S2 | Testes e qualidade | Testes de unidade, integração e propriedade, TDD, análise estática, fuzzing, código legado | S1 | Beck; Feathers | Tornar testável um código sem testes e alterá-lo com segurança |
| S3 | Requisitos e modelagem | Elicitação, especificação, casos de uso, modelagem de domínio, Domain-Driven Design, notações (UML, C4) | S1 | Wiegers e Beatty; Evans; Sommerville | Transformar um problema de negócio em modelo de domínio e requisitos verificáveis |
| S4 | Arquitetura de software | Atributos de qualidade, estilos arquiteturais, arquitetura limpa e hexagonal, monólito e microsserviços, mensageria, registro de decisões, modernização de legado | S1, S3, C8, C7 | Bass, Clements e Kazman; Richards e Ford; Fowler (PoEAA); Martin | Propor uma arquitetura, explicitar os trade-offs e documentá-la |
| S5 | Entrega e operação | Integração e entrega contínuas, DevOps, SRE, objetivos de nível de serviço, métricas, logs e traces, resposta a incidentes | S2, G1, G2 | Humble e Farley; Beyer et al. (SRE); Majors et al. | Levar um serviço a produção com pipeline, SLO e observabilidade |
| S6 | Sistemas escaláveis e resilientes | Padrões de estabilidade, cache, filas, contrapressão, degradação, capacidade, segurança no ciclo de desenvolvimento | S4, C9 | Nygard; Kleppmann | Projetar um sistema que degrada com controle sob falha e sob carga |

### 2.6 Catálogo — Eixo E, Engenharia de Dados

| Cód. | Disciplina | Tópicos, na ordem | Pré-req. | Referência-base | Competência ao concluir |
| --- | --- | --- | --- | --- | --- |
| D1 | Modelagem de dados e SQL avançado | Modelagem relacional e dimensional, OLTP e OLAP, funções de janela, CTE, planos de execução, indexação e tuning | C8 | Kimball e Ross; Winand; Celko | Modelar um domínio para transação e para análise e otimizar consultas pelo plano |
| D2 | Arquiteturas analíticas | Data Warehouse, Data Lake, Lakehouse, formatos colunares, formatos de tabela, ETL e ELT, engenharia analítica | D1 | Kimball e Ross; Reis e Housley; Armbrust et al.; documentação do dbt | Escolher a arquitetura de armazenamento analítico para um caso e justificar |
| D3 | Processamento distribuído batch | MapReduce, Spark por dentro (RDD, DAG, shuffle, otimizador), particionamento, assimetria, tuning | D2, C9, C6 | Dean e Ghemawat; Zaharia et al.; Chambers e Zaharia | Prever e corrigir o custo de um job distribuído a partir do plano físico |
| D4 | Streaming e CDC | Log como abstração, Kafka por dentro, semânticas de entrega, tempo de evento e marcas d'água, janelas, estado, captura de mudanças | D3, C9 | Akidau et al.; Kreps et al.; Narkhede et al. | Projetar um pipeline de eventos com garantias de entrega e de ordem explícitas |
| D5 | Orquestração, qualidade e governança | Orquestração de pipelines, linhagem, qualidade de dados, contratos de dados, catálogo, privacidade | D2, S5 | DAMA-DMBOK; Reis e Housley; documentação do Airflow | Operar pipelines com testes de dados, contratos e linhagem |
| D6 | Arquitetura de plataformas de dados | Projeto de ponta a ponta, camadas de serviço, multi-inquilino, custo, malha de dados, dimensionamento | D3, D4, D5, G3, S4 | Kleppmann; Dehghani; Reis e Housley | Arquitetar uma plataforma de dados com requisitos de latência, custo e confiabilidade |

### 2.7 Catálogo — Eixo F, Inteligência Artificial e Ciência de Dados

| Cód. | Disciplina | Tópicos, na ordem | Pré-req. | Referência-base | Competência ao concluir |
| --- | --- | --- | --- | --- | --- |
| A1 | Machine Learning | Aprendizado supervisionado e não supervisionado, viés e variância, regularização, modelos lineares, árvores e ensembles, SVM, validação, engenharia de atributos | M5, M6, M7, M10 | James et al. (ISLR); Hastie et al.; Bishop; Stanford CS229 | Treinar, validar e diagnosticar um modelo, derivando o algoritmo que o ajusta |
| A2 | Deep Learning | Perceptron multicamada, retropropagação, otimização, redes convolucionais e recorrentes, atenção e transformers, regularização | A1, M4 | Goodfellow et al.; Prince; Stanford CS231n | Implementar e treinar uma rede do zero e depurar seu treinamento |
| A3 | PLN e LLMs | Representações, modelos de linguagem, transformers, pré-treino e ajuste fino, modelos generativos, avaliação | A2 | Jurafsky e Martin; Stanford CS224n; Vaswani et al. | Explicar e reproduzir em pequena escala o funcionamento de um modelo de linguagem |
| A4 | Sistemas de IA | Recuperação de informação, busca vetorial, RAG, agentes e uso de ferramentas, sistemas de recomendação, avaliação de ponta a ponta | A3, C8, S4 | Manning et al.; Lewis et al.; Aggarwal | Construir uma aplicação com LLM e medir sua qualidade com método |
| A5 | MLOps e avaliação | Pipelines de treino, repositório de atributos, serving, desvio de dados, experimentação, monitoramento, dívida técnica | A1, S5, D5 | Huyen; Sculley et al. | Operar um modelo em produção com monitoramento e retreino |

### 2.8 Catálogo — Eixo G, Infraestrutura

| Cód. | Disciplina | Tópicos, na ordem | Pré-req. | Referência-base | Competência ao concluir |
| --- | --- | --- | --- | --- | --- |
| G1 | Linux, Unix e shell | Sistema de arquivos, processos, permissões, shell scripting, ferramentas de texto, chamadas de sistema, serviços | P1 | Shotts; Kerrisk; MIT Missing Semester | Administrar e automatizar uma máquina Linux pela linha de comando |
| G2 | Virtualização, containers e Kubernetes | Hipervisores, namespaces e cgroups, Docker, orquestração, arquitetura do Kubernetes, rede de containers | G1, C5, C7 | Documentação do Kubernetes; Burns et al. | Explicar um container como processo isolado e operar um cluster pequeno |
| G3 | Cloud e infraestrutura como código | Modelos de serviço, computação, armazenamento e rede, identidade e acesso, AWS como base com mapeamento para Azure e GCP, Terraform, custo | G2, C7 | Documentação oficial e Well-Architected; Brikman | Provisionar por código um ambiente reproduzível e estimar seu custo |
| G4 | Alta disponibilidade e desempenho | Balanceamento, failover, recuperação de desastre, análise de desempenho, profiling, segmentação de rede | G3, C9, C5 | Gregg; Beyer et al. (SRE) | Encontrar um gargalo com método e projetar para uma meta de disponibilidade |

### 2.9 Catálogo — Eixo H, Engenharia generalista e interdisciplinar

| Cód. | Disciplina | Tópicos, na ordem | Pré-req. | Referência-base | Competência ao concluir |
| --- | --- | --- | --- | --- | --- |
| H1 | Engenharia de controle | Modelagem, função de transferência, estabilidade, PID, lugar das raízes, resposta em frequência, espaço de estados | E6, M8, M5 | Åström e Murray; Ogata | Projetar e sintonizar um controlador para uma planta modelada |
| H2 | Automação, robótica, IoT e sistemas ciberfísicos | Sensores e atuadores, automação industrial, cinemática, estimação e filtro de Kalman, protocolos de IoT, sistemas ciberfísicos | H1, E5, M6 | Lynch e Park; Thrun et al.; Lee e Seshia | Integrar sensor, estimador, controlador e atuador em um sistema físico |
| H3 | Engenharia de produção e economia da tecnologia | Processos e capacidade, filas e produção enxuta, custos, economia de plataformas e de informação | — | Slack et al.; Shapiro e Varian | Avaliar uma decisão técnica pelo custo, pela capacidade e pelo efeito de rede |
| H4 | Gestão de projetos de engenharia | Escopo, estimativa, risco, abordagens ágeis e preditivas, liderança técnica | S3 | Brooks; Guia PMBOK | Planejar e conduzir um projeto técnico com riscos explícitos |
| H5 | Metodologia científica e escrita técnica | Método, leitura de artigos, desenho experimental, reprodutibilidade, escrita, revisão por pares, apresentação | M7 | Booth, Colomb e Williams; Zobel; Keshav | Ler um artigo criticamente e escrever um relatório técnico reprodutível |
| H6 | Filosofia da ciência e história da computação | Demarcação, falseabilidade, paradigmas; história da computação e da engenharia | — | Chalmers; Kuhn; Popper; Ceruzzi | Situar uma tecnologia na história das ideias que a produziram |

### 2.10 Matriz de carga e profundidade por plano

Cada célula traz horas e nível-alvo (escala de 1 a 7 da seção 12); o traço indica que a disciplina fica fora do plano. As horas incluem teoria, exercícios e os laboratórios do curso de referência.

| Cód. | Disciplina | A (2 anos) | B (4 anos) | C (5 anos) | D (7 anos) | E (8 anos) | F (10 anos) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M0 | Pré-cálculo | 40 · 3 | 50 · 3 | 50 · 3 | 60 · 3 | 50 · 3 | 60 · 3 |
| M1 | Lógica, provas e conjuntos | 60 · 3 | 80 · 3 | 80 · 3 | 80 · 3 | 80 · 3 | 100 · 4 |
| M2 | Matemática discreta | 150 · 4 | 160 · 4 | 160 · 4 | 160 · 4 | 160 · 4 | 170 · 5 |
| M3 | Cálculo I | 120 · 3 | 150 · 4 | 140 · 3 | 160 · 4 | 150 · 4 | 170 · 4 |
| M4 | Geom. analítica e cálculo multivariável | 60 · 2 | 120 · 3 | 100 · 3 | 130 · 4 | 120 · 3 | 150 · 4 |
| M5 | Álgebra linear | 170 · 4 | 170 · 4 | 180 · 4 | 170 · 4 | 190 · 5 | 190 · 5 |
| M6 | Probabilidade | 150 · 4 | 160 · 4 | 170 · 4 | 160 · 4 | 170 · 4 | 180 · 5 |
| M7 | Estatística | 80 · 3 | 120 · 3 | 110 · 3 | 130 · 4 | 150 · 4 | 160 · 4 |
| M8 | Equações diferenciais | — | 50 · 2 | — | 80 · 3 | 70 · 3 | 100 · 4 |
| M9 | Métodos numéricos | — | 50 · 2 | 40 · 2 | 60 · 3 | 60 · 3 | 90 · 4 |
| M10 | Otimização | — | 70 · 3 | 50 · 2 | 70 · 3 | 110 · 4 | 130 · 4 |
| M11 | Pesquisa operacional | — | — | — | 40 · 2 | 30 · 1 | 60 · 3 |
| M12 | Teoria da informação | — | — | 30 · 2 | 30 · 2 | 40 · 2 | 70 · 3 |
| M13 | Análise real | — | — | — | — | — | 140 · 4 |
| F1 | Mecânica clássica | — | 80 · 3 | — | 100 · 3 | 90 · 3 | 110 · 4 |
| F2 | Eletricidade e magnetismo | 30 · 1 | 100 · 3 | 60 · 2 | 110 · 3 | 100 · 3 | 120 · 4 |
| F3 | Termodinâmica e ondulatória | — | 30 · 2 | — | 60 · 3 | 30 · 1 | 70 · 3 |
| F4 | Física moderna | — | — | — | 40 · 2 | 30 · 1 | 70 · 3 |
| E1 | Circuitos elétricos | — | 60 · 3 | 30 · 2 | 70 · 3 | 70 · 3 | 80 · 3 |
| E2 | Eletrônica analógica e digital | — | — | — | 50 · 2 | 40 · 2 | 70 · 3 |
| E3 | Sistemas digitais | 80 · 3 | 100 · 4 | 80 · 3 | 100 · 4 | 100 · 4 | 100 · 4 |
| E4 | Arquitetura de computadores | 100 · 3 | 140 · 4 | 130 · 4 | 140 · 4 | 140 · 4 | 150 · 5 |
| E5 | Microcontroladores e embarcados | — | 50 · 2 | — | 70 · 3 | 90 · 4 | 100 · 4 |
| E6 | Sinais e sistemas | — | — | — | — | 70 · 3 | 90 · 4 |
| P1 | Programação e abstração | 180 · 5 | 180 · 5 | 180 · 5 | 180 · 5 | 180 · 5 | 180 · 5 |
| P2 | Programação de sistemas | 180 · 4 | 190 · 5 | 190 · 5 | 180 · 4 | 190 · 5 | 190 · 5 |
| C1 | Algoritmos e estruturas de dados | 260 · 5 | 270 · 5 | 280 · 5 | 270 · 5 | 280 · 5 | 300 · 6 |
| C2 | Teoria da computação e complexidade | 40 · 2 | 70 · 3 | 60 · 2 | 80 · 3 | 70 · 3 | 100 · 4 |
| C3 | Linguagens e paradigmas | 40 · 2 | 70 · 3 | 60 · 2 | 80 · 3 | 70 · 3 | 100 · 4 |
| C4 | Compiladores | — | 70 · 3 | 60 · 2 | 80 · 3 | 60 · 2 | 100 · 4 |
| C5 | Sistemas operacionais | 160 · 4 | 190 · 5 | 190 · 5 | 180 · 4 | 190 · 5 | 200 · 5 |
| C6 | Concorrência e paralelismo | 40 · 2 | 70 · 3 | 110 · 5 | 70 · 3 | 90 · 4 | 100 · 4 |
| C7 | Redes de computadores | 100 · 3 | 130 · 4 | 130 · 4 | 130 · 4 | 130 · 4 | 140 · 4 |
| C8 | Bancos de dados | 180 · 5 | 210 · 5 | 280 · 6 | 200 · 5 | 260 · 6 | 260 · 6 |
| C9 | Sistemas distribuídos | 140 · 4 | 190 · 4 | 280 · 6 | 180 · 4 | 260 · 6 | 260 · 7 |
| C10 | Segurança da informação | 30 · 2 | 60 · 3 | 50 · 2 | 70 · 3 | 60 · 3 | 80 · 3 |
| S1 | Projeto e construção de software | 60 · 4 | 70 · 4 | 60 · 4 | 70 · 5 | 70 · 4 | 70 · 5 |
| S2 | Testes e qualidade | 40 · 3 | 50 · 4 | 40 · 3 | 50 · 4 | 50 · 4 | 50 · 4 |
| S3 | Requisitos e modelagem | — | 40 · 3 | — | 50 · 4 | 30 · 2 | 50 · 4 |
| S4 | Arquitetura de software | 40 · 3 | 80 · 4 | 70 · 4 | 90 · 5 | 90 · 5 | 100 · 6 |
| S5 | Entrega e operação | 40 · 3 | 70 · 3 | 50 · 3 | 70 · 4 | 70 · 4 | 70 · 4 |
| S6 | Sistemas escaláveis e resilientes | — | 50 · 3 | 50 · 4 | 60 · 4 | 60 · 4 | 70 · 5 |
| D1 | Modelagem de dados e SQL avançado | 100 · 5 | 90 · 5 | 80 · 5 | 90 · 5 | 90 · 5 | 90 · 5 |
| D2 | Arquiteturas analíticas | 60 · 4 | 70 · 4 | 60 · 4 | 70 · 4 | 70 · 4 | 70 · 4 |
| D3 | Processamento distribuído batch | 80 · 4 | 80 · 4 | 110 · 6 | 80 · 4 | 100 · 5 | 100 · 5 |
| D4 | Streaming e CDC | 60 · 3 | 70 · 3 | 110 · 6 | 70 · 3 | 100 · 5 | 100 · 5 |
| D5 | Orquestração, qualidade e governança | 30 · 2 | 40 · 3 | 30 · 3 | 50 · 3 | 50 · 3 | 50 · 3 |
| D6 | Arquitetura de plataformas de dados | — | 40 · 3 | 70 · 6 | 60 · 4 | 80 · 6 | 80 · 6 |
| A1 | Machine Learning | — | 110 · 3 | 80 · 2 | 120 · 3 | 160 · 5 | 160 · 5 |
| A2 | Deep Learning | — | — | — | 70 · 2 | 150 · 5 | 150 · 5 |
| A3 | PLN e LLMs | — | — | — | — | 90 · 4 | 110 · 4 |
| A4 | Sistemas de IA | — | — | — | — | 60 · 4 | 80 · 4 |
| A5 | MLOps e avaliação | — | — | — | — | 50 · 4 | 60 · 3 |
| G1 | Linux, Unix e shell | 60 · 4 | 60 · 4 | 50 · 4 | 60 · 4 | 60 · 4 | 60 · 4 |
| G2 | Virtualização, containers e Kubernetes | 40 · 3 | 60 · 3 | 50 · 3 | 60 · 4 | 60 · 4 | 60 · 4 |
| G3 | Cloud e IaC | 40 · 3 | 60 · 3 | 50 · 3 | 60 · 4 | 60 · 4 | 60 · 4 |
| G4 | Alta disponibilidade e desempenho | — | — | 40 · 3 | 40 · 3 | 50 · 4 | 60 · 4 |
| H1 | Engenharia de controle | — | — | — | — | 80 · 3 | 110 · 4 |
| H2 | Automação, robótica, IoT e CPS | — | — | — | — | 60 · 3 | 90 · 4 |
| H3 | Eng. de produção e economia da tecnologia | — | — | — | 30 · 2 | — | 40 · 2 |
| H4 | Gestão de projetos de engenharia | — | — | — | 30 · 2 | 20 · 2 | 40 · 3 |
| H5 | Metodologia científica e escrita técnica | — | 30 · 2 | 40 · 3 | 40 · 2 | 50 · 3 | 70 · 5 |
| H6 | Filosofia da ciência e história da computação | — | — | — | 30 · 2 | 20 · 1 | 50 · 3 |

### 2.11 Orçamento de horas por eixo e por plano

| Linha | A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| Eixo A — Matemática | 830 | 1.180 | 1.110 | 1.330 | 1.380 | 1.770 |
| Eixo B — Física e engenharia | 210 | 560 | 300 | 740 | 760 | 960 |
| Eixo C — Computação | 1.350 | 1.700 | 1.870 | 1.700 | 1.840 | 2.010 |
| Eixo D — Engenharia de software | 180 | 360 | 270 | 390 | 370 | 410 |
| Eixo E — Dados | 330 | 390 | 460 | 420 | 490 | 490 |
| Eixo F — IA | 0 | 110 | 80 | 190 | 510 | 560 |
| Eixo G — Infraestrutura | 140 | 180 | 190 | 220 | 230 | 240 |
| Eixo H — Interdisciplinar | 0 | 30 | 40 | 130 | 230 | 400 |
| **Disciplinas** | **3.040** | **4.510** | **4.320** | **5.120** | **5.810** | **6.840** |
| Revisão cumulativa e avaliações | 240 | 360 | 400 | 560 | 560 | 640 |
| Projetos integradores | 560 | 890 | 1.130 | 1.040 | 1.010 | 1.260 |
| Pesquisa | 0 | 0 | 150 | 0 | 300 | 860 |
| **Total** | **3.840** | **5.760** | **6.000** | **6.720** | **7.680** | **9.600** |
| Número de disciplinas | 34 | 47 | 44 | 56 | 61 | 63 |

## 3. Plano A — 2 anos: núcleo de sistemas em tempo integral

Em 3.840 h, o Plano A forma um engenheiro de software e de dados com base de sistemas incomum para o tempo investido, e deixa de fora física, eletrônica, IA e toda a camada interdisciplinar. É um plano de uma única trilha: matemática essencial, a pilha da máquina ao sistema distribuído, e dados.

### 3.1 Identidade

| Item | Definição |
| --- | --- |
| Filosofia | Seleção radical: só entra o que sustenta o vértice de sistemas de dados; o resto é adiado, não resumido |
| Intensidade | Extrema; equivale a um emprego em tempo integral |
| Carga | 40 h/semana · 1.920 h/ano · 3.840 h no total |
| Disciplinas | 34 das 63 |
| Prioridades | P1, P2, C1, C5, C8, C9, M2, M5, M6, D1–D3 |
| Aprofundadas (nível 4–5) | Programação, algoritmos, bancos de dados, SQL e modelagem, sistemas operacionais, sistemas distribuídos, álgebra linear, discreta, probabilidade |
| Introdutórias (nível 1–3) | Cálculo multivariável, estatística, teoria da computação, linguagens, concorrência, segurança, arquitetura de software, cloud, streaming, eletricidade conceitual |
| Fora do plano | F1, F3, F4, E1, E2, E5, E6, M8–M13, C4, S3, S6, D6, todo o eixo F (IA), G4, todo o eixo H |
| Competências | Implementar estruturas, um banco de dados reduzido e replicação por consenso; operar um pipeline de dados em cloud; ler código de sistemas |
| Limitações | Sem base física nem de hardware real; matemática contínua rasa; nenhuma IA; pouca consolidação, já que o último semestre empilha 13 disciplinas curtas; risco alto de esgotamento |
| Resultado realista | Engenheiro de software ou de dados de nível pleno em fundamentos, júnior em experiência; não é um engenheiro generalista |

### 3.2 Distribuição semanal média (40 h)

| Atividade | Horas | Observação |
| --- | --- | --- |
| Teoria (leitura do livro-texto, aula como apoio) | 9 | Nunca mais que a soma de exercícios e implementação |
| Resolução de exercícios | 9 | Listas do curso de referência, sem gabarito à vista |
| Programação e implementação (labs) | 10 | Labs de CS:APP, xv6, 15-445 e 6.5840 |
| Projetos integradores | 6 | 560 h no plano |
| Revisão cumulativa e avaliações | 2,5 | 240 h no plano |
| Leitura técnica (artigos, documentação) | 3,5 | Cresce no segundo ano |
| Pesquisa | 0 | Fora do escopo |

### 3.3 Cronograma

As disciplinas aparecem na ordem de estudo; o número após o código são as horas no semestre. Cada semestre soma 960 h, sendo 60 h de revisão e avaliações.

| Semestre | Etapa | Disciplinas (cód. · h) | Projetos (h) | Marco observável ao final |
| --- | --- | --- | --- | --- |
| 1 | Fundação | M0 40, P1 180, M1 60, M3 120, G1 60, E3 80, M2 150, M5 90 | PJ2 (120) | Escrevo provas por indução corretas; resolvo uma prova final de Cálculo I; entrego um programa de mil linhas com testes; minha CPU simulada executa um programa em assembly |
| 2 | Máquina e algoritmos | M5 80, C3 40, P2 180, C1 260, E4 100, M4 60, F2 30 | PJ1 (70), PJ3 (80) | Implemento e analiso qualquer estrutura clássica; leio o assembly de uma função em C e explico pilha e cache; meu alocador de memória passa nos testes |
| 3 | Sistemas | S1 60, M6 150, S2 40, C5 160, C8 180, C7 100, D1 100 | PJ7 reduzido (110) | Acrescento chamada de sistema e paginação a um kernel didático; explico o caminho de uma consulta do SQL ao disco; implemento transporte confiável sobre rede com perdas |
| 4 | Distribuição e dados | M7 80, C2 40, C6 40, C9 140, C10 30, S4 40, G2 40, D2 60, G3 40, S5 40, D3 80, D4 60, D5 30 | PJ11 (180) | Minha implementação de Raft sobrevive a partições de rede; opero um pipeline batch em cloud, provisionado por código e com testes de dados; defendo a arquitetura em revisão escrita |

Marcos de evolução: ao fim do ano 1, nível 4 em programação, algoritmos e matemática discreta; ao fim do ano 2, nível 4–5 no vértice de dados, com tudo o mais em nível 2–3.

## 4. Plano B — 4 anos: bacharelado comprimido

Em 5.760 h, o Plano B reproduz o núcleo de um bacharelado em Engenharia de Computação com ênfase em dados: 47 disciplinas, quase todas em nível 3–4, com o tronco de sistemas em nível 5. É o primeiro plano que inclui física, circuitos, compiladores e Machine Learning.

### 4.1 Identidade

| Item | Definição |
| --- | --- |
| Filosofia | Currículo universitário clássico, sem as redundâncias de uma grade formal: uma disciplina, um livro-texto, um conjunto de labs |
| Intensidade | Alta; exige meio período de trabalho ou abrir mão de quase todo o tempo livre |
| Carga | 30 h/semana · 1.440 h/ano · 5.760 h no total |
| Disciplinas | 47 das 63 |
| Prioridades | M2, M5, M6, C1, P2, E4, C5, C8, C9 |
| Aprofundadas (nível 4–5) | Programação, programação de sistemas, algoritmos, sistemas operacionais, bancos de dados, SQL e modelagem, redes, sistemas digitais e arquitetura, cálculo I, álgebra linear, discreta, probabilidade |
| Introdutórias (nível 2–3) | Equações diferenciais, métodos numéricos, otimização, mecânica, eletromagnetismo, termodinâmica, circuitos, embarcados, teoria da computação, compiladores, concorrência, segurança, Machine Learning, streaming, plataformas de dados |
| Fora do plano | M11–M13, F4, E2, E6, A2–A5, G4, H1–H4, H6 |
| Competências | Construir interpretador, pilha de rede, banco de dados e serviço replicado; projetar e operar um pipeline de dados; modelar com probabilidade e álgebra linear |
| Limitações | Um único vértice e ainda em nível 4–5; IA limitada ao clássico; física sem laboratório; sem pesquisa; pouca folga para imprevistos |
| Resultado realista | Formação equivalente em fundamentos a um bom bacharel em computação, com portfólio de sistemas superior à média; base para se especializar depois |

### 4.2 Distribuição semanal média (30 h)

| Atividade | Horas | Observação |
| --- | --- | --- |
| Teoria | 7 |  |
| Resolução de exercícios | 7 | Concentrada nos anos 1 e 2 (matemática e física) |
| Programação e implementação (labs) | 7 | Concentrada nos anos 2 e 3 |
| Projetos integradores | 4,5 | 890 h no plano; sobe de 2,5 para 9 h/semana |
| Revisão cumulativa e avaliações | 2 | 360 h no plano |
| Leitura técnica | 2,5 | Artigos clássicos a partir do semestre 5 |
| Pesquisa | 0 | H5 cobre apenas leitura crítica e escrita |

### 4.3 Cronograma

Cada semestre soma 720 h, sendo 45 h de revisão e avaliações.

| Semestre | Etapa | Disciplinas (cód. · h) | Projetos (h) | Marco observável ao final |
| --- | --- | --- | --- | --- |
| 1 | Fundação | M0 50, P1 180, M1 80, M3 150, G1 60, M5 95 | PJ1 fase 1 (60) | Escrevo provas curtas corretas; resolvo uma prova final de Cálculo I; programo com recursão e abstração de dados; automatizo tarefas no shell |
| 2 | Fundação | M5 75, M2 160, E3 100, M4 120, F1 80, C1 60 | PJ2 (80) | Decomponho matrizes e interpreto autovalores; modelo problemas com grafos e contagem; projeto um circuito síncrono; resolvo dinâmica newtoniana |
| 3 | Núcleo de computação | C1 210, C3 70, P2 190, M6 115 | PJ1 conclusão, PJ3 (90) | Projeto e provo algoritmos de grafos e programação dinâmica; explico um programa em C até o nível do assembly; escrevo em estilo funcional |
| 4 | Núcleo de computação | M6 45, F2 100, S1 70, E4 140, E1 60, M8 50, C2 70, S2 50 | PJ4 (90) | Estimo o desempenho de código a partir de pipeline e cache; analiso um circuito RLC; provo NP-completude por redução; meu interpretador executa closures |
| 5 | Sistemas | C5 190, C7 130, M7 120, C8 125 | PJ5 (110) | Modifico escalonador e memória virtual de um kernel didático; minha pilha TCP conversa com uma real; desenho um experimento e analiso com intervalo de confiança |
| 6 | Sistemas | C8 85, F3 30, M9 50, C6 70, C4 70, D1 90, G2 60, S3 40, M10 70 | PJ7 (110) | Meu banco de dados executa SQL com índice B+ e recuperação após falha; compilo uma linguagem pequena; modelo um domínio nas formas relacional e dimensional |
| 7 | Distribuição e especialização | C9 190, A1 110, S4 80, G3 60, D2 70, C10 25 | PJ9 (140) | Meu armazenamento chave-valor replicado tolera falhas e partições; treino e valido modelos clássicos; documento uma arquitetura com decisões e trade-offs |
| 8 | Integração | C10 35, S5 70, D3 80, E5 50, D4 70, S6 50, D5 40, D6 40, H5 30 | PJ11 com streaming (210) | Opero uma plataforma de dados batch e streaming com SLO, contratos e custo estimado; escrevo o relatório técnico do projeto; programo um microcontrolador com interrupções |

Marcos de evolução: ano 1, matemática de base e programação em nível 4; ano 2, a máquina compreendida do transistor lógico ao sistema operacional; ano 3, capacidade de construir sistemas de armazenamento; ano 4, capacidade de projetar e operar sistemas distribuídos de dados.

## 5. Plano C — 5 anos: formação em T

Em 6.000 h, o Plano C estuda menos disciplinas que o Plano B (44 contra 47) e leva o vértice de sistemas de dados distribuídos ao nível 6, o de quem arquiteta soluções completas. O ano extra não compra amplitude: compra 1.130 h de projetos, 150 h de pesquisa e um ano final de trabalho autoral.

### 5.1 Identidade

| Item | Definição |
| --- | --- |
| Filosofia | Profundidade antes de amplitude: base horizontal enxuta, um vértice vertical levado ao limite do autodidata |
| Intensidade | Alta, mas compatível com emprego em tempo integral: 3 h por dia útil e 10 h no fim de semana |
| Carga | 25 h/semana · 1.200 h/ano · 6.000 h no total |
| Disciplinas | 44 das 63 |
| Prioridades | C8, C9, C6, D3, D4, D6 e tudo o que os sustenta (C1, P2, C5, C7, M2, M6) |
| Aprofundadas (nível 5–6) | Bancos de dados por dentro, sistemas distribuídos, concorrência, processamento batch e streaming, arquitetura de plataformas, programação de sistemas, sistemas operacionais, algoritmos |
| Introdutórias (nível 2–3) | Eletromagnetismo e circuitos (só o necessário para arquitetura), teoria da computação, linguagens, compiladores, otimização, métodos numéricos, teoria da informação, segurança, Machine Learning |
| Fora do plano | M8, M11, M13, F1, F3, F4, E2, E5, E6, S3, A2–A5, H1–H4, H6 |
| Competências | Construir um SGBD com transações e um log replicado; projetar uma plataforma de dados com requisitos quantificados; ler e reproduzir artigos de sistemas |
| Limitações | Não é generalista: física, hardware, controle e IA ficam em nível de reconhecimento ou ausentes; o perfil depende de o vértice escolhido continuar relevante |
| Resultado realista | Especialista em sistemas de dados com fundamentos de nível sênior; capaz de contribuir com projetos de código aberto de infraestrutura de dados |

### 5.2 Distribuição semanal média (25 h)

| Atividade | Horas | Observação |
| --- | --- | --- |
| Teoria | 5 |  |
| Resolução de exercícios | 5 | Anos 1 e 2 |
| Programação e implementação (labs) | 6 | A maior fatia: o vértice se aprende construindo |
| Projetos integradores | 4,5 | 1.130 h no plano; 15 h/semana no ano 5 |
| Revisão cumulativa e avaliações | 1,5 | 400 h no plano |
| Leitura técnica | 2,5 | Um artigo de sistemas por semana a partir do semestre 6 |
| Pesquisa | 0,5 | 150 h no ano 5: reprodução de um artigo e extensão |

### 5.3 Cronograma

Cada semestre soma 600 h, sendo 40 h de revisão e avaliações.

| Semestre | Etapa | Disciplinas (cód. · h) | Projetos e pesquisa (h) | Marco observável ao final |
| --- | --- | --- | --- | --- |
| 1 | Base | M0 50, P1 180, M1 80, M3 140, G1 50 | PJ1 fase 1 (60) | Escrevo provas curtas; resolvo uma prova final de Cálculo I; programo com abstração de dados e testes |
| 2 | Base | M5 180, M2 160, E3 80, C1 80 | PJ2 (60) | Decomponho matrizes; modelo com grafos e recorrências; minha CPU simulada executa assembly |
| 3 | Base | C1 200, M4 100, P2 190 | PJ1 conclusão, PJ3 (70) | Projeto e provo algoritmos; explico um programa em C até o assembly; meu alocador passa nos testes |
| 4 | Máquina | M6 170, C3 60, S1 60, E4 130, F2 60 | PJ4 (80) | Modelo incerteza com distribuições conjuntas; estimo desempenho a partir do cache; meu interpretador executa closures |
| 5 | Sistemas | E1 30, C2 60, C5 190, C7 130, S2 40 | PJ5 (110) | Modifico um kernel didático; minha pilha TCP conversa com uma real; reconheço problemas intratáveis |
| 6 | Vértice | M7 110, C8 280, C6 60 | PJ7 (110) | Meu banco executa junções com índice B+ e otimizador simples; prevejo o plano de execução de um SGBD real e acerto |
| 7 | Vértice | C6 50, D1 80, G2 50, M10 50, M9 40, C4 60, C9 110 | PJ7 com transações (120) | Meu banco tem controle de concorrência e recuperação; escrevo uma estrutura concorrente e argumento sua correção |
| 8 | Vértice | C9 170, S5 50, D2 60, G3 50, A1 80 | PJ9 (150) | Meu armazenamento replicado e particionado passa em testes de injeção de falhas; explico cada modelo de consistência com um contraexemplo |
| 9 | Autoria | D3 110, S4 70, C10 50, M12 30, D4 45 | PJ12 (180), pesquisa (75) | Meu log replicado entrega com garantia explícita; diagnostico um job distribuído pelo plano físico; reproduzi os resultados de um artigo de sistemas |
| 10 | Autoria | D4 65, D5 30, G4 40, S6 50, H5 40, D6 70 | PJ13 (190), pesquisa (75) | Entrego uma plataforma de dados com SLO medido, teste de carga e custo; publico o relatório técnico e a extensão do artigo reproduzido |

Marcos de evolução: anos 1–2, base em nível 4; ano 3, a máquina e o sistema operacional em nível 5; ano 4, o vértice em nível 5; ano 5, o vértice em nível 6, demonstrado por um sistema próprio e um relatório público.

## 6. Plano D — 7 anos: engenharia completa em ritmo sustentável

Em 6.720 h, a 20 h por semana, o Plano D cobre 56 disciplinas em nível 3–5 e é o primeiro com a física básica inteira, eletrônica, Deep Learning introdutório e as disciplinas de gestão e história. Troca a profundidade de vértice do Plano C por amplitude consistente e por uma rotina que cabe ao lado de um emprego por sete anos.

### 6.1 Identidade

| Item | Definição |
| --- | --- |
| Filosofia | Currículo em espiral, em três ciclos: cada ciclo abre com prova de pré-requisitos do anterior e reaplica a matemática em contexto novo |
| Intensidade | Moderada: 2 h por dia útil e 10 h no fim de semana |
| Carga | 20 h/semana · 960 h/ano · 6.720 h no total |
| Disciplinas | 56 das 63 |
| Prioridades | Fundamentos universais completos; engenharia de software e arquitetura (S1, S4 em nível 5), porque o trabalho diário as reforça |
| Aprofundadas (nível 4–5) | Toda a matemática de M2 a M7, algoritmos, bancos de dados, SQL e modelagem, projeto e arquitetura de software, sistemas digitais e arquitetura de computadores, redes, infraestrutura |
| Introdutórias (nível 2–3) | Física moderna, eletrônica, pesquisa operacional, teoria da informação, Deep Learning, streaming, embarcados, gestão, economia, filosofia da ciência |
| Fora do plano | M13, E6, A3–A5, H1, H2 |
| Competências | Transitar da física do circuito à plataforma de dados explicando cada camada; arquitetar sistemas de software; conduzir um projeto técnico |
| Limitações | Nenhuma área chega ao nível 6; sem pesquisa; sem controle nem robótica; sete anos expõem o plano a mudanças de vida e à perda do que foi estudado no início |
| Resultado realista | Engenheiro de computação generalista de base ampla, com maturidade arquitetural reforçada pela prática profissional paralela |

### 6.2 Distribuição semanal média (20 h)

| Atividade | Horas | Observação |
| --- | --- | --- |
| Teoria | 5 |  |
| Resolução de exercícios | 5 | A fatia de matemática e física é a maior entre os planos de um vértice |
| Programação e implementação (labs) | 4,5 |  |
| Projetos integradores | 3 | 1.040 h no plano |
| Revisão cumulativa e avaliações | 1,5 | 560 h no plano; a espiral depende dela |
| Leitura técnica | 1 |  |
| Pesquisa | 0 |  |

### 6.3 Cronograma

Cada semestre soma 480 h, sendo 40 h de revisão e avaliações.

| Semestre | Ciclo | Disciplinas (cód. · h) | Projetos (h) | Marco observável ao final |
| --- | --- | --- | --- | --- |
| 1 | 1 — Fundamentos | M0 60, P1 180, M1 80, M3 80 | PJ1 fase 1 (40) | Programo com recursão e abstração de dados; escrevo provas curtas |
| 2 | 1 | M3 80, G1 60, H6 30, M5 170, M2 50 | PJ1 fase 1 (50) | Resolvo uma prova final de Cálculo I; decomponho matrizes; trabalho só pela linha de comando |
| 3 | 1 | M2 110, F1 100, E3 100, C1 80 | PJ2 (50) | Modelo com grafos e contagem; resolvo dinâmica newtoniana; minha CPU simulada executa assembly |
| 4 | 1 | C1 190, M4 130, P2 60 | PJ1 conclusão (60) | Projeto e provo algoritmos; derivo e integro em várias variáveis |
| 5 | 1 | P2 120, F2 110, M6 160 | PJ3 (50) | Explico um programa em C até o assembly; explico capacitor e indutor pelas equações de campo; calculo com distribuições conjuntas |
| 6 | 2 — Máquina e sistemas | C3 80, S1 70, E1 70, E4 140 | PJ4 (80) | Meu interpretador executa closures; analiso um circuito RLC; estimo desempenho a partir de pipeline e cache |
| 7 | 2 | M8 80, S2 50, F3 60, C2 80, C5 100 | PJ6 início (70) | Classifico a estabilidade de um sistema dinâmico; provo NP-completude por redução; cubro com testes um código legado |
| 8 | 2 | C5 80, C7 130, M7 130, E2 50 | PJ5 reduzido (50) | Modifico memória virtual de um kernel didático; implemento transporte confiável; desenho e analiso um experimento |
| 9 | 2 | C8 200, M9 60, F4 40, C6 70 | PJ7 (70) | Prevejo o plano de execução de um SGBD; implemento um solver e estimo seu erro; explico o transistor pela física de bandas |
| 10 | 2 | C4 80, D1 90, G2 60, S3 50, M10 70 | PJ7 conclusão (90) | Meu banco executa SQL com índice e recuperação; compilo uma linguagem pequena; modelo um domínio com DDD e de forma dimensional |
| 11 | 3 — Distribuição e integração | C9 180, E5 70, A1 120 | PJ9 (70) | Meu serviço replicado tolera falhas; treino e valido modelos clássicos; escrevo firmware com interrupções |
| 12 | 3 | S4 90, G3 60, D2 70, C10 70, S5 70 | PJ16 (80) | Documento uma arquitetura com trade-offs; provisiono um ambiente por código; faço a modelagem de ameaças de um sistema |
| 13 | 3 | M11 40, H4 30, D3 80, A2 70, D4 70, S6 60 | PJ11 (90) | Diagnostico um job distribuído; treino uma rede neural pequena; projeto um serviço que degrada com controle |
| 14 | 3 | D5 50, G4 40, M12 30, H3 30, H5 40, D6 60 | PJ11 com streaming, PJ20 (190) | Opero uma plataforma de dados com SLO e contratos; conduzo a modernização de um sistema legado com decisões registradas; escrevo o relatório técnico |

Marcos de evolução: fim do ciclo 1 (ano 2,5), nível 4 em matemática de base, programação e algoritmos; fim do ciclo 2 (ano 5), a pilha inteira do circuito ao banco de dados em nível 4; fim do ciclo 3 (ano 7), nível 5 em arquitetura de software e modelagem de dados.

## 7. Plano E — 8 anos: generalista com dois vértices

Em 7.680 h, o Plano E entrega a base ampla do Plano D e acrescenta dois vértices profundos, sistemas de dados distribuídos (nível 6) e inteligência artificial (nível 5), mais uma ponte para o mundo físico por sinais, controle e embarcados. É o primeiro plano em que o perfil generalista de alto nível se torna realista.

### 7.1 Identidade

| Item | Definição |
| --- | --- |
| Filosofia | Perfil em π: base horizontal larga e duas pernas verticais que se reforçam, porque sistemas de IA são sistemas de dados |
| Intensidade | Moderada e longa: 20 h por semana durante oito anos |
| Carga | 20 h/semana · 960 h/ano · 7.680 h no total |
| Disciplinas | 61 das 63 |
| Prioridades | C8, C9, D3, D4, D6 no primeiro vértice; M5, M10, A1, A2 no segundo; E5, E6, H1 como ponte |
| Aprofundadas (nível 5–6) | Bancos de dados, sistemas distribuídos, plataformas de dados, batch e streaming, álgebra linear, Machine Learning, Deep Learning, programação de sistemas, sistemas operacionais, arquitetura de software |
| Introdutórias (nível 1–3) | Termodinâmica, física moderna, pesquisa operacional, teoria da informação, compiladores, requisitos, controle, robótica e IoT, gestão, história |
| Fora do plano | M13, H3 |
| Competências | Arquitetar plataformas de dados; treinar, avaliar e operar modelos, incluindo aplicações com LLM; integrar sensor, firmware, pipeline e modelo em um sistema físico; iniciar pesquisa aplicada |
| Limitações | Projetos integradores são 13% da carga, a menor fatia entre os planos, o que pede disciplina para não virar estudo teórico; física moderna e termodinâmica ficam em reconhecimento; pesquisa é inicial (300 h) |
| Resultado realista | Engenheiro generalista sênior em fundamentos, com dois domínios de autoridade técnica e capacidade de liderar sistemas que cruzam software, dados e IA |

### 7.2 Distribuição semanal média (20 h)

| Atividade | Horas | Observação |
| --- | --- | --- |
| Teoria | 4,5 |  |
| Resolução de exercícios | 4,5 |  |
| Programação e implementação (labs) | 5 | Inclui treino de modelos |
| Projetos integradores | 2,5 | 1.010 h no plano |
| Revisão cumulativa e avaliações | 1,5 | 560 h no plano |
| Leitura técnica | 1,2 | Um artigo por quinzena a partir do ano 4 |
| Pesquisa | 0,8 | 300 h nos anos 7 e 8 |

### 7.3 Cronograma

Cada semestre soma 480 h, sendo 35 h de revisão e avaliações.

| Semestre | Etapa | Disciplinas (cód. · h) | Projetos e pesquisa (h) | Marco observável ao final |
| --- | --- | --- | --- | --- |
| 1 | Base | M0 50, P1 180, M1 80, M3 105 | PJ1 fase 1 (30) | Programo com recursão e abstração de dados; escrevo provas curtas |
| 2 | Base | M3 45, G1 60, M5 190, M2 110 | PJ1 fase 1 (40) | Resolvo uma prova final de Cálculo I; explico o que cada fator da SVD significa |
| 3 | Base | M2 50, E3 100, F1 90, C1 165 | PJ2 (40) | Modelo com grafos; minha CPU simulada executa assembly; resolvo dinâmica newtoniana |
| 4 | Base | C1 115, M4 120, P2 160 | PJ1 conclusão (50) | Projeto e provo algoritmos; leio o assembly de um programa em C |
| 5 | Máquina | P2 30, F2 100, M6 170, C3 70, S1 25 | PJ3 (50) | Meu alocador passa nos testes; calculo com distribuições conjuntas; escrevo em estilo funcional |
| 6 | Máquina | S1 45, E1 70, E4 140, M8 70, S2 50 | PJ4 (70) | Estimo desempenho a partir do cache; analiso um circuito RLC; meu interpretador executa closures |
| 7 | Sistemas | C2 70, C5 190, C7 130 | PJ5 reduzido (55) | Modifico um kernel didático; implemento transporte confiável; reconheço problemas intratáveis |
| 8 | Sistemas | M7 150, H6 20, C8 215 | PJ7 (60) | Desenho e analiso um experimento; prevejo o plano de execução de um SGBD real |
| 9 | Vértice 1 | C8 45, E2 40, M9 60, C6 90, D1 90, G2 60 | PJ7 conclusão (60) | Meu banco tem transações e recuperação; escrevo uma estrutura concorrente e argumento sua correção |
| 10 | Vértice 1 | C4 60, M10 110, C9 205 | PJ9 (70) | Meu serviço replicado passa em injeção de falhas; formulo um problema como otimização convexa |
| 11 | Vértice 2 | C9 55, E6 70, A1 160, S3 30, S4 60 | PJ14 parte 1 (70) | Derivo e implemento do zero regressão, árvores e SVM; analiso um sinal amostrado no domínio da frequência |
| 12 | Ponte física | S4 30, G3 60, D2 70, F3 30, S5 70, E5 90 | PJ16 (95) | Meu firmware lê sensores com restrição de tempo e publica telemetria; levo um serviço a produção com SLO |
| 13 | Vértice 2 | D3 100, H5 50, A2 150 | PJ11 (70), pesquisa (75) | Minha biblioteca de diferenciação automática treina uma rede; diagnostico um job distribuído; resumo criticamente um artigo |
| 14 | Integração | C10 60, D4 100, H1 80, D5 50 | PJ12 (80), pesquisa (75) | Meu log replicado tem garantia de entrega explícita; sintonizo um controlador PID para uma planta modelada |
| 15 | Integração | S6 60, F4 30, A3 90, G4 50, M11 30, H4 20 | PJ15 (90), pesquisa (75) | Treino um transformer pequeno do zero; minha aplicação RAG tem avaliação quantitativa; encontro um gargalo com método |
| 16 | Síntese | M12 40, D6 80, H2 60, A5 50, A4 60 | PJ17 sobre a plataforma de PJ11 e PJ12 (80), pesquisa (75) | Entrego um sistema físico com controle, telemetria em streaming e modelo em produção; publico a reprodução de um artigo com uma extensão |

Marcos de evolução: ano 2, base em nível 4; ano 4, sistemas em nível 5; ano 5, primeiro vértice em nível 5–6; ano 7, segundo vértice em nível 5; ano 8, integração entre hardware, dados e IA demonstrada em um sistema único.

## 8. Plano F — 10 anos: polímata e pesquisador

Em 9.600 h, o Plano F cobre as 63 disciplinas, leva um vértice ao nível 7 e reserva 860 h para pesquisa, o que nenhum outro plano faz. É o único que inclui análise real, física em nível intermediário e controle em nível de projeto, e o único cujo resultado esperado é produzir conhecimento, não só aplicá-lo.

### 8.1 Identidade

| Item | Definição |
| --- | --- |
| Filosofia | Três fases de quatro, três e três anos: fundamentos com rigor matemático; sistemas e vértices; pesquisa e síntese original |
| Intensidade | Moderada e muito longa: 20 h por semana durante dez anos |
| Carga | 20 h/semana · 960 h/ano · 9.600 h no total |
| Disciplinas | 63 das 63 |
| Prioridades | Maturidade matemática (M1, M2, M13 com provas), a pilha completa de computação, dois vértices (dados distribuídos e IA), ponte física (E5, E6, H1, H2), H5 em nível 5 |
| Aprofundadas (nível 5–7) | Sistemas distribuídos (7), algoritmos, bancos de dados, arquitetura de software, plataformas de dados (6), discreta, álgebra linear, probabilidade, arquitetura de computadores, sistemas operacionais, Machine Learning, Deep Learning, metodologia científica (5) |
| Introdutórias (nível 2–3) | Engenharia de produção e economia, pesquisa operacional, teoria da informação, termodinâmica, física moderna, eletrônica, segurança, governança de dados |
| Fora do plano | Nada do catálogo; ficam de fora apenas os aprofundamentos de segunda ordem de cada área |
| Competências | Tudo o que o Plano E entrega, mais: provar com rigor, modelar sistemas físicos, formular um problema de pesquisa, conduzir experimentos e publicar |
| Limitações | Dez anos de constância são o maior risco do conjunto; as ferramentas estudadas no ano 3 estarão defasadas no ano 10; pesquisa sem orientador tende a ser incremental; projetos integradores são só 13% da carga |
| Resultado realista | Engenheiro generalista com formação comparável a graduação mais mestrado em amplitude e em um vértice, com uma contribuição original documentada |

### 8.2 Distribuição semanal média (20 h)

| Atividade | Horas | Observação |
| --- | --- | --- |
| Teoria | 4,5 | Na fase 1, com demonstrações refeitas à mão |
| Resolução de exercícios | 4,5 | Inclui exercícios de prova |
| Programação e implementação (labs) | 4,5 |  |
| Projetos integradores | 2,5 | 1.260 h no plano |
| Revisão cumulativa e avaliações | 1,5 | 640 h no plano |
| Leitura técnica | 0,7 | Documentação e livros de prática |
| Pesquisa | 1,8 | 860 h: 0 na fase 1, cerca de 1,7 h/semana na fase 2 e 4 h/semana na fase 3 |

### 8.3 Cronograma

Cada semestre soma 480 h, sendo 32 h de revisão e avaliações.

| Semestre | Fase | Disciplinas (cód. · h) | Projetos e pesquisa (h) | Marco observável ao final |
| --- | --- | --- | --- | --- |
| 1 | 1 — Fundamentos | M0 60, P1 180, M1 100, M3 78 | PJ1 fase 1 (30) | Programo com abstração de dados; escrevo provas por indução e por contradição |
| 2 | 1 | M3 92, G1 60, H6 50, M5 190, M2 26 | PJ1 fase 1 (30) | Resolvo uma prova final de Cálculo I; provo teoremas básicos de álgebra linear; situo Turing, Shannon e von Neumann na história |
| 3 | 1 | M2 144, F1 110, E3 100, C1 64 | PJ2 (30) | Resolvo problemas de combinatória e grafos com prova; resolvo mecânica com cálculo; minha CPU simulada executa assembly |
| 4 | 1 | C1 236, M4 150, P2 32 | PJ1 conclusão (30) | Projeto, provo e implemento algoritmos avançados; aplico os teoremas de Green, Stokes e Gauss |
| 5 | 1 | P2 158, F2 120, M6 120 | PJ3 (50) | Explico um programa em C até o assembly; resolvo eletromagnetismo com cálculo vetorial |
| 6 | 1 | M6 60, C3 100, S1 70, M13 140, E1 28 | PJ4 (50) | Provo convergência com ε e δ; meu interpretador tem closures e verificação de tipos |
| 7 | 1 | E1 52, E4 150, M8 100, S2 50, F3 70 | PJ4 conclusão (26) | Projeto um processador com pipeline em HDL; classifico a estabilidade de um sistema dinâmico; analiso um circuito RLC |
| 8 | 1 | C2 100, C5 200, C7 98 | PJ6 (50) | Estendo um kernel didático; provo indecidibilidade e NP-completude por redução |
| 9 | 2 — Sistemas e vértices | C7 42, M7 160, E2 70, C8 66 | PJ5 (70), leitura de artigos (40) | Minha pilha TCP conversa com uma real; desenho e analiso um experimento; projeto um estágio com amplificador operacional |
| 10 | 2 | C8 194, M9 90, F4 70 | PJ7 (54), leitura de artigos (40) | Prevejo o plano de execução de um SGBD; implemento um solver com análise de erro; explico o transistor pela física de bandas |
| 11 | 2 | C6 100, E6 90, C4 100, D1 48 | PJ7 conclusão (70), leitura de artigos (40); PJ8 nos labs de C4 | Meu banco tem transações e recuperação; meu compilador gera código de máquina; filtro um sinal amostrado |
| 12 | 2 | D1 42, G2 60, S3 50, M10 130, H5 70 | PJ19 (56), leitura de artigos (40) | Formulo e resolvo otimização convexa; escrevo a resenha crítica de um artigo; minha simulação numérica tem erro controlado |
| 13 | 2 | C9 260, E5 68 | PJ9 (80), leitura de artigos (40) | Meu serviço replicado e particionado passa em injeção de falhas; explico cada modelo de consistência com um contraexemplo |
| 14 | 2 | E5 32, A1 160, S4 100, G3 60 | PJ14 parte 1 (56), leitura de artigos (40) | Derivo e implemento do zero os modelos clássicos; escrevo firmware de tempo real; documento uma arquitetura com trade-offs |
| 15 | 3 — Pesquisa e síntese | D2 70, C10 80, H1 110, S5 28 | PJ16 (80), PJ18 reprodução (80) | Projeto um controlador em espaço de estados; reproduzo os resultados de um artigo do vértice |
| 16 | 3 | S5 42, M11 60, D3 100, A2 86 | PJ11 (80), PJ18 reprodução (80) | Diagnostico um job distribuído; minha biblioteca de diferenciação automática treina uma rede; formulo uma pergunta de pesquisa com hipótese testável |
| 17 | 3 | A2 64, M12 70, D4 100 | PJ12 (99), PJ18 pesquisa original (115) | Meu log replicado tem garantias explícitas; tenho um desenho experimental revisado por um par |
| 18 | 3 | H4 40, S6 70, D5 50, A3 110 | PJ15 (63), PJ18 (115) | Treino um transformer pequeno do zero; tenho resultados experimentais preliminares e ameaças à validade listadas |
| 19 | 3 | G4 60, H2 90, H3 40, A5 60 | PJ17 (83), PJ18 (115) | Entrego um sistema físico com estimação, controle e telemetria; tenho o rascunho completo do artigo |
| 20 | 3 | D6 80, A4 80 | PJ13 (173), PJ18 submissão (115) | Entrego uma plataforma de dados com SLO medido que serve um modelo; submeto o artigo ou publico o relatório técnico com código e dados |

Marcos de evolução: fim da fase 1 (ano 4), fundamentos em nível 4–5 com maturidade de prova; fim da fase 2 (ano 7), sistemas em nível 5–6 e hábito de leitura de artigos formado, com cerca de 120 lidos; fim da fase 3 (ano 10), nível 7 no vértice, com uma contribuição original submetida à crítica externa.

## 9. Metodologia de aprendizagem

A regra que vale para os seis planos: uma hora só conta se produzir algo verificável, como um exercício resolvido sem consulta, um teste passando ou uma explicação escrita. Aula assistida e capítulo lido são insumo, não progresso.

### 9.1 Método por tipo de conhecimento

| Tipo | Método principal | Como aplicar | Sinal de domínio |
| --- | --- | --- | --- |
| Matemática | Prática deliberada com problemas; active recall de definições e teoremas | Ler a seção, fechar o livro, reescrever definições e a ideia da prova; resolver de 60% a 70% dos exercícios sem gabarito; manter um caderno de erros; intercalar listas de capítulos anteriores | Resolver uma prova antiga do curso de referência no tempo regulamentar |
| Física | Aprendizagem baseada em problemas; técnica de Feynman | Para cada problema: desenho, modelo, hipóteses, solução simbólica, casos-limite e análise dimensional antes de números; explicar o fenômeno por escrito sem fórmulas | Prever o resultado qualitativo antes de calcular |
| Algoritmos | Implementação do zero; prática deliberada; interleaving | Para cada algoritmo: enunciar o invariante, provar a correção, analisar o custo, implementar sem consulta, testar por propriedade; problemas misturados por técnica, sem rótulo | Resolver um problema inédito e justificar a técnica escolhida |
| Programação | Aprendizagem baseada em projetos; leitura de código | Labs do curso de referência sem olhar soluções; ler um código-fonte de qualidade por mês; reescrever o próprio código após 30 dias | Um colega entende e altera o código sem perguntar |
| Arquitetura de software | Estudo de casos; aprendizagem baseada em investigação | Para cada estilo ou padrão: que problema resolve, que custo impõe, quando não usar; escrever registros de decisão para projetos próprios; analisar relatórios públicos de incidentes | Defender por escrito uma decisão e a alternativa rejeitada |
| Engenharia de dados | Mecanismo antes da ferramenta; projetos | Ler o artigo original, implementar a versão mínima (um log, um shuffle), só então usar a ferramenta; todo pipeline com volume realista, falha injetada e custo medido | Prever o comportamento sob falha e sob assimetria antes de executar |
| Infraestrutura | Laboratório prático; documentação oficial | Construir à mão antes de automatizar (um container com namespaces, um cluster sem instalador); quebrar de propósito e diagnosticar; tudo versionado como código | Recriar o ambiente do zero com um comando |
| Inteligência artificial | Derivação e implementação do zero; experimentação controlada | Derivar o gradiente no papel, implementar sem biblioteca, comparar com a biblioteca; todo experimento com linha de base, semente fixa e conjunto de teste intocado | Explicar por que um treino falhou a partir das curvas |
| Pesquisa científica | Aprendizagem baseada em investigação; leitura ativa em três passagens | Um artigo por semana com resumo de uma página (problema, ideia, evidência, limitações); reproduzir antes de estender; diário de pesquisa; buscar revisão externa | Um leitor da área aceita o desenho experimental |

### 9.2 Onde cada técnica entra

| Técnica | Uso na formação |
| --- | --- |
| Active recall | Abertura de toda sessão: 10 minutos reescrevendo de memória o conteúdo da sessão anterior |
| Spaced repetition | Cartões só para definições, enunciados de teoremas, invariantes e comandos; no máximo 15 minutos por dia; nunca para procedimentos |
| Técnica de Feynman | Fechamento de cada capítulo: uma página explicando o mecanismo a um leigo; lacunas viram a pauta da sessão seguinte |
| Interleaving | Duas ou três disciplinas em paralelo por semestre, uma teórica e uma de construção; listas de exercícios misturadas |
| Prática deliberada | Exercícios no limite da competência, com correção imediata e repetição dos tipos errados |
| Aprendizagem baseada em problemas | Matemática aplicada, física, algoritmos |
| Aprendizagem baseada em projetos | Eixos C, D, E, G e os projetos integradores da seção 11 |
| Aprendizagem baseada em investigação | Vértices e pesquisa: a pergunta vem antes da leitura |
| Leitura ativa de livros técnicos | Perguntas antes de ler, anotação à margem, exercícios do capítulo como parte da leitura |
| Revisão cumulativa | Orçamento próprio em cada plano: semanal (1 h), mensal (prova mista) e semestral (prova de pré-requisitos) |

### 9.3 Regras contra a ilusão de competência

1. **Limite de trabalho em andamento.** No máximo três disciplinas abertas (durante a graduação, duas do complemento; ver 16.6); uma nova só começa quando outra passa pelo critério de conclusão da seção 12.
2. **Uma fonte principal por disciplina.** O livro e o curso de referência são seguidos até o fim; uma segunda fonte só entra para um tópico em que a primeira falhou.
3. **Teoria nunca passa de 30% da semana.** Se passar, a semana seguinte compensa com exercícios e implementação.
4. **Teste antes de avançar.** Cada capítulo termina com um conjunto de problemas feito sem consulta; menos de 70% de acerto significa refazer, não seguir.
5. **Nada de copiar solução.** Em lab ou projeto travado, o limite é uma pista, nunca o código pronto.
6. **Registro semanal.** Horas por atividade, exercícios resolvidos, testes passando. O que não foi registrado não conta para o orçamento.
7. **Troca de assunto tem custo declarado.** Abandonar uma disciplina no meio exige anotar o motivo e a data de retomada.

## 10. Bibliografia e referências acadêmicas

Cada disciplina tem uma fonte principal, a primeira citada no catálogo da seção 2, e no máximo uma ou duas de aprofundamento. A lista foi escrita de memória, sem consulta a catálogos: os títulos e autores são de obras consagradas, mas edições e códigos de cursos mudam e devem ser conferidos na hora de adquirir ou acessar.

Nível: Intro. = introdutório, Interm. = intermediário, Avanç. = avançado.

### 10.1 Matemática

| Título | Autor | Disc. | Nível | Momento de uso |
| --- | --- | --- | --- | --- |
| Basic Mathematics | Serge Lang | M0 | Intro. | Diagnóstico e revisão, primeiras semanas |
| Precalculus: A Prelude to Calculus | Sheldon Axler | M0 | Intro. | Alternativa com mais exercícios |
| How to Prove It | Daniel Velleman | M1 | Intro. | Antes de qualquer disciplina com provas |
| Naive Set Theory | Paul Halmos | M1 | Interm. | Segunda metade de M1 |
| Mathematics for Computer Science | Lehman, Leighton, Meyer | M2 | Intro. | Texto principal, com MIT 6.042J |
| Discrete Mathematics and Its Applications | Kenneth Rosen | M2 | Intro. | Banco de exercícios |
| Calculus | James Stewart | M3, M4 | Intro. | Texto principal |
| Calculus | Michael Spivak | M3, M13 | Avanç. | Segunda passagem, planos D a F |
| Introduction to Linear Algebra | Gilbert Strang | M5 | Intro. | Texto principal, com MIT 18.06 |
| Linear Algebra Done Right | Sheldon Axler | M5 | Avanç. | Segunda passagem, antes de A1 e M10 |
| Introduction to Probability | Blitzstein, Hwang | M6 | Interm. | Texto principal, com Harvard Stat 110 |
| All of Statistics | Larry Wasserman | M7 | Interm. | Texto principal |
| Statistical Inference | Casella, Berger | M7 | Avanç. | Planos E e F |
| Elementary Differential Equations and Boundary Value Problems | Boyce, DiPrima | M8 | Intro. | Texto principal, com MIT 18.03 |
| Nonlinear Dynamics and Chaos | Steven Strogatz | M8 | Interm. | Antes de H1 |
| Numerical Analysis | Burden, Faires | M9 | Intro. | Texto principal |
| Numerical Linear Algebra | Trefethen, Bau | M9 | Avanç. | Plano F |
| Convex Optimization | Boyd, Vandenberghe | M10 | Interm. | Texto principal |
| Numerical Optimization | Nocedal, Wright | M10 | Avanç. | Junto com A2 |
| Introduction to Operations Research | Hillier, Lieberman | M11 | Intro. | Texto principal |
| Elements of Information Theory | Cover, Thomas | M12 | Interm. | Texto principal |
| Information Theory, Inference, and Learning Algorithms | David MacKay | M12, A1 | Interm. | Ponte entre M12 e IA |
| Understanding Analysis | Stephen Abbott | M13 | Interm. | Texto principal |
| Principles of Mathematical Analysis | Walter Rudin | M13 | Avanç. | Depois de Abbott |

### 10.2 Física e engenharia

| Título | Autor | Disc. | Nível | Momento de uso |
| --- | --- | --- | --- | --- |
| Curso de Física Básica (4 volumes) | H. Moysés Nussenzveig | F1–F4 | Interm. | Texto principal para quem tem cálculo firme |
| Fundamentals of Physics | Halliday, Resnick, Walker | F1–F3 | Intro. | Alternativa mais gradual |
| An Introduction to Mechanics | Kleppner, Kolenkow | F1 | Avanç. | Plano F |
| Electricity and Magnetism | Purcell, Morin | F2 | Avanç. | Plano F |
| An Introduction to Thermal Physics | Daniel Schroeder | F3 | Interm. | Planos D e F |
| Modern Physics | Tipler, Llewellyn | F4 | Intro. | Texto principal |
| Introduction to Quantum Mechanics | David Griffiths | F4 | Avanç. | Plano F, capítulos iniciais |
| Electric Circuits | Nilsson, Riedel | E1 | Intro. | Texto principal |
| Foundations of Analog and Digital Electronic Circuits | Agarwal, Lang | E1, E2 | Interm. | Com MIT 6.002 |
| Microelectronic Circuits | Sedra, Smith | E2 | Interm. | Texto principal |
| The Art of Electronics | Horowitz, Hill | E2 | Interm. | Consulta durante PJ16 |
| Digital Design and Computer Architecture | Harris, Harris | E3, E4 | Intro. | Texto principal de E3 |
| The Elements of Computing Systems | Nisan, Schocken | E3 | Intro. | Guia de PJ2 |
| Computer Organization and Design (edição RISC-V) | Patterson, Hennessy | E4 | Interm. | Texto principal, com Berkeley CS61C |
| Computer Architecture: A Quantitative Approach | Hennessy, Patterson | E4 | Avanç. | Plano F |
| Introduction to Embedded Systems: A Cyber-Physical Systems Approach | Lee, Seshia | E5, H2 | Interm. | Texto principal |
| Embedded Systems: Introduction to ARM Cortex-M Microcontrollers | Jonathan Valvano | E5 | Intro. | Guia de laboratório |
| Signals and Systems | Oppenheim, Willsky | E6 | Interm. | Texto principal |
| Feedback Systems | Åström, Murray | H1 | Interm. | Texto principal |
| Modern Control Engineering | Katsuhiko Ogata | H1 | Interm. | Exercícios |
| Modern Robotics | Lynch, Park | H2 | Interm. | Texto principal |
| Probabilistic Robotics | Thrun, Burgard, Fox | H2 | Avanç. | Estimação, plano F |

### 10.3 Ciência da Computação e infraestrutura

| Título | Autor | Disc. | Nível | Momento de uso |
| --- | --- | --- | --- | --- |
| Structure and Interpretation of Computer Programs | Abelson, Sussman | P1, C3 | Interm. | Texto principal de P1 |
| The C Programming Language | Kernighan, Ritchie | P1, P2 | Intro. | Transição para C |
| Computer Systems: A Programmer's Perspective | Bryant, O'Hallaron | P2 | Interm. | Texto principal, com os labs de CMU 15-213 |
| Introduction to Algorithms | Cormen, Leiserson, Rivest, Stein | C1 | Interm. | Texto principal, com MIT 6.006 e 6.046 |
| Algorithms | Sedgewick, Wayne | C1 | Intro. | Primeira passagem, implementações |
| Introduction to the Theory of Computation | Michael Sipser | C2 | Interm. | Texto principal |
| Computational Complexity: A Modern Approach | Arora, Barak | C2 | Avanç. | Plano F |
| Programming Languages: Application and Interpretation | Shriram Krishnamurthi | C3 | Interm. | Texto principal |
| Types and Programming Languages | Benjamin Pierce | C3 | Avanç. | Plano F |
| Programming in Haskell | Graham Hutton | C3 | Intro. | Prática funcional |
| Compilers: Principles, Techniques, and Tools | Aho, Lam, Sethi, Ullman | C4 | Interm. | Texto principal, com Stanford CS143 |
| Crafting Interpreters | Robert Nystrom | C4 | Intro. | Guia de PJ4 |
| Modern Compiler Implementation in ML | Andrew Appel | C4 | Avanç. | Guia de PJ8 |
| Operating Systems: Three Easy Pieces | Arpaci-Dusseau, Arpaci-Dusseau | C5 | Interm. | Texto principal, com os labs do xv6 |
| The Art of Multiprocessor Programming | Herlihy, Shavit | C6 | Avanç. | Texto principal |
| Computer Networking: A Top-Down Approach | Kurose, Ross | C7 | Intro. | Texto principal |
| TCP/IP Illustrated, Volume 1 | W. Richard Stevens | C7 | Interm. | Durante PJ5 |
| Database System Concepts | Silberschatz, Korth, Sudarshan | C8 | Interm. | Texto principal, com CMU 15-445 |
| Database Internals | Alex Petrov | C8 | Interm. | Durante PJ7 |
| Designing Data-Intensive Applications | Martin Kleppmann | C9, S6, D6 | Interm. | Leitura de entrada do vértice de dados |
| Distributed Systems | van Steen, Tanenbaum | C9 | Interm. | Texto de apoio teórico |
| Security Engineering | Ross Anderson | C10 | Interm. | Texto principal |
| Introduction to Modern Cryptography | Katz, Lindell | C10 | Avanç. | Planos E e F |
| The Linux Command Line | William Shotts | G1 | Intro. | Primeiro semestre |
| The Linux Programming Interface | Michael Kerrisk | G1, P2 | Interm. | Consulta permanente |
| Kubernetes: Up and Running | Burns, Beda, Hightower | G2 | Intro. | Depois de construir um container à mão |
| Terraform: Up and Running | Yevgeniy Brikman | G3 | Intro. | Junto com a documentação oficial |
| Systems Performance | Brendan Gregg | G4 | Avanç. | Texto principal |

### 10.4 Engenharia de software

| Título | Autor | Disc. | Nível | Momento de uso |
| --- | --- | --- | --- | --- |
| A Philosophy of Software Design | John Ousterhout | S1 | Intro. | Texto principal |
| Design Patterns | Gamma, Helm, Johnson, Vlissides | S1 | Interm. | Depois de um projeto próprio de médio porte |
| Refactoring | Martin Fowler | S1, S2 | Interm. | Durante a revisão de PJ1 |
| Test-Driven Development: By Example | Kent Beck | S2 | Intro. | Texto principal |
| Working Effectively with Legacy Code | Michael Feathers | S2 | Interm. | Antes de PJ20 |
| Software Requirements | Wiegers, Beatty | S3 | Intro. | Texto principal |
| Domain-Driven Design | Eric Evans | S3, S4 | Avanç. | Com experiência em um domínio real |
| Software Engineering | Ian Sommerville | S3 | Intro. | Visão geral |
| Software Architecture in Practice | Bass, Clements, Kazman | S4 | Interm. | Texto principal |
| Fundamentals of Software Architecture | Richards, Ford | S4 | Intro. | Primeira leitura |
| Patterns of Enterprise Application Architecture | Martin Fowler | S4 | Interm. | Consulta |
| Clean Architecture | Robert C. Martin | S4 | Intro. | Leitura crítica, comparada a Ousterhout |
| Continuous Delivery | Humble, Farley | S5 | Interm. | Texto principal |
| Site Reliability Engineering | Beyer, Jones, Petoff, Murphy (org.) | S5, G4 | Interm. | Capítulos de SLO, incidentes e sobrecarga |
| Observability Engineering | Majors, Fong-Jones, Miranda | S5 | Interm. | Durante PJ11 |
| Release It! | Michael Nygard | S6 | Interm. | Texto principal |
| The Mythical Man-Month | Frederick Brooks | H4 | Intro. | Leitura de entrada |

### 10.5 Dados e inteligência artificial

| Título | Autor | Disc. | Nível | Momento de uso |
| --- | --- | --- | --- | --- |
| The Data Warehouse Toolkit | Kimball, Ross | D1, D2 | Interm. | Texto principal de modelagem dimensional |
| SQL Performance Explained | Markus Winand | D1 | Interm. | Depois de C8 |
| SQL for Smarties | Joe Celko | D1 | Avanç. | Consulta |
| Fundamentals of Data Engineering | Reis, Housley | D2, D5, D6 | Intro. | Mapa do campo, antes das ferramentas |
| Spark: The Definitive Guide | Chambers, Zaharia | D3 | Interm. | Depois do artigo de RDD |
| Streaming Systems | Akidau, Chernyak, Lax | D4 | Avanç. | Texto principal |
| Kafka: The Definitive Guide | Narkhede, Shapira, Palino | D4 | Interm. | Depois do artigo do Kafka |
| DAMA-DMBOK | DAMA International | D5 | Interm. | Consulta |
| Data Mesh | Zhamak Dehghani | D6 | Interm. | Leitura crítica |
| An Introduction to Statistical Learning | James, Witten, Hastie, Tibshirani | A1 | Intro. | Primeira passagem |
| The Elements of Statistical Learning | Hastie, Tibshirani, Friedman | A1 | Avanç. | Planos E e F |
| Pattern Recognition and Machine Learning | Christopher Bishop | A1 | Avanç. | Visão bayesiana |
| Deep Learning | Goodfellow, Bengio, Courville | A2 | Interm. | Texto principal |
| Understanding Deep Learning | Simon Prince | A2 | Interm. | Alternativa mais recente |
| Speech and Language Processing | Jurafsky, Martin | A3 | Interm. | Texto principal, com Stanford CS224n |
| Introduction to Information Retrieval | Manning, Raghavan, Schütze | A4 | Interm. | Guia de PJ10 e de RAG |
| Recommender Systems: The Textbook | Charu Aggarwal | A4 | Interm. | Consulta |
| Designing Machine Learning Systems | Chip Huyen | A5 | Interm. | Texto principal |

### 10.6 Interdisciplinares

| Título | Autor | Disc. | Nível | Momento de uso |
| --- | --- | --- | --- | --- |
| Operations Management | Slack, Brandon-Jones | H3 | Intro. | Texto principal |
| Information Rules | Shapiro, Varian | H3 | Intro. | Economia de plataformas |
| Guia PMBOK | Project Management Institute | H4 | Intro. | Consulta |
| The Craft of Research | Booth, Colomb, Williams | H5 | Intro. | Antes do primeiro relatório |
| Writing for Computer Science | Justin Zobel | H5 | Interm. | Durante PJ18 |
| What Is This Thing Called Science? | Alan Chalmers | H6 | Intro. | Texto principal |
| The Structure of Scientific Revolutions | Thomas Kuhn | H6 | Interm. | Depois de Chalmers |
| The Logic of Scientific Discovery | Karl Popper | H6 | Avanç. | Plano F |
| A History of Modern Computing | Paul Ceruzzi | H6 | Intro. | Leitura contínua |

### 10.7 Artigos fundamentais

| Artigo | Autores, ano | Disc. | Momento de uso |
| --- | --- | --- | --- |
| On Computable Numbers, with an Application to the Entscheidungsproblem | Turing, 1936 | C2, H6 | Fim de C2 |
| A Mathematical Theory of Communication | Shannon, 1948 | M12 | Abertura de M12 |
| A Relational Model of Data for Large Shared Data Banks | Codd, 1970 | C8 | Abertura de C8 |
| On the Criteria To Be Used in Decomposing Systems into Modules | Parnas, 1972 | S1 | Abertura de S1 |
| Time, Clocks, and the Ordering of Events in a Distributed System | Lamport, 1978 | C9 | Abertura de C9 |
| Access Path Selection in a Relational Database Management System | Selinger et al., 1979 | C8 | Otimização de consultas |
| End-to-End Arguments in System Design | Saltzer, Reed, Clark, 1984 | C7, S4 | Fim de C7 |
| Learning Representations by Back-Propagating Errors | Rumelhart, Hinton, Williams, 1986 | A2 | Abertura de A2 |
| ARIES: A Transaction Recovery Method | Mohan et al., 1992 | C8 | Recuperação, durante PJ7 |
| Paxos Made Simple | Lamport, 2001 | C9 | Consenso |
| The Google File System | Ghemawat, Gobioff, Leung, 2003 | C9, D3 | Antes de D3 |
| MapReduce: Simplified Data Processing on Large Clusters | Dean, Ghemawat, 2004 | D3 | Abertura de D3 |
| Dynamo: Amazon's Highly Available Key-value Store | DeCandia et al., 2007 | C9 | Consistência eventual |
| Architecture of a Database System | Hellerstein, Stonebraker, Hamilton, 2007 | C8 | Fim de C8 |
| Kafka: a Distributed Messaging System for Log Processing | Kreps, Narkhede, Rao, 2011 | D4 | Abertura de D4 |
| Resilient Distributed Datasets | Zaharia et al., 2012 | D3 | Antes de usar Spark |
| Spanner: Google's Globally-Distributed Database | Corbett et al., 2012 | C9 | Transações distribuídas |
| In Search of an Understandable Consensus Algorithm (Raft) | Ongaro, Ousterhout, 2014 | C9 | Durante PJ9 |
| The Dataflow Model | Akidau et al., 2015 | D4 | Tempo de evento e janelas |
| Hidden Technical Debt in Machine Learning Systems | Sculley et al., 2015 | A5 | Abertura de A5 |
| Attention Is All You Need | Vaswani et al., 2017 | A3 | Abertura de A3 |
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Lewis et al., 2020 | A4 | Durante PJ15 |
| Lakehouse: A New Generation of Open Platforms | Armbrust et al., 2021 | D2 | Fim de D2 |
| How to Read a Paper | Keshav, 2007 | H5 | Antes do primeiro artigo |

### 10.8 Cursos abertos

| Instituição | Cursos | Disciplinas |
| --- | --- | --- |
| MIT | 18.01, 18.02, 18.03, 18.06; 6.042J; 6.006, 6.046J; 8.01, 8.02; 6.002; 6.1810 (antigo 6.S081); 6.5840 (antigo 6.824); 6.858; The Missing Semester | M3, M4, M8, M5; M2; C1; F1, F2; E1; C5; C9; C10; G1 |
| Harvard | Stat 110; CS50 | M6; nivelamento de P1 |
| Berkeley | CS61A, CS61C, CS162, CS186 | P1, E4, C5, C8 |
| Stanford | CS143, CS144, CS149, CS229, CS231n, CS224n | C4, C7, C6, A1, A2, A3 |
| Carnegie Mellon | 15-213, 15-445, 15-721 | P2, C8, C8 avançado |

Documentação oficial é a referência para ferramentas: PostgreSQL, Apache Spark, Apache Kafka, Apache Airflow, dbt, Docker, Kubernetes, Terraform e os guias de arquitetura de AWS, Azure e GCP. Ela entra depois do livro ou do artigo que explica o mecanismo.

## 11. Projetos integradores

São 20 projetos em quatro degraus de complexidade; cada plano usa um subconjunto, nos semestres indicados nos cronogramas. Um projeto só vale como prova de domínio se cumprir as cinco condições de 11.2.

### 11.1 Catálogo de projetos

| Cód. | Projeto | Disciplinas consolidadas | Complexidade | Competência demonstrada | Momento (plano · semestre) |
| --- | --- | --- | --- | --- | --- |
| PJ1 | Biblioteca de estruturas de dados e algoritmos, com testes de propriedade e benchmarks | P1, C1, S2 | Baixa | Implementar do zero e medir o custo real contra o assintótico | A·2, B·1–3, C·1–3, D·1–4, E·1–4, F·1–4 |
| PJ2 | Computador da porta NAND ao assembler | E3, E4 | Baixa | Explicar a máquina camada por camada | A·1, B·2, C·2, D·3, E·3, F·3 |
| PJ3 | Shell Unix e alocador de memória em C | P2, G1 | Média | Trabalhar com processos, sinais e memória sem rede de proteção | A·2, B·3, C·3, D·5, E·5, F·5 |
| PJ4 | Interpretador de uma linguagem com closures e coleta de lixo | C3, C1 | Média | Implementar a semântica de uma linguagem | B·4, C·4, D·6, E·6, F·6–7 |
| PJ5 | Pilha TCP/IP em espaço de usuário e servidor HTTP sobre ela | C7, P2 | Média | Implementar um protocolo confiável a partir da especificação | B·5, C·5, D·8, E·7, F·9 |
| PJ6 | Extensões em um kernel didático (escalonador, memória, sistema de arquivos) | C5, E4 | Média | Alterar um sistema operacional e medir o efeito | D·7, F·8 |
| PJ7 | Banco de dados relacional simplificado: páginas, índice B+, executor, log de recuperação, controle de concorrência | C8, C1, C6 | Alta | Construir armazenamento transacional correto sob falha | A·3 (reduzido), B·6, C·6–7, D·9–10, E·8–9, F·10–11 |
| PJ8 | Compilador com otimizações para uma arquitetura real | C4, E4 | Alta | Traduzir linguagem de alto nível em código de máquina eficiente | F·11 |
| PJ9 | Armazenamento chave-valor distribuído com consenso, particionamento e testes de injeção de falhas | C9, C6, C7 | Alta | Garantir consistência sob falha parcial | B·7, C·8, D·11, E·10, F·13 |
| PJ10 | Mecanismo de busca: coletor, índice invertido, ranqueamento | C1, C8, A4, M6 | Média | Projetar estruturas para consulta em larga escala | Eletivo; substitui PJ5 a partir de C8 |
| PJ11 | Pipeline de dados completo: ingestão, lakehouse, modelo dimensional, testes de dados, orquestração, infraestrutura por código | D1, D2, D3, D5, G3, S5 | Alta | Operar dados de ponta a ponta com qualidade verificável | A·4, B·8, D·13–14, E·13, F·16 |
| PJ12 | Log replicado no estilo de um broker de eventos, com processamento em janelas e captura de mudanças | D4, C9 | Alta | Implementar garantias de entrega e de ordem | C·9, E·14, F·17 |
| PJ13 | Plataforma de dados escalável com SLO medido, contratos, observabilidade, teste de carga e custo | D6, G4, S6, S4 | Muito alta | Arquitetar e justificar uma plataforma com requisitos quantificados | C·10, F·20 |
| PJ14 | Biblioteca de diferenciação automática e modelos clássicos do zero; depois, um modelo em produção com monitoramento | A1, A2, A5, M5, M10 | Alta | Entender o treino por dentro e operar um modelo | E·11 e 13, F·14 e 16 |
| PJ15 | Transformer pequeno treinado do zero e aplicação RAG com avaliação quantitativa | A3, A4 | Alta | Construir e avaliar com método uma aplicação de IA generativa | E·15, F·18 |
| PJ16 | Sistema embarcado: firmware sem sistema operacional, tempo real, telemetria em rede | E5, E2, C7 | Média | Programar sob restrição de tempo, memória e energia | D·12, E·12, F·15 |
| PJ17 | Sistema ciberfísico integrado: planta controlada, embarcado, streaming de telemetria e modelo | H1, H2, E5, D4, A1 | Muito alta | Integrar hardware, software e dados em um sistema único | E·16, F·19 |
| PJ18 | Trabalho de pesquisa: reprodução de um artigo, extensão original, relatório ou artigo | H5 e o vértice | Muito alta | Produzir e defender conhecimento novo | C·9–10 (reduzido), E·13–16, F·15–20 |
| PJ19 | Simulação numérica de um sistema físico, com análise de erro e de estabilidade | M9, M8, F1 | Média | Ligar modelo matemático, método numérico e fenômeno | F·12 |
| PJ20 | Modernização de um sistema legado com registro de decisões de arquitetura | S2, S3, S4, S6 | Alta | Evoluir um sistema existente sem interrompê-lo | D·14 |

No Plano A, PJ9 não tem horas próprias: os laboratórios de MIT 6.5840, dentro de C9, cumprem esse papel.

No plano adaptado à graduação, os projetos aparecem nos portões de 16.5 e 17.2 e na tabela 17.3. O Projeto Integrado do curso pode cumprir PJ11 ou PJ20, e o portão de D6 cumpre o papel de PJ13.

### 11.2 Condições para um projeto contar como prova de domínio

1. **Especificação antes do código.** Uma página com requisitos, o que fica de fora e os critérios de aceitação mensuráveis.
2. **Sem tutorial.** As referências são o livro, o artigo e a especificação; repositórios de solução não são consultados.
3. **Correção verificada.** Conjunto de testes automatizados e, nos projetos de sistemas, injeção de falhas.
4. **Medição.** Pelo menos um experimento de desempenho, com método descrito e resultado comparado a uma previsão feita antes.
5. **Relatório técnico.** De duas a seis páginas: decisões, alternativas rejeitadas, limitações conhecidas. A partir de PJ7, com revisão de alguém de fora.

## 12. Critérios de avaliação

Uma disciplina só é dada como concluída quando a evidência do nível-alvo existe e pode ser mostrada a outra pessoa. Leitura terminada não é evidência de nenhum nível.

### 12.1 Escala de domínio e evidência exigida

| Nível | Definição | Evidência exigida | Carga típica por disciplina |
| --- | --- | --- | --- |
| 1 Reconhecimento | Conheço os conceitos | Mapa conceitual de uma página feito sem consulta; acerto de 80% em um questionário de definições | 20–40 h |
| 2 Compreensão | Explico os mecanismos | Explicação escrita de cada mecanismo central, com exemplo próprio e um caso em que ele falha | 40–70 h |
| 3 Aplicação | Resolvo problemas | 70% em prova antiga do curso de referência, no tempo regulamentar e sem consulta | 70–130 h |
| 4 Implementação | Construo soluções | Labs do curso de referência completos e passando nos testes; em matemática e física, 80% na prova e exercícios de prova resolvidos | 130–190 h |
| 5 Análise | Identifico limitações e otimizo | Relatório com previsão, medição e explicação da diferença; uma otimização justificada pela medição | 180–260 h, com projeto |
| 6 Projeto | Arquiteto soluções completas | Sistema próprio entregue contra requisitos quantificados, com documento de arquitetura revisado por alguém de fora | 260 h ou mais, com projeto de complexidade alta |
| 7 Pesquisa | Investigo problemas não triviais e produzo conhecimento | Reprodução de artigo e resultado original submetido à crítica externa (conferência, periódico, workshop ou relatório público com revisão) | Disciplina mais 400 h ou mais de pesquisa |

### 12.2 Ciclo de avaliações

| Frequência | Avaliação | Formato | Consequência |
| --- | --- | --- | --- |
| Semanal | Autoteste de recuperação | 30 minutos, questões das três últimas semanas, sem consulta | Erros entram no caderno de erros e na revisão espaçada |
| Mensal | Prova mista | 2 horas, problemas de todas as disciplinas abertas e de uma já concluída | Abaixo de 70% em uma disciplina concluída: ela volta à revisão |
| Fim de disciplina | Prova de conclusão | Prova antiga do curso de referência, mais a evidência do nível-alvo de 12.1 | Sem a evidência, a disciplina continua aberta e ocupa uma das três vagas |
| Semestral | Prova de pré-requisitos | 3 horas, cobrindo os pré-requisitos das disciplinas do semestre seguinte | Abaixo de 70%: as primeiras semanas do semestre são de recuperação, tiradas do orçamento de revisão |
| Semestral | Banca do projeto | Apresentação de 20 minutos e relatório, para um par ou mentor | O projeto só conta com as cinco condições de 11.2 |
| Anual | Auditoria do plano | Horas registradas contra o orçamento, níveis atingidos contra a matriz 2.10 (no plano adaptado, contra 16.5 e 17.2) | Desvio acima de 15%: replanejar o ano seguinte ou mudar de plano |

### 12.3 Regras de conclusão

- **O nível é o da evidência mais fraca.** Quem passa na prova (nível 3) e não termina os labs não está no nível 4.
- **Domínio decai.** Uma disciplina de nível 4 ou mais que fique dois anos sem uso passa por nova prova mista antes de servir de pré-requisito.
- **Avaliação externa nos níveis 6 e 7.** Autoavaliação não vale; é preciso revisor, mantenedor de projeto de código aberto, banca ou parecerista.
- **Marcos dos cronogramas são eliminatórios.** Um semestre só termina quando todas as frases do marco podem ser demonstradas.

## 13. Comparação dos seis planos

Os planos não formam uma escala de “menos a mais”: C é mais profundo que D com menos horas, e D é mais amplo que C sem chegar ao nível 6 em nada. A escolha é entre perfis, não entre tamanhos.

### 13.1 Quadro executivo

| Critério | A · 2 anos | B · 4 anos | C · 5 anos | D · 7 anos | E · 8 anos | F · 10 anos |
| --- | --- | --- | --- | --- | --- | --- |
| Horas semanais | 40 | 30 | 25 | 20 | 20 | 20 |
| Horas anuais | 1.920 | 1.440 | 1.200 | 960 | 960 | 960 |
| Horas totais | 3.840 | 5.760 | 6.000 | 6.720 | 7.680 | 9.600 |
| Disciplinas (de 63) | 34 | 47 | 44 | 56 | 61 | 63 |
| Profundidade acadêmica (base · vértice) | 3–4 · 4–5 | 4 · 5 | 4 · 6 | 4 · 5 | 4 · 6 e 5 | 4–5 · 7 e 5 |
| Amplitude | Estreita: sem física, IA e eixo H | Média | Média-baixa | Alta | Muito alta | Completa |
| Capacidade de implementação | Alta em sistemas de dados | Alta | Muito alta no vértice | Alta | Muito alta em dois domínios | Muito alta |
| Maturidade arquitetural | Baixa (S4 em nível 3) | Média (nível 4) | Alta no vértice (D6 em nível 6) | Alta (S4 em nível 5) | Alta (S4 em 5, D6 em 6) | Muito alta (S4 em nível 6) |
| Capacidade de pesquisa | Nenhuma | Leitura crítica | Reprodução de artigo | Leitura crítica | Pesquisa aplicada inicial | Contribuição original |
| Sustentabilidade da rotina | Muito baixa | Baixa | Média | Alta | Média-alta | Média: o risco é a duração |
| Principais riscos | Esgotamento; consolidação fraca; dois anos sem renda | Conflito com o trabalho; atraso em cascata | Especialização estreita; vértice perder relevância | Esquecimento do início; nenhum diferencial profundo | Menor fatia de projetos; dispersão entre dois vértices | Abandono; defasagem das ferramentas; pesquisa sem orientação |
| Perfil esperado | Engenheiro de software e dados com base de sistemas | Bacharel em computação por equivalência, com portfólio de sistemas | Especialista em sistemas de dados distribuídos | Engenheiro de computação generalista de base ampla | Generalista sênior com dois domínios de autoridade | Generalista pesquisador, com amplitude de graduação e mestrado |

### 13.2 Vantagens e desvantagens

| Plano | Vantagem central | Desvantagem central | Faz sentido quando |
| --- | --- | --- | --- |
| A | Resultado profissional mais rápido; imersão reduz o esquecimento | Não forma um generalista; pouco tempo para o conhecimento assentar | Há dois anos livres e financiados, e o objetivo imediato é mudar de carreira |
| B | Cobre o núcleo clássico com boa relação entre horas e amplitude | 30 h semanais por quatro anos raramente coexistem com emprego integral | O trabalho é de meio período ou o estudo é a atividade principal |
| C | Melhor retorno profissional por hora: nível 6 em um domínio valorizado em cinco anos | Abre mão de física, hardware e IA | O objetivo é autoridade técnica em sistemas de dados, com a amplitude adiada |
| D | Rotina mais sustentável; formação equilibrada | Sete anos sem atingir nível 6 em nada | A prioridade é cultura de engenharia ampla, apoiada pela prática no emprego |
| E | Primeiro plano que entrega de fato o perfil generalista com profundidade | Oito anos de constância; projetos em apenas 13% da carga | O objetivo é o descrito neste projeto, sem ambição acadêmica formal |
| F | Único que inclui rigor matemático pleno e pesquisa original | As 1.920 h a mais que o Plano E vão em sua maior parte para pesquisa, matemática e física, com pouco retorno profissional direto | Há interesse genuíno em pesquisar, com ou sem pós-graduação |

## 14. Recomendação técnica final

O Plano E (8 anos, 20 h por semana, 7.680 h) é o que melhor atende ao objetivo declarado; o Plano C (5 anos, 25 h por semana) é a alternativa se o retorno profissional em prazo menor pesar mais que a amplitude. Os planos A e F ficam nos extremos por razões opostas: A não forma um generalista, e F cobra 1.920 h adicionais por algo que só vale para quem quer pesquisar.

**Atualização:** com a graduação em Engenharia de Software e a sua rotina, a recomendação passa a ser o Plano E adaptado. A seção 18 cobre o nivelamento, a seção 16 os quatro anos do curso e a seção 17 os anos seguintes. Sem contar fins de semana, o total fica entre 9 anos, se boa parte do nivelamento for dispensada ou feita antes do curso, e cerca de 9 anos e meio no cenário típico. As seções 14.2 e 14.3 já estão escritas para essa versão.

### 14.1 Por que E e não os outros

| Critério | Leitura |
| --- | --- |
| Profundidade | E e C são os planos mais curtos que chegam ao nível 6; D gasta sete anos sem chegar lá |
| Amplitude | E cobre 61 das 63 disciplinas e é o primeiro com sinais, controle, embarcados e IA em nível útil; C cobre 44 e deixa essas áreas de fora |
| Sustentabilidade | 20 h por semana cabem ao lado de um emprego; 25 h (C) exigem abrir mão de quase todo o lazer por cinco anos; 30 h e 40 h (B e A) não cabem |
| Aplicação profissional | Em E, o núcleo do primeiro vértice (C8 e C9 em nível 6) fica pronto no ano 5, mesmo prazo de C; os anos 6 a 8 somam IA e a ponte física sobre uma base que já rende profissionalmente |
| Custo marginal de F | Os dois anos extras compram análise real, física intermediária e 560 h a mais de pesquisa; sem intenção de pesquisar, o retorno é baixo |

### 14.2 Como executar: um tronco comum e três pontos de decisão

No plano adaptado, os quatro anos da graduação seguem a seção 16. As decisões ficam nos pontos em que o rumo pode mudar sem quebrar a sequência de pré-requisitos.

1. **Início.** Seguir a semana-base de 16.1 e registrar as horas reais desde a primeira semana.
2. **Decisão 1, fim do ano 1.** Média real do complemento abaixo de 9 h por semana: manter a ordem de 16.5 e deixar a fila deslizar, sem cortar portões. Fins de semana frequentes: antecipar as disciplinas de 16.8, na ordem indicada lá.
3. **Decisão 2, fim do ano 2.** Interesse em rigor matemático e em pesquisa: acrescentar M13 (análise real) logo depois de M4 e seguir a física com o aprofundamento do Plano F, ao custo de cerca de meio ano a mais.
4. **Decisão 3, fim da graduação.** Confirmar o segundo vértice: IA, como está na seção 17, ou hardware e controle, levando E5, E6, H1 e H2 ao nível 5 e reduzindo A3 a A5.

### 14.3 Primeiros 90 dias

- [ ] Fazer os diagnósticos dos blocos A (aritmética) e L (lógica de programação) do nivelamento
- [ ] Fixar na agenda as janelas de 16.1 e montar a planilha de registro de horas e evidências
- [ ] Abrir NM1 e NL1 e seguir a rota crítica de 18.5
- [ ] Escrever a especificação de PJ1 fase 1
- [ ] Encontrar um par ou mentor para as bancas semestrais
- [ ] Aplicar a primeira prova mista mensal ao fim da quarta semana

## 15. Integração com a graduação em Engenharia de Software

A grade da graduação cobre quase todo o eixo D do catálogo (engenharia de software) e a camada introdutória de programação, estruturas de dados, bancos de dados e matemática discreta. Não cobre cálculo, álgebra linear, física, hardware, o funcionamento interno de sistemas operacionais e bancos de dados, sistemas distribuídos, engenharia de dados em escala nem IA. Por isso, cerca de 600 h do Plano E são creditadas ao curso (15.4); o restante está sequenciado nas seções 16 e 17.

### 15.1 Premissas

- Duração da graduação: 4 anos, 8 semestres (confirmado)
- Ordem das unidades do curso: ainda não definida; a sequência de 16.3 é proposta a partir das ementas
- Carga do curso: assumida em 13 h por semana; ajustar 16.1 quando o valor real for conhecido
- Níveis do curso: Base, Intermediário e Avançado lidos como níveis 2, 3 e 3–4 da escala da seção 12, estimativa feita só pelas ementas

### 15.2 Mapa da grade para o catálogo

| Eixo do curso | Unidade (nível no curso) | Disciplinas do catálogo | O que o plano acrescenta |
| --- | --- | --- | --- |
| 01 Construção | Produto Completo com Scrum, Design Thinking e Low-Code (Interm.) | H4, S3 em parte | Nada; Scrum, Design Thinking e low-code ficam só com o curso |
| 01 | Python, Dados e Desenvolvimento com Assistência de IA (Base) | P1 em parte | Abstração e recursão no nível do SICP; linguagem C |
| 01 | Estruturas de Dados: Listas, Árvores, Hash e Grafos (Interm.) | C1 em parte | Provas de correção, programação dinâmica, gulosos, análise amortizada, fluxo |
| 01 | POO e Trabalho Colaborativo em Repositório (Interm.) | S1 | Ocultação de informação e complexidade (Ousterhout, Parnas) |
| 02 Dados | Modelagem Conceitual e Relacional com Normalização (Base) | C8 em parte, D1 em parte | Modelagem dimensional |
| 02 | SQL de Consulta e Implementação do Banco Físico (Base) | C8 em parte, D1 em parte | Janelas, planos de execução, tuning |
| 02 | Exposição de Dados por APIs (Interm.) | S4 em parte, C7 em parte | O protocolo por baixo da API |
| 02 | Integridade, Testes e Documentação de Dados (Interm.) | D5 em parte, S2 em parte | Contratos, linhagem, orquestração |
| 03 Requisitos | Elicitação de Requisitos com Entrevistas e Oficinas (Base) | S3 | Nada |
| 03 | Requisitos Verificáveis, Rastreabilidade e Mudanças (Interm.) | S3 | Nada |
| 03 | Modelagem com UML, SysML e BPMN (Interm.) | S3 | Domain-Driven Design, como leitura |
| 03 | Do Problema Real ao Protótipo Funcional (Interm.) | S3 | Nada |
| 04 Infraestrutura | Memória, Processos, Concorrência e Redes (Interm.) | P2, C5, C6, C7 em visão geral | Quase tudo: CS:APP, kernel didático, pilha TCP, estruturas concorrentes |
| 04 | Segurança do Tráfego e Operação do Sistema (Interm.) | C10 em parte, S5 em parte | Criptografia aplicada, segurança de memória |
| 04 | Integração com Serviços Externos e Nuvem (Avanç.) | G3 em parte, S4 em parte | Infraestrutura por código, custo, rede em nuvem |
| 04 | Testes de Integração, Logs e Simulação de Falhas (Avanç.) | S2, S5 em parte, S6 em parte | Injeção de falhas em sistemas distribuídos (C9) |
| 05 Arquitetura | Estilos e Padrões de Arquitetura (Avanç.) | S4 | Nada |
| 05 | Atributos de Qualidade e Decisões Arquiteturais (Avanç.) | S4 | Nada |
| 05 | Fronteira e Responsabilidades do Sistema (Avanç.) | S4, S3 | Nada |
| 05 | Incremento Arquitetado com Decisões Medidas (Avanç.) | S4, S6 em parte | Padrões de estabilidade sob carga (Nygard) |
| 06 Fundamentos | Matemática Discreta, Lógica e Matrizes (Base) | M1 em parte, M2 em parte, M5 só operações | Provas, teoria dos números; álgebra linear inteira |
| 06 | Probabilidade, Estatística e Otimização (Interm.) | M6, M7, M10 em visão aplicada | As três disciplinas completas, que dependem de cálculo |
| 06 | Teoria da Computação, Autômatos e Grafos (Avanç.) | C2 em parte | Reduções e provas de indecidibilidade (Sipser) |
| 06 | Custo de Algoritmos e Limites do Software (Avanç.) | C1 em parte, C2 em parte | Análise com recorrências e prova |
| 07 Qualidade | Testes em Vários Níveis com Automação (Interm.) | S2 | Testes de propriedade e fuzzing |
| 07 | Inspeção, Verificação e Validação (Interm.) | S2 | Nada |
| 07 | Métricas de Esforço, Defeitos e Maturidade (Avanç.) | H4 em parte | Nada; fica só com o curso |
| 07 | Verificação de Incremento e Melhoria de Processo (Avanç.) | S2, H4 | Nada |
| 08 Organização | Sistemas de Informação e Arquitetura Empresarial (Base) | H3 em parte, D5 em parte | Nada |
| 08 | Gestão de Projetos, Riscos e Débito Técnico (Interm.) | H4 | Nada |
| 08 | Entrega Contínua com DevOps e Observabilidade (Avanç.) | S5 | Containers e Kubernetes por dentro (G2), SLO |
| 08 | Projeto Integrado: Sistema Completo e Plano de Evolução (Avanç.) | Projeto integrador | Serve como PJ11 ou PJ20 se cumprir as condições de 11.2 |
| 09 Profissional | Ética Profissional e Proteção de Dados (Base) | Fora do catálogo | Nada; fica só com o curso |
| 09 | Efeitos Sociais, Inclusão e Acessibilidade (Base) | Fora do catálogo | Nada; fica só com o curso |
| 09 | Escrita Técnica e Apresentação de Decisões (Base) | H5 em parte | Leitura de artigos e desenho experimental |
| 09 | Colaboração, Feedback e Gestão de Conflitos (Base) | Fora do catálogo | Nada; fica só com o curso |

### 15.3 O que a graduação não cobre

| Eixo do catálogo | Disciplinas sem cobertura na grade | Consequência |
| --- | --- | --- |
| A Matemática | Base do Ensino Fundamental e Médio (nivelamento, seção 18), M3, M4, M5 (além de matrizes), M8, M9, M11, M12, M13 | É a maior lacuna e a prioridade do estudo próprio nos dois primeiros anos |
| B Física e engenharia | F1–F4, E1–E6 | Tudo por conta do plano |
| C Computação | P2, C3, C4, C9; C5, C6 e C7 além da visão geral; C8 por dentro | O tronco de sistemas continua sendo do plano |
| E Dados | D2, D3, D4, D6 | O vértice de dados continua sendo do plano |
| F IA | A1–A5 | O curso usa IA como ferramenta; não ensina como ela funciona |
| G Infraestrutura | G1, G2, G4 | Por conta do plano |
| H Interdisciplinar | H1, H2, H6 | Por conta do plano |

### 15.4 Crédito de horas no Plano E

O crédito só vale depois da prova de conclusão da seção 12 no nível-alvo: aprovação na unidade do curso não é, sozinha, evidência. Os valores são estimativas pelas ementas.

| Disciplina | Plano E (h) | Com a graduação (h) | O que resta estudar por conta própria |
| --- | --- | --- | --- |
| P1 Programação e abstração | 180 | 120 | SICP e C |
| C1 Algoritmos e estruturas de dados | 280 | 220 | CLRS com provas; técnicas de projeto |
| M1 Lógica, provas e conjuntos | 80 | 60 | Técnicas de prova |
| M2 Matemática discreta | 160 | 130 | Combinatória, teoria dos números, probabilidade discreta |
| C2 Teoria da computação | 70 | 40 | Reduções e complexidade |
| C8 Bancos de dados | 260 | 230 | Armazenamento, índices, execução, transações |
| D1 Modelagem e SQL avançado | 90 | 50 | Dimensional, janelas, planos |
| S1 Projeto e construção | 70 | 20 | Ousterhout e Parnas |
| S2 Testes e qualidade | 50 | 10 | Propriedade e fuzzing |
| S3 Requisitos e modelagem | 30 | 0 | — |
| S4 Arquitetura de software | 90 | 30 | Leitura de Bass et al. e casos |
| S5 Entrega e operação | 70 | 30 | SLO e prática de SRE |
| S6 Sistemas escaláveis e resilientes | 60 | 40 | Padrões de estabilidade |
| C10 Segurança | 60 | 50 | Criptografia, segurança de software |
| G3 Cloud e IaC | 60 | 40 | Infraestrutura por código, custo |
| D5 Qualidade e governança de dados | 50 | 30 | Orquestração, contratos |
| H4 Gestão de projetos | 20 | 0 | — |
| H5 Metodologia e escrita | 50 | 30 | Leitura de artigos, experimentos |
| **Total das 18 disciplinas** | **1.730** | **1.130** | **600 h creditadas** |

## 16. Plano dos quatro anos da graduação, na sua rotina

Nos quatro anos da graduação, o plano usa só os dias úteis: cerca de 28 h por semana, das quais 12 h nas manhãs vão para o complemento (matemática e sistemas que o curso não dá) e 13 h, quase todas à noite, vão para o curso. Os fins de semana não entram na conta. Em oito semestres, isso fecha as 36 unidades do curso e 14 disciplinas do catálogo, cada uma com um portão de saída que precisa ser cumprido antes de a seguinte começar.

### 16.1 Semana-base (segunda a sexta)

| Janela | Duração útil | Tipo de trabalho | Conteúdo | Motivo |
| --- | --- | --- | --- | --- |
| Quatro manhãs | 12 h | Carga cognitiva alta: teoria nova, provas, exercícios difíceis, labs de sistemas | Complemento: uma disciplina pesada por vez | É o período de maior atenção e o único que o trabalho não desgasta antes |
| Uma manhã | 3 h | Carga alta | Curso: a unidade mais exigente do semestre | Garante uma manhã para o que o curso tiver de mais difícil |
| Almoço, cinco dias | 3,75 h | Carga baixa: recordação ativa, cartões, caderno de erros | Revisão do que foi estudado de manhã e das disciplinas já fechadas | Bloco curto não serve para conteúdo novo; serve para fixar |
| Quatro noites | 10 h | Carga média: aulas, leituras, trabalhos, programação guiada | Curso: unidades do semestre | À noite, tarefas estruturadas rendem mais que teoria nova |
| Uma noite | 0 h | Folga fixa | — | Uma noite livre por semana sustenta os quatro anos |

Total: 28,75 h por semana, sendo 12 h de complemento, 13 h de curso e 3,75 h de revisão.

Por semestre de 24 semanas, o complemento soma 288 h: 240 h de disciplinas e 48 h de provas de portão e projetos.

### 16.2 Fins de semana: três cenários, nenhum obrigatório

| Cenário | Teto | Uso, nesta ordem de prioridade |
| --- | --- | --- |
| Sábado e domingo livres | 10 h, com uma tarde de descanso | 1. Recuperar atraso da semana. 2. Prova de portão ou prova mista mensal. 3. Bloco longo de projeto (PJ). 4. Antecipar disciplina adiada (16.7) |
| Só sábado | 5 h | 1. Recuperar atraso. 2. Lista de exercícios longa. 3. Projeto |
| Sem disponibilidade | 0 h | Nada a compensar: o cronograma não conta com essas horas |

Provas de portão pedem de 2 a 3 horas seguidas; quando não houver fim de semana livre no mês, a prova ocupa uma das manhãs.

### 16.3 Sequência dos oito semestres

A trilha do curso vai de Base a Avançado; a trilha do complemento segue o grafo de pré-requisitos da seção 2. As duas correm em paralelo e se encontram nos pontos marcados em 16.4.

| Semestre | Etapa | Curso: unidades | Complemento: disciplinas (cód. · h) | Portões a fechar |
| --- | --- | --- | --- | --- |
| 1 | Alicerce | U1.2 Python · U6.1 Discreta, Lógica e Matrizes · U2.1 Modelagem · U9.3 Escrita Técnica · U9.4 Colaboração | M1 60, P1 120, depois da rota crítica do nivelamento (seção 18) | M1, P1 |
| 2 | Alicerce | U2.2 SQL · U1.4 POO · U1.3 Estruturas de Dados · U3.1 Elicitação · U9.1 Ética | M3 150, G1 60, M2 30 | M3, G1 |
| 3 | Construção | U3.2 Requisitos Verificáveis · U3.3 UML, SysML e BPMN · U2.3 APIs · U7.1 Testes · U8.1 Sistemas de Informação | M2 100, M5 140 | M2 |
| 4 | Construção | U2.4 Integridade de Dados · U3.4 Do Problema ao Protótipo · U1.1 Produto Completo · U9.2 Efeitos Sociais | M5 50, C1 190 | M5 |
| 5 | Sistemas | U6.2 Probabilidade, Estatística e Otimização · U6.4 Custo de Algoritmos · U7.2 Inspeção e V&V · U8.2 Gestão de Projetos · U4.1 Memória, Processos e Redes | C1 30, P2 190, M4 20 | C1, P2 |
| 6 | Sistemas | U4.2 Segurança · U6.3 Teoria da Computação · U5.1 Estilos de Arquitetura · U5.2 Atributos de Qualidade | M4 100, M6 140 | M4 |
| 7 | Arquitetura | U4.3 Integração e Nuvem · U4.4 Testes de Integração · U5.3 Fronteira do Sistema · U7.3 Métricas | M6 30, E3 100, E4 110 | M6, E3 |
| 8 | Síntese | U5.4 Incremento Arquitetado · U8.3 DevOps · U7.4 Melhoria de Processo · U8.4 Projeto Integrado | E4 30, C5 190, margem 20 | E4, C5 |

Se a instituição fixar outra ordem para as unidades, a trilha do complemento não muda: ela depende só dos próprios portões.

### 16.4 Unidades do curso: pré-requisitos e paralelos

| Sem. | Unidade | Nível | Pré-requisitos | Em paralelo ou em apoio |
| --- | --- | --- | --- | --- |
| 1 | U1.2 Python, Dados e Desenvolvimento com IA | Base | — | P1 aprofunda nas manhãs |
| 1 | U6.1 Matemática Discreta, Lógica e Matrizes | Base | Nivelamento: NM0 a NM6, NM18 e NL1 | M1 nas manhãs |
| 1 | U2.1 Modelagem Conceitual e Relacional | Base | — | — |
| 1 | U9.3 Escrita Técnica | Base | — | Usada em todos os relatórios |
| 1 | U9.4 Colaboração e Feedback | Base | — | — |
| 2 | U2.2 SQL e Banco Físico | Base | U2.1 | — |
| 2 | U1.4 POO e Repositório | Interm. | U1.2 | — |
| 2 | U1.3 Estruturas de Dados | Interm. | U1.2, U6.1, P1 | PJ1 como trabalho da unidade |
| 2 | U3.1 Elicitação de Requisitos | Base | — | — |
| 2 | U9.1 Ética e Proteção de Dados | Base | — | — |
| 3 | U3.2 Requisitos Verificáveis | Interm. | U3.1 | — |
| 3 | U3.3 UML, SysML e BPMN | Interm. | U3.1, U1.4 | — |
| 3 | U2.3 APIs | Interm. | U2.2, U1.4 | — |
| 3 | U7.1 Testes com Automação | Interm. | U1.4 | — |
| 3 | U8.1 Sistemas de Informação | Base | — | — |
| 4 | U2.4 Integridade, Testes e Documentação de Dados | Interm. | U2.3, U7.1 | — |
| 4 | U3.4 Do Problema ao Protótipo | Interm. | U3.2, U3.3 | — |
| 4 | U1.1 Produto Completo com Scrum | Interm. | U1.4, U2.2, U3.2 | — |
| 4 | U9.2 Efeitos Sociais e Acessibilidade | Base | — | — |
| 5 | U6.2 Probabilidade, Estatística e Otimização | Interm. | U6.1, M3 | M6 completa vem no semestre 6 |
| 5 | U6.4 Custo de Algoritmos | Avanç. | U1.3, U6.1, M2 | C1 fecha no mesmo semestre |
| 5 | U7.2 Inspeção, Verificação e Validação | Interm. | U7.1, U3.2 | — |
| 5 | U8.2 Gestão de Projetos e Riscos | Interm. | U8.1, U1.1 | — |
| 5 | U4.1 Memória, Processos, Concorrência e Redes | Interm. | U1.3, G1 | P2 nas manhãs |
| 6 | U4.2 Segurança do Tráfego e Operação | Interm. | U4.1 | — |
| 6 | U6.3 Teoria da Computação, Autômatos e Grafos | Avanç. | U6.1, U6.4, M2, C1 | — |
| 6 | U5.1 Estilos e Padrões de Arquitetura | Avanç. | U2.3, U3.3, U1.1 | — |
| 6 | U5.2 Atributos de Qualidade e Decisões | Avanç. | U5.1 | — |
| 7 | U4.3 Integração com Serviços e Nuvem | Avanç. | U4.2, U2.3 | — |
| 7 | U4.4 Testes de Integração e Simulação de Falhas | Avanç. | U4.3, U7.2 | — |
| 7 | U5.3 Fronteira e Responsabilidades | Avanç. | U5.2 | — |
| 7 | U7.3 Métricas e Maturidade | Avanç. | U7.2, U8.2, U6.2 | — |
| 8 | U5.4 Incremento Arquitetado | Avanç. | U5.3, U4.4 | — |
| 8 | U8.3 DevOps e Observabilidade | Avanç. | U7.1, U4.3 | — |
| 8 | U7.4 Verificação de Incremento e Melhoria | Avanç. | U7.3 | — |
| 8 | U8.4 Projeto Integrado | Avanç. | U5.4 e U8.3 em andamento; todo o resto | Conta como PJ11 ou PJ20 se cumprir 11.2 |

Os pré-requisitos entre unidades foram deduzidos das ementas e dos níveis; a instituição pode declarar outros.

### 16.5 Disciplinas do complemento: pré-requisitos, portão de saída e o que liberam

Uma disciplina só é considerada dominada quando o portão é cumprido sem consulta e no tempo regulamentar. Sem portão cumprido, a seguinte não abre.

| Ordem | Disciplina | Pré-requisitos | Fundamento que precisa estar firme antes | Portão de saída | Libera |
| --- | --- | --- | --- | --- | --- |
| 1 | Nivelamento (seção 18) | — | Diagnóstico de cada bloco | Portão de cada um dos 28 módulos; rota crítica concluída antes do curso | M1, P1, M3, M5 e a física |
| 2 | M1 Lógica e provas | NM4, NL1 | Manipulação algébrica | 8 de 10 provas escritas corretas (indução, contradição, contrapositiva) | M2, E3 |
| 3 | P1 Programação e abstração | NL4 | Python básico da U1.2 | Programa de cerca de mil linhas com testes; exercícios de recursão sem consulta | G1, C1, P2 |
| 4 | M3 Cálculo I | NM9, NM11, NM14 | Funções, trigonometria, logaritmos | 70% em prova final antiga do MIT 18.01 | M4, M6 |
| 5 | G1 Linux e shell | P1 | — | Uma tarefa real automatizada em shell; uma semana de trabalho só no terminal | P2 |
| 6 | M2 Matemática discreta | M1, NM16 | Técnicas de prova | 70% em prova final antiga do MIT 6.042J | C1, M6 |
| 7 | M5 Álgebra linear | NM9, NM18, M1 | Sistemas lineares, notação de somatório | 70% em prova final antiga do MIT 18.06; explicação escrita da SVD | M4, e depois M7, M10 e A1 |
| 8 | C1 Algoritmos | P1, M2 | Recursão, indução, grafos | 70% em prova antiga do MIT 6.006; PJ1 concluído | C2, C8, P2 |
| 9 | P2 Programação de sistemas | P1, G1, C1 | C com ponteiros | Labs de CS:APP passando nos testes, incluindo o alocador | C5, C7, C8 |
| 10 | M4 Cálculo multivariável | M3, M5, NM15 | Derivada, integral, vetores | 70% em prova final antiga do MIT 18.02 | M6 contínua, M8, M10 |
| 11 | M6 Probabilidade | M2, M3, M4, NM17 | Contagem, séries, integral dupla | 70% em prova final antiga de Harvard Stat 110 | M7, A1, M12 |
| 12 | E3 Sistemas digitais | M1 | Álgebra booleana | PJ2: a CPU simulada executa um programa em assembly | E4 |
| 13 | E4 Arquitetura de computadores | E3, P2 | Assembly, lógica sequencial | 70% em prova antiga de Berkeley CS61C; simulador de cache funcionando | C5 |
| 14 | C5 Sistemas operacionais | P2, E4 | Processos e memória em C | Labs do xv6 passando; explicação escrita de memória virtual e escalonamento | C6, C9, G2 |

### 16.6 O que pode correr em paralelo

| Regra | Detalhe |
| --- | --- |
| No máximo duas disciplinas do complemento abertas | Uma pesada nas manhãs e, quando houver, uma leve (G1, início da seguinte) |
| Nunca duas disciplinas de prova matemática ao mesmo tempo | M2 termina antes de M5 avançar; M4 termina antes de M6 avançar |
| Pares que se reforçam | Um módulo NM com um NL, no nivelamento; M1 + U6.1; P1 + U1.2; C1 + U6.4; P2 + U4.1; E3 seguido de E4 |
| Curso e complemento em janelas separadas | Manhã para o complemento, noite para o curso; não misturar no mesmo bloco |
| Revisão é sempre paralela | O almoço cobre as disciplinas já fechadas, em rodízio |

### 16.7 O que é flexível e o que não é

| Pode mudar | Não pode mudar |
| --- | --- |
| O ritmo: uma disciplina pode levar mais semanas que o previsto | A ordem da tabela 16.5 |
| A distribuição entre manhãs, desde que a pesada fique de manhã | Abrir uma disciplina sem o portão da anterior |
| Inserir semanas de revisão ou de recuperação | Passar de duas disciplinas abertas no complemento |
| Usar ou não o fim de semana | Contar com o fim de semana para cumprir a semana |
| Trocar unidades do curso de semestre, respeitando 16.4 | A noite de folga semanal e o horário-limite à noite |

Quando um portão não é cumprido, a fila inteira do complemento desliza; nada é pulado. O curso segue o calendário da instituição. Se o curso pedir mais que 13 h em alguma semana, as horas saem primeiro do almoço e da manhã de quarta, e só depois das quatro manhãs do complemento.

### 16.8 O que fica para depois da formatura

Em relação ao Plano E com o crédito de 15.4, ficam adiadas 600 h: C7 (130), F2 (100), F1 (90), E1 (70), C3 (70), M8 (70), C2 (40), S1 (20) e S2 (10). Há dois caminhos, e os dois preservam a sequência:

- **Com fins de semana:** uma média de 3 h por semana nos fins de semana disponíveis, ao longo dos quatro anos, absorve essas 600 h e encurta o plano completo para cerca de 8 anos e meio. Ordem de antecipação: C7, C3, C2, M8, F1, F2, E1.
- **Sem fins de semana:** as 600 h entram depois da formatura, dentro da sequência da seção 17, e o plano completo fica em 9 anos.

## 17. Depois da formatura: a mesma regra de dependência até o fim do plano

As 45 disciplinas que restam depois da graduação seguem o mesmo modelo da seção 16: ordem fixa, pré-requisitos explícitos e um portão de saída por disciplina. São 3.320 h de disciplinas em dez semestres de 20 h por semana, o que leva o plano completo a 9 anos se os fins de semana não forem usados.

### 17.1 Rotina depois da formatura

| Janela | Horas por semana | Uso |
| --- | --- | --- |
| Manhãs, cinco dias | 15 | Disciplina pesada da vez: matemática, física ou teoria de sistemas |
| Almoço | 3,75 | Revisão, como antes |
| Duas noites | 5 | Labs e projetos integradores |
| Demais noites e fins de semana | 0 | Livres; fim de semana continua opcional, com as prioridades de 16.2 |

Com as noites do curso liberadas, o limite sobe para três disciplinas abertas: uma de matemática ou física, uma de sistemas e uma aplicada. A regra de nunca abrir duas de prova matemática ao mesmo tempo continua.

### 17.2 Sequência, pré-requisitos e portões

A ordem é a de estudo. Pré-requisitos com código U são unidades do curso; os demais são disciplinas do catálogo, todas já fechadas antes na fila.

| Sem. | Ordem | Disciplina (h) | Pré-requisitos | Portão de saída | Libera |
| --- | --- | --- | --- | --- | --- |
| 9 | 1 | C7 Redes (130) | P2 | Pilha TCP dos labs de Stanford CS144 passando; diagnóstico de uma captura de tráfego | C9, G2, C10, S4 |
| 9 | 2 | H6 Filosofia e história (20) | — | Ensaio de duas páginas situando uma tecnologia na história | — |
| 9 | 3 | C8 Bancos de dados (230) | C1, P2, U2.2 | Projetos de CMU 15-445 passando; prever o plano de execução de dez consultas e acertar oito | D1, C9, S4 |
| 10 | 4 | M7 Estatística (150) | M5, M6 | 70% em prova antiga do MIT 18.650; um experimento desenhado e analisado | A1, H5 |
| 10 | 5 | C3 Linguagens e paradigmas (70) | P1, M1 | PJ4: interpretador com closures | C4 |
| 10 | 6 | C2 Teoria da computação (40) | M2, C1, U6.3 | Três provas por redução corretas, de NP-completude e de indecidibilidade | C4 |
| 10 | 7 | C6 Concorrência (90) | C5, C1 | Estrutura concorrente com argumento de correção escrito, sem falha em teste de estresse | D3 |
| 10–11 | 8 | D1 Modelagem e SQL avançado (50) | C8 | Modelo dimensional de um domínio real; cinco consultas otimizadas pelo plano | D2 |
| 11 | 9 | G2 Containers e Kubernetes (60) | G1, C5, C7 | Container montado à mão com namespaces e cgroups; cluster pequeno operado | G3, S5 |
| 11 | 10 | M8 Equações diferenciais (70) | M4, M5 | 70% em prova antiga do MIT 18.03 | E6, H1, F4 |
| 11 | 11 | M9 Métodos numéricos (60) | M5, M3, P1 | Solver implementado, com análise de erro | Apoia M10 e A2 |
| 11 | 12 | M10 Otimização (110) | M4, M5 | 70% em lista de Boyd e Vandenberghe sem consulta; dois problemas formulados e resolvidos | A1, M11 |
| 11–12 | 13 | C4 Compiladores (60) | C2, C3, P2 | Compilador de linguagem pequena gera código executável | — |
| 12 | 14 | C9 Sistemas distribuídos (260) | C5, C7, C8 | Labs de MIT 6.5840 passando em execuções repetidas; cada modelo de consistência explicado com contraexemplo | D3, D4, S6, G4 |
| 12 | 15 | F1 Mecânica (90) | M3, NF3 | 70% em prova antiga do MIT 8.01 | F2, F3 |
| 13 | 16 | F2 Eletricidade e magnetismo (100) | F1, M4, NF5 | 70% em prova antiga do MIT 8.02 | E1, F4 |
| 13 | 17 | E1 Circuitos (70) | F2 | Análise de RLC no tempo e na frequência, em prova antiga do MIT 6.002 | E2, E5 |
| 13 | 18 | E2 Eletrônica (40) | E1 | Explicação escrita do inversor CMOS e de um estágio com amplificador operacional | PJ16 |
| 13 | 19 | E6 Sinais e sistemas (70) | M8, M4 | 70% em prova antiga de um curso de sinais e sistemas; filtro digital implementado | H1 |
| 13–14 | 20 | A1 Machine Learning (160) | M5, M6, M7, M10 | Regressão, árvore e SVM implementados do zero e conferidos com biblioteca; 70% em prova antiga de Stanford CS229 | A2, A5 |
| 14 | 21 | S1 Projeto de software (20) | U1.4, C1 | PJ1 revisado segundo Ousterhout, com relatório | S4 |
| 14 | 22 | S2 Testes (10) | S1, U7.1 | Testes de propriedade acrescentados a PJ1 | S5 |
| 14 | 23 | S4 Arquitetura (30) | S1, C7, C8, eixo 05 do curso | Documento de arquitetura de PJ7 com decisões e alternativas rejeitadas | S6, D6, A4 |
| 14 | 24 | G3 Cloud e IaC (40) | G2, C7 | Ambiente recriado do zero por código, com custo estimado | D6, G4 |
| 14 | 25 | D2 Arquiteturas analíticas (70) | D1 | A mesma carga em warehouse e em lakehouse, com comparação escrita | D3, D5 |
| 14 | 26 | S5 Entrega e operação (30) | S2, G1, G2, U8.3 | Serviço em produção com pipeline, SLO e alerta | D5, A5 |
| 14 | 27 | F3 Termodinâmica e ondas (30) | F1, M4, NF4 | Mapa conceitual e 80% em questionário de definições | F4 |
| 14–15 | 28 | E5 Embarcados (90) | E4, P2, E1 | PJ16: firmware com interrupções e restrição de tempo medida | H2 |
| 15 | 29 | D3 Processamento batch (100) | D2, C9, C6 | Prever o custo de um job pelo plano físico e corrigir uma assimetria | D4, D6 |
| 15 | 30 | H5 Metodologia científica (30) | M7, U9.3 | Resenha crítica de três artigos; desenho experimental revisado por alguém de fora | Pesquisa |
| 15–16 | 31 | A2 Deep Learning (150) | A1, M4 | Biblioteca própria de diferenciação automática treina uma rede; um treino com falha diagnosticado pelas curvas | A3 |
| 16 | 32 | C10 Segurança (50) | C5, C7, M2 | Modelagem de ameaças de PJ9; labs de exploração e correção concluídos | — |
| 16 | 33 | D4 Streaming e CDC (100) | D3, C9 | PJ12: log replicado com garantias de entrega explícitas | D6 |
| 16 | 34 | H1 Controle (80) | E6, M8, M5 | PID sintonizado para uma planta modelada, com análise de estabilidade | H2 |
| 17 | 35 | D5 Qualidade e governança (30) | D2, S5 | Pipeline com testes de dados, contrato e linhagem | D6, A5 |
| 17 | 36 | S6 Sistemas resilientes (40) | S4, C9 | Teste de carga com degradação controlada | D6 |
| 17 | 37 | F4 Física moderna (30) | F2, F3, M8 | Explicação escrita do transistor pela física de bandas | — |
| 17 | 38 | A3 PLN e LLMs (90) | A2 | Transformer pequeno treinado do zero | A4 |
| 17 | 39 | G4 Disponibilidade e desempenho (50) | G3, C9, C5 | Um gargalo encontrado com método, com relatório | D6 |
| 17 | 40 | M11 Pesquisa operacional (30) | M10, M6 | Um modelo de filas aplicado a um caso real | — |
| 18 | 41 | M12 Teoria da informação (40) | M6 | Entropia e limite de compressão de uma fonte calculados; explicação escrita | — |
| 18 | 42 | D6 Plataformas de dados (80) | D3, D4, D5, G3, S4 | Plataforma com SLO medido e arquitetura revisada por alguém de fora | — |
| 18 | 43 | H2 Robótica, IoT e CPS (60) | H1, E5, M6 | PJ17: sistema físico com estimação e controle | — |
| 18 | 44 | A5 MLOps (50) | A1, S5, D5 | Modelo em produção com monitoramento de desvio | — |
| 18 | 45 | A4 Sistemas de IA (60) | A3, C8, S4 | Aplicação RAG com avaliação quantitativa | — |

### 17.3 Carga por semestre

Cada semestre soma 480 h, sendo 35 h de revisão.

| Semestre | Etapa | Disciplinas (h) | Projetos (h) | Pesquisa (h) |
| --- | --- | --- | --- | --- |
| 9 | Tronco de sistemas | 380 | PJ5 reduzido (65) | — |
| 10 | Tronco de sistemas | 375 | PJ4 (70) | — |
| 11 | Matemática aplicada | 365 | PJ7 (80) | — |
| 12 | Vértice de dados | 370 | PJ7 conclusão (75) | — |
| 13 | Base física | 365 | PJ9 (80) | — |
| 14 | Vértice de IA e operação | 355 | PJ14 parte 1 (90) | — |
| 15 | Vértices | 280 | PJ16 (90) | 75 |
| 16 | Vértices | 270 | PJ12 (100) | 75 |
| 17 | Integração | 270 | PJ15, parte do transformer (100); a parte RAG fecha com o portão de A4 | 75 |
| 18 | Síntese | 290 | PJ17 (80) | 75 |

### 17.4 Cadeias críticas

São os caminhos mais longos do grafo; atraso em qualquer elo atrasa o fim da cadeia.

| Cadeia | Sequência |
| --- | --- |
| Vértice de dados | P1 → C1 → P2 → E4 → C5 → C7 → C8 → C9 → D3 → D4 → D6 |
| Vértice de IA | NM9 → NM11 → NM14 → M3 → M4 → M6 → M7 → M10 → A1 → A2 → A3 → A4 |
| Ponte física | M3 → F1 → F2 → E1 → E5 → H2, com M8 → E6 → H1 → H2 em paralelo |
| Arquitetura | Eixo 05 do curso → S4 → S6 → D6 |

As regras de 16.7 continuam valendo: o ritmo e a posição no calendário podem mudar, a ordem e os portões não.

## 18. Fase 0 — Nivelamento

Antes do plano principal, uma fase de nivelamento reconstrói a matemática do Ensino Fundamental e do Médio, a física básica e a lógica de programação. São 28 módulos em sete blocos, com no máximo 790 h. A fase parte do pressuposto de que existem lacunas, mas não as presume: cada bloco começa com um diagnóstico, e só se estuda o que ele mostrar que falta. O nivelamento substitui a antiga M0 (Pré-cálculo) e passa a ser pré-requisito das disciplinas que exigem base matemática, física ou de programação.

### 18.1 Como cada módulo é estudado

1. **Diagnóstico do bloco.** De 20 a 30 questões sobre todos os módulos do bloco, sem consulta e com tempo marcado. Com 85% ou mais nas questões de um módulo, ele vai direto para a prova de saída. Entre 60% e 84%, estudam-se só os tópicos com erro. Abaixo de 60%, o módulo inteiro.
2. **Estudo guiado.** Para cada tópico: explicação, exemplos refeitos sem olhar e exercícios dos níveis 1 (fixação) e 2 (aplicação).
3. **Aplicação.** Pelo menos três problemas de nível 3, ligados a engenharia, física, computação ou ciência de dados. O nível 4 (desafio) é opcional.
4. **Prova de saída.** Quando uma lista mista sem consulta passar de 80%. Com 80% ou mais na prova, o módulo fica concluído, ou dispensado se veio direto do diagnóstico.
5. **Revisão espaçada.** Revisões de 15 a 20 minutos, no almoço, 7, 30 e 90 dias depois do portão. Abaixo de 70%, o módulo volta para revisão.

### 18.2 Mapa dos blocos

&#91;embedded content: nivelamento · 7 blocos, 28 módulos, até 790 h\]

A aritmética (A) sustenta todo o resto. A álgebra (B) leva às funções (C), que levam à trigonometria (D) e daí à física (F). A lógica (L) e a contagem (E) saem direto da aritmética e podem correr em paralelo. A caixa de baixo mostra qual módulo libera cada disciplina do plano principal.

### 18.3 Módulos de matemática

Portão de todos: 80% na prova de saída, de 15 a 20 questões, sem consulta e sem calculadora. A ordem alterna os blocos para que a lógica de programação corra em paralelo (18.5).

| Bloco | Módulo | Pré-req. | Até (h) | Tópicos, na ordem | Aplicações |
| --- | --- | --- | --- | --- | --- |
| A · Aritmética | NM0 Operações fundamentais | — | 40 | Adição e subtração com reserva e empréstimo; tabuada; multiplicação e divisão no papel, com um e dois algarismos; quociente e resto; prova real; cálculo mental e estimativa | Troco e orçamento; bytes e pixels; dividir arquivos em partes; converter tempo |
| A · Aritmética | NM1 Números inteiros e operações | NM0 | 20 | Numeração posicional; operações com inteiros; sinais; divisibilidade, primos, MMC e MDC | Sistema binário; resto da divisão (operador %); algoritmo de Euclides |
| A | NM2 Frações e números decimais | NM1 | 25 | Equivalência e simplificação; operações; conversão entre fração e decimal; dízimas; arredondamento | Erro de ponto flutuante; proporções de misturas; leitura de medidas |
| A | NM3 Potenciação, radiciação e notação científica | NM2 | 20 | Propriedades das potências e raízes; expoente racional; racionalização; notação científica e ordem de grandeza | Potências de 2 em memória; constantes físicas; estimativas de Fermi |
| A | NM4 Expressões numéricas e algébricas | NM3 | 20 | Ordem das operações; variáveis e expressões; valor numérico; monômios e polinômios simples; simplificação | Precedência de operadores; fórmulas físicas; fórmulas de planilha |
| A | NM5 Razão, proporção, regra de três e porcentagem | NM2, NM4 | 30 | Proporção direta e inversa; regra de três simples e composta; porcentagem e variações sucessivas; juros simples e compostos | Escalas; dimensionamento de servidores; taxas de erro de modelos; variação de métricas |
| B · Álgebra | NM6 Equações, inequações e sistemas do 1º grau | NM4 | 25 | Equação do 1º grau; problemas; inequações; sistemas 2x2; interpretação gráfica | Ponto de equilíbrio entre custo e receita; encontro de móveis |
| B | NM18 Matrizes, determinantes e sistemas lineares | NM6 | 25 | Operações com matrizes; inversa; determinantes; escalonamento; discussão de sistemas | Imagens como matrizes; transformações gráficas; circuitos por malhas |
| B | NM7 Produtos notáveis e fatoração | NM4 | 20 | Quadrados, cubos e produto da soma pela diferença; fatoração; frações algébricas | Simplificar fórmulas antes de implementar; base para limites |
| B | NM8 Equações do 2º grau e redutíveis | NM6, NM7 | 25 | Fórmula resolutiva; soma e produto; biquadradas, fracionárias e irracionais | Trajetória de projéteis; área máxima; tempo de queda |
| E · Contagem | NM16 Análise combinatória | NM4 | 25 | Princípio fundamental; fatorial; permutações, arranjos e combinações; binômio de Newton | Espaço de senhas e força bruta; caminhos em grades; casos de teste |
| C · Funções | NM9 Conjuntos e funções | NM6, NM8 | 40 | Intervalos; domínio e imagem; gráficos; funções afim, quadrática e modular; composição e inversa; inequações produto e quociente | Funções de programação como mapeamentos; modelos de custo; regressão linear |
| D · Geometria | NM13 Geometria plana | NM3, NM6 | 35 | Ângulos; triângulos e semelhança; Pitágoras; polígonos; círculo; áreas e perímetros | Distância entre pontos de dados; colisão em jogos; desenho técnico |
| C | NM11 Funções exponenciais e logaritmos | NM3, NM9 | 30 | Função exponencial; logaritmo e propriedades; mudança de base; equações e inequações | Busca binária em O(log n); decibéis e pH; crescimento e decaimento; entropia |
| E | NM17 Probabilidade e estatística básica | NM5, NM16 | 30 | Espaço amostral; probabilidade clássica e condicional; independência; média, mediana, moda, variância e desvio-padrão; gráficos | Testes A/B; resumo de um conjunto de dados; taxa de falha |
| C | NM10 Polinômios e números complexos | NM7, NM9 | 25 | Operações e divisão; Briot-Ruffini; teorema do resto; relações de Girard; complexos na forma algébrica | Interpolação; detecção de erros (CRC); corrente alternada |
| C | NM12 Sequências: PA e PG | NM9, NM11 | 20 | Termo geral; soma da PA; soma finita e infinita da PG; problemas mistos | Custo de laços aninhados; vetores dinâmicos que dobram; juros compostos |
| D | NM14 Trigonometria | NM9, NM13 | 40 | Triângulo retângulo; radianos e ciclo; seno, cosseno e tangente; identidades; adição de arcos; leis dos senos e cossenos; equações | Decomposição de vetores; sinais periódicos; rotação em computação gráfica |
| D | NM15 Geometria espacial e analítica | NM9, NM13 | 35 | Áreas e volumes de sólidos; plano cartesiano; distância; equação da reta; circunferência | Volume de reservatórios; coordenadas e GPS; a reta como modelo de dados |

Total de matemática: até 530 h. O NM0 abre o bloco A reforçando as quatro operações; suas quatro listas, com 110 exercícios cada em cinco níveis, estão no repositório, em exercicios/NM0.

### 18.4 Módulos de lógica de programação e de física

Portão da lógica: 80% na prova de saída, com teste de mesa e programas escritos sem consulta. Portão da física: 80% na prova de saída, de 12 a 15 problemas, sem consulta e com calculadora científica.

| Bloco | Módulo | Pré-req. | Até (h) | Tópicos, na ordem | Aplicações |
| --- | --- | --- | --- | --- | --- |
| L · Lógica | NL1 Lógica proposicional e raciocínio | — | 20 | Proposições e conectivos; tabelas-verdade; equivalências e De Morgan; implicação; quantificadores; problemas de raciocínio | Condições em if; filtros em SQL; portas lógicas |
| L | NL2 Algoritmos e pensamento computacional | NL1 | 20 | Decomposição; pseudocódigo; fluxogramas; variáveis, tipos e atribuição; entrada e saída | Processos de negócio e procedimentos de engenharia como algoritmos |
| L | NL3 Estruturas de controle e teste de mesa | NL2, NM4 | 30 | Operadores; condicionais; laços; contadores e acumuladores; teste de mesa | Validação de entradas; simulação passo a passo; somas sobre registros |
| L | NL4 Funções, listas e primeiros programas em Python | NL3 | 35 | Funções e retorno; listas e strings; matrizes como listas; busca e ordenação simples; arquivos | Estatísticas de um CSV; fórmulas de física como funções; automações |
| F · Física | NF1 Grandezas, unidades e vetores | NM3, NM5, NM14 | 20 | Sistema Internacional; análise dimensional; algarismos significativos; vetores e decomposição | Conferir fórmulas pela dimensão; conversão de unidades em projetos |
| F | NF2 Cinemática | NF1, NM8, NM9 | 30 | MU e MUV; gráficos; queda livre e lançamentos; movimento circular | Movimento em jogos; distância de frenagem; animação |
| F | NF3 Dinâmica, trabalho e energia | NF2 | 40 | Leis de Newton; atrito, plano inclinado e polias; trabalho e potência; conservação de energia; impulso e colisões | Motores de física; eficiência de máquinas; esforços em estruturas |
| F | NF4 Termologia, ondas e óptica | NF1, NM11, NM14 | 30 | Calor e temperatura; dilatação; gases; termodinâmica básica; ondas e som; reflexão e refração | Dissipação em processadores e data centers; clock; fibra óptica |
| F | NF5 Eletricidade e magnetismo básicos | NF3, NM6, NM18 | 35 | Carga e campo; tensão; corrente e resistência; lei de Ohm; circuitos série e paralelo; potência; indução básica | Consumo de computadores; resistores e LEDs com microcontroladores; motores |

Totais: lógica até 105 h; física até 155 h.

### 18.5 Ordem de estudo, rota crítica e calendário

A ordem alterna uma trilha pesada nas manhãs (matemática, depois física) com a lógica de programação nas noites, sempre com no máximo dois módulos abertos. A **rota crítica** (NM0 a NM6, NM18 e NL1 a NL4) cobre o que as unidades do primeiro semestre do curso pressupõem, Python e Matemática Discreta, Lógica e Matrizes, e deve terminar antes delas.

Ordem completa: NM0, NM1, NL1, NM2, NL2, NM3, NM4, NL3, NM5, NM6, NL4, NM18 (fim da rota crítica), NM7, NM16, NM8, NM9, NM13, NM11, NM17, NM10, NM12, NM14, NM15, NF1, NF2, NF3, NF4, NF5.

| Cenário do diagnóstico | Horas | Antes do curso (≈ 24 h por semana) | Durante o curso (≈ 15 h por semana) |
| --- | --- | --- | --- |
| Lacunas em quase tudo | ≈ 790 | ≈ 33 semanas | ≈ 53 semanas |
| Lacunas típicas, cerca de 40% dispensado | ≈ 450 | ≈ 19 semanas | ≈ 30 semanas |
| Base razoável, cerca de 70% dispensado | ≈ 230 | ≈ 10 semanas | ≈ 15 semanas |

Antes do curso, as noites e a manhã de quarta também vão para o nivelamento. Depois que o curso começa, ele ocupa as quatro manhãs do complemento, e a contagem de semestres do complemento (seção 16) só começa quando a fase termina. A data de início do curso decide quanto do nivelamento cabe antes dele.

Os cenários acima são referências fixas. A previsão real fica no PROGRESSO.md do repositório, que recalcula as horas restantes a partir de cada diagnóstico (20%, 50% ou 100% do máximo do módulo) e projeta a data de término pelo ritmo das últimas semanas registradas. Depois do diagnóstico do bloco A, em 18/11/2026, ela aponta o cenário máximo.

### 18.6 Avaliações continuadas

Os exercícios são pedidos ao Claude ao longo de todo o estudo e registrados no repositório (`registro/avaliacoes.md`).

| Tipo | Quando | Formato | Decide |
| --- | --- | --- | --- |
| Diagnóstico | Início de cada bloco | 20 a 30 questões, sem consulta, com tempo | O que estudar em cada módulo |
| Exercícios | Durante o módulo | Listas por nível: 1 fixação, 2 aplicação, 3 contexto, 4 desafio | Quando pedir a prova de saída |
| Prova de saída | Fim do módulo | 15 a 20 questões, sem consulta, com tempo | Se o portão foi cumprido |
| Revisão | 7, 30 e 90 dias depois do portão | 5 a 10 questões mistas, de 15 a 20 minutos | Se o conteúdo continua dominado |

Modelos de pedido:

- **Diagnóstico:** "Diagnóstico do bloco A do nivelamento (NM1 a NM5): 25 questões, sem calculadora, indicando o módulo de cada questão. Gabarito separado."
- **Exercícios:** "Exercícios de NM5, nível 2, 10 questões, 3 delas com contexto de computação. Gabarito separado."
- **Prova de saída:** "Prova de saída de NM5: 15 questões, 60 minutos, sem calculadora. Gabarito separado."
- **Correção:** "Corrija minhas respostas e classifique cada erro como conceito, procedimento ou atenção."

Erro de conceito pede reestudo do tópico; erro de procedimento, mais exercícios do mesmo tipo; erro de atenção, um método de conferência.

### 18.7 Integração com o plano principal

| Disciplina do plano | Passa a depender de |
| --- | --- |
| M1 Lógica, provas e conjuntos | NM4, NL1 |
| P1 Programação e abstração | NL4 |
| M3 Cálculo I | NM9, NM11, NM14 |
| M5 Álgebra linear | NM9, NM18, M1 |
| M2 Matemática discreta | M1, NM16 |
| M4 Cálculo multivariável | M3, M5, NM15 |
| M6 Probabilidade | M2, M3, M4, NM17 |
| F1 Mecânica clássica | M3, NF3 |
| F2 Eletricidade e magnetismo | F1, M4, NF5 |
| F3 Termodinâmica e ondulatória | F1, M4, NF4 |

As tabelas 16.5 e 17.2 já trazem esses pré-requisitos. Nos planos A a F, que são alternativas genéricas, o nivelamento substitui a M0 da mesma forma.

### 18.8 Referências do nivelamento

Escritas de memória, como as da seção 10: confira as edições antes de adquirir.

| Título | Autor | Uso | Módulos |
| --- | --- | --- | --- |
| Portal da Matemática (Portal do Saber) | OBMEP | Vídeos e exercícios gratuitos do 6º ano ao Ensino Médio | Bloco A e início do B |
| Fundamentos de Matemática Elementar (11 volumes) | Gelson Iezzi, Osvaldo Dolce, Samuel Hazzan e outros | Texto principal do Ensino Médio, por volume | NM3 em diante |
| Matemática: Ciência e Aplicações | Iezzi et al. | Alternativa mais gradual que a coleção acima | Blocos B a E |
| Análise Combinatória e Probabilidade | Morgado, Carvalho, Carvalho e Fernandez (SBM) | Contagem e probabilidade com rigor | NM16, NM17 |
| Os Fundamentos da Física (3 volumes) | Ramalho, Nicolau e Toledo | Texto principal de física | NF1 a NF5 |
| Lógica de Programação | Forbellone e Eberspächer | Algoritmos e teste de mesa | NL1 a NL3 |
| Introdução à Programação com Python | Nilo Ney Coutinho Menezes | Primeiros programas | NL3, NL4 |
| Khan Academy | — | Exercícios com correção imediata | Todos os blocos de matemática |
