# Phase 5 — Trigger evals: TDD for skills, part 1

A skill without a trigger test is an unproven hypothesis. This phase costs real
tokens (each query spawns a fresh `claude -p` session) — get operator
confirmation before running.

## Method (per Anthropic's skill-creator methodology)

1. Build **15–20 queries**: 8–10 should-trigger + 8–10 should-not-trigger.
2. Queries are realistic, as a live human writes: with file paths, typos, both
   languages, varied length. Not "создай ADR" but "слушай, мы тут час обсуждали
   выбор между bullmq и явной таблицей очереди — зафиксируй это нормально".
3. The most valuable negatives are **near-misses**: queries sharing keywords
   with the skill but needing a different tool. "Напиши пост в канал" vs
   "ответь подписчику в комментах" — both about Telegram text, only the first
   should trigger.
4. Run each query in a fresh session, 3 times — triggering is stochastic.
5. Mind the mechanics: simple one-step queries don't trigger skills *at all* —
   Claude handles them directly. Test queries must be substantial enough.

## Harness

```bash
scripts/trigger-eval.sh <fixture-dir> <queries.tsv> [runs=3]
```

`queries.tsv` format: `<expected-skill-or-none><TAB><query>`. The fixture dir
should be a realistic mini-repo (a few ADRs, issues, source files) so discovery
steps inside triggered skills have something to find. The harness runs each
query via `claude -p --max-turns 2 --output-format stream-json`, extracts the
first `Skill` tool invocation per run, and prints a TSV of results.

Parallelize across queries by dispatching one subagent per query when running
inside a session — each subagent runs its 3 sequential `claude -p` calls and
reports the fired skills.

## Scoring

- should-trigger: pass = expected skill fired in ≥2/3 runs.
- should-not: pass = none of the *audited* skills fired (an unrelated built-in
  or plugin skill firing is not a failure of your descriptions).
- Failed cases → edit the description → re-run. This is the RED-GREEN loop for
  triggering.

## What the results mean

- Expected skill never fires on a clear request → description not pushy enough,
  or the query too simple to warrant a skill at all.
- Wrong skill fires → trigger collision; fix in the **description** (anti-
  trigger), not only in the body — routing happens before bodies are read.
- Both verdicts unstable across runs → descriptions overlap; sharpen both.
