# Plano de estudos — engenheiro generalista

Registro e motor de uma formação de cerca de 9 anos: uma fase de nivelamento (matemática do Fundamental e do Médio, física básica, lógica de programação), 4 anos de graduação em Engenharia de Software com estudo complementar e 5 anos de estudo próprio. São 28 módulos de nivelamento e 58 disciplinas, cada um com pré-requisitos e um portão de saída que comprova o domínio.

O objetivo não é cumprir conteúdo: é chegar a resolver problemas complexos sozinho, e continuar resolvendo até o fim da trilha. Por isso o plano mede autonomia, mapeia deficiências a partir dos erros e volta a cobrar o que já foi concluído.

| Para ver | Abra |
| --- | --- |
| Onde estou agora e onde estou fraco | `PROGRESSO.md` e `MAPA.md` da sua branch de estudo, `estudo_<nome>` ([como criar a sua](docs/fluxo-git.md)); na `main` eles mostram o plano vazio |
| Eixos, unidades, projetos e escalas | [catalogo/](catalogo/README.md) |
| Arquitetura, decisões e débitos | [docs/arquitetura/](docs/arquitetura/README.md) e [ADRs](docs/adr/README.md) |
| Modelos para criar disciplina, lista ou conceito | [templates/](templates/README.md) |
| Em qual branch cada coisa vai | [Fluxo de git](docs/fluxo-git.md) |
| O documento de origem do plano (cópia congelada) | [Mapa de Formação](docs/referencia/mapa-de-formacao-rev74.md) |
| Como estudar com a skill no dia a dia | [Guia de uso](docs/skills/07_user_guide.md) |
| Como funcionam diagnósticos, níveis, provas e revisões | [AVALIACOES.md](AVALIACOES.md) |
| O que o nivelamento cobre | [NIVELAMENTO.md](NIVELAMENTO.md) |

## Começar

```bash
pip install -r requirements.txt
python scripts/progresso.py --checar   # só valida
python scripts/progresso.py            # na branch de estudo: valida e regera PROGRESSO.md e MAPA.md
```

Depois, numa conversa do projeto "Estudos" no claude.ai, peça a primeira lista: *"Lista de NM0, adição, 12 itens"*.

## O ciclo de estudo

O estudo do dia a dia passa pela skill [estudo-guiado](skills/estudo-guiado/SKILL.md), que trabalha sobre os arquivos deste repositório:

```
lista de exercícios → correção → mapa de deficiências → perguntas até a lacuna → próxima lista
                                         ↑
                    fixação: questões de módulos já concluídos voltam sempre
```

| Modo | Peça algo como | O que acontece |
| --- | --- | --- |
| Exercícios | "Lista de NM2, frações, 12 itens" | Lista mista e verificada, com gabarito separado: fluência, dois métodos, simplificação, armadilhas, pensamento crítico, âncora e fixação |
| Correção | "Corrige a lista 3: 1) 7/8, 2) …" ou foto da folha | Correção item a item, com o tipo de cada erro e outros jeitos de resolver; registro em `respostas.csv` |
| Diagnóstico | "Não entendi onde errei no item 3" | Perguntas, uma por vez, até você mesmo achar a lacuna |
| Mapa | "Onde estou fraco?", "o que faço hoje?" | Leitura do `MAPA.md` e um próximo passo concreto |
| Fixação | "O que preciso revisar?" | Avisos de queda e de fixação vencida, mais uma revisão curta |

No começo a skill ajuda bastante para não gerar frustração; as provas de portão mantêm todos os critérios. Para fechar um módulo do nivelamento são necessários **80% na prova de saída e 5 problemas-âncora resolvidos sem ajuda em 3 dias diferentes** (valores em `plano.yml`).

## Rotina

**A cada sessão:** a skill registra as respostas e pergunta se pode fazer o commit. Diga sim, senão o registro se perde.

