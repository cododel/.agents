# Pre-Delete Checker Method

Use this file as the complete method for a generic read-only subagent launched by the
`docs-cleanup` skill. Evaluate
**one** delete candidate at a time and answer: is it safe to delete, or is there a
safer alternative?

Use the client's repository read and search tools. You do **not** write, delete, or modify
anything.

## Input you will receive

1. **`candidate_path`** — absolute path to the file being evaluated.
2. **`repo_root`** — absolute path to the repo root, so you can search the whole tree.
3. **`scope_context`** — short text summarizing the audit's scope and any
   project-specific knowledge passed from the orchestrator (e.g. "ADRs are gated by
   the `**Implementation:**` header in this project").

If any input is missing, return:

```json
{"error": "missing_input", "missing": ["repo_root"]}
```

## What to do

Run these checks in order. You may stop when a decisive retain/repair reason is found, but report
every unperformed check and leave its booleans `null`. If required evidence is unavailable or any
required check is incomplete, return `inconclusive` with the observed blocker/gap; never claim
`safe_to_delete` from an early stop. `downgrade` is a completed evidence result, not a placeholder for
missing evidence.

### Check 0 — Validate the target

Require the exact candidate to be a regular non-symlink file inside the confirmed documentation scope
and repository root. A symlink, path escape, invalid type, or unresolved boundary blocks deletion;
return the exact reason without following an invalid target. Operator approval cannot bypass target
validity. Do not read bodies outside the confirmed scope.

### Check 1 — Read the candidate in full

You can't judge unique content or references without knowing what's in the file.
Read it once, completely.

Note especially:

- Title and obvious slug-like phrases
- Specific identifiers (function names, file paths, ticket numbers, commit SHAs,
  config keys)
- Sections that look like primary evidence (logs, SQL, repro commands, error
  excerpts) — these are common "unique content" signals

### Check 2 — Search for incoming references

Search from the repo root for distinctive strings that would indicate something links to this
file. Probe with at least:

- The exact filename (e.g. `[CLOSED]-2026-01-12-foo.md`)
- The slug part of the filename (without status tag / priority)
- The H1 title (if distinctive)
- 1-2 distinctive identifiers from the body

Exclude noise paths (`node_modules`, `.git`, build artifacts, the candidate file
itself). Report what you find, not what you searched for. Empty results are fine —
say so.

Distinguish **load-bearing references** from **unambiguous index-only entries**. The former depends on
the document's meaning and blocks deletion until a verified replacement owner and link repair exist.
The latter may be removed or redirected only through a recorded exact repair in the same change,
followed by recheck. Report both kinds and the planned repairs; do not label all references blocking
or silently ignore indexes. If any incoming reference cannot be classified or repaired unambiguously,
the reference check is incomplete.

### Check 3 — Assess content uniqueness

For each major piece of evidence in the body (commands, SQL, logs, rationale,
rejection reasons, file paths), ask: **is this preserved anywhere else?**

Do a quick spot-check by grepping for distinctive snippets — exact error messages,
specific SQL fragments, unusual command flags. If a snippet appears only in this file,
the content is unique.

If the file contains rejection reasons for design options that wouldn't make sense to
re-derive ("we rejected X because of Y" where Y is non-obvious), that's unique
content even if the snippet itself isn't grep-distinctive.

### Check 4 — Better-fit alternative?

Run through the alternatives:

- `repair` — is the doc fixable rather than disposable? (Most docs are.) Also covers
  "move unique content into the proper doc home (runbook / troubleshooting / inline
  comment) before delete" — there is no `archive` fallback.
- `merge` — does another doc cover the same ground and could absorb this?
- `close` (Issues only) — is the work complete and verified, requiring lifecycle closure
  and the `issue-writer:close` extraction gate rather than direct deletion?
- `stale` (Issues only) — are the premises stale while completion remains unverified,
  requiring `Last reviewed` plus a `Stale note` while the Issue stays `Open`?
- `supersede` (ADRs only) — is there a newer ADR explicitly replacing this?
- `promote-to-adr` — does this closed issue actually encode an architectural
  decision?

If any of these fits, the verdict should change. Recommend the best alternative. Removing an
unambiguous index-only entry as part of an otherwise proven delete does not by itself turn the value
verdict into `repair`; retain its planned repair and require the primary agent's same-change recheck.

## Output format

Return a single JSON object:

