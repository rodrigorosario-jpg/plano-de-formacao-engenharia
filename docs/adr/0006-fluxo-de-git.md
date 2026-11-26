# ADR 0006 · Fluxo de git: andamento e estrutura em branches diferentes

- **Status:** Aceita
- **Data:** 25/11/2026

## Contexto

Enquanto o andamento morar no cabeçalho das disciplinas ([ADR 0004](0004-separar-andamento-do-curriculo.md)), a branch de estudo e a `main` divergem nos mesmos arquivos. A [auditoria de 25/11/2026](../arquitetura/auditoria.md) encontrou que a regra de branches não estava escrita, nem no repositório nem na skill: uma sessão sem esse contexto podia gravar progresso na `main`. Os registros de estudo mais recentes existiam só na branch `estudo_rodrigorosario`.

## Decisão

1. **Andamento** vai na branch `estudo_rodrigorosario`: `registro/`, os campos de andamento do cabeçalho de `disciplinas/` (menos `portao.criterio`), `PROGRESSO.md` e `MAPA.md`.
2. **Estrutura** vai na `main`, por pull request: listas, gabaritos, verificações, texto e demais campos das disciplinas, `catalogo/`, `scripts/`, `tests/`, a skill e a documentação. Pode entrar direto quando o estudante pedir.
3. `estudo_rodrigorosario` nunca é mesclada na `main`. A `main` é trazida para a branch de estudo com `git merge origin/main`.
4. Mudança de estrutura que altera uma decisão vem com uma ADR nova no mesmo pull request.
5. A definição completa e única da regra, com o que fazer em conflito, está em [docs/fluxo-git.md](../fluxo-git.md). Esta ADR registra a decisão; não a repete em detalhe.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Tudo na `main` | Mistura dados de quem estuda com o currículo e arrisca sobrescrever registros |
| Branch de estudo como fonte de tudo | A estrutura ficaria sem revisão por pull request e sem uma base limpa para outros consumidores |
| Regra só na memória das sessões | Foi o que causou o achado da auditoria |

## Consequências

- A skill 1.0.2 e o [guia de manutenção](../skills/08_maintenance_guide.md) seguem a regra.
- Lista nova é estrutura: precisa chegar à `main`, e a `main` à branch de estudo, antes de registrar respostas.
- `PROGRESSO.md` e `MAPA.md` da `main` são cópias antigas; não se regeram lá. Na `main`, só `python scripts/progresso.py --checar`.
- Quando a [ADR 0004](0004-separar-andamento-do-curriculo.md) for implementada, a regra fica mais simples: o andamento passa a ser só `registro/`.

## Revisão de 26/11/2026

A `main` virou modelo limpo, reutilizável por outras pessoas. A branch de estudo deixa de ter nome fixo: cada pessoa tem a sua, `estudo_<nome>`, identificada por `registro/estudante.yml` (branch e conta do GitHub que assina os commits). A skill descobre a branch pela conta do GitHub da sessão (sem como saber, confirma com o estudante; nenhuma dele, oferece criar) e nunca grava na de outra pessoa. A `estudo_rodrigorosario` continua sendo a do Rodrigo.
