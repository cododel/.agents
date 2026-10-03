# Recovery-aware delete control

A delete candidate must pass both a **value check** and a **recovery check**. Local deletion is not
inherently irreversible: an exact tracked file whose current contents are clean and committed can be
reviewed and restored. Valid untracked/modified content needs a separate recovery checkpoint;
historical-decision deletion needs explicit semantic authority. Unresolved value or target validity
blocks deletion regardless of approval.

## 1. Evidence gate

Run `pre-delete-method.md` first. A candidate is not deletable when it has:

- load-bearing incoming references without a verified replacement owner/link repair;
- unique rationale, evidence, commands, repros, or current normative behavior;
- uncertain lifecycle/status;
- a better `repair`, `close`, `stale`, `merge`, `supersede`, or `promote-to-adr` action.

Downgrade it and route the value. Do not use deletion to resolve uncertainty.
Unavailable or incomplete required checks are `inconclusive` and block deletion. Untested booleans
remain `null`, never false. A `safe_to_delete` result is evidence only; it grants no mutation authority.

An unambiguous index-only entry is a repairable reference when the exact entry removal/redirection is
planned in the same change, with remaining links rechecked. A semantic reference that depends on the
document's content stays blocking until that meaning has a verified owner and its link is repaired.
If the repair is ambiguous or cannot complete, retain the candidate.

## 2. Recovery classification

Immediately before apply, prove each remaining candidate is a regular non-symlink file inside the
confirmed scope and record a content fingerprint.

Classify **recoverable** only when all are true:

1. Git tracks the exact path;
2. working-tree and index contents for that path are unchanged from a committed revision;
3. the committed blob containing the current contents is reachable in the repository;
4. no concurrent drift occurred since pre-check.

Classify **blocked** when the target is a symlink, escapes the confirmed root, has an invalid or
changed type, or its exact scope remains unresolved. Correct the target and rerun checks; no approval
phrase can bypass target validity or failed/incomplete evidence.

For a valid exact-file target, classify **gated** when any are true:

- untracked, staged, modified, ignored-only, or not proven committed;
- recovery depends on an unverified backup rather than current Git evidence;
- the candidate is an ADR or other intentional immutable history;

Audit/review mode remains read-only regardless of recovery class; report the proposal and required
apply intent without treating audit authority as file evidence.

A `blocked` evidence verdict never becomes deletable through the recovery check.

## 3. Authorization behavior

- In **audit mode**, delete nothing.
- In **apply mode**, exact recoverable candidates may be deleted without a second round-trip only
  when the cleanup request covers their confirmed scope and action. Recovery evidence alone is not
  authorization.
- For gated candidates, show only the affected exact paths, fingerprint/recovery state, reason for the
  gate, and safer alternative. Require an exact-path choice such as:

```text
approve unrecoverable delete: <path>
keep: <path>
repair: <path>
cancel
```

A phrase such as `approve all` is valid only when it clearly refers to the already rendered gated
list and no candidate changed afterward. It never authorizes paths that were not shown.

## 4. Apply checkpoint

For every authorized path:

1. re-resolve canonical path and require a regular non-symlink file inside scope;
2. re-read and recompute fingerprint;
3. repeat the decisive reference and Git-state checks;
4. abort only that path on drift;
5. apply the planned unambiguous index/link repair and remove the exact file in the same change;
6. recheck repaired/remaining references; restore only this task's exact deletion if the repair
   failed, and report the candidate as retained/blocked.

Staging/committing follows checkout authority. Never use a broad glob or recursive directory delete.

## ADR special case

Prefer `supersede` or `deprecate` over deletion. Even when Git-recoverable, deleting meaningful ADR
history requires explicit exact-path operator intent because the semantic loss is the action, not only
the filesystem recovery risk. Empty/generated duplicates may be proposed, never inferred.
