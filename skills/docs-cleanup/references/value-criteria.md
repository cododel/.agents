# Value criteria: classification labels and signals

This is the rulebook the classifier (subagent or inline) uses to assign verdicts.
Eight labels, ordered from "definitely keep as-is" to "definitely remove."

There is intentionally **no `archive` verdict**. Closed issues either have extractable
documentation value (`promote-to-adr`, or — for non-decision value like durable current-state
behavior, ops procedures, or unique repros — `repair` to move the value into the right home first),
or they are `delete`. The `issue-writer:close` workflow enforces this at sweep time
with a mandatory pre-extraction check.

## The eight labels

| Label              | Meaning                                                                                          |
|--------------------|--------------------------------------------------------------------------------------------------|
| `keep`             | Still changes future engineering behavior. Open, accurate, useful as written.                    |
| `repair`           | Potentially useful but under-specified, stale in document details, missing evidence, or poorly formatted while the tracked work remains valid. Also covers "extract content into a different doc home (living contract via `$contract-writer` / runbook / troubleshooting / README) before close." |
| `close`            | Open/implementing issue is complete and verified; rename to `[CLOSED]` so the next `issue-writer:close` sweep handles it.         |
| `stale`            | Open issue has stale premises but completion is unverified; add review evidence without changing status.                        |
| `merge`            | Duplicate or fragmented record that should be folded into a canonical document.                  |
| `supersede`        | ADR or decision record replaced by a newer decision; mark superseded with link.                  |
| `promote-to-adr`   | Closed issue that's actually an architectural decision; should live as an ADR instead.           |
| `delete`           | Proposed removal because the content appears to have no unique long-term value; separate pre-delete evidence, recovery, and authority checks must still pass. |

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
- A decision invariant is tied to a significant choice and explains when that choice holds
- A data model, provider, framework, package manager, language, or runtime choice and
  its rationale are recorded
- The reason a legacy approach exists is captured (so future engineers don't
  re-debate it from scratch)
- A cross-cutting policy records the significant choice, alternatives, and rationale rather
  than only the current rule

## Keep a temporary feature brief if any of these is true

- Its feature is still under operator review or active implementation
- Its `Draft` questions still materially affect the feature contract
- Its `Agreed` scope is still the active implementation and acceptance reference

## Repair signals

A document is `repair` (not `delete`) when:

- The decision or issue is real, but the body is thin, vague, or missing key fields
- Filename status doesn't match body status (e.g. `[CLOSED]` filename, `Status: Open` body)
- Evidence (logs, repro steps, file paths, line numbers) is missing where the local
  template expects them
