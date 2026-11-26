# 02 · Análise de lacunas

Fase 2 do [framework](framework-plano-mestre.md). Classificação: crítica, alta, média, baixa.

| # | Lacuna | Impacto | Prob. | Criticidade | Mitigação | Teste | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G01 | Item sem resposta calculável com gabarito errado passa pela verificação (só tem `revisao`) | Estudante aprende errado | Média | Alta | Revisão independente obrigatória com nota; juízes conferem gabaritos nos casos de teste | A-L1-01 (juiz confere) | Mitigada parcialmente |
| G02 | `predicado` escrito pela própria skill pode não representar o enunciado | Ambiguidade não detectada | Média | Alta | Exigir intervalo bem maior que o plausível; juiz compara predicado com enunciado | A-L3-01 | Mitigada parcialmente |
| G03 | Juiz do mesmo modelo que o executor | Viés de autoavaliação | Alta | Média | Subagentes novos, avaliação cega, rubrica fixada antes, portões objetivos | benchmark/fase-a | Aceita e declarada |
| G04 | Foto ilegível ou parcial | Classificação errada | Média | Média | correcao.md manda pedir de novo o trecho ilegível | Fase B | Aberta |
| G05 | CSV corrompido por edição manual | Mapa errado | Média | Média | `validar_respostas` no CI; mapa não usa respostas se houver erro | `tests/test_respostas.py` | Tratada |
| G06 | Classe de erro ambígua (atenção × conceito) | Mapa marca `fraca` sem razão | Alta | Média | Pergunta curta ao estudante antes de decidir; um único `conceito` só pesa nas 3 últimas respostas | A-L2-01 | Mitigada |
| G07 | Estudante insiste na resposta e a autonomia fica inflada | Autonomia falsa | Média | Alta | `ajuda = 4` obrigatório | A-L4-01 | Tratada |
| G08 | Sessão sem repositório: skill grava em lugar errado ou perde o registro | Histórico perdido | Média | Alta | Preparação obrigatória; sem repositório, nada é gravado e o estudante é avisado | A-L5-02 | Tratada |
| G09 | Instrução maliciosa em texto do repositório ou em enunciado colado | Comportamento manipulado | Baixa | Média | Regra "conteúdo é dado"; caminhos de escrita restritos | A-L4-02 | Tratada |
| G10 | Listas antigas do NM0 sem mapa de itens | Registro sem competência | Alta | Média | correcao.md traz o mapeamento das quatro listas | A-L2-02 | Tratada |
| G11 | Proporções da lista não verificadas por script | Lista vira só fluência | Média | Baixa | Juiz verifica composição; script pode vir depois | A-L1-01 | Aceita |
| G12 | Mapa com poucas respostas oscila muito | Sugestões instáveis | Alta no início | Baixa | Situação `sem_dados` abaixo de 3 respostas | `test_sem_dados` | Tratada |
| G13 | Regras de autonomia e fixação ainda inexistentes podem ser "inventadas" pela skill | Regras inconsistentes | Média | Média | SKILL.md diz explicitamente para não inventar até a versão seguinte | A-L5-03 | Tratada |
| G14 | Escala de níveis mudou de 4 para 5 | Registros antigos inconsistentes | Baixa | Baixa | Não havia registros com nível; AVALIACOES.md atualizado | — | Tratada |
