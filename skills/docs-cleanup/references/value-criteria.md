# Value criteria: classification labels and signals

This is the rulebook the classifier (subagent or inline) uses to assign verdicts.
Seven labels, ordered from "definitely keep as-is" to "definitely remove."

There is intentionally **no `archive` verdict**. Resolved issues either have extractable
documentation value (`promote-to-adr`, or — for non-architectural value like ops
procedures or unique repros — `repair` to move the value into the right home first),
or they are `delete`. The `issue-writer:close` workflow enforces this at sweep time
with a mandatory pre-extraction check.

## The seven labels

| Label              | Meaning                                                                                          |
|--------------------|--------------------------------------------------------------------------------------------------|
| `keep`             | Still changes future engineering behavior. Active, accurate, useful as written.                  |
| `repair`           | Potentially useful but under-specified, stale on details, missing evidence, or poorly formatted. Also covers "extract content into a different doc home (runbook / troubleshooting / README) before close." |
| `resolve`          | Active issue is no longer actionable (fix has landed); rename to `[RESOLVED]` so the next `issue-writer:close` sweep handles it. |
| `merge`            | Duplicate or fragmented record that should be folded into a canonical document.                  |
| `supersede`        | ADR or decision record replaced by a newer decision; mark superseded with link.                  |
| `promote-to-adr`   | Resolved issue that's actually an architectural decision; should live as an ADR instead.         |
| `delete`           | No unique long-term value remains after reference and evidence checks.                           |

## Keep an issue if any of these is true

- An open action item remains
- Reproducible evidence of a real problem
- An unresolved risk
- A recurring symptom pattern (look for `## Incidents` sections with multiple rows)
- Production, financial, security, or data-integrity relevance
- Knowledge not captured anywhere else (rare commands, hard-won SQL, operator
  procedure)

## Keep an ADR if any of these is true

- A non-trivial trade-off with rejected options is documented
- An architectural invariant or system boundary is established
- A data model, provider, framework, package manager, language, or runtime choice is
  recorded
- The reason a legacy approach exists is captured (so future engineers don't
  re-debate it from scratch)
- A cross-cutting policy (auth, errors, logging, i18n, deploy, security) is set

## Repair signals

A document is `repair` (not `delete`) when:

- The decision or issue is real, but the body is thin, vague, or missing key fields
- Filename status doesn't match body status (e.g. `[RESOLVED]` filename, `Status:
  Active` body)
- Evidence (logs, repro steps, file paths, line numbers) is missing where the local
  template expects them
- Project guardrails (the local README's "respect these rules" list) are violated by
  the recommended fix or are absent from the rationale

## Resolve signals (issues only)

A document is `resolve` when:

- The original problem is gone in the current codebase, but the issue still has
  `[ACTIVE]` or `[INVESTIGATING]` status
- The fix can be pointed to (commit, PR, file path) — leave the issue file in place,
  rename to `[RESOLVED]`, add a brief resolution note. The next sweep
  (`issue-writer:close`) will handle extraction-then-delete.

## Merge signals

A document is `merge` when:

- Multiple files describe the same incident, decision, or symptom — common when
  several people opened separate issues independently
- A long-running issue has spawned several follow-up issues that didn't get linked
  back to the parent

## Supersede signals (ADRs only)

A document is `supersede` when:

- A newer ADR explicitly contradicts or replaces it
- The system has clearly moved on (the ADR's chosen option is no longer in the code,
  and a different approach has its own ADR)

The action: keep the file, add a `**Superseded by:** <newer-adr-path>` header line.
Do not delete superseded ADRs — they explain why the current state was chosen.

## Resolved issues with no ADR signal

A `[RESOLVED]` issue whose body does **not** match any promote-to-ADR signal (no
rejected options, no invariant, no framework/policy choice) and whose unique knowledge
(if any) is operational, not architectural, is handled like this:

- If it contains unique repros, commands, or procedures worth keeping: mark `repair`
  with a note to move that content into the appropriate home (runbook, troubleshooting
  doc, inline code comment) before close. The classifier's `recommended_alt` field
  carries the suggested target.
- If it contains nothing beyond what the fix commit already records: mark `delete`.
  The operator will run `issue-writer:close`, which re-checks for extractable value
  in its own gate before any `rm`.

There is no `archive` verdict. Resolved issues either get their value extracted into
a real doc home or they get deleted — they don't accumulate in an archive subdirectory.

## Promote-to-ADR signals (issues only)

A resolved issue should be `promote-to-adr` when its body matches any of:

- Non-trivial trade-off with rejected options spelled out
- Establishes an architectural invariant
- Choice of data model, provider, framework, package manager, language, runtime
- Cross-cutting policy
- Rationale for keeping a legacy approach
- "By design" decision

For these, **surface the `adr-writer:from-issue` flow** rather than doing the
promote inline. That flow has the proper merge support and deletes the source issue
after the ADR is saved (with explicit operator confirmation).

## Delete signals

A document is `delete` only when **all** of these are true:

- The pre-delete-checker subagent confirmed no incoming references
- Content is not unique (rationale, evidence, commands not preserved elsewhere)
- No `repair` / `merge` / `supersede` / `promote-to-adr` is a better fit
- Operator approves explicitly via the gate

For `[RESOLVED]` issue files specifically, prefer routing through `issue-writer:close`
rather than deleting via this skill's gate — `close` runs a second-pass pre-extraction
check that's tuned for issue bodies (rejected options, ops procedures, unique repros).
The two safety nets are intentional: this skill catches `delete` candidates that
shouldn't have been classified that way; `close` catches the same plus issue-specific
documentation patterns.

## What is NOT sufficient for `delete`

These signals are **insufficient on their own** — they often look like delete
candidates but usually deserve `repair`, `merge`, or `promote-to-adr`:

- Old age. A 3-year-old ADR may still be the only record of why X exists.
- Low priority. P3 doesn't mean "no value."
- Weak formatting. Poor markdown is a `repair` task, not a delete reason.
- Looks duplicate-ish. Confirm with the classifier — superficial similarity isn't
  the same as actual duplication. Mark `merge` if confirmed.
- "We don't need this anymore." Need-now and value-as-history are different.
- Unique operational knowledge (procedure, repro, command sequence). That's `repair`
  with a note to move the content into a runbook or troubleshooting doc first.

## Boundary cases the classifier surfaces

If a document is genuinely ambiguous (between `delete` and `repair`, or between
`promote-to-adr` and `repair`), the classifier returns label `ambiguous` plus a
reason. The orchestrator surfaces ambiguous items in the report for the user to
disambiguate manually — never silently picks the more-destructive option.
