#!/usr/bin/env bash
# post-commit hook for auto-docs.
#
# Install:
#   cp .agents/skills/auto-docs/scripts/post-commit-hook.sh .git/hooks/post-commit
#   chmod +x .git/hooks/post-commit

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
mkdir -p "$REPO_ROOT/.doc-agent"

# 1. Immediately regenerate deterministic Git history and project structure
if command -v node >/dev/null 2>&1; then
  if [ -f "$REPO_ROOT/.agents/plugins/hook-auto-docs/scripts/update-structure-docs.js" ]; then
    ( cd "$REPO_ROOT" && node .agents/plugins/hook-auto-docs/scripts/update-structure-docs.js >/dev/null 2>&1 || true )
    ( cd "$REPO_ROOT" && node .agents/plugins/hook-auto-docs/scripts/generate-git-history.js >/dev/null 2>&1 || true )
    echo "📚 [auto-docs] Updated documentation/PROJECT_STRUCTURE.md and documentation/GIT_HISTORY.md"
  fi
fi

# 2. Flag semantic documentation for coding assistant
PROMPT="A new commit just landed. Run the auto-docs skill: read the git history since the last documented commit (.doc-agent/last-commit.txt), analyze the diff, and write a draft to .doc-agent/draft-<range>.md. Do NOT apply anything to CHANGELOG.md, docs/, or RELEASE_NOTES.md without approval."

if command -v claude >/dev/null 2>&1; then
  ( cd "$REPO_ROOT" && claude -p "$PROMPT" --skill auto-docs ) \
    || echo "[auto-docs] Semantic draft generation failed — run it manually later." >&2
else
  touch "$REPO_ROOT/.doc-agent/pending-commit.flag"
  echo "$(git rev-parse HEAD)" >> "$REPO_ROOT/.doc-agent/pending-commit.flag"
fi

if ls "$REPO_ROOT"/.doc-agent/draft-*.md >/dev/null 2>&1; then
  echo ""
  echo "📝 [auto-docs] A documentation draft is waiting for your review in .doc-agent/"
  echo "📝 [auto-docs] Ask your AI assistant to review and apply the draft when ready."
fi
