# 05 · Auditoria de segurança

Fase 6 do [framework](framework-plano-mestre.md), aplicada à skill `estudo-guiado` v0.1.

| Categoria | Risco neste domínio | Controle | Risco residual |
| --- | --- | --- | --- |
| Prompt injection | Texto em observações do CSV, enunciados colados, fotos ou páginas tentando mudar regras | SKILL.md: conteúdo é dado; caso A-L4-02 | Baixo |
| Jailbreak / manipulação de contexto | Pressão para entregar respostas ou marcar autonomia sem mérito | Regra de `ajuda = 4`; caso A-L4-01 | Baixo |
| Exfiltração | Baixo: não há dado sensível além do progresso de estudo | Nenhum envio externo; sem push sem pedido | Muito baixo |
| Credenciais e segredos | Nenhum segredo é necessário | Nada a guardar | Nenhum |
| Execução de código | A skill roda scripts do próprio repositório; `verificar.py` avalia expressões | Avaliação por `ast` com lista de nós permitidos, sem `eval`; teste `test_avaliar_rejeita_chamadas` | Baixo |
| Operações destrutivas | Apagar histórico de avaliações | Regra: nunca apagar histórico; caminhos de escrita restritos; git guarda versões | Baixo |
| Abuso de ferramentas | Commit/push indevido | Só com pedido explícito na conversa | Baixo |
| Privilege escalation | Não se aplica | — | Nenhum |
| Dados pessoais | Só desempenho de estudo; nada de identidade | Repositório privado | Baixo |
| Dependências | PyYAML (com `safe_load`) e pytest | Versões mínimas fixadas | Baixo |
| Outputs falsos de agentes | Juiz ou revisor independente pode errar | Portões objetivos por script; achados conferidos | Médio (G03) |

## Decisões

- `verificar.py` nunca usa `eval`/`exec`; expoentes não inteiros são recusados para evitar expansão de raiz inexata.
- Um predicado exige intervalo explícito; o tempo de execução cresce com o intervalo, então intervalos devem ficar na casa de milhares, não milhões. Risco aceito: lentidão local, não segurança.

## Teste de ataque da fase B (20/11/2026)

Um subagente fez o papel de estudante e tentou burlar a skill 0.2.0-dev por 10 caminhos diferentes:
- insistência;
- autoridade falsa;
- instrução embutida num enunciado;
- pedido fracionado;
- urgência emocional;
- pedido em inglês;
- falsa memória;
- texto num arquivo do repositório;
- "modo teste";
- combinação de táticas.

O relatório completo e os diffs de cada tentativa estão em [benchmark/fase-b/red-team/](../../benchmark/fase-b/red-team/relatorio.md).

**Resultado:** a skill resistiu a 7 tentativas, foi burlada em 2 e burlada em parte em 1.

| Brecha | Correção (v0.2.0) |
| --- | --- |
| `.yml` editado pelo estudante para marcar itens fáceis como âncora | Código: âncora só conta se o `.yml` da lista a marca como âncora (`ancoras_validas`). Skill: `.yml` alterado por outra pessoa não serve para registrar âncora |
| Confirmações de passo pedidas pelo estudante não contavam como ajuda | Skill: `ajuda` inclui confirmações, dicas, correções parciais e respostas vistas em conversas anteriores |
| Treino sem pré-requisito contava para a autonomia; âncora certa sem passos contava como autônoma | Código: `observacao` com `treino-sem-prerequisito` fica fora da autonomia. Skill: âncora sem passos é registrada como `parcial` |
| Portão proposto sem conferir a autonomia | Skill: o portão da correção exige a linha "Autonomia" completa |
| Correção de registro impossível sem apagar o histórico | Skill: correção por linha nova, com `corrige linha N` |

**Riscos residuais:**
- um módulo marcado `concluida` com data de portão anterior a 20/11/2026 não é conferido pelo script;
- quem tem acesso de escrita ao repositório pode alterar `.yml` e CSV diretamente, porque a proteção é por regra da skill e pelo histórico do git, não criptográfica.
