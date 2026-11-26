# Nível 9 · Segurança e governança Git

[G5](../../disciplinas/G5-git-avancado-e-engenharia-de-versionamento.md) · [guias da G5](README.md) · [árvore](../NG1/README.md)

## 1. Objetivo

Proteger um repositório: credenciais fora do Git, identidade verificável nos commits, branch principal protegida, permissões mínimas, dependências vigiadas e um registro auditável de quem mudou o quê.

## 2. Conceitos

- **Gestão de credenciais:** como o Git se autentica no remoto: SSH com chave, ou HTTPS com o credential helper do sistema. Token nunca vai em arquivo do repositório nem na URL.
- **SSH:** par de chaves; a pública fica no GitHub, a privada só na sua máquina, protegida por senha.
- **GPG e assinatura SSH:** assinam commits e tags, provando que foi você. O GitHub mostra "Verified".
- **Secret scanning e push protection:** o GitHub procura padrões de segredos no conteúdo e, com push protection, recusa o push que traz um.
- **Branch protection e rulesets:** regras na branch principal, como exigir PR, checks e assinaturas, e proibir force push e exclusão.
- **CODEOWNERS:** revisão obrigatória por dono de caminho.
- **Privilégio mínimo:** cada pessoa, token e workflow recebe só a permissão que precisa.
- **Segurança da cadeia de suprimentos:** o que entra pelo que você não escreveu: dependências, actions de terceiros, imagens.
- **Dependabot:** alertas e PRs de atualização de dependências vulneráveis.
- **Políticas:** `SECURITY.md` (como relatar vulnerabilidade), licença, guia de contribuição.
- **Auditabilidade:** conseguir responder quem mudou o quê, quando, por quê e quem aprovou.

## 3. Explicação

O maior risco prático de um repositório pequeno não é um ataque sofisticado; é **um segredo commitado** ou **um dado pessoal publicado**. Apagar o arquivo no commit seguinte não resolve: o histórico guarda, e clones e forks já copiaram. A resposta a um segredo vazado é sempre a mesma, nesta ordem: **revogar e gerar outro**, depois limpar o histórico se fizer sentido (`git filter-repo`, com reescrita e force push combinados com todos), e por fim impedir que se repita (`.gitignore`, push protection, um hook local).

Proteção de branch transforma combinados em regras: "ninguém faz push direto na main" deixa de depender de memória. Mas o que vive nas configurações do GitHub **não está nos arquivos**: um `SECURITY.md` que fala de rulesets não liga ruleset nenhum. Documente o estado de cada configuração dizendo quem conferiu e quando.

Cada dependência e cada action de terceiro roda com as suas permissões. Fixe versões (actions pelo SHA do commit, não pela tag, que pode ser movida), dê ao `GITHUB_TOKEN` só leitura por padrão e revise o que entra.

## 4. Comandos

| Comando | Para quê |
| --- | --- |
| `ssh-keygen -t ed25519 -C "<rótulo>"` | Cria uma chave SSH |
| `git config --global gpg.format ssh` e `user.signingkey` | Assina commits com a chave SSH |
| `git commit -S`, `git tag -s` | Commit ou tag assinados |
| `git log --show-signature` | Confere assinaturas |
| `git config --global credential.helper <helper>` | Guarda credenciais HTTPS no cofre do sistema |
| `git log -p -S "<padrão>"` | Procura um texto em todo o histórico |
| `gitleaks git .` | Varre o histórico atrás de segredos (ferramenta externa) |

## 5. Sintaxe

```text
# .gitignore
.env
.env.*
!.env.exemplo
*.pem
*.key
id_ed25519*
```

```yaml
# workflow: permissões mínimas e action fixada por SHA
permissions:
  contents: read
steps:
  - uses: actions/checkout@<sha-de-40-caracteres>   # v4.x
    with:
      persist-credentials: false
```

## 6. Exemplos reais

A auditoria deste repositório em 26/11/2026 ([segurança](../../docs/arquitetura/seguranca.md)) encontrou problemas reais, nenhum deles exótico:

