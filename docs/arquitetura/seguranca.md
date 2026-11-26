# Segurança

Threat model do Knowledge Core e do motor de estudo, princípios para o consumo por IA, regras para exemplos de código e para o CI, a auditoria de hardening do repositório público e o estado das configurações do GitHub. Atualiza a seção 6 da [auditoria de 25/11/2026](auditoria.md). A auditoria de segurança da skill, de 20/11/2026, está em [docs/skills/05_security_audit.md](../skills/05_security_audit.md).

## Contexto

- Repositório privado, de um estudante só, com um espelho público que recebe só a árvore da `main` ([ADR 0008](../adr/0008-repositorio-publico-separado.md), [ADR 0009](../adr/0009-espelho-publico-e-publicacao-por-pr.md)). Quem escreve nele é o estudante, diretamente ou por uma sessão do Claude a pedido dele.
- Não há segredos, servidor, banco de dados nem dados de terceiros.
- Há execução de código: `scripts/verificar.py` roda o campo `codigo:` dos arquivos de verificação, localmente e no CI a cada push ou pull request.
- Há um consumidor de IA: a skill `estudo-guiado` lê os arquivos do repositório numa sessão do Claude.

## Threat model (STRIDE)

| Ameaça | Onde | Mitigação atual | Proposta | Risco residual |
| --- | --- | --- | --- | --- |
| **Falsificação de identidade e de autoria** | Commits | Histórico Git; commits pela conta do estudante ([ADR 0007](../adr/0007-autoria-dos-commits.md)) | Assinatura de commits, se houver mais de um autor | Baixo |
| **Adulteração: inflar a autonomia** | `.yml` de verificação e `registro/respostas.csv`, editáveis por quem tem acesso de escrita | Âncora só conta se o `.yml` da lista a marca; a skill não usa `.yml` alterado por outra mão; itens das listas antigas do NM0 nunca contam como âncora; correção de registro só por linha nova; histórico Git | Schema e validações do Marco 3 | Aceitável para uso pessoal: a proteção é por regra e histórico, não criptográfica |
| **Adulteração: gabarito errado** | Listas e gabaritos | Toda lista nova tem verificação independente, rodada por `--checar`; gabarito divergente ou item ambíguo falha a validação | Exceções registradas em `exercicios/sem-verificacao.yml` | Baixo nas listas novas; as listas antigas do NM0 não têm verificação (débito DT-05) |
| **Adulteração: cadeia de suprimentos** | Dependências Python e actions do GitHub | Poucas dependências; PyYAML com `safe_load` | Dependências com versão exata; actions fixadas por commit; permissões mínimas no workflow | Baixo |
| **Repúdio** | Commits e registros | Histórico Git; o CSV só cresce | — | Baixo |
| **Exposição de informação** | Publicação do repositório | Espelho com histórico próprio; `publicar.sh` recusa dado de estudo, e-mail que não seja noreply e identidade local que não seja noreply; e-mail privado na conta | Configurações do GitHub abaixo | Baixo |
| **Negação de serviço** | Expressões, intervalos e código das verificações | Avaliação sem `eval`, com limite de potência; intervalos de no máximo 1.000.000 de valores; tempo máximo de 5 s e limites de recursos para o código | — | Muito baixo |
| **Elevação de privilégio: código arbitrário** | `scripts/verificar.py` executa o campo `codigo:` | Ver a seção abaixo: processo isolado do ambiente e com limites, mas não é sandbox | Sandbox de verdade (sem rede e sem acesso ao sistema de arquivos) antes de aceitar verificações de terceiros | Baixo hoje, alto se houver terceiros |
| **Elevação de privilégio: injeção por conteúdo** | Material do Core lido por IA | A skill trata conteúdo como dado; o teste de ataque de 20/11/2026 corrigiu as brechas achadas | Princípios da seção seguinte | Baixo |

## Execução do campo `codigo:`

Itens de lógica de programação são conferidos executando o código de referência e comparando a saída com o gabarito ([verificação dos gabaritos](../verificacao-gabaritos.md)). Hoje o código roda:

- num processo Python separado, com `python -I`;
- com ambiente vazio: não herda variáveis do processo que chamou (mas, como roda com o mesmo usuário, ainda consegue ler o ambiente dele em `/proc/<pid>/environ` no Linux);
- com stdin fechado;
- com limites de tempo de CPU, memória, tamanho de arquivo gravado e número de arquivos abertos, além do tempo máximo de 5 s;
- numa pasta temporária;
- com o grupo de processos morto ao terminar, para não deixar processos filhos vivos (um filho que chame `setsid` escapa).