**Toda semana:** uma linha em `registro/semanal.md` com as horas por disciplina (`NM3: 6, NL1: 4,5`). Cada avaliação vai para `registro/avaliacoes.md`.

**Ao longo de uma disciplina**, o andamento fica em `registro/estado.yml`, só na branch de estudo, com uma linha por módulo que já saiu do padrão:

```yaml
schema_version: 1
modulos:
  NM0: {status: em_andamento, inicio: 2026-01-05}
  NM1: {diagnostico: 0}
```

Módulo que não aparece está no padrão: `status: nao_iniciada` e demais campos nulos. O `status` segue este caminho:

```
nao_iniciada → em_andamento → no_portao → concluida (ou dispensada, se o diagnóstico permitiu pular)
                                              ↓
                                          em_revisao  (prova mista abaixo de 70%)
```

- Ao abrir: `status: em_andamento` e `inicio`.
- Depois do diagnóstico do bloco: `diagnostico` (% de acertos no módulo).
- Ao passar no portão: `portao` com `data`, `resultado` e `evidencia` (link para a prova corrigida, o repositório ou o relatório), e `nivel_atingido`.
- A cada etapa: `semestre_atual` em `plano.yml` (0 no nivelamento). Na formatura, `limite_abertas: 3`.

Depois de mudar o andamento, rode o script e commite junto o `PROGRESSO.md` e o `MAPA.md` regerados, na branch de estudo ([fluxo de git](docs/fluxo-git.md)).

## O que o script verifica

`scripts/progresso.py` sai com código 1 quando encontra erro, e a verificação do GitHub Actions falha no commit. `Liberada` e `Bloqueada` não são escritos à mão: o script os calcula.

**Plano**
- Nenhuma disciplina sai de `nao_iniciada` antes de os pré-requisitos estarem `concluida`, `dispensada` ou `em_revisao`, nem está planejada para começar antes do fim deles.
- Nenhuma dependência circular, em nenhuma etapa.
- Nenhum link interno quebrado em arquivos `.md`.
- Cabeçalhos, catálogo, verificações e `plano.yml` validam nos [schemas](schemas/README.md); nenhum código de disciplina repetido.
- Unidades (`requer_unidades`, `unidades_relacionadas`), projetos (`PJ<n>`) e eixos citados existem no [catálogo](catalogo/README.md); código aposentado não volta a ser usado.
- O diagrama do `NIVELAMENTO.md` está igual ao gerado por `scripts/diagrama.py`.

**Portões e autonomia**
- Disciplina concluída ou dispensada precisa de data e resultado do portão.
- Módulos do nivelamento com portão a partir de 20/11/2026 precisam da autonomia exigida; só contam âncoras confirmadas no `.yml` da lista e respondidas fora de treino.

**Registros**
- Só códigos, tipos de avaliação e competências existentes.
- `respostas.csv` com colunas, codificação e números de item válidos; uma linha inválida fica fora do mapa até ser corrigida, e as demais continuam valendo.
- O resumo em `avaliacoes.md` bate com a soma das respostas do mesmo dia e da mesma lista.

**Exercícios**
- Toda lista tem gabarito com a mesma numeração, e cada item do gabarito é conferido de forma independente ([como](docs/verificacao-gabaritos.md)).
- Toda lista tem `.yml` de verificação ou está registrada como exceção em `exercicios/sem-verificacao.yml`.
- A escala de dificuldade de `AVALIACOES.md` bate com `catalogo/escalas.yml`.

**Avisos** (não falham a validação)
- Módulo de nivelamento concluído com resultado do portão abaixo de 80%.
- Mais disciplinas abertas que o limite; horas reais 50% acima das previstas; revisão abaixo de 70% sem `em_revisao`.
- `autonomia-em-queda`, `fixacao-vencida` (competência de módulo concluído sem prática há 30 dias) e `sem-intercalacao` (3 itens seguidos da mesma competência numa lista).

O `PROGRESSO.md` também lista as revisões espaçadas vencidas (7, 30 e 90 dias depois do portão) e prevê o fim do nivelamento pelo ritmo real das últimas semanas.

