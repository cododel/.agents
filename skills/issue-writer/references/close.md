# Close workflow

Review, close, or remove repository Issues according to the requested lifecycle action. Closure
records verified completion; source removal additionally requires preservation of durable value.

## Authority

Review is read-only. An explicit close request authorizes the selected Issue's verified status
transition and applicable index update, retaining its source by default. Removal requires an
operator instruction covering deletion and its scope, or an established local lifecycle that
makes removal part of the requested closure. Do not infer deletion from the word "close" alone.

Every deletion uses [the shared procedure](../../_shared/document-deletion.md), including its
recovery and authority gates. Lifecycle work never authorizes remote tracker writes or commits in
the primary checkout. Review permits no lifecycle edits, extraction writes, index changes or deletion.

## 1. Resolve one Issues scope

Use shared discovery and `conventions.md`. If several project/module Issue roots are plausible, ask
which scope is intended; never sweep all roots by default.

## Review a selected Issue for relevance or completion

A request such as "is this Issue still relevant?", "was it already fixed?", or "can we close it?"
authorizes read-only review of the selected record, including an open Issue. It does not authorize
closure, deletion, repairs, or a sweep of other records. Read the report and its completion criteria;
extract concrete symptoms, triggering conditions, environment, and report date.

Check the current affected code path and relevant Git changes against those claims. A removed error
string can be a rename or move; inspect the actual change before calling it a fix. Use runtime or
data evidence when the claim depends on it, through project-approved access only. Code, history,
and live data are complementary sources, not three mandatory gates for every Issue. Distinguish a
fix in the inspected checkout from a fix verified in the deployed version.

Accepted unresolved debt is not resolved by acceptance alone. Preserve its decision and reconsideration
conditions; do not start repair or mark it completed merely because a lifecycle review was requested.

Report one of: relevant, resolved, currently unobserved, or inconclusive. Zero matching rows or no
recent events establishes only the observed scope and time; it does not prove the defect cannot
recur. Cite applicable file/line, commit/date, or scoped runtime/query evidence and name the precise
evidence gap when inconclusive. Preserve source status separately from the review conclusion.
A deeper causal investigation belongs to `troubleshooter`; an overview/grouping of multiple problems
belongs to `issue-triage`. Neither handoff grants authority to repair or mutate records.

For a relevance-only request, stop with the conclusion and next decision. If closure is authorized
and completion is verified, update status and the unambiguous index under local conventions. Under
the fallback, set the body status to `Closed` and retain the stable filename and source. If completion
is unresolved, retain the current status and report the gap. Accepted unresolved debt remains open.
Proceed to removal only when that action is authorized; a status change alone does not establish
safe deletion or recoverability of the newly modified source.

## 2. Enumerate authorized removal candidates

For authorized removal, use the proven local lifecycle convention. Enumerate regular Markdown files with `rg --files` or
`fd`. Under the stable-name fallback, a completed candidate has the exact body status `Closed`;
the filename carries no status. Missing, conflicting or unrecognized status values are ambiguous,
not evidence of completion. Do not infer status from prose mentioning a closed issue.

For established status-prefixed conventions, parse and compare complete filename tags and body
status values. The previous fallback requires exactly `[CLOSED]` and `Closed`. Recognize legacy
`Resolved` or percent-status syntax only when the local convention proves it. If either representation
indicates completion but the other disagrees, retain the source and report the mismatch. Loose
prefixes such as `[CLOSEDNESS]`, `[RESOLVED-old]`, or `Closed pending verification` do not establish
completion. Candidate status alone never replaces the completion, value, reference and recovery gates.

## 3. Extract-value gate

Read every non-ambiguous candidate in full and route unique value through
`../../_shared/durable-documentation.md`.

Block source deletion when it contains value not yet owned elsewhere, including:

- significant operator decision with real alternatives/rationale → `$adr:from-issue`;
- non-obvious stable product/UI/API/domain/persistence/security/module behavior → existing or justified
  missing living contract through `$contract-writer`;
- repeatable operation, recovery, incident, or diagnostic technique → runbook/reference/test/comment;
- unresolved work, risk, or completion criterion → retain; reopen only within authorized lifecycle
  scope, otherwise report the mismatch. This workflow does not authorize implementation repairs.

Current implementation shape alone is not ADR evidence. Preserve actual operator-decision intent;
an authorized extraction/removal workflow may preserve a fully evidenced significant agreed decision through
`$adr` without a separate promotion request. Do not create an ADR merely because an Issue closes.
If evidence is incomplete, retain the source and report the gap; do not invent rationale or expand
into a retrospective ADR sweep. Contract extraction requires all four value conditions for a new owner, confirmed semantics/scope/language/ownership, and authoring
authority covering the change. Review mode never invokes writers or silently records new debt.

A candidate is `safe-to-delete` only when no unique long-term value or unresolved work remains beyond
canonical docs, implementation, and committed history.

## 3.5. Check incoming references

Use the shared procedure's reference check; preserve the following Issue-specific provenance.

Do not replace links to historical decision evidence with a current contract that drops its rationale.
If an ADR receives the history, retain its verified source provenance (reachable committed SHA plus
repository-relative path) when the Issue will be deleted. Choose retained versus deletion-bound
sources before backlink edits using `../../adr/references/from-issue.md`; a newly modified backlink
does not satisfy the original clean-source gate.

## 4. Delete eligible sources

After completion and value checks, apply [document deletion](../../_shared/document-deletion.md)
to each exact eligible source. Its final recheck includes this workflow's status/completion criteria
and extraction/provenance; `Closed` alone never establishes eligibility. A recovery checkpoint cannot
substitute for these requirements. Keep the existing report below rather than creating another ledger.

## 5. Report

Return a compact semantic result:

- review conclusion and any verified status changes;
- retained sources or deleted recoverable paths/count, according to the requested action;
- gated or drift-skipped paths and exact reason;
- ambiguous status records;
- blocked durable-value records grouped by contract/ADR/runbook/reopen route;
- index updates.

Do not paste Issue bodies or classify every retained open Issue.