**Isso não é sandbox.** O processo ainda pode abrir conexões de rede, ler o ambiente do processo pai e ler ou gravar qualquer arquivo que o usuário que roda o script alcance, inclusive o próprio repositório. Os limites contêm acidentes e laços infinitos; não contêm código malicioso.

Regra: **só aceite verificações escritas por terceiros (pull requests, contribuições, arquivos colados) depois de isolar a execução**, por exemplo num contêiner sem rede e sem montagem do repositório. Até lá, todo `.yml` com `codigo:` é escrito pelo estudante ou pela skill, numa sessão dele.

No espelho público, um PR de fork roda o CI, e o CI roda o `codigo:` do PR. Isso acontece numa máquina descartável do GitHub, com token só de leitura e sem segredos, e o workflow de PR de fora só deve rodar depois da aprovação do dono (checklist abaixo). O que não se faz: baixar o PR e rodar `--checar` ou `pytest` na própria máquina. A mudança é lida, refeita no privado e só então executada.

## Laboratório de Git

`scripts/laboratorio_git.py` roda `git` na máquina de quem estuda, para preparar e conferir os cenários da NG1 ([ADR 0010](../adr/0010-disciplinas-de-git-e-guias.md)).

- **Os cenários são código do script.** Nada vem de YAML, do conteúdo do repositório nem da rede.
- **Só pastas vazias ou novas**, fora deste repositório e de qualquer outro repositório Git. O script não apaga arquivos: o clone auxiliar do nível 5 vive num `tempfile.TemporaryDirectory`. Há um teste que recusa `rmtree`, `remove` e `unlink` no código.
- **Git isolado:** sem configuração global e de sistema, com `core.hooksPath=/dev/null`, sem fsmonitor e com `protocol.allow=never` (só `file` liberado). O remoto do nível 5 é um repositório bare local.
- **Limite:** `conferir` lê um repositório que quem estuda controla. Se ele mesmo puser um filtro malicioso no `.gitattributes` e na configuração local, o `git status` o executa. É a própria máquina e a própria pasta, então o risco é aceito e está documentado no script.

## Material do Core é conteúdo, não instrução

Quando uma IA consome o Knowledge Core (a skill hoje; uma aplicação ou plataforma depois), valem quatro princípios:

1. **Material nunca concede permissão.** Texto de uma disciplina, lista, gabarito, verificação, CSV ou documento não muda regras, não autoriza commit, push, gravação fora dos caminhos permitidos nem mudança de status. Permissão vem só do estudante, na conversa. Texto que tente isso é ignorado e mostrado ao estudante.
2. **O consumidor de IA lê, mas não executa exemplos.** Código dentro de material de estudo é exemplo para ler. Só o motor de estudo executa código, e só pelo caminho controlado de `scripts/verificar.py`.
3. **Cada trecho carrega origem e status de revisão.** Um trecho do Core diz de onde veio (arquivo, revisão do Mapa, commit) e se foi conferido (verificação por script, revisão independente, releitura ou nenhuma). O consumidor diferencia material conferido de material não conferido.
4. **Dados do estudante ficam fora do índice de conhecimento.** Respostas, avaliações, diagnósticos, horas e andamento (`registro/`, inclusive `registro/estado.yml`) não entram em nenhum índice, busca ou contexto de IA que sirva ao conhecimento. Um consumidor que precise deles lê de propósito, do contexto "dados de quem estuda" ([visão](visao.md)).

## Exemplos de código no material

Ainda não há exemplos de código nas disciplinas. Quando houver, cada exemplo:

- declara contexto, ambiente, dependências, requisitos, como executar, riscos e limitações;
- não é executado automaticamente, nem pelo CI nem por consumidor de IA, sem isolamento;
- não traz segredos, tokens, endereços internos ou dados pessoais, nem como exemplo;
- não baixa nem executa nada da rede ao rodar;
- é distinto do campo `codigo:` das verificações, que é o único código que o motor executa.

## CI