### Comandos

```bash
python scripts/progresso.py                     # valida e regera PROGRESSO.md e MAPA.md
python scripts/progresso.py --checar            # só valida (é o que o CI roda)
python scripts/progresso.py --sortear-fixacao 4 # sorteia 4 competências de módulos concluídos para fixação
python scripts/diagrama.py                      # regera o diagrama do NIVELAMENTO.md
python scripts/qualidade.py                     # relatório dos critérios do Knowledge Core
pytest -q                                       # testes dos scripts
```

## Estrutura do repositório

```
disciplinas/            módulos de nivelamento (NM, NF, NL) e disciplinas do plano: cabeçalho YAML + conteúdo
exercicios/<código>/    listas, gabaritos/ e verificacao/ (como conferir cada item)
registro/               semanal.md, avaliacoes.md, respostas.csv, diagnosticos/ e estado.yml (andamento, só na branch de estudo)
catalogo/               eixos, unidades, projetos, códigos aposentados e escalas
schemas/                JSON Schema de cabeçalhos, catálogo, verificações, plano.yml e estado.yml
templates/              modelos de disciplina, módulo, lista, gabarito, verificação e conceito
plano.yml               etapa atual, limite de disciplinas abertas e parâmetros de mapa, autonomia e fixação
scripts/                progresso.py e os módulos que ele usa (mapa, autonomia, fixação, verificação)
tests/                  testes dos scripts; tests/skill/ tem os casos de avaliação da skill
skills/estudo-guiado/   a skill de estudo guiado
docs/fluxo-git.md       em qual branch cada mudança vai
docs/arquitetura/       visão, modelo, segurança, roadmap, débitos e a auditoria
docs/adr/               uma decisão de arquitetura por arquivo
docs/referencia/        cópia congelada do Mapa de Formação
docs/skills/            design, plano, validação e guias de uso e manutenção da skill
benchmark/              saídas e avaliações das fases de construção da skill
PROGRESSO.md, MAPA.md   gerados pelo script; não editar à mão
```

**Arquivo de disciplina.** O cabeçalho YAML é só o plano (semestre, horas previstas, nível-alvo, pré-requisitos, `competencias`, `portao.criterio`) e só muda num replanejamento. O andamento (`status`, `inicio`, `diagnostico`, `nivel_atingido`, `portao.data`, `portao.resultado`, `portao.evidencia`) fica em `registro/estado.yml`, na branch de estudo; o schema recusa esses campos no cabeçalho. O corpo traz os tópicos na ordem, a referência principal, a competência ao concluir, o portão de saída e anotações livres.

**IDs de competência** (`NM1.c03`) nunca mudam nem são reaproveitados: o histórico do `respostas.csv` depende deles.

**MAPA.md.** Para cada competência, a situação sobre as últimas respostas: 🔴 fraca, 🟡 em formação, 🟢 forte, 🟠 em queda (módulo concluído que voltou a falhar) ou ⚪ sem dados. Cada módulo mostra a linha de autonomia, e a última seção aponta lacunas prováveis em pré-requisitos.

## Para manter

- Mudanças na skill: [guia de manutenção](docs/skills/08_maintenance_guide.md), com o processo de versão e avaliação.
- Estado e restrições da versão atual: [validação final](docs/skills/09_final_validation.md).
- Decisões de projeto: [design](docs/skills/design.md).

## Fonte

O plano completo, com cronograma por semestre, metodologia, bibliografia e projetos integradores, está no documento *Mapa de Formação — Engenheiro Generalista Polímata*. As seções 16, 17 e 18 correspondem a este repositório.

## Licença

Código (`scripts/`, `tests/`, `schemas/`, `.github/`) sob [MIT](LICENSE); conteúdo sob [CC BY 4.0](LICENSE-CONTEUDO.md). Como a versão pública é publicada: [docs/publicacao.md](docs/publicacao.md).
