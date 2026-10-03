# Close workflow

Sweep completed repository Issues after extracting durable value. Closed Issues are not a second
archive: keep active debt in the Issues root and move enduring knowledge to its canonical owner.

## Authority

A clear request to close/sweep/apply completed Issues authorizes exact local reversible lifecycle
edits and deletion of **tracked, clean, committed** source files that pass this workflow. A request to
audit/review only is read-only.

Require an exact operator checkpoint for valid untracked, staged/modified, or otherwise unrecoverable
sources. Symlink, path escape, invalid type, or unresolved scope is blocked until corrected and
rechecked; approval cannot bypass target validity. Never infer remote tracker writes, commits in the
primary checkout, or broad directory deletion. Review mode performs the same diagnosis without
lifecycle edits, extraction writes, index changes, or deletion.

## 1. Resolve one Issues scope

Use shared discovery and `conventions.md`. If several project/module Issue roots are plausible, ask
which scope is intended; never sweep all roots by default.

## 2. Enumerate completed candidates

Use the proven local lifecycle convention. Enumerate regular Markdown files with `rg --files` or
`fd`, then parse the complete filename tag and complete body status value. Under the fallback,
completed candidates have exactly `[CLOSED]` and `Closed`. Recognize exact legacy `Resolved` or
percent-status syntax only when the local convention proves it. A file whose filename or body
indicates completion enters mismatch review; loose prefixes such as `[CLOSEDNESS]`, `[RESOLVED-old]`,
or `Closed pending verification` do not establish completion.

Compare filename and body status. Mismatches are `ambiguous`: keep them and report the exact conflict.
Do not silently decide whether work is complete.

## 3. Extract-value gate

Read every non-ambiguous candidate in full and route unique value through
`../../_shared/durable-documentation.md`.

Block source deletion when it contains value not yet owned elsewhere, including:

- significant operator decision with real alternatives/rationale → `$adr-writer:from-issue`;
- non-obvious stable product/UI/API/domain/persistence/security/module behavior → existing or justified
  missing living contract through `$contract-writer`;
- repeatable operation, recovery, incident, or diagnostic technique → runbook/reference/test/comment;
- unresolved work, risk, or completion criterion → reopen/repair rather than close.

Current implementation shape alone is not ADR evidence. Preserve actual operator-decision intent;
an Issue close request does not itself authorize ADR creation. Use `$adr-writer` only when promotion
authority is explicit, otherwise retain the source and report the route. Contract extraction requires
all four value conditions for a new owner, confirmed semantics/scope/language/ownership, and authoring
authority covering the change. Review mode never invokes writers or silently records new debt.

A candidate is `safe-to-delete` only when no unique long-term value or unresolved work remains beyond
canonical docs, implementation, and committed history.

## 3.5. Check incoming references

Before deletion, search the confirmed repository for the exact filename/path, slug, and distinctive
decision/problem identifiers, excluding generated/dependency trees and the candidate itself. Trace
actual links rather than treating every text match as load-bearing.

- A semantic reference depending on the Issue's evidence/rationale blocks deletion until that
  content has a verified canonical owner and the reference is repaired.
- An unambiguous index-only entry may be removed or redirected through an exact planned repair in
  the same change, followed by recheck.
- Unknown reference meaning, incomplete search, or an ambiguous repair keeps the source.

Do not replace links to historical decision evidence with a current contract that drops its rationale.
If an ADR receives the history, retain its verified source provenance (reachable committed SHA plus
repository-relative path) when the Issue will be deleted. Choose retained versus deletion-bound
sources before backlink edits using `../../adr-writer/references/from-issue.md`; a newly modified backlink
does not satisfy the original clean-source gate.

## 4. Prove recovery

For each `safe-to-delete` candidate, resolve canonical path, require a regular non-symlink file inside
the confirmed Issue root, and record a fingerprint.

- **Recoverable:** Git tracks the exact path; working tree and index are clean for it; current contents
  are present in a reachable commit whose SHA and repository-relative path are recorded.
- **Gated:** valid untracked, staged/modified, ignored-only files, or recovery is not
  proven.
- **Blocked:** invalid symlink/type/path/scope, unresolved value/status/reference, or incomplete checks.

Never auto-commit or stage a modified source to make recovery look proven. A planned backlink or
extraction edit changes source state and requires a fresh recovery assessment; preserve exact current
contents and separate their state from the committed version.

In an explicit close/apply workflow, recoverable candidates need no second ceremonial approval.
Render a compact exact-path gate only for gated candidates:

```text
Issue deletion requiring a recovery checkpoint:
- <path> — <state, fingerprint, why recovery is not proven>

Reply with:
- approve unrecoverable delete: <path>[, <path>]
- keep: <path>[, <path>]
- cancel
```

A bulk approval applies only to the already rendered exact list and only while fingerprints/state stay
unchanged. It never authorizes unseen paths. Blocked value candidates cannot be overridden through
this recovery gate; extract/resolve their value first.

## 5. Apply

Immediately before each authorized deletion:

1. re-resolve path/type/scope and re-read the file;
2. recompute fingerprint and Git state;
3. repeat the decisive status/value/reference check;
4. skip that path on drift;
5. apply planned unambiguous index/link repairs and remove the exact file in the same change;
6. recheck remaining/repaired incoming links; if repair fails, restore only this task's exact
   deletion and retain/report that source.

Staging/committing follows checkout authority. Never use a broad glob or recursive delete.

## 6. Report

Return a compact semantic result:

- deleted recoverable paths/count;
- gated or drift-skipped paths and exact reason;
- ambiguous status records;
- blocked durable-value records grouped by contract/ADR/runbook/reopen route;
- index updates.

Do not paste Issue bodies or classify every retained open Issue.
