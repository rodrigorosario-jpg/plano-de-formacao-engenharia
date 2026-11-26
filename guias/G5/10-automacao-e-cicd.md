# Nível 10 · GitOps, automação e CI/CD

[G5](../../disciplinas/G5-git-avancado-e-engenharia-de-versionamento.md) · [guias da G5](README.md) · [árvore](../NG1/README.md)

## 1. Objetivo

Fazer do repositório a fonte de verdade: cada mudança validada automaticamente, releases geradas a partir do histórico e implantações (e rollbacks) disparadas e registradas pelo Git.

## 2. Conceitos

- **Git como fonte de verdade:** o que está implantado é o que está numa branch ou tag; mudar a produção é mudar o repositório.
- **CI (integração contínua):** cada push e cada PR rodam build, testes e verificações.
- **CD (entrega e implantação contínuas):** o que passa na CI fica pronto para implantar (entrega) ou é implantado sozinho (implantação).
- **GitHub Actions:** workflows em YAML em `.github/workflows/`, disparados por eventos (`push`, `pull_request`, `schedule`, `workflow_dispatch`, `release`).
- **Pipeline:** a sequência de jobs e passos.
- **Artefato:** o produto de um build (pacote, imagem, binário), versionado e guardado.
- **Ambiente:** destino de implantação (homologação, produção), com segredos e regras de aprovação próprios.
- **Fluxo de aprovação:** revisão humana obrigatória antes de um ambiente protegido.
- **GitOps:** um agente no ambiente compara o estado real com o descrito no repositório e corrige a diferença.
- **Infraestrutura como código (IaC):** servidores, redes e permissões descritos em arquivos versionados (Terraform, OpenTofu, Pulumi).
- **Release automatizada:** versão, changelog e tag gerados a partir dos commits (Conventional Commits, nível 8).
- **Rollback:** voltar à versão anterior, por revert ou reimplantando a tag anterior.

## 3. Explicação

Um bom pipeline é rápido, determinístico e tem o mínimo de permissão. Rápido, porque ninguém espera 40 minutos por um PR de documentação. Determinístico, porque um teste que falha "às vezes" ensina a ignorar a CI. Mínimo de permissão, porque o workflow roda código do PR e, se tiver token de escrita e segredos, um PR malicioso os usa.

O evento importa. `pull_request` vindo de fork roda sem segredos e com token só de leitura: é seguro para rodar testes. `pull_request_target` roda no contexto do repositório de destino, com segredos e escrita; se ele fizer checkout do código do PR e rodar, você entregou as chaves. Outra armadilha é a **injeção de comandos**: `run: echo "${{ github.event.pull_request.title }}"` deixa o título do PR virar shell. Passe valores por variável de ambiente.

No GitOps, o rollback é um `git revert` no repositório de configuração: o agente vê o commit e reconcilia. A trilha de auditoria é o próprio histórico.

## 4. Comandos

| Comando ou recurso | Para quê |
| --- | --- |
| `.github/workflows/*.yml` | Define os workflows |
| `gh workflow run <nome>` | Dispara um `workflow_dispatch` |
| `gh run list`, `gh run view --log` | Acompanha execuções |
| `environment:` no job | Usa um ambiente com regras e segredos próprios |
| `concurrency:` | Evita duas implantações simultâneas |
| `git revert` + push | Rollback rastreável |

## 5. Sintaxe

```yaml
name: validar
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: validar-${{ github.ref }}
  cancel-in-progress: true
jobs:
  testes:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@<sha>
        with: {persist-credentials: false}
      - uses: actions/setup-python@<sha>
        with: {python-version: "3.12", cache: pip}
      - run: pip install -r requirements.txt
      - run: python -m pytest -q
      - env:
          TITULO: ${{ github.event.pull_request.title }}   # nunca interpolado direto no run
        run: printf '%s\n' "$TITULO"
```

## 6. Exemplos reais