- um merge feito pelo site gravou o **e-mail pessoal** da conta num commit público. A correção exigiu ligar o e-mail privado na conta e recriar o repositório público;
- a primeira publicação levou **horários da rotina** e uma data pessoal no conteúdo;
- o repositório público aceitava push direto e force push na `main`.

O workflow `validar.yml` já seguia o básico: permissão só de leitura, actions fixadas por commit e checkout sem credencial persistida.

## 7. Cenários de uso

- Configurar um repositório novo de equipe no primeiro dia.
- Responder a "commitei a chave da AWS".
- Preparar um repositório privado para virar público.

## 8. Erros comuns

- **Revogar o segredo depois de limpar o histórico**, ou nunca. A ordem é revogar primeiro.
- **Chave SSH sem senha** em notebook compartilhado.
- **Achar que repositório privado dispensa cuidado:** ele pode virar público, ser clonado por um colaborador ou vazar.
- **Ruleset com bypass para todo mundo.**
- **Documentar como ativa uma proteção que só foi recomendada.**

## 9. Riscos

- `git filter-repo` e BFG reescrevem **todo** o histórico: todos os colaboradores precisam reclonar, e forks e clones antigos continuam com o segredo. Só com autorização explícita do dono.
- Assinatura de commit prova quem assinou, não que o código é bom.
- Dependabot com auto-merge pode introduzir uma dependência comprometida sem revisão.

## 10. Boas práticas

- E-mail noreply do GitHub nos commits; *Keep my email addresses private* e *Block command line pushes that expose my email* ligados na conta.
- Push protection ligado; `.gitignore` cobrindo segredos desde o primeiro commit.
- Ruleset na principal: PR obrigatório, check de CI obrigatório, sem force push nem exclusão, bypass só do administrador.
- Workflows com `permissions: contents: read` por padrão.
- Revisão periódica de quem tem acesso e de quais tokens existem.

## 11. Exercício básico

Gere uma chave SSH com senha, cadastre-a no GitHub e passe a clonar e enviar por SSH. Configure a assinatura de commits com a mesma chave e confira o "Verified" num commit.

## 12. Exercício intermediário

Num repositório de treino, commite um arquivo `.env` com um token falso, envie, e depois "conserte" apagando o arquivo. Mostre com `git log -p -S` que o token continua acessível. Escreva o plano de resposta completo, na ordem certa.

## 13. Exercício avançado

Configure no seu repositório do projeto da G5: ruleset na `main`, secret scanning com push protection, Dependabot alerts, relato privado de vulnerabilidade, `SECURITY.md` e `CODEOWNERS`. Tente um push direto e um force push na `main` e registre as recusas.

## 14. Desafio aplicado ao repositório

Só leitura:

1. Leia a auditoria em [segurança](../../docs/arquitetura/seguranca.md) e, para cada achado, diga em uma frase qual prática deste nível o teria evitado.
2. Rode `git log --format='%an <%ae>' | sort -u` no seu clone e confira quais identidades aparecem. Alguma não é noreply?
3. Leia `.github/workflows/validar.yml` e liste as três decisões de segurança dele.

> Na versão pública deste repositório o histórico tem um commit por publicação. Se for o seu caso, faça este desafio num projeto seu com histórico (veja [desafios que leem histórico](../NG1/README.md#desafios-que-leem-histórico)).

## 15. Checklist de validação

- [ ] Clono e envio por SSH, com chave protegida por senha.
- [ ] Meus commits saem assinados e com e-mail noreply.
- [ ] Sei a ordem de resposta a um segredo vazado.
- [ ] Configuro um ruleset e explico cada regra.
- [ ] Escrevo workflow com permissões mínimas e actions fixadas por SHA.
- [ ] Distingo proteção ativa de proteção documentada.

## 16. Critério de conclusão

O exercício avançado está feito, com as recusas registradas, e o plano do exercício intermediário está escrito.

## 17. Próximo módulo

[Nível 10 · GitOps, automação e CI/CD](10-automacao-e-cicd.md), ou [nível 11 · Internals](11-internals-e-escala.md), que só depende do nível 7.