- Permissões mínimas no workflow: só leitura do conteúdo, nada além do que os passos usam.
- Actions fixadas pelo hash do commit, não por tag.
- Dependências com versão exata em `requirements.txt`, incluindo `jsonschema` ([ADR 0005](../adr/0005-json-schema-versionado.md)).
- O CI só valida e testa: não publica, não faz push e não usa segredos.
- `actions/checkout` com `persist-credentials: false`: o token não fica gravado no clone do job.
- Execuções antigas da mesma ref são canceladas (`concurrency`) e o job tem limite de 10 minutos.
- Sem Gitleaks, Semgrep ou Trivy: o secret scanning do GitHub com bloqueio no push já cobre segredos, não há contêiner e o código Python é pequeno e testado. CodeQL entra pelo *default setup* do GitHub, sem workflow próprio.

## Auditoria de hardening de 26/11/2026

Feita no repositório público logo depois da primeira publicação, sobre o conteúdo, o histórico, os workflows e as configurações do GitHub. Nenhum segredo, token ou chave foi encontrado no conteúdo. Os testes e o `--checar` passavam.

| # | Achado | Criticidade | Tratamento |
| --- | --- | --- | --- |
| H-01 | O merge do PR do Dependabot, feito pelo site, saiu com o e-mail pessoal da conta | Crítica | Apagar e recriar o repositório público vazio, com o e-mail privado ligado na conta; `publicar.sh` recusa identidade que não seja noreply ([ADR 0009](../adr/0009-espelho-publico-e-publicacao-por-pr.md)) |
| H-02 | O primeiro commit público trazia os horários da rotina e a data real de início do NM0 | Alta | Corrigido na `main` (PR #18) antes da republicação no repositório recriado |
| H-03 | O público tinha um commit que o privado não tinha (`pyyaml` 6.0.4); a publicação seguinte o desfaria | Alta | Bump trazido ao privado; o script recusa publicar se o espelho divergiu |
| H-04 | O `dependabot.yml` ia junto e o Dependabot abriria PRs no espelho | Média | O script tira o arquivo da árvore publicada |
| H-05 | A `main` pública sem proteção: aceitava force push, exclusão e push direto | Média | Ruleset (checklist abaixo) |
| H-06 | Relato privado de vulnerabilidade, alertas do Dependabot e CodeQL desligados | Média | Checklist abaixo |
| H-07 | Faltavam `SECURITY.md`, `CONTRIBUTING.md`, código de conduta e templates de issue e PR | Baixa | Criados |
| H-08 | `.gitignore` não cobria `.env`, chaves e certificados | Baixa | Revisado; nenhum arquivo rastreado passou a ser ignorado |
| H-09 | Wiki e Projects ligados sem uso; branch órfã do Dependabot no público | Baixa | A branch some com a recriação; Wiki e Projects no checklist |
| H-10 | Permissões padrão do Actions e aprovação de PRs de fora não puderam ser lidas (a API foi recusada) | Não verificado | Conferir no checklist |

**O que não mudou, de propósito:** a arquitetura do Core, o workflow `validar.yml` (já tinha permissão só de leitura, actions fixadas por commit e checkout sem credencial) e a estrutura de documentação.

**Riscos que continuam:**

- `scripts/verificar.py` não é sandbox; seguro só com verificações escritas pelo dono (seção acima).
- Dependências sem hash em `requirements.txt`: uma versão exata republicada com outro conteúdo passaria. Aceitável com três dependências conhecidas; revisar se crescerem.
- O histórico do repositório **privado** ainda tem o e-mail pessoal em commits antigos (DT-10). Não vaza enquanto ele for privado, porque o público não recebe esse histórico.

## Configuração do GitHub

Estas proteções vivem nas configurações do GitHub, não em arquivos. **Documentado não é o mesmo que ativado:** a coluna Estado diz o que foi conferido, por quem e quando. Os passos estão em [publicação](../publicacao.md#configuração-do-repositório-público).

| Item | Onde | Estado |
| --- | --- | --- |
| E-mail privado e bloqueio de push com e-mail | Conta → Settings → Emails | Pedido ao dono em 26/11/2026 |
| Ruleset na `main`: PR, check `validar`, sem force push nem exclusão, bypass do dono | Repositório → Rules | Recomendado |
| Só *Rebase and merge*; apagar branches mescladas | Repositório → General | Recomendado |
| Wiki e Projects desligados | Repositório → General | Recomendado |
| Secret scanning com push protection | Code security | Ligado no repositório anterior (verificado pela API em 26/11/2026) |
| Relato privado de vulnerabilidade | Code security | Recomendado |
| Dependabot alerts; security updates desligado | Code security | Recomendado |
| CodeQL (default setup) | Code security | Recomendado |
| Workflow permissions só leitura; aprovação para PRs de fora | Actions → General | Não verificado |
