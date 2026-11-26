# Registro de débitos

Problemas conhecidos que não serão resolvidos agora. Cada débito tem um ID que não é reaproveitado. Quando um débito for resolvido, mantenha a linha e escreva na coluna "Quando tratar" a data e o pull request que o resolveram.

Origem: [auditoria de 25/11/2026](auditoria.md), seções 4 e 5, e as decisões das [ADRs](../adr/README.md).

## Currículo e conteúdo

| ID | Descrição | Impacto | Proposta | Quando tratar |
| --- | --- | --- | --- | --- |
| DT-02 | A seção 14.3 do Mapa manda começar por NM1 e NL1; o repositório começa pelo NM0 | Quem ler o Mapa pode começar pelo módulo errado | Nenhuma edição: a [cópia do Mapa](../referencia/mapa-de-formacao-rev74.md) é congelada e já lista a divergência no cabeçalho. Vale o repositório ([ADR 0001](../adr/0001-git-fonte-de-verdade.md)) | Não se trata; fica registrado |
| DT-05 | As quatro listas antigas do NM0 não têm arquivo de verificação. A exceção está registrada em `exercicios/sem-verificacao.yml` | Os itens não podem contar como âncora, e o gabarito não é conferido por script | Manter a exceção. Novas listas sempre com verificação | Só se as listas antigas voltarem a ser editadas |
| DT-06 | Competências existem só nos 28 módulos de nivelamento (156 no total). As 58 disciplinas do plano principal não têm | Essas disciplinas não podem receber respostas nem aparecer no mapa de deficiências | Definir as competências de cada disciplina antes de estudá-la, sem preencher em massa | Antes de estudar cada disciplina |

## Arquitetura

| ID | Descrição | Impacto | Proposta | Quando tratar |
| --- | --- | --- | --- | --- |
| DT-15 | Conceitos não existem como entidade, com relações entre si (complementa, contrasta, relacionado) | Não há onde guardar texto explicativo reaproveitável | Criar `conceitos/` e o modelo de conceito ([modelo](modelo.md)) | Quando houver o primeiro texto explicativo |

## Segurança e publicação

| ID | Descrição | Impacto | Proposta | Quando tratar |
| --- | --- | --- | --- | --- |
| DT-08 | A execução do campo `codigo:` em `scripts/verificar.py` tem ambiente vazio e limites de recursos, mas não é sandbox: rede, leitura do ambiente do processo pai por `/proc` e leitura e gravação de arquivos continuam possíveis | Uma verificação maliciosa poderia ler arquivos ou usar a rede, localmente ou no CI | Isolar a execução (contêiner sem rede e sem o repositório montado) ([segurança](seguranca.md)) | Antes de aceitar verificações de terceiros |

## Processo e autoria

| ID | Descrição | Impacto | Proposta | Quando tratar |
| --- | --- | --- | --- | --- |
| DT-11 | Quatro commits do PR #5 têm autor "Claude" | O histórico não fica uniforme na conta do estudante | Mantidos por decisão do estudante ([ADR 0007](../adr/0007-autoria-dos-commits.md)) | Não se trata; fica registrado |
| DT-12 | O ambiente de execução acrescenta aos pull requests um rodapé de "Generated with Claude Code" | Contraria a regra 7 do [fluxo de git](../fluxo-git.md) | Retirar o rodapé à mão a cada pull request, até o ambiente permitir desligá-lo | A cada pull request |
| DT-13 | Não há verificação para provas formais nem para projetos: o `scripts/verificar.py` confere cálculo, predicado, código e revisão | A skill não serve para as disciplinas da graduação que avaliam por prova ou projeto | Definir novas formas de verificação e reavaliar a skill ([guia de manutenção](../skills/08_maintenance_guide.md)) | Antes de a graduação usar a skill |
| DT-14 | A skill nunca foi testada com o estudante real; só com casos de benchmark | O comportamento em uso pode diferir das notas da validação | Um mês de uso real, como recomenda a validação, com cada comportamento errado virando caso de teste ([validação final](../skills/09_final_validation.md)) | No primeiro mês de estudo com a skill |
| DT-19 | A skill `estudo-guiado` 1.0.4 não conhece a NG1: pedida uma lista do módulo, ela tentaria gerar exercícios numéricos, e não sabe registrar o portão pelo laboratório ([ADR 0010](../adr/0010-disciplinas-de-git-e-guias.md)) | O estudo da NG1 com a skill pode sair do formato combinado | Versão 1.0.5: para módulos em `autonomia_por_laboratorio`, guiar pelos guias e pelo laboratório e anotar as datas do `conferir` na evidência do portão; regressão com casos novos antes de instalar | Antes de começar a NG1 com a skill |

