#!/usr/bin/env bash
# Phase 5 trigger-eval harness: run each query in fresh `claude -p` sessions,
# record which skill (if any) fires first per run.
#
# Usage: trigger-eval.sh <fixture-dir> <queries.tsv> [runs=3]
#   queries.tsv: <expected-skill-or-none><TAB><query text>   (# comments allowed)
#
# Output: TSV  expected<TAB>query<TAB>run1,run2,run3
# Transcripts (and a sibling .err per run) are kept in a temp dir (printed to
# stderr) for inspection.
set -uo pipefail

FIX="${1:?usage: trigger-eval.sh <fixture-dir> <queries.tsv> [runs]}"
QFILE="${2:?queries.tsv required}"
RUNS="${3:-3}"

case "$RUNS" in ''|*[!0-9]*|0) echo "runs must be a positive integer" >&2; exit 1;; esac
command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }
command -v claude >/dev/null || { echo "claude CLI is required" >&2; exit 1; }
[ -d "$FIX" ] || { echo "fixture dir not found: $FIX" >&2; exit 1; }
[ -f "$QFILE" ] || { echo "queries file not found: $QFILE" >&2; exit 1; }

# macOS ships no `timeout`; coreutils installs it as `gtimeout`.
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout || true)"
[ -n "$TIMEOUT_BIN" ] || echo "warning: no timeout/gtimeout — runs are uncapped" >&2

OUT="$(mktemp -d "${TMPDIR:-/tmp}/trigger-eval.XXXXXX")"
printf 'expected\tquery\truns\n'

i=0
# `|| [ -n "$expected" ]` processes a final line with no trailing newline.
while IFS=$'\t' read -r expected query || [ -n "${expected:-}" ]; do
  case "${expected:-}" in ''|'#'*) continue;; esac
  if [ -z "${query:-}" ]; then
    echo "skipping malformed line (no tab): $expected" >&2
    continue
  fi
  i=$((i + 1))
  results=()
  for r in $(seq 1 "$RUNS"); do
    f="$OUT/q${i}_r${r}.jsonl"
    # stderr to a separate file so an auto-update notice can't corrupt the JSONL
    # stream; </dev/null so claude can't consume the queries.tsv on fd 0.
    ( cd "$FIX" && ${TIMEOUT_BIN:+"$TIMEOUT_BIN" 240} claude -p "$query" \
        --max-turns 2 --output-format stream-json --verbose >"$f" 2>"$f.err" </dev/null ) || true
    # fromjson? tolerates any stray non-JSON line instead of aborting the parse.
    skill=$(jq -rR 'fromjson? | select(.type=="assistant")
                    | .message.content[]?
                    | select(.type=="tool_use" and .name=="Skill")
                    | (.input.skill // empty)' "$f" 2>/dev/null | head -1)
    if [ -z "${skill:-}" ] && ! grep -q '"type":"assistant"' "$f" 2>/dev/null; then
      skill="error"   # session never produced an assistant turn — inspect transcript
    fi
    results+=("${skill:-none}")
  done
  printf '%s\t%s\t%s\n' "$expected" "$query" "$(IFS=,; echo "${results[*]}")"
done < "$QFILE"

echo "transcripts: $OUT" >&2