- O `validar.yml` deste repositório roda `pytest` e `progresso.py --checar` em todo PR, com permissão só de leitura.
- A publicação para o repositório público é um script (`scripts/publicar.sh`) que confere a árvore antes de enviar: recusa dado de estudo na `main` e e-mail que não seja noreply. É uma automação com guardas, disparada por decisão humana, não um deploy automático.
- Rollback por GitOps: o commit `feat: réplicas 3 → 5` deu problema; `git revert <sha>` e o agente volta a 3.

## 7. Cenários de uso

- Impedir merge de PR que quebra os testes (CI + ruleset do nível 9).
- Publicar uma release com changelog quando uma tag `v*` é enviada.
- Manter a infraestrutura de um projeto em Terraform revisada por PR.

## 8. Erros comuns

- **Actions fixadas por tag** (`@v4`), que o autor pode mover.
- **`permissions` ausente:** o padrão do repositório pode ser escrita.
- **Segredo impresso no log** por um `set -x` ou `echo` de depuração.
- **Pipeline que só roda na `main`:** o erro aparece depois do merge.
- **Deploy sem `concurrency`:** duas implantações se atropelam.

## 9. Riscos

- `pull_request_target` com checkout do código do PR: execução de código de terceiros com segredos.
- Artefatos e caches guardados com dados sensíveis ficam baixáveis por quem tem acesso ao repositório.
- Download e execução de scripts externos (`curl ... | bash`) no pipeline: confira o hash ou fixe a versão.
- Implantação automática em produção sem fluxo de aprovação.

## 10. Boas práticas

- `permissions: contents: read` no topo; escrita só no job que precisa.
- Actions por SHA, e o Dependabot do ecossistema `github-actions` para atualizá-las.
- `persist-credentials: false` no checkout.
- `timeout-minutes` em todo job.
- Ambientes protegidos com aprovação para produção.
- Toda mudança de produção passa por commit, PR e revisão.

## 11. Exercício básico

No repositório do projeto da G5, crie um workflow que roda os testes em `pull_request` e em push na `main`, com permissões mínimas e actions por SHA. Abra um PR que quebra um teste e veja o check vermelho.

## 12. Exercício intermediário

Escreva um workflow vulnerável a injeção (título do PR interpolado no `run`) num repositório de treino, abra um PR com o título `"; echo INJETADO; "` e mostre a injeção no log. Corrija passando por variável de ambiente e mostre que o texto passa a ser só texto.

## 13. Exercício avançado

Automatize releases: em push de tag `v*`, um workflow gera as notas a partir dos commits desde a tag anterior e cria a release no GitHub. O job que escreve tem `contents: write`; os outros, só leitura.

## 14. Desafio aplicado ao repositório

Só leitura:

1. Leia `.github/workflows/validar.yml` e, no repositório de origem, `.github/dependabot.yml` (o espelho público não leva este arquivo; o motivo está no [ADR 0009](../../docs/adr/0009-espelho-publico-e-publicacao-por-pr.md)) e desenhe o pipeline: eventos, jobs, passos e permissões.
2. Leia `scripts/publicar.sh` e liste todas as condições em que ele se recusa a publicar. Para cada uma, diga que risco ela evita.
3. Proponha, por escrito, um job que rode `scripts/publicar.sh` sem `--enviar` em todo PR, como verificação. Que permissão ele precisaria? Por que não deveria ter o token de escrita do repositório público?

## 15. Checklist de validação

- [ ] Escrevo um workflow de CI com permissões mínimas, actions por SHA e timeout.
- [ ] Explico a diferença entre `pull_request` e `pull_request_target`.
- [ ] Reconheço e corrijo injeção de expressões no `run`.
- [ ] Automatizo uma release a partir de tags.
- [ ] Explico GitOps e rollback por revert.

## 16. Critério de conclusão

O repositório do projeto da G5 tem CI obrigatória por ruleset e releases automatizadas por tag, e o exercício intermediário está documentado.

## 17. Próximo módulo

[Nível 11 · Internals e repositórios grandes](11-internals-e-escala.md), ou direto ao [nível 12](12-engenharia-de-versionamento.md) se o 11 já foi feito.
