# Fluxo de git

O andamento do estudo e a estrutura do plano ficam em branches diferentes. Esta página é a única definição dessa regra.

| O que mudou | Branch |
| --- | --- |
| **Andamento:** `registro/` inteiro, inclusive `registro/estado.yml` (`status`, `inicio`, `diagnostico`, `nivel_atingido` e `portao` com `data`, `resultado` e `evidencia` de cada módulo), `registro/estudante.yml`, `PROGRESSO.md` e `MAPA.md` | a sua branch de estudo, `estudo_<nome>` |
| **Estrutura:** listas, gabaritos, verificações, os arquivos de `disciplinas/` inteiros (cabeçalho e texto), `catalogo/`, `scripts/`, `tests/`, skill e documentação | `main` |

A `main` é um modelo limpo, reutilizável por qualquer pessoa: não guarda resultados de estudo. Nela, `registro/` só tem os arquivos vazios (cabeçalhos das tabelas) e `PROGRESSO.md` e `MAPA.md` mostram o plano sem nada estudado. Quem estuda cria a própria branch de estudo a partir dela.

## A sua branch de estudo

Cada pessoa tem uma branch `estudo_<nome>` com um arquivo `registro/estudante.yml`:

```yaml
schema_version: 1
branch: estudo_<nome>      # o nome desta branch
github: <usuário>          # conta do GitHub que assina os commits
```

Para descobrir qual é a do estudante, no começo da sessão:

1. `git fetch origin`, liste as branches com `git branch -r --list 'origin/estudo_*'` e leia o `github` de cada uma (`git show origin/estudo_<nome>:registro/estudante.yml`).
2. Descubra a conta do GitHub da sessão, se der (por exemplo `gh api user --jq .login`).
3. Decida:
   - **Uma branch com o `github` da conta da sessão:** é ela.
   - **Não deu para saber a conta:** se houver uma branch só, confirme com o estudante ("a sua é a `estudo_<nome>`, da conta `<usuário>`?") antes de ler o andamento ou gravar; se houver várias, pergunte qual é a dele.
   - **Nenhuma branch da conta da sessão** (inclusive quando só existem branches de outras pessoas): pergunte o nome e o usuário do GitHub e, só com o sim dele, crie a branch a partir de `origin/main` (`git switch -c estudo_<nome> origin/main`), com o `registro/estudante.yml` preenchido. Ela vai para o GitHub no primeiro push que ele autorizar.
4. Use a mesma branch até o fim da sessão. Nunca leia o andamento de outra pessoa como se fosse dele, nem grave na branch de outra pessoa.

Nas regras abaixo, "branch de estudo" é essa branch.

Os cabeçalhos de `disciplinas/` não têm campos de andamento ([ADR 0004](adr/0004-separar-andamento-do-curriculo.md)): são iguais nas duas branches. A `main` não tem `registro/estado.yml`; sem ele, os scripts tratam todos os módulos como `nao_iniciada`.

## Regras

1. **Estude na sua branch de estudo.** No começo da sessão: `git fetch origin`, `git switch estudo_<nome>` e `git merge origin/main`. **Antes desse merge**, confira se algum cabeçalho de `disciplinas/` da branch de estudo ainda tem andamento (`grep -l '^status:' disciplinas/*.md`). Se tiver, faça primeiro a migração única descrita no fim desta página; sem ela, o merge dá conflito nesses cabeçalhos e o andamento se perde. `PROGRESSO.md` e `MAPA.md` com o seu andamento são os desta branch; os da `main` mostram o plano vazio e não recebem resultados.
2. **Estrutura entra na `main`** por pull request, ou direto quando o estudante pedir. Parta de `origin/main` e valide com `python scripts/progresso.py --checar`, que não reescreve `PROGRESSO.md` nem `MAPA.md`.
3. **Lista nova também é estrutura.** Leia o `MAPA.md` na branch de estudo, grave a lista numa branch criada de `origin/main` e valide com `--checar`. Ela precisa chegar à `main`, e a `main` à branch de estudo (`git merge origin/main`), antes de registrar respostas: o script recusa respostas de uma lista que não existe na branch.
4. **Nunca mescle uma branch de estudo na `main`**, nem uma branch de estudo em outra.
5. **Conflito ao trazer a `main`:** em `registro/`, `PROGRESSO.md` e `MAPA.md`, fica a versão da branch de estudo; no resto, a da `main`. Exceção: conflito num cabeçalho de `disciplinas/` com `status`, `inicio` ou `portao` quer dizer que faltou a migração única. Não resolva escolhendo a `main`, que apagaria o andamento: rode `git merge --abort` e migre antes. Depois rode `python scripts/progresso.py` para regerar `PROGRESSO.md` e `MAPA.md`.
6. **Commit e push** só quando o estudante pedir. Isso vale também para o merge da `main`, que cria um commit: se ainda não houve o pedido, peça antes.
7. **Autoria:** todo commit sai pela conta do estudante, sem assinatura do Claude. Antes do primeiro commit da sessão, leia `github` em `registro/estudante.yml` da branch de estudo e rode `git config user.name "<usuário>"` e `git config user.email "<usuário>@users.noreply.github.com"`. Vale também para commits de estrutura na `main`. Se o arquivo não existir, pergunte o usuário ao estudante antes de comitar. Não acrescente linhas `Co-Authored-By` ou `Claude-Session` na mensagem, nem rodapé de "Generated with Claude Code" em pull requests.

## Migração única da branch de estudo

Até o Marco 4, o andamento ficava no cabeçalho de `disciplinas/`. Na primeira vez que a branch de estudo for trazer uma `main` com o Marco 4, faça a migração **antes** do merge, uma vez só. São dois commits (a migração e o merge): peça o sim do estudante antes, como manda a regra 6.

```bash
git fetch origin
git switch estudo_<nome>
git show origin/main:scripts/migrar_estado.py > /tmp/migrar_estado.py
python /tmp/migrar_estado.py --raiz .
git add disciplinas registro/estado.yml
git commit -m "estudo: andamento migrado para registro/estado.yml"
git merge origin/main
python scripts/progresso.py
```

- O script tira dos cabeçalhos só as linhas dos campos de andamento e os dois comentários que as precediam, grava os valores fora do padrão em `registro/estado.yml` e confere que nada mais mudou. Rodar de novo não muda nada.
- Depois da migração, os cabeçalhos ficam iguais aos da `main`, e o merge não tem conflito neles.
- Não rode `scripts/progresso.py` entre o commit da migração e o `git merge origin/main`: o script antigo da branch espera `status` no cabeçalho e para com erro.
- Se o merge foi feito antes da migração e deu conflito, desfaça com `git merge --abort` e siga os passos acima. Nunca resolva esse conflito ficando com a versão da `main`: ela não tem o andamento. Se o merge já foi concluído sem conflito, `python scripts/progresso.py --checar` aponta cada cabeçalho com campo de andamento; rode `python scripts/migrar_estado.py` e comite.
- Na `main` a migração já foi feita com `--nao-gravar-estado`, que limpa os cabeçalhos sem criar `registro/estado.yml`.
- A migração é reversível pelo Git: antes do merge, `git revert` do commit da migração devolve os cabeçalhos como eram e tira `registro/estado.yml`. Depois do merge, a `main` já não aceita andamento no cabeçalho.
