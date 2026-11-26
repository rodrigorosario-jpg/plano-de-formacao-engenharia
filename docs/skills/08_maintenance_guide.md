# 08 · Guia de manutenção

Para quem for mudar a skill, os scripts ou os dados (inclusive a futura plataforma).

## Onde fica cada coisa

| O quê | Onde |
| --- | --- |
| Instruções da skill | `skills/estudo-guiado/SKILL.md` e `references/*.md`; a versão instalada na conta é proposta a partir daqui e guarda só o `SKILL.md`, que lê os `references/` do repositório clonado |
| Regras de dados e validação | `scripts/` (progresso, respostas, mapa, autonomia, fixação, verificação, competências, config) |
| Parâmetros | `plano.yml` (limites do mapa, autonomia, fixação) |
| Testes de código | `tests/test_*.py` (pytest, rodam no CI) |
| Casos de teste da skill | `tests/skill/` (desenvolvimento, validação e holdout por fase); `preparar_caso.py` e `coletar.py` |
| Benchmarks | `benchmark/fase-*/` (saídas brutas, avaliações cegas, chave A/B, relatórios) |
| Decisões e fundamentos | `docs/skills/` (design, plano, registro de execução, pesquisa, segurança, validação) |

## Regras de mudança

0. **Branches:** mudanças deste guia são estrutura e seguem o [fluxo de git](../fluxo-git.md).
1. **Código:** teste antes, vendo o teste falhar, e depois a implementação. `pytest -q` e `python scripts/progresso.py --checar` precisam passar.
2. **Skill:** toda mudança de comportamento entra no `CHANGELOG.md`. Mudança em regra invariável (não entregar a resposta, registro da ajuda, caminhos de gravação, commit) exige rodar de novo, no mínimo, a regressão (A-L4-01, V-03, BV-02, BV-05) com nota de pelo menos 4,5 e nenhum portão violado.
3. **Conjuntos de teste:** ajuste a skill só com os casos de desenvolvimento. A validação roda uma vez depois dos ajustes. O holdout da fase D já foi usado: uma versão nova precisa de um holdout novo.
4. **IDs de competência** nunca mudam nem são reaproveitados. O histórico de `registro/respostas.csv` depende deles.
5. **Registro:** nunca edite linhas antigas do CSV; correções entram como linhas novas (`corrige linha N`).

## Quando reavaliar

Conforme o framework (seção 10), reavalie quando:
- mudar o modelo usado no claude.ai, o formato de skills ou as ferramentas da sessão;
- surgir uma brecha nova (repita o teste de ataque da fase B);
- o estudante relatar um comportamento errado (vira um caso de teste antes da correção);
- a trilha avançar para a graduação, que precisa de novas formas de verificação (provas e projetos).

## Como rodar um benchmark

1. Para cada caso e grupo, rode `python tests/skill/preparar_caso.py <ID> <baseline|with_skill> <pasta>`.
2. Dispare executores novos (subagentes) com a mensagem do caso; cada um grava a resposta.
3. Rode `python tests/skill/coletar.py <bench> <ID> <grupo> <destino.md>` para juntar resposta, diff e `--checar`.
4. Monte os pacotes cegos (A e B sorteados, caminhos anonimizados) e dispare juízes novos com a rubrica de `tests/skill/test_cases.md`.
5. Abra a chave A/B só depois das notas; escreva o relatório com as limitações.
