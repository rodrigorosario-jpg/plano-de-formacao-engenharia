# 09 · Validação da fase A

Portões do [framework](framework-plano-mestre.md) (fase 15) para a skill `estudo-guiado` v0.1.2, verificados em 20/11/2026.

| Portão | Critério | Evidência | Situação |
| --- | --- | --- | --- |
| Requisitos | Rastreabilidade completa; requisitos críticos tratados | [01_requirements_traceability.md](01_requirements_traceability.md): os 4 requisitos P0 da fase A (R01 a R04) têm implementação, teste e evidência; R22 (foto) fica para a fase B, com justificativa | ✅ |
| Arquitetura | Arquitetura documentada e decisões justificadas | [design.md](design.md) §6; decisões de execução no registro do plano; [00_environment_audit.md](00_environment_audit.md) | ✅ |
| Segurança | Auditoria, testes e riscos críticos tratados | [05_security_audit.md](05_security_audit.md); casos A-L4-02 e V-04 (injeção), A-L5-02 (sem repositório), sem violação do portão E4; avaliação de expressões por lista branca de `ast`, com limites de custo | ✅ |
| Testes | Baterias básica, intermediária, avançada, adversarial e de casos-limite | 55 testes automatizados (`pytest -q`); 16 casos de desenvolvimento e 6 de validação cobrindo L1 a L5; teste de fumaça em [benchmark/fase-a/smoke.md](../../benchmark/fase-a/smoke.md) | ✅ |
| Benchmark | Baseline, skill, métricas e evidências | [benchmark/fase-a/benchmark_report.md](../../benchmark/fase-a/benchmark_report.md): saídas brutas preservadas, juízes cegos, rubrica prévia; desenvolvimento +0,01, validação +0,23; 0 portões eliminatórios | ✅ com restrições |
| Generalização | Holdout, regressões e limitações | Holdout ainda não existe (previsto para a fase D); validação feita uma única vez com casos novos | ⏳ fase D |
| Documentação | Documentação consistente e completa | README (MAPA, verificação), AVALIACOES (5 níveis, tipos de item), SKILL.md e referências, CHANGELOG, este documento | ✅ |

## Revisão independente

Revisão final do código (subagente novo, modelo mais capaz) sem achados críticos. Os achados importantes foram corrigidos com testes que falharam antes e passaram depois:

- CSV malformado passava em silêncio ou derrubava o script com traceback;
- gabarito com unidade era recusado;
- resumos parciais da mesma lista acusavam divergência falsa;
- YAML inválido derrubava o script;
- uma expressão de custo ilimitado travava a verificação;
- o mapa era zerado por uma linha inválida;
- faltava validar o número do item;
- faltava avisar que as mudanças não foram enviadas.

Os achados menores ficaram registrados para depois.

## Status

**APROVADA COM RESTRIÇÕES** para uso no nivelamento, bloco A, nos modos Exercícios, Correção e Mapa.

As restrições são:

1. **Generalização não comprovada:** sem holdout; amostra pequena, com estudante simulado e juízes do mesmo modelo.
2. **Ganho sobre o baseline modesto e indicativo** (+0,23 na validação). Boa parte da qualidade vem do próprio repositório (scripts e documentos), que ajuda com ou sem a skill.
3. **A skill ainda pode citar regras de fases futuras** (caso V-06). A fase B deve reforçar essa regra e testá-la.
4. **Correção por foto sem caso de teste real.**

## Próximo passo

Fase B do [plano](plano.md): diagnóstico por perguntas, apoio graduado, regras de autonomia, fundamentação com fontes reais e red team.


---

# Validação da fase B (20/11/2026)

Skill `estudo-guiado` v0.2.0: modo Diagnóstico, autonomia no código e competências de NM0 a NM18.

| Portão | Evidência | Situação |
| --- | --- | --- |
| Requisitos | R30 a R33 implementados e testados ([01](01_requirements_traceability.md)) | ✅ |
| Arquitetura | `references/diagnostico.md`, `scripts/autonomia.py`, decisões fundamentadas em fontes ([03](03_research_and_references.md)) | ✅ |
| Segurança | Teste de ataque com 10 tentativas; as brechas encontradas foram corrigidas, 2 delas no código com teste ([05](05_security_audit.md)) | ✅ com risco residual declarado |
| Testes | 65 testes automatizados; 12 casos de desenvolvimento e 6 de validação | ✅ |
| Benchmark | [benchmark/fase-b/benchmark_report.md](../../benchmark/fase-b/benchmark_report.md): desenvolvimento 3,93 → 4,67; validação 4,39 → 4,62; 0 portões violados com a skill | ✅ |
| Generalização | Ainda sem holdout (fase D) | ⏳ |
| Documentação | Skill, CHANGELOG 0.2.0, AVALIACOES com o portão de autonomia, teste de fumaça | ✅ |

**Status: APROVADA COM RESTRIÇÕES.** As restrições são três:
- a avaliação foi turno a turno, sem conversa livre;
- não há holdout;
- um portão marcado antes de 20/11/2026 não é conferido pelo script.


---

# Validação final · v1.0 (fases C e D, 20/11/2026)

| Portão | Evidência | Situação |
| --- | --- | --- |
| Requisitos | R30 a R38 implementados; R37 (tarefa agendada) entra só como oferta, que é o comportamento definido | ✅ |
| Arquitetura | Cinco modos; scripts de fixação, autonomia e verificação; [design](design.md), [plano](plano.md), [pesquisa](03_research_and_references.md) | ✅ |
| Segurança | Teste de ataque (fase B) e ataque combinado no holdout (H-06: 4,94, sem gravação indevida); [05](05_security_audit.md) | ✅ com risco residual declarado |
| Testes | 77 testes automatizados; 61 casos de skill nas quatro fases; regressão aprovada | ✅ |
| Benchmark | [fase C](../../benchmark/fase-c/benchmark_report.md): desenvolvimento +0,13, validação −0,02; [fase D](../../benchmark/fase-d/benchmark_report.md): holdout +0,06 | ✅ com restrições |
| Generalização | Holdout de 8 casos rodado uma vez: sem portões violados, ganho pequeno (+0,06), ganhos de profundidade e autonomia mantidos | ✅ com restrições |
| Documentação | [07 · guia de uso](07_user_guide.md), [08 · manutenção](08_maintenance_guide.md), README, CHANGELOG 1.0.0 | ✅ |

## Status final da skill estudo-guiado v1.0.0

**APROVADA COM RESTRIÇÕES.** As restrições são estas:

1. **Ganho sobre o baseline pequeno no holdout (+0,06).** O valor consistente da skill está em não violar as regras eliminatórias e na profundidade pedagógica. Boa parte do resto vem da infraestrutura do repositório, que ajuda com ou sem a skill.
2. **Achados do holdout ainda abertos.** São três: rigidez na correção de itens críticos, prioridade do próximo passo no mapa e respostas longas. Estão registrados no CHANGELOG e precisam de um holdout novo para validar a correção.
3. **Sem estudante real.** Estudante simulado e juízes do mesmo modelo. Recomendação: usar por um mês, transformar os problemas encontrados em casos de teste e reavaliar.
4. **Escopo: nivelamento.** Graduação e pós-formatura precisam de outras formas de verificação (provas formais, projetos).
