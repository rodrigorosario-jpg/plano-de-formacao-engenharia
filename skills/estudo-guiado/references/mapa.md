# Modo Mapa

Lê o mapa de deficiências e propõe o próximo passo. Não calcula nada por conta própria: o `MAPA.md` é gerado por `scripts/progresso.py` a partir de `registro/respostas.csv`.

## 1. Antes de responder

Rode `python scripts/progresso.py` para garantir que o `MAPA.md` está atualizado, e leia-o junto com o `PROGRESSO.md` (seção "Agora").

## 2. Como ler as situações

| Situação | Significa |
| --- | --- |
| 🔴 fraca | Erro de conceito recente (nas 3 últimas respostas ou no dia mais recente), ou menos de 60% de acerto nas últimas respostas |
| 🟡 em_formacao | Acertando, mas ainda com ajuda ou com poucas respostas |
| 🟢 forte | Pelo menos 5 respostas recentes, 85% de acerto, 80% delas sem ajuda |
| 🟠 em_queda | Módulo já concluído que voltou a falhar |
| ⚪ sem_dados | Menos de 3 respostas |

Os limites estão em `plano.yml`; use os valores de lá se tiverem mudado.

## 3. Próximo passo, nesta ordem

1. **Lacuna em pré-requisito** (última seção do mapa): sugira voltar à competência do pré-requisito com uma lista curta antes de seguir.
2. **Competência 🟠 em_queda ou 🔴 fraca** do módulo em andamento: lista focada nela, com itens de `metodos` e `critico`.
3. **Competência 🟡 em_formacao:** lista mista com menos apoio, incluindo uma `ancora`.
4. **Tudo 🟢 forte no módulo:** propor a prova de saída (se ainda não foi feita) ou avançar de nível.
5. **Muitas ⚪ sem_dados:** propor uma lista curta de sondagem cobrindo essas competências.

Explique o porquê da sugestão em uma ou duas frases, citando a linha do mapa que a justifica. A decisão é do estudante.

## 4. O que não fazer

- Não afirme uma situação que não está no `MAPA.md`.
- Não trate `sem_dados` como fraco nem como forte.
- Não afirme a causa de uma dificuldade ("entende o conceito, mas erra o algoritmo") com menos de 5 respostas na competência; diga que são poucos dados e proponha como obter mais.
- Prefira fechar um próximo passo concreto, de preferência com uma lista que já exista no repositório, a terminar com um menu de opções. Alternativas podem vir depois, em uma linha.
- Não sugira avançar para um módulo cujos pré-requisitos não estão concluídos.
