#!/usr/bin/env bash
# Initialize this folder as a STANDALONE, ANONYMIZED git repo and (optionally) push it.
#
#   Usage:
#     ./setup_anon_repo.sh                       # init + anonymized commit only
#     ./setup_anon_repo.sh <git-remote-url>      # ...and push to your throwaway account
#
#   Example remote (throwaway account you created):
#     ./setup_anon_repo.sh https://github.com/anonstride2026/stride-transitions
#
# Anonymity guarantees enforced here:
#   * commit author/committer are set REPO-LOCALLY to "Anonymous" (your global
#     ~/.gitconfig name/email are never used or changed for this repo);
#   * no author, affiliation, or machine metadata is written.
set -euo pipefail
cd "$(dirname "$0")"

REMOTE="${1:-}"
ANON_NAME="Anonymous"
ANON_EMAIL="anonymous@anon.review"

echo "==> Checking video file sizes (GitHub rejects files > 100 MB)…"
BIG=0
while IFS= read -r -d '' f; do
  sz=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f")
  mb=$(( sz / 1024 / 1024 ))
  if [ "$mb" -ge 90 ]; then
    echo "    !! ${f#./}  = ${mb} MB  (too large — compress before pushing)"
    BIG=1
  fi
done < <(find videos -type f \( -name '*.mp4' -o -name '*.webm' -o -name '*.mov' \) -print0 2>/dev/null)
if [ "$BIG" -eq 1 ]; then
  echo "    Tip: ffmpeg -i in.mp4 -vf scale=256:-2 -crf 30 -an out.mp4   (drops audio, shrinks a lot)"
  echo "    Aborting so you can compress first. Re-run when clips are < 90 MB."
  exit 1
fi
echo "    OK."

echo "==> Regenerating clips.json from videos/ …"
python3 gen_manifest.py

if [ ! -d .git ]; then
  echo "==> git init"
  git init -q
  git checkout -q -b main 2>/dev/null || git branch -q -m main 2>/dev/null || true
fi

# Repo-local anonymized identity (does NOT touch your global git config).
git config user.name  "$ANON_NAME"
git config user.email "$ANON_EMAIL"

echo "==> Staging + committing as ${ANON_NAME} <${ANON_EMAIL}>"
git add -A
if git diff --cached --quiet; then
  echo "    Nothing new to commit."
else
  GIT_AUTHOR_NAME="$ANON_NAME"   GIT_AUTHOR_EMAIL="$ANON_EMAIL" \
  GIT_COMMITTER_NAME="$ANON_NAME" GIT_COMMITTER_EMAIL="$ANON_EMAIL" \
    git commit -q -m "Add anonymous qualitative transition comparisons"
  echo "    Committed."
fi

echo
echo "==> Author sanity check (must read Anonymous, NOT your real name):"
git log -1 --pretty='    author=%an <%ae>%n    commit=%cn <%ce>'

if [ -n "$REMOTE" ]; then
  echo
  echo "==> Setting remote + pushing to: $REMOTE"
  git remote remove origin 2>/dev/null || true
  git remote add origin "$REMOTE"
  git push -u origin main
  echo
  echo "Pushed. Now enable GitHub Pages: repo Settings → Pages → Deploy from branch → main / (root)."
else
  echo
  echo "No remote given. To publish:"
  echo "  1) Create a throwaway GitHub account (fresh email, pseudonym, no real name)."
  echo "  2) Create an EMPTY public repo (no README) on that account."
  echo "  3) Re-run:  ./setup_anon_repo.sh <that-repo's-https-url>"
fi