- Project guardrails (the local README's "respect these rules" list) are violated by
  the recommended fix or are absent from the rationale
- A completed temporary feature brief contains durable behavior not yet captured in a living
  contract; route it through `$contract-writer` before proposing deletion. A missing contract may be
  created when current semantics and ownership are already explicit; otherwise preserve the brief and
  surface the material contract decision.

## Close and stale signals (issues only)

A document is `close` when:

- The original problem is gone in the current codebase, but the issue still has
  `[OPEN]` or `[IMPLEMENTING]` status
- The fix can be pointed to (commit, PR, file path) — leave the issue file in place,
  rename to `[CLOSED]`, add a brief completion note. The next sweep
  (`issue-writer:close`) will handle extraction-then-delete.

A document is `stale` when its premises no longer match current evidence but completion
cannot be verified. Keep `Status: Open`, update `Last reviewed`, and recommend a concise
`Stale note` that states the evidence. Do not use stale as a fourth lifecycle status.

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

## Closed issues with no ADR signal

A `[CLOSED]` issue whose body does **not** preserve a significant choice and rationale
and whose unique knowledge (if any) is non-decision documentation is handled like this:

- If it establishes durable product, UI, API, domain, persistence, security, or current
  architecture behavior: mark `repair` with a note to update the existing living contract via
  `$contract-writer` before close. If none exists, `$contract-writer` may establish it when current
  semantics, language, scope, and ownership are already explicit; otherwise report the material fork.
- If it contains unique repros, commands, or procedures worth keeping: mark `repair`
  with a note to move that content into the appropriate home (runbook, troubleshooting
  doc, inline code comment) before close. The classifier's `recommended_alt` field
  carries the suggested target.
- If it contains nothing beyond what the fix commit already records: mark `delete`.
  The operator will run `issue-writer:close`, which re-checks for extractable value
  before any exact deletion, with a recovery gate for valid unrecoverable paths and a block for
  unresolved value/scope or invalid targets.

There is no `archive` verdict. Closed issues either get their value extracted into
a real doc home or they get deleted — they don't accumulate in an archive subdirectory.

## Promote-to-ADR signals (issues only)

A closed issue should be `promote-to-adr` only when its body and linked evidence preserve a significant
operator-made choice and specific rationale, such as:

- Non-trivial trade-off with rejected options spelled out
- A decision invariant tied to a choice between real alternatives
- Choice of data model, provider, framework, package manager, language, or runtime with
  concrete rationale
- Cross-cutting policy with the actual fork and rationale, not only the current rule
- Rationale for keeping a legacy approach
- "By design" decision

For these, **surface the `adr-writer:from-issue` flow** rather than promoting inline. It verifies
operator-decision evidence, groups only one coherent decision, writes provenance/backlinks, and keeps
source cleanup as a separate recovery-aware action under explicit cleanup intent.

## Delete signals

A classifier may propose `delete` when the fully read record has no apparent unique long-term value
or unresolved work, and no `repair` / `close` / `stale` / `merge` / `supersede` / `promote-to-adr` action
better preserves its meaning. Cite the observed redundancy; age or thin formatting is insufficient.

This is a value proposal in both audit and apply modes. It does not require a pre-delete subagent to
have already run or apply authorization to exist. The primary agent next runs the same read-only
one-candidate safety method inline or through a subagent, then separately proves recovery and mutation
authority. Complete evidence, no unresolved load-bearing references, preserved unique content, and
authorized exact-file cleanup are required before deletion. Index-only references may be repaired in
the same change under `pre-delete-method.md` and `delete-gate.md`; they are not silently ignored.

For `[CLOSED]` issue files specifically, prefer routing through `issue-writer:close`
rather than deleting via this skill's gate — `close` runs a second-pass pre-extraction
check that's tuned for issue bodies (rejected options, ops procedures, unique repros).
The two safety nets are intentional: this skill catches `delete` candidates that
shouldn't have been classified that way; `close` catches the same plus issue-specific
documentation patterns.

## What is NOT sufficient for `delete`

These signals are **insufficient on their own** — they often look like delete
candidates but usually deserve `repair`, `merge`, or `promote-to-adr`:

- Old age. A 3-year-old ADR may still be the only record of why X exists.
- Low priority. Urgency does not determine documentation value or severity.
- Weak formatting. Poor markdown is a `repair` task, not a delete reason.
- Looks duplicate-ish. Confirm with the classifier — superficial similarity isn't
  the same as actual duplication. Mark `merge` if confirmed.
- "We don't need this anymore." Need-now and value-as-history are different.
- Unique operational knowledge (procedure, repro, command sequence). That's `repair`
  with a note to move the content into a runbook or troubleshooting doc first.
- A temporary feature brief whose implementation is complete. Extract durable current-state value
  into the living contract through `$contract-writer`; extract rationale into an ADR only when it
  independently passes the significance gate; then use the normal recovery-aware delete control.

## Boundary cases the classifier surfaces

If a document is genuinely ambiguous (between `delete` and `repair`, or between
`promote-to-adr` and `repair`), the classifier returns label `ambiguous` plus a
reason. The orchestrator surfaces ambiguous items in the report for the user to
disambiguate manually — never silently picks the more-destructive option.
