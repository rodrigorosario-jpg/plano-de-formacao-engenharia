# 00 · Inspeção do ambiente

Fase 0 do [framework](framework-plano-mestre.md), feita em 19/11/2026 para a skill `estudo-guiado`.

## Onde a skill roda

| Item | Situação |
| --- | --- |
| Plataforma | claude.ai, projeto "Estudos", sessão com ferramentas de código (terminal Linux, Python 3, git) |
| Repositório | `rodrigorosario-jpg/plano-de-estudos`, privado, branch `main` (hoje: [fluxo de git](../fluxo-git.md)); anexado à sessão com escrita. Em sessão nova precisa ser anexado e clonado |
| Dependências | Python 3.12+, PyYAML, pytest (`requirements.txt`) |
| Instalação da skill | Pelo cartão de proposta de skill do claude.ai; a fonte versionada fica em `skills/estudo-guiado/` |
| CI | GitHub Actions: `pytest -q` e `progresso.py --checar` a cada push |

## Capacidades disponíveis

- **Subagentes independentes:** sim (ferramenta de agentes). Usados para revisão do design, execução de baseline e com skill, e juízes.
- **Busca na web:** sim. Necessária na fase B (fundamentação em ciências da aprendizagem).
- **Leitura de imagens:** sim; correção a partir de foto é possível.
- **Tarefas agendadas:** a ferramenta existe, mas não foi testada; a fase C decide.
- **Memória entre conversas:** existe, mas a skill não depende dela: o estado vive no repositório.

## Materiais preexistentes preservados

- 86 arquivos de disciplina com frontmatter (status, portões, pré-requisitos), sem alteração de semântica; NM0 a NM5 ganharam `competencias`.
- `registro/avaliacoes.md` com 5 linhas de diagnóstico; ganhou a coluna opcional Lista (linhas antigas com a célula vazia).
- Quatro listas do NM0 (110 itens cada) e seus gabaritos, intocados.
- `scripts/progresso.py`: comportamento anterior mantido; recebeu validações e a geração do `MAPA.md`.

## Limitações registradas

1. **Juízes do mesmo modelo** que executa a skill: risco de viés de autoavaliação, mitigado por subagentes novos, avaliação cega e rubrica fixada antes.
2. **Estudante simulado** nos testes: respostas com erros plantados não reproduzem toda a variedade de um estudante real.
3. **Amostra pequena** na fase A: sem afirmação de significância estatística.
4. **Sem execução real de prompts com e sem skill no mesmo contexto de produto:** o baseline roda num subagente sem as instruções da skill, o que aproxima, mas não é idêntico, ao uso no claude.ai.
5. **Commits** só quando o estudante pede; o trabalho da fase A fica numa branch local até lá.
