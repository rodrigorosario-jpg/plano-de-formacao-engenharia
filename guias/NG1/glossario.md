# Glossário de Git

Termos da [árvore de estudos de Git](README.md). O número entre parênteses é o nível em que o termo aparece primeiro.

| Termo | Significado |
| --- | --- |
| Amend (6) | Substituir o último commit por um novo, com outra mensagem ou outro conteúdo |
| Ancestral comum, base (4) | O commit mais recente que duas branches têm em comum; ponto de partida do three-way merge |
| Bare (5) | Repositório sem diretório de trabalho, só o `.git`; é o formato dos remotos |
| Blob (11) | Objeto que guarda o conteúdo de um arquivo, sem nome |
| Branch (1) | Nome móvel que aponta para um commit |
| Branch de rastreamento remoto (5) | `origin/main` e afins: cópia local de onde a branch remota estava no último fetch |
| Branch protection, ruleset (9) | Regras do GitHub que impedem push direto, force push ou exclusão de uma branch |
| Changelog (12) | Lista legível das mudanças de cada versão |
| Cherry-pick (6) | Aplicar numa branch as mudanças de um commit de outra |
| CODEOWNERS (8) | Arquivo que define quem revisa cada caminho do repositório |
| Commit (1) | Retrato completo do projeto, com autor, data, mensagem e pai(s) |
| Commit assinado (9) | Commit com assinatura GPG ou SSH, que prova quem o criou |
| Conflito (4) | Mesmo trecho mudado de formas diferentes nos dois lados de um merge ou rebase |
| Conventional Commits (8) | Padrão de mensagem `tipo(escopo): resumo` |
| Detached HEAD (7) | HEAD apontando direto para um commit, sem branch |
| Diretório de trabalho (1) | Os arquivos que você vê e edita |
| Fast-forward (4) | Merge em que o ponteiro só avança, sem commit novo |
| Fetch (5) | Baixar commits do remoto sem mexer nas suas branches |
| Force push (5) | Push que sobrescreve a branch remota; apaga commits que só existiam lá |
| Fork (5) | Cópia de um repositório na sua conta do GitHub |
| Garbage collection (11) | Limpeza de objetos inalcançáveis e compactação em packfiles |
| GitOps (10) | Usar um repositório Git como fonte de verdade do que está implantado |
| HEAD (1) | "Onde você está": normalmente aponta para a branch atual |
| Hook (9) | Script que o Git roda em eventos como commit e push |
| Hotfix (12) | Correção urgente de uma versão em produção |
| LFS (11) | Extensão que guarda arquivos grandes fora do repositório, com ponteiros no lugar |
| Merge (4) | Integrar o histórico de outra branch na atual |
| Monorepo (11) | Um repositório com vários projetos |
| Objeto órfão, inalcançável (7) | Commit que nenhuma branch, tag ou reflog alcança; some no gc |
| Packfile (11) | Arquivo que guarda muitos objetos comprimidos, com deltas |
| Pull (5) | Fetch seguido de integração na branch atual |
| Pull request (8) | Pedido, no GitHub, para integrar uma branch em outra, com revisão e checks |
| Push (5) | Enviar commits e mover a branch no remoto |
| Rebase (6) | Reaplicar commits em cima de outra base, gerando commits novos |
| Reflog (7) | Diário local de para onde HEAD e as branches apontaram |
| Release (8) | Versão publicada, associada a uma tag |
| Remoto (5) | Outro repositório com um apelido, como `origin` |
| Reset (7) | Mover a branch atual para outro commit, com efeito opcional no staging e na pasta |
| Revert (7) | Commit novo que desfaz as mudanças de um commit anterior |
| SemVer (8) | Versão `MAIOR.MENOR.CORREÇÃO`, em que cada parte diz o tipo de mudança |
| SHA, hash (1) | Identificador de um objeto, calculado a partir do conteúdo |
| Sparse checkout (11) | Ter na pasta só parte dos arquivos do repositório |
| Squash (6) | Juntar vários commits num só |
| Staging, índice (1) | Rascunho do próximo commit |
| Stash (7) | Guardar mudanças não commitadas numa pilha, para recuperar depois |
| Submodule (11) | Repositório dentro de outro, fixado num commit |
| Tag (8) | Nome fixo para um commit, usado em versões |
| Three-way merge (4) | Merge que compara base e as duas pontas e gera commit de merge |
| Tracking branch (5) | Branch local configurada para acompanhar uma remota |
| Tree (11) | Objeto que representa uma pasta: nomes, permissões e ponteiros para blobs e trees |
| Trunk-based (12) | Estratégia com branches curtíssimas integradas na principal várias vezes por dia |
| Upstream (5) | O repositório original de um fork; também a remota que uma branch acompanha |
| Worktree (11) | Segundo diretório de trabalho ligado ao mesmo repositório |
