# Delete review gate

Deletion is irreversible. The gate is mandatory, non-skippable, and runs for **every**
`delete` candidate — regardless of how categorical the operator's phrasing sounded.

Phrases that do **not** waive the gate: "they're definitely stale", "just clean it up",
"delete everything old", "do not ask", "trust me", "точно мусор".

The cost of one approval round-trip is trivial. The cost of losing a unique evidence
file is much higher.

## Pre-gate: pre-delete-checker must run first

For every `delete` candidate from classification, spawn the `pre-delete-checker`
subagent (one invocation per candidate, in parallel if multiple). It returns a
safety report — see `references/pre-delete-method.md` for the JSON contract.

If the checker finds:

- **Incoming references** → downgrade verdict to `repair` (or `merge` if the
  references are content overlap) and explain in the gate row.
- **Unique content** → downgrade to `repair` with a note about where the content
  should be moved (runbook, troubleshooting doc, ADR via `adr-writer:from-issue`)
  before the file is deleted. There is no `archive` fallback.
- **A safer alternative fits** → switch the verdict to that alternative.

Only candidates that pass the checker enter the gate as `delete`. Everything else is
shown with its downgraded verdict and reason.

## Gate format

```markdown
## Delete Review Gate

Proposed deletes require your explicit approval. I will only delete files you approve
by exact path.

| Path | Type | Status | Summary | Rationale | FP risk | Safer alt |
|------|------|--------|---------|-----------|---------|-----------|
| `docs/issues/[RESOLVED]P3-2024-03-01-foo.md` | issue | resolved/stale | One-sentence content summary. | Why no durable value remains. | Low / Medium / High + reason. | repair / merge / supersede / promote-to-adr |

Pre-delete checks summary:
  - Checked references: <N> files scanned, <M> hits — see per-candidate notes above
  - Checked unique content: <N> candidates → unique=<K>, redundant=<N-K>
  - Downgraded by checker (not in delete table): <list with new verdicts>

Approval format (reply with one or more):
  - `approve delete: <path>, <path>`
  - `keep: <path>`
  - `repair: <path>`
  - `supersede: <path>`
  - `promote-to-adr: <path>`
  - `cancel`
```

The table must include for **each candidate**:

- One-sentence factual content summary (not "this issue is about X" — say what's in it)
- Concrete deletion rationale (not "stale" — *why* stale, *what* makes it valueless)
- Which pre-delete checks were run and what they found
- False-positive risk: Low / Medium / High **with the reason**
- A safer non-delete alternative — there's almost always one

## Approval matching rules

- Match by **exact path**, not by glob, slug, or substring.
- "Approve all" / "delete everything in the list" is **not** valid approval — require
  per-path approval. A bulk reply forces the operator to actually look at the list;
  the friction is the safety feature.
- If the operator approves a path that wasn't in the table, refuse and ask them to
  re-state. Don't infer.
- Partial approval is fine: delete only the approved paths, leave the rest with their
  current verdict (visible in the next report).

## Apply phase

After approval, for each approved path:

1. **Re-read the file immediately before deletion.** Repo state may have changed
   between gate and apply (someone else committed updates). If the body now
   contradicts the rationale, abort that path and surface in the report.
2. **Re-check references with one more grep.** Same reason — defense in depth.
3. Delete the file.
4. If the candidate was linked from a sibling index (`README.md`), update the index
   in the same change.

## ADR special case

ADRs almost never delete. Defaults:

- `supersede` over `delete` for any ADR with content. There is no `archive` fallback
  — superseded ADRs stay in place with a header note.
- Delete an ADR only when it's empty, generated noise, or the operator **explicitly
  chooses delete over the safer alternatives** in the gate response.
- For superseded ADRs, the action is `add header "Superseded by: <newer-adr>" and
  keep the file` — not move, not delete. Superseded ADRs are still load-bearing
  history.
