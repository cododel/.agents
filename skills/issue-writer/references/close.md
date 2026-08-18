# Close workflow

Sweep completed repository Issues after extracting durable value. Closed Issues are not a second
archive: keep active debt in the Issues root and move enduring knowledge to its canonical owner.

## Authority

A clear request to close/sweep/apply completed Issues authorizes exact local reversible lifecycle
edits and deletion of **tracked, clean, committed** source files that pass this workflow. A request to
audit/review only is read-only.

Require an exact operator checkpoint for untracked, staged/modified, symlinked, path-ambiguous, or
otherwise unrecoverable sources. Never infer remote tracker writes, commits in the primary checkout,
or broad directory deletion.

## 1. Resolve one Issues scope

Use shared discovery and `conventions.md`. If several project/module Issue roots are plausible, ask
which scope is intended; never sweep all roots by default.

## 2. Enumerate completed candidates

Use the proven local lifecycle convention. Under the fallback, take the union of:

```bash
find <issues-dir> -maxdepth 1 -type f \( -name '[[]CLOSED]*.md' -o -name '[[]RESOLVED*' \)
grep -lEi '^\*\*Status:\*\*[[:space:]]+(Closed|Resolved)' <issues-dir>/*.md
```

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

Current implementation shape alone is not ADR evidence. A contract may be created autonomously only
when current semantics, scope, language, and ownership are already explicit; otherwise report its
material decision gate.

A candidate is `safe-to-delete` only when no unique long-term value or unresolved work remains beyond
canonical docs, implementation, and committed history.

## 4. Prove recovery

For each `safe-to-delete` candidate, resolve canonical path, require a regular non-symlink file inside
the confirmed Issue root, and record a fingerprint.

- **Recoverable:** Git tracks the exact path; working tree and index are clean for it; current contents
  are present in a reachable commit.
- **Gated:** untracked, staged/modified, ignored-only, symlink/type/path ambiguity, or recovery is not
  proven.

In an explicit close/apply workflow, recoverable candidates need no second ceremonial approval.
Render a compact exact-path gate only for gated candidates:

```text
Unrecoverable/ambiguous Issue deletion:
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
5. remove the exact file and its unambiguous index entry.

Staging/committing follows checkout authority. Never use a broad glob or recursive delete.

## 6. Report

Return a compact semantic result:

- deleted recoverable paths/count;
- gated or drift-skipped paths and exact reason;
- ambiguous status records;
- blocked durable-value records grouped by contract/ADR/runbook/reopen route;
- index updates.

Do not paste Issue bodies or classify every retained open Issue.
