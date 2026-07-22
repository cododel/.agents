# Docs Classifier Method

Use this file as the complete method for a generic read-only subagent launched by the
`docs-cleanup` skill. Read a batch of documentation files and return a structured
classification for each. You do
**not** write to files, do **not** delete, do **not** mutate state. Read-only.

## Input you will receive

The orchestrator passes:

1. **`candidates`** — a list of file paths (absolute) to classify.
2. **`scope_context`** — text containing:
   - Confirmed docs directories the audit covers
   - Local convention summary from each directory's `README.md` (filename pattern,
     status taxonomy, project guardrails)
   - Any user instructions narrowing the audit (e.g. "skip anything created in the
     last 30 days")
3. **`value_criteria_path`** — the absolute path to
   `docs-cleanup/references/value-criteria.md`. Read it inside the subagent context.

If any input is missing, return a single error object:

```json
{"error": "missing_input", "missing": ["scope_context"], "expected": "..."}
```

## What to do

For each candidate path:

1. **Read the file in full.** Don't sample. Body matters — that's the whole point of
   the subagent existing.
2. **Apply the value criteria** from `value-criteria.md`. Pick exactly one verdict
   from the supported labels (or `ambiguous` when the signal is genuinely unclear).
   There is no `archive` verdict — resolved issues either route to `promote-to-adr`,
   to `repair` (with a note to move unique content into a runbook / troubleshooting
   doc before close), or to `delete`.
3. **Record evidence.** A one-sentence quote or paraphrase of the signal that matched
   the label, so the orchestrator and operator can audit your call without re-reading
   the file.
4. **Note false-positive risk** for `delete` verdicts. If you suspect the file might
   still be referenced elsewhere or contain unique operational knowledge, lean
   toward `repair` / `merge` / `promote-to-adr` and explain in the evidence field.

You may read additional files for context (e.g. checking whether an ADR is superseded
by reading the newer one referenced in the candidate's body). Do not exhaustively
scan the repo — the orchestrator runs the pre-delete-checker for that.

## Output format

Return a single JSON array with one object per candidate, in the same order as input:

```json
[
  {
    "path": "/abs/path/to/docs/issues/[RESOLVED]P2-2026-01-12-foo.md",
    "verdict": "promote-to-adr",
    "evidence": "Body has 'Options Considered' with three rejected alternatives and rationale for picking Bun; establishes package-manager policy across the monorepo.",
    "fp_risk": "low",
    "recommended_alt": null,
    "title": "[RESOLVED] Package manager policy: Bun only",
    "status_filename": "[RESOLVED]",
    "status_body": "Resolved"
  },
  {
    "path": "/abs/path/to/docs/issues/[ACTIVE]P3-2025-09-04-bar.md",
    "verdict": "repair",
    "evidence": "Status is [ACTIVE] but body says 'fixed in #1234, verified in staging' — looks resolved; filename and body disagree.",
    "fp_risk": null,
    "recommended_alt": "rename to [RESOLVED] and let issue-writer:close sweep it",
    "title": "[ACTIVE] Foo bar timeout",
    "status_filename": "[ACTIVE]",
    "status_body": "Active"
  }
]
```

Field rules:

- `verdict` — one of: `keep`, `repair`, `resolve`, `merge`, `supersede`,
  `promote-to-adr`, `delete`, `ambiguous`, `skipped`.
- `evidence` — one sentence quoting or paraphrasing the matched signal. **Required.**
  Cite specific phrases from the body if useful.
- `fp_risk` — `low | medium | high | null`. Required for `delete`; null for others.
- `recommended_alt` — short text suggesting an alternative if `verdict` is `delete`
  and `fp_risk >= medium`, OR if `verdict == ambiguous`, OR if `verdict == repair`
  and the suggested fix is "move content into a different doc home" (specify the
  target: runbook path, troubleshooting doc, ADR via `adr-writer:from-issue`). Null
  otherwise.
- `title` — the document's H1 heading or filename if no H1.
- `status_filename` — status tag from filename (`[ACTIVE]`, `[RESOLVED]`, etc.) or
  null if no convention.
- `status_body` — status from body header (`**Status:** Resolved`) or null if
  missing.

The `status_filename` / `status_body` fields are critical: the orchestrator uses
them to detect mismatches, which are common signals for `repair` regardless of the
primary verdict.

## Constraints

- **Read-only.** No file writes, edits, deletes, or moves. The orchestrator handles
  all mutations after operator approval.
- **One verdict per file.** If the file is genuinely between two labels, return
  `ambiguous` with both candidates named in `evidence`, not split rows.
- **Don't summarize file bodies in the JSON.** The `evidence` field is one sentence,
  not a paragraph. The operator reads the file themselves if they want details.
- **Don't fabricate signals.** If you can't find a matched signal for any label,
  return `ambiguous` with an honest explanation.

## Boundaries

- You are not the pre-delete checker. Your `delete` verdicts are *proposals*; the
  orchestrator runs a separate safety check before any deletion.
- You are not the operator gate. Your output is the input to the gate, not the gate
  itself.
- If the scope brief excludes a candidate, return an object for that path with
  `"verdict": "skipped"` and a one-sentence reason. Never emit an invalid empty array element.