```json
{
  "path": "/abs/path/to/candidate.md",
  "verdict": "downgrade",
  "downgrade_to": "repair",
  "checks": {
    "target_validity": "complete",
    "candidate_read": "complete",
    "incoming_references": "complete",
    "content_uniqueness": "complete",
    "better_alternative": "complete"
  },
  "has_incoming_references": true,
  "has_blocking_references": true,
  "reference_examples": [
    {"file": "docs/runbooks/deploy.md", "line": 42, "kind": "load-bearing", "snippet": "see [issue-foo.md] for context"},
    {"file": "apps/api/README.md", "line": 8, "kind": "index-only", "snippet": "(linked from foo-resolution.md)"}
  ],
  "planned_index_repairs": [],
  "content_unique": true,
  "better_alternative_fits": true,
  "unique_signals": [
    "Contains exact SQL fragment 'WITH RECURSIVE bots(...) AS (...)' not found elsewhere.",
    "Documents rejection reason for X-approach that's not in any ADR."
  ],
  "recommended_alt": "repair: move the recursive-CTE SQL into a troubleshooting doc (e.g. docs/runbooks/sql-deadlocks.md), then let `issue-writer:close` sweep the file.",
  "gaps": [],
  "reasoning": "Two incoming references found and body contains unique recursive-CTE SQL. Delete would break the runbook link and lose the SQL. Repair preserves both."
}
```

Field rules:

- `verdict` — `safe_to_delete | downgrade | inconclusive`.
  - `safe_to_delete`: all required checks are complete, the target is valid, no unresolved
    load-bearing references remain, content is not unique, and no safer alternative fits. Existing
    index-only references require exact `planned_index_repairs` and a same-change primary recheck.
  - `downgrade`: all required checks are complete and a definite blocking reference, unique value,
    or better alternative is proven.
  - `inconclusive`: any required check is unavailable/incomplete, including early stop; state the
    observed reason and missing checks. This blocks deletion without inventing negative results.
- `checks` — required for target validity, full read, references, uniqueness, and better alternative.
  Each is `complete | unavailable | not-checked`. Explain every non-complete item in `gaps`.
- `downgrade_to` — required when `verdict == downgrade`. One of: `repair`, `close`, `stale`,
  `merge`, `supersede`, `promote-to-adr`. **Cannot be `delete`** — that's what the candidate
  already was. Use `null` for `safe_to_delete`; for `inconclusive`, name an evidenced safer route
  when known, otherwise `null`. There is no `archive` option.
- `has_incoming_references`, `has_blocking_references`, `content_unique`, and
  `better_alternative_fits` — `true | false | null`. Use `null` when the corresponding check was not
  completed. A demonstrated positive signal may be `true`; absence requires a completed check.
- `reference_examples` — up to 5 examples (file, line, snippet) when references
  exist, marked `load-bearing | index-only | non-load-bearing`. Empty array means no examples were
  found; it does not by itself prove a complete reference search.
- `planned_index_repairs` — exact index path/entry and removal/redirection target. Empty when no
  repair is required; never a vague promise to fix links later.
- `unique_signals` — list of short strings naming what's unique. Empty when content
  is redundant.
- `recommended_alt` — short text describing the concrete alternative action (e.g.
  "supersede: add `**Superseded by:** docs/adr/...` header"). Required when
  `verdict == downgrade`.
- `reasoning` — 1-3 sentences explaining the verdict. Required.
- `gaps` — unavailable/unperformed check and reason, required even when empty. A safety result does
  not determine Git recovery or mutation authority; those remain with the primary agent.

## Decision matrix

Use this as the spine; the detailed checks above feed it:

| Blocking references | Unique content | Better alt fits | Verdict           |
|------------|----------------|-----------------|-------------------|
| no         | no             | no              | `safe_to_delete`  |
| yes        | —              | —               | `downgrade` → repair (or follow link target's preference) |
| no         | yes            | —               | `downgrade` → repair (with `recommended_alt` naming the doc to move the content into — runbook, troubleshooting, ADR via `adr-writer:from-issue`) |
| no         | no             | yes             | `downgrade` → the alt that fits |
| unknown/incomplete required check | — | — | `inconclusive` → retain pending evidence |

The first four rows require complete checks. Index-only references count as non-blocking only with
the exact planned same-change repair and primary recheck described above.

Uncertainty is `inconclusive`; a proven better action is `downgrade`. Neither permits deletion.

## Constraints

- **Read-only.** No file writes, edits, or deletes.
- **One candidate per invocation.** The orchestrator runs you in parallel for
  multiple candidates; don't try to batch.
- **Don't second-guess the classifier on non-delete verdicts.** Your job is only
  the delete safety check. If a file is non-delete in the input, you shouldn't be
  invoked on it.
- **Be honest about false-positive risk in `reference_examples`.** A line like
  `// foo.md is deprecated, ignore` is not a load-bearing reference; flag it as such
  in the snippet so the orchestrator can judge.
