# SDD ledger — plan: docs/skills/plano.md
Spec: docs/skills/design.md
Setup: Ruling: trabalho na branch local skills/fase-a, sem commits — o estudante só autoriza commit quando pedir — custo se errado: commits feitos depois em lote.
Pre-flight:
- T3 consome competencias(disc) de T1: assinatura bate.
- T4 estende carregar_avaliacoes (progresso.py) e usa linhas de T3: bate.
- T5 consome carregar_config (T2), carregar_respostas (T3), competencias (T1): bate.
- T7 consome formatos de T1–T6: bate.
Task 1: complete (sem commit; tests: pytest -q → 5 passed; --checar rc=0)
Task 2: complete (sem commit; tests: pytest -q → 7 passed; --checar rc=0)
Task 3: complete (sem commit; tests: pytest -q → 17 passed; caso de erro do design: --checar rc=1 com 2 csv-invalido)
Task 4: complete (sem commit; tests: pytest -q → 21 passed; --checar rc=0)
Task 5: Ruling: com erros no CSV, o MAPA.md é gerado sem respostas e o script avisa — evita mapa calculado sobre dado inválido — custo se errado: mapa vazio até corrigir o CSV.
Task 5: complete (sem commit; tests: pytest -q → 31 passed; MAPA.md gerado com 33 competências sem_dados)
Task 6: Ruling: gabarito lido da tabela '| N | resposta |' (formato real do NM0), além de 'N. resposta' do plano — o plano supunha outro formato — custo se errado: nenhum, os dois são aceitos.
Task 6: Ruling: normalizar trata '1.000' como mil e ',' como decimal (padrão brasileiro); nas expressões de calculo vale a sintaxe Python (ponto decimal) — custo se errado: gabarito com '3.5' lido como 3,5.
Task 6: complete (sem commit; tests: pytest -q → 42 passed; --checar rc=0)
Task 7: Ruling: mapa de itens (competencia, tipo_item, nivel) fica no .yml de verificação, não numa tabela no gabarito — uma tabela '| N |' extra quebraria listas_sem_gabarito e ler_gabarito — custo se errado: nenhum funcional.
Task 7: complete (sem commit; tests: pytest -q → 43 passed; SKILL.md 41 linhas; links checados pelo --checar rc=0)
Task 8: complete (00, 01, 02, 05 escritos; P0/P1 da fase A com implementação e teste apontados)
Task 9: complete (16 casos dev, 6 validação, rubrica e portões fixados antes; fixtures verificados)
Task 9: Ruling: corrigida a regra do MAPA — só descarta respostas quando há csv-invalido (antes qualquer erro, inclusive de pré-requisito, zerava o mapa) — achado ao preparar A-L3-02 — teste test_mapa_usa_respostas_quando_erro_nao_e_do_csv RED→GREEN
Task 10: Ruling: executores em 4 lotes de 4 casos por grupo (8 subagentes), cada caso em cópia isolada — 32 subagentes seria custo desproporcional — custo se errado: leve contaminação entre casos do mesmo lote, declarada no relatório.
Task 11: Ruling: 'erro de conceito recente' = nas 3 últimas respostas OU em qualquer resposta do dia mais recente — numa mesma lista a ordem dos itens escondia o erro (achado no smoke) — teste test_conceito_na_mesma_sessao_conta_como_recente RED→GREEN — custo se errado: competência marcada fraca por um dia a mais.
Task 10: Ruling: links_quebrados ignora benchmark/ e .superpowers/ — saídas brutas preservadas citam caminhos de outras cópias — test_links_ignoram_saidas_brutas_do_benchmark RED→GREEN.
Task 10: complete (16 dev + 6 validação; juízes cegos; relatório benchmark/fase-a/benchmark_report.md; dev +0,01, validação +0,23, 0 portões)
Final: fixed coluna a mais / aspa aberta / Latin-1 viram csv-invalido — test_coluna_a_mais..., test_aspa_nao_fechada..., test_csv_em_latin1... RED→GREEN, suite 55/55
Final: fixed gabarito com unidade, %, R$ e − unicode — test_normalizar_tira_unidade_e_porcentagem RED→GREEN, suite 55/55
Final: fixed resumos da mesma lista no mesmo dia somados — test_dois_resumos_mesma_lista_mesmo_dia_somam RED→GREEN, suite 55/55
Final: fixed YAML malformado e predicado inválido viram gabarito-divergente — test_yaml_malformado_nao_derruba RED→GREEN, suite 55/55
Final: fixed limites de expoente e intervalo (antes 9**9**9 travava) — test_intervalo_e_expoente_limitados RED (travou) → GREEN, suite 55/55
Final: fixed mapa descarta só linhas inválidas do CSV — test_mapa_descarta_so_linhas_invalidas RED→GREEN, suite 55/55
Final: fixed item do CSV validado como inteiro ≥ 1 — test_item_deve_ser_inteiro_positivo RED→GREEN, suite 55/55
Final: Ruling: item não é conferido contra a numeração do gabarito — exigiria acoplar respostas.py ao formato das listas; inteiro ≥1 já pega o erro comum — custo se errado: item 999 passa sem aviso.
Final: fixed (doc) aviso de não-commit ao encerrar; IDs nunca reaproveitados; tabela de listas permitida; regra única de data — skill 0.1.2.
Final: minor (deferred): _logico acessível no predicado; normalizar("0.750") = 750 e "2, 3 e 5" vira número; MAPA muda a data todo dia; CSV de 0 bytes dá "cabeçalho difere"; datas futuras aceitas; competência sem id dá traceback; linhas do CSV sem resumo não avisam.
Task 11: complete (smoke OK; 09_final_validation APROVADA COM RESTRIÇÕES; skill proposta pelo cartão; tests: pytest -q → 55 passed; --checar rc=0)
B1: complete (tests: pytest -q → 63 passed; --checar rc=0)
B4: complete (13 módulos, 79 competências; --checar rc=0)
B3: complete (diagnostico.md, roteamento, registro/diagnosticos; --checar rc=0)
B2, B5, B6: complete (10 fontes; dev 3,93→4,67; validação 4,39→4,62; red team 7/10 resistiu, brechas corrigidas; 65 testes; skill 0.2.0)
C, D: complete (fase C dev +0,13, val −0,02, regressão OK; holdout +0,06; skill 1.0.0 APROVADA COM RESTRIÇÕES; 77 testes)