## Resolvidos

| ID | Descrição | Como foi resolvido |
| --- | --- | --- |
| DT-16 | O diagrama do [NIVELAMENTO.md](../../NIVELAMENTO.md) era mantido à mão e omitia NM3 → NF1 e NM6 → NF5 | `scripts/diagrama.py` gera o diagrama a partir de `disciplinas/`; `progresso.py --checar` falha se ele estiver desatualizado. 25/11/2026, pull request dos Marcos 1 a 3 |
| DT-07 | O andamento (`status`, `inicio`, `diagnostico`, `nivel_atingido`, `portao.data`, `portao.resultado`, `portao.evidencia`) ainda fica no cabeçalho de `disciplinas/` | Migração por `scripts/migrar_estado.py`; andamento em `registro/estado.yml`, só na branch de estudo; schema v2 recusa andamento no cabeçalho. 25/11/2026, pull request do Marco 4 |
| DT-17 | A exigência de autonomia (5 âncoras sem ajuda em 3 dias) só aparece no texto do portão do NM0; os outros 27 módulos de nivelamento não a citam, embora a regra valha para todos desde 20/11/2026 | Linha no portão de saída dos 27 módulos, remetendo ao AVALIACOES.md, sem mudar `portao.criterio`. 26/11/2026 |
| DT-01 | O portão de NL1 a NL4 pede "exercícios de teste de mesa e programas escritos sem consulta". O texto é o mesmo nos quatro e veio do Mapa, mas NL1 é um módulo de lógica proposicional, sem programação | Decisão do estudante (26/11/2026): um critério por módulo. NL1: lógica (tabelas-verdade, equivalências, argumentos); NL2: algoritmos com teste de mesa; NL3: teste de mesa e programas com controle; NL4: programas em Python. Todos 80%, sem consulta |
| DT-18 | As 58 disciplinas fora do nivelamento terminam o portão com "cumprido sem consulta e no tempo regulamentar", inclusive quando o portão é um projeto ou documento (S4, C5) | Decisão do estudante (26/11/2026): 39 disciplinas com entrega fecham com "de forma individual, com a entrega funcionando e defendida numa explicação oral"; 8 mistas separam prova e entrega; 11 só de prova mantêm "sem consulta e no tempo regulamentar" |
| DT-03 | `M13`, `S3`, `H3` e `H4` estão no Mapa e não têm arquivo em `disciplinas/`. O projeto `PJ20` cita `S3` | Decisão do estudante (26/11/2026): não criar arquivos. `catalogo/fora-do-plano.yml` registra o motivo (S3 e H4 cobertas pelo curso, H3 em parte, M13 só no plano de 10 anos), e o `--checar` exige motivo para todo código sem arquivo |
| DT-04 | 199 dos 440 gabaritos do NM0, em geral problemas em texto, nunca foram conferidos. A auditoria conferiu por aritmética os outros 241, sem divergência | Os 440 itens das listas 1 a 4 foram conferidos por quatro agentes independentes em 26/11/2026: nenhuma resposta errada; quatro respostas completadas ([registro](../verificacao-gabaritos.md)) |
| DT-09 | O repositório não tem licença | MIT no código e CC BY 4.0 no conteúdo (26/11/2026, ADR 0008) |
| DT-10 | Há um e-mail pessoal em commits antigos (3, pela contagem da auditoria) | O público é um repositório novo, com histórico próprio e sem os commits antigos (ADR 0008); o privado mantém o histórico |
