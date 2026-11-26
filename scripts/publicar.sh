#!/usr/bin/env bash
# Publica a árvore da main deste repositório (privado) no repositório público, que é só um espelho.
# Uso: scripts/publicar.sh <remoto-publico> [--enviar]
#
# Sem --enviar, só mostra o que seria publicado. O histórico privado nunca vai junto (ADR 0008).
# Com --enviar:
#   - público vazio: envia o commit direto para a main (primeira publicação, antes do ruleset);
#   - público com main: envia para a branch publicacao/<sha> e abre um pull request, porque a
#     main pública exige PR e o CI passando (ADR 0009). O dono mescla com "Rebase and merge".
#
# Recusa publicar se:
#   - a main tiver dado de estudo (registro/estado.yml, registro/estudante.yml, resultados);
#   - a árvore tiver um e-mail que não seja noreply/exemplo;
#   - a identidade do git local não for um e-mail noreply do GitHub;
#   - o público tiver mudanças que não vieram de uma publicação (o espelho divergiu).
set -euo pipefail

remoto="${1:?informe o remoto do repositório público}"
enviar="${2:-}"
# Arquivos da main que não vão para o espelho: o Dependabot roda só no privado.
excluir=(.github/dependabot.yml)
prefixo="Publica a main privada"

erro() { echo "ERRO: $*" >&2; exit 1; }

git fetch -q origin main
# --prune: se o público foi apagado e recriado, a ref antiga "$remoto/main" não pode sobrar.
git fetch -q --prune "$remoto" 2>/dev/null || true

# 1. Dados de estudo nunca saem do privado.
for proibido in registro/estado.yml registro/estudante.yml; do
  if git cat-file -e "origin/main:$proibido" 2>/dev/null; then
    erro "a main tem $proibido, que é dado de estudo; não publico."
  fi
done
if git show origin/main:registro/avaliacoes.md | grep -qE '^\| [0-9]{4}-[0-9]{2}-[0-9]{2} \|'; then
  erro "registro/avaliacoes.md da main tem resultados; não publico."
fi
if [ "$(git show origin/main:registro/respostas.csv | wc -l)" -gt 1 ]; then
  erro "registro/respostas.csv da main tem respostas; não publico."
fi

# 2. Nenhum e-mail real na árvore publicada.
emails=$(git grep -IhoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' origin/main -- . \
  | grep -viE '@(users\.noreply\.github\.com|example\.(com|org|net)|exemplo\.(com|org))$|noreply@' | sort -u || true)
if [ -n "$emails" ]; then
  erro "a main tem e-mail que não é noreply ($(echo "$emails" | wc -l) ocorrência(s)); confira com git grep antes de publicar."
fi

# 3. O commit de publicação sai com a identidade local: ela precisa ser noreply.
ident=$(git var GIT_COMMITTER_IDENT)
case "$ident" in
  *@users.noreply.github.com\>*) ;;
  *) erro "a identidade do git local não é um e-mail noreply do GitHub; configure user.email antes de publicar." ;;
esac

# 4. Árvore do espelho: a da main, sem os arquivos excluídos.
indice=$(mktemp)
trap 'rm -f "$indice"' EXIT
GIT_INDEX_FILE="$indice" git read-tree origin/main
for f in "${excluir[@]}"; do GIT_INDEX_FILE="$indice" git rm -q --cached --ignore-unmatch -- "$f"; done
arvore=$(GIT_INDEX_FILE="$indice" git write-tree)

# 5. O espelho não pode ter divergido: a main pública tem de ser igual à última publicação.
pai=$(git rev-parse -q --verify "$remoto/main" || true)
if [ -n "$pai" ]; then
  ultima=$(git log -1 --format=%H --grep="^$prefixo" "$pai" || true)
  [ -n "$ultima" ] || erro "o público não tem nenhuma publicação anterior; não sei de onde ele veio."
  if ! git diff --quiet "$ultima" "$pai"; then
    git diff --stat "$ultima" "$pai" >&2
    erro "o público tem mudanças que não vieram de uma publicação. Traga-as para a main privada por PR e só então publique."
  fi
  if [ "$(git rev-parse "$pai^{tree}")" = "$arvore" ]; then
    echo "Nada a publicar: o público já está igual à main."; exit 0
  fi
fi

curto=$(git rev-parse --short origin/main)
msg="$prefixo de $(git log -1 --format=%cs origin/main) ($curto)"
if [ -n "$pai" ]; then commit=$(git commit-tree "$arvore" -p "$pai" -m "$msg"); else commit=$(git commit-tree "$arvore" -m "$msg"); fi
echo "Commit $commit: $msg"
[ -n "$pai" ] && git diff --stat "$pai" "$commit" | tail -1

if [ "$enviar" != "--enviar" ]; then echo "(simulação: use --enviar para publicar)"; exit 0; fi

if [ -z "$pai" ]; then
  git push "$remoto" "$commit:refs/heads/main"
  echo "Primeira publicação enviada para a main. Aplique agora o ruleset (docs/publicacao.md)."
  exit 0
fi

branch="publicacao/$curto"
git push "$remoto" "$commit:refs/heads/$branch"
url=$(git remote get-url "$remoto")
repo=""
if [[ "$url" =~ ^(git@github\.com:|https://github\.com/)([^/]+/[^/]+)$ ]]; then
  repo="${BASH_REMATCH[2]%.git}"
fi
if [ -n "$repo" ] && command -v gh >/dev/null 2>&1; then
  gh api "repos/$repo/pulls" -f title="$msg" -f head="$branch" -f base=main \
    -f body="Publicação da main privada ($curto). Mescle com **Rebase and merge** depois do CI passar." \
    -q .html_url
else
  echo "Branch $branch enviada. Abra o pull request para a main no GitHub e mescle com Rebase and merge."
fi
