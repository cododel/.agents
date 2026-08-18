# Recovery-aware delete control

A delete candidate must pass both a **value check** and a **recovery check**. Local deletion is not
inherently irreversible: an exact tracked file whose current contents are clean and committed can be
reviewed and restored. Untracked, modified, ambiguous, or historical-decision content is different and
requires an operator checkpoint.

## 1. Evidence gate

Run `pre-delete-method.md` first. A candidate is not deletable when it has:

- load-bearing incoming references;
- unique rationale, evidence, commands, repros, or current normative behavior;
- uncertain lifecycle/status;
- a better `repair`, `close`, `stale`, `merge`, `supersede`, or `promote-to-adr` action.

Downgrade it and route the value. Do not use deletion to resolve uncertainty.

## 2. Recovery classification

Immediately before apply, prove each remaining candidate is a regular non-symlink file inside the
confirmed scope and record a content fingerprint.

Classify **recoverable** only when all are true:

1. Git tracks the exact path;
2. working-tree and index contents for that path are unchanged from a committed revision;
3. the committed blob containing the current contents is reachable in the repository;
4. no concurrent drift occurred since pre-check;
5. the requested cleanup/apply intent covers this scope.

Classify **gated** when any are true:

- untracked, staged, modified, ignored-only, or not proven committed;
- symlink, path escape, type change, or scope ambiguity;
- recovery depends on an unverified backup rather than current Git evidence;
- the candidate is an ADR or other intentional immutable history;
- the operator requested audit/review but not mutation.

A `blocked` evidence verdict never becomes deletable through the recovery check.

## 3. Authorization behavior

- In **audit mode**, delete nothing.
- In **apply mode**, exact recoverable candidates may be deleted without a second round-trip.
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
5. remove the exact file and update an unambiguous index/link owner in the same change.

Staging/committing follows checkout authority. Never use a broad glob or recursive directory delete.

## ADR special case

Prefer `supersede` or `deprecate` over deletion. Even when Git-recoverable, deleting meaningful ADR
history requires explicit exact-path operator intent because the semantic loss is the action, not only
the filesystem recovery risk. Empty/generated duplicates may be proposed, never inferred.
