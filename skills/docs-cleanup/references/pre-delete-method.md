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

Run these checks in order. Stop as soon as you have enough to downgrade the verdict.

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

- The exact filename (e.g. `[RESOLVED]P2-2026-01-12-foo.md`)
- The slug part of the filename (without status tag / priority)
- The H1 title (if distinctive)
- 1-2 distinctive identifiers from the body

Exclude noise paths (`node_modules`, `.git`, build artifacts, the candidate file
itself). Report what you find, not what you searched for. Empty results are fine —
say so.

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
- `supersede` (ADRs only) — is there a newer ADR explicitly replacing this?
- `promote-to-adr` — does this resolved issue actually encode an architectural
  decision?

If any of these fits, the verdict should change. Recommend the best alternative.

## Output format

Return a single JSON object:

```json
{
  "path": "/abs/path/to/candidate.md",
  "verdict": "downgrade",
  "downgrade_to": "repair",
  "has_incoming_references": true,
  "reference_examples": [
    {"file": "docs/runbooks/deploy.md", "line": 42, "snippet": "see [issue-foo.md] for context"},
    {"file": "apps/api/README.md", "line": 8, "snippet": "(linked from foo-resolution.md)"}
  ],
  "content_unique": true,
  "unique_signals": [
    "Contains exact SQL fragment 'WITH RECURSIVE bots(...) AS (...)' not found elsewhere.",
    "Documents rejection reason for X-approach that's not in any ADR."
  ],
  "recommended_alt": "repair: move the recursive-CTE SQL into a troubleshooting doc (e.g. docs/runbooks/sql-deadlocks.md), then let `issue-writer:close` sweep the file.",
  "reasoning": "Two incoming references found and body contains unique recursive-CTE SQL. Delete would break the runbook link and lose the SQL. Repair (rename to [RESOLVED]) preserves both."
}
```

Field rules:

- `verdict` — `safe_to_delete` | `downgrade`.
  - `safe_to_delete`: no incoming references AND content is not unique AND no safer
    alternative fits.
  - `downgrade`: anything else.
- `downgrade_to` — required when `verdict == downgrade`. One of: `repair`, `merge`,
  `supersede`, `promote-to-adr`. **Cannot be `delete`** — that's what the candidate
  already was. There is no `archive` option.
- `has_incoming_references` — boolean.
- `reference_examples` — up to 5 examples (file, line, snippet) when references
  exist. Empty array otherwise.
- `content_unique` — boolean.
- `unique_signals` — list of short strings naming what's unique. Empty when content
  is redundant.
- `recommended_alt` — short text describing the concrete alternative action (e.g.
  "supersede: add `**Superseded by:** docs/adr/...` header"). Required when
  `verdict == downgrade`.
- `reasoning` — 1-3 sentences explaining the verdict. Required.

## Decision matrix

Use this as the spine; the detailed checks above feed it:

| References | Unique content | Better alt fits | Verdict           |
|------------|----------------|-----------------|-------------------|
| no         | no             | no              | `safe_to_delete`  |
| yes        | —              | —               | `downgrade` → repair (or follow link target's preference) |
| no         | yes            | —               | `downgrade` → repair (with `recommended_alt` naming the doc to move the content into — runbook, troubleshooting, ADR via `adr-writer:from-issue`) |
| no         | no             | yes             | `downgrade` → the alt that fits |

When in doubt, **lean toward downgrade**. The cost of an unnecessary `repair` is
zero; the cost of an unsafe `delete` is permanent loss.

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
