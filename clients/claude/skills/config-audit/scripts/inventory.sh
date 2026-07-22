#!/usr/bin/env bash
# Phase 0 inventory snapshot of a Claude Code config dir.
# Usage: inventory.sh <config-dir>      (e.g. .claude or ~/.claude)
set -uo pipefail

DIR="${1:?usage: inventory.sh <config-dir>}"
cd "$DIR" || exit 1

# Runtime-state dirs that would drown the snapshot — pruned from the structure
# listing (the skill's own thesis: context is the scarce resource).
NOISE='node_modules|.git|projects|todos|debug|shell-snapshots|statsig|cache|backups|daemon|plugins|file-history|sessions|session-env|paste-cache|ide|jobs|tasks|telemetry|usage-data|plans|image-cache|history'

echo "== Structure =="
if command -v tree >/dev/null; then
  tree -L 3 --dirsfirst -I "$NOISE" .
else
  find . -maxdepth 3 -type d | grep -Ev "/($NOISE)(/|$)" | sort
fi

echo; echo "== Always-loaded files (line counts) =="
# A project .claude/ sits beside the real always-loaded files (project-root
# CLAUDE.md / CLAUDE.local.md) — usually the largest. Count them too.
ALWAYS=()
[ -f CLAUDE.md ] && ALWAYS+=("CLAUDE.md")
if [ "$(basename "$PWD")" = ".claude" ]; then
  [ -f ../CLAUDE.md ] && ALWAYS+=("../CLAUDE.md")
  [ -f ../CLAUDE.local.md ] && ALWAYS+=("../CLAUDE.local.md")
fi
[ -f CLAUDE.local.md ] && ALWAYS+=("CLAUDE.local.md")
while IFS= read -r r; do ALWAYS+=("$r"); done < <(find rules -name '*.md' 2>/dev/null)
[ "${#ALWAYS[@]}" -gt 0 ] && wc -l "${ALWAYS[@]}" || echo "no always-loaded CLAUDE.md/rules found"

echo; echo "== SKILL.md sizes (limit 500) =="
find skills -name SKILL.md -print0 2>/dev/null | xargs -0 wc -l 2>/dev/null | sort -n

echo; echo "== Agent sizes (separate context, but authored weight) =="
find agents -name '*.md' -print0 2>/dev/null | xargs -0 wc -l 2>/dev/null | sort -n || echo "no agents/"

echo; echo "== Description bytes per skill (loaded every session unless disable-model-invocation) =="
for f in skills/*/SKILL.md; do
  [ -f "$f" ] || continue
  # Print the description: line and its folded-scalar continuation, stopping at
  # the next top-level key OR the closing --- of the frontmatter. Without the
  # --- guard, a description that is the last key swallows the whole body.
  bytes=$(awk '
    /^description:/ {d=1; print; next}
    d { if (/^---[ \t]*$/ || /^[A-Za-z_-]+:/) exit; print }
  ' "$f" | wc -c | tr -d ' ')
  # disable-model-invocation must be read from frontmatter only, not the body.
  dmi=$(awk 'NR>1 && /^---[ \t]*$/{exit} /^disable-model-invocation:[ \t]*true/{f=1} END{exit !f}' "$f" && echo 1 || echo 0)
  printf '%6s  %s%s\n' "$bytes" "$f" "$([ "$dmi" = 1 ] && echo '  [manual-only: zero cost]')"
done | sort -rn

echo; echo "== Last modified (git) =="
# A non-versioned project .claude inside a versioned parent reports the PARENT's
# history — flag that rather than mislabel parent drift as config drift.
TOP="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -n "$TOP" ] && [ "$TOP" != "$PWD" ] && [ ! -d .git ]; then
  echo "(this dir is tracked by a parent repo at $TOP — dates/drift below are repo-wide)"
fi
for p in CLAUDE.md settings.json .gitignore rules skills/*/ agents hooks commands; do
  [ -e "$p" ] || continue
  d="$(git log -1 --format=%cs -- "$p" 2>/dev/null)"
  printf '%s  %s\n' "${d:-untracked }" "$p"
done

echo; echo "== Agents / hooks / commands roster =="
ls agents 2>/dev/null || echo "no agents/"
ls hooks 2>/dev/null || echo "no hooks/"
ls commands 2>/dev/null || echo "no commands/ (good — legacy)"

echo; echo "== Uncommitted config drift =="
git status --short 2>/dev/null || echo "not a git repo (finding: config unversioned)"

echo; echo "== Plugin skill count (description tax) =="
PLUG="$HOME/.claude/plugins/cache"
[ -d "$PLUG" ] && { printf '%s plugin SKILL.md files load every session\n' "$(find "$PLUG" -name SKILL.md | wc -l | tr -d ' ')"; } || echo "no plugin cache"
