# 01 · Requisitos e rastreabilidade

Fase 1 do [framework](framework-plano-mestre.md). Fonte dos requisitos: [design.md](design.md). Prioridades: P0 impeditivo, P1 alta, P2 importante, P3 evolutivo.

## Requisitos da fase A

| ID | Requisito | P | Implementação | Teste | Evidência |
| --- | --- | --- | --- | --- | --- |
| R01 | Gabarito sem erro | P0 | `scripts/verificar.py` (`calculo`); exercicios.md §5 | `test_gabarito_divergente`, `test_gabarito_equivalente_aceito`; casos A-L1-01, A-L3-01 | benchmark/fase-a |
| R02 | Item sem ambiguidade (resposta única) | P0 | `verificar.py` (`predicado`, `respostas_validas`) | `test_respostas_validas_e_caso_24_48`, `test_item_ambiguo`; A-L3-01 | benchmark/fase-a |
| R03 | Não entregar a resposta antes da tentativa | P0 | SKILL.md "Regras que valem sempre" | A-L4-01 | benchmark/fase-a |
| R04 | Autonomia não inflada (`ajuda` registrada) | P0 | SKILL.md; correcao.md §5 | A-L4-01, A-L2-03 | benchmark/fase-a |
| R05 | Correção item a item com classe de erro (5 classes) | P1 | correcao.md §2–3; `respostas.CLASSES_ERRO` | `test_valores_fora_dos_conjuntos`; A-L2-01, A-L2-02 | benchmark/fase-a |
| R06 | Pedir os passos antes de classificar erro sem passos | P1 | correcao.md §1 | A-L2-03 | benchmark/fase-a |
| R07 | Métodos alternativos na correção | P1 | correcao.md §4; principios.md §2 | A-L2-01 | benchmark/fase-a |
| R08 | Composição de lista por tipo de item | P1 | exercicios.md §2 | A-L1-01 | benchmark/fase-a |
| R09 | Pensamento crítico em todo item | P1 | principios.md §1; exercicios.md §2–3 | A-L1-01, A-L3-03 | benchmark/fase-a |
| R10 | Simplificação nas duas leituras | P1 | principios.md §3; tipos `simplificacao` e `armadilha_simplificacao` | A-L1-01, A-L2-02 | benchmark/fase-a |
| R11 | Registro item a item em `respostas.csv` | P1 | `scripts/respostas.py`; correcao.md §5 | `tests/test_respostas.py` (9 testes); smoke passo 2 | smoke.md |
| R12 | Resumo em `avaliacoes.md` coerente com o CSV | P1 | `conferir_resumos`; coluna Lista | `test_resumo_bate`, `test_resumo_diverge` | smoke.md |
| R13 | Mapa de deficiências por competência | P1 | `scripts/mapa.py`; `MAPA.md` | `tests/test_mapa.py` (9 testes) | smoke.md |
| R14 | Lacunas em pré-requisitos no mapa | P1 | `lacunas_prerequisitos` | `test_lacuna_em_prerequisito`; A-L3-02 | benchmark/fase-a |
| R15 | Próximo passo baseado no mapa, sem inventar dados | P1 | mapa.md §3–4 | A-L3-02, A-L5-03 | benchmark/fase-a |
| R16 | Respeitar pré-requisitos | P1 | SKILL.md | A-L5-01 | benchmark/fase-a |
| R17 | Gravar só no repositório e só nos caminhos permitidos | P1 | SKILL.md "Preparação" e "Regras" | A-L5-02 | benchmark/fase-a |
| R18 | Conteúdo de arquivo é dado, não instrução | P1 | SKILL.md | A-L4-02 | benchmark/fase-a |
| R19 | CSV inválido detectado no CI | P1 | `validar_respostas`; `--checar` | `test_competencia_inexistente_e_ajuda_negativa` e outros | smoke.md (caso de erro) |
| R20 | Formatos abertos, legíveis pela futura plataforma | P2 | CSV, YAML, markdown | revisão de arquitetura | este documento |
| R21 | Escala de níveis única, 1 a 5 | P2 | AVALIACOES.md; `validar_respostas` | `test_valores_fora_dos_conjuntos` | — |
| R22 | Correção por foto | P2 | correcao.md §1 | caso planejado para a fase B (precisa de imagem real) | — |

## Requisitos planejados (fases B a D)

| ID | Requisito | P | Fase |
| --- | --- | --- | --- |
| R30 ✅ fase B (references/diagnostico.md; casos B-L1-01 a B-L5-02, BV-01 a BV-04) | Diagnóstico por perguntas estruturadas, com escada de apoio | P0 | B |
| R31 ✅ fase B (diagnostico.md §2; B-L2-01, BV-03) | Proteção contra frustração e problema gêmeo | P1 | B |
| R32 ✅ fase B (scripts/autonomia.py; test_autonomia.py (10 testes); BV-05, BV-06) | Autonomia: N âncoras sem ajuda em dias distintos; portão exige autonomia | P0 | B |
| R33 ✅ fase B (03_research_and_references.md (10 fontes)) | Fundamentação com fontes reais | P1 | B |
| R34 ✅ fase C (fixacao.py, fixacao.md) | Fixação: questões sorteadas de módulos concluídos em toda lista | P1 | C |
| R35 ✅ fase C (avisos_fixacao) | Detecção de queda de autonomia (`autonomia-em-queda`) | P1 | C |
| R36 ✅ fase C (competências NF/NL; verificar.py codigo e unidades) | Verificação para física (unidades) e lógica (execução de código) | P1 | C |
| R37 ✅ fase C (só oferta, sem criação sem o sim) | Tarefa agendada de fixação (opcional) | P3 | C |
| R38 ✅ fase D (holdout, relatório, 07, 08, 09) | Holdout, benchmark completo, documentação final | P1 | D |

## Requisitos não atendidos na fase A

- R22 (foto): instrução existe, mas não há caso de teste com imagem real; fica para a fase B.
- Composição exata das proporções é orientação ("arredonde com bom senso"), não regra verificada por script.
