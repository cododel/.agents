---
name: docs-cleanup
description: "Audit and optionally apply broad cleanup across repository Issues, ADRs, briefs, incidents, and runbooks. Use for stale/duplicate docs or milestone cleanup; read-only unless the operator clearly requests cleanup/apply. Not for ADR-only audits or ordinary Issue authoring."
---

# Docs Cleanup

Classify repository documentation by long-term value, preserve unique knowledge in one canonical
owner, and remove proven noise without treating every local file deletion as irreversible.

## Modes and authority

- **Audit** is the default: classify, run safety checks, and recommend exact actions without mutation.
- **Apply** requires clear operator intent such as `clean up`, `apply the cleanup`, or `delete the
  proven stale docs`. That request authorizes exact local reversible repairs and deletion of candidates
  that pass the evidence and recovery gates below.
- A separate checkpoint remains required for untracked/modified/unrecoverable content, ambiguous
  scope/value, ADR-history deletion, broad globs/directories, or any remote/shared side effect.

Never infer apply intent from a request to inspect, review, audit, or report.

## Workflow

### 1. Discover scope

Read `../_shared/repository-discovery.md`. Resolve the exact docs root(s), local conventions, and Git
checkout. Ask only when several plausible project/module scopes remain; do not sweep an entire
monorepo by default.

### 2. Enumerate candidates

List Markdown documentation under the confirmed scope, excluding established archives, generated
output, dependencies, and unrelated trees. Record exact regular-file paths; do not follow symlinks or
construct delete globs.

### 3. Classify value

Read `references/value-criteria.md`.

- Up to 10 candidates: classify inline.
- More than 10: delegate coherent read-only batches using `references/classifier-method.md`, then
  integrate compact JSON verdicts in the primary context.

Valid outcomes include `keep`, `repair`, `close`, `stale`, `merge`, `supersede`,
`promote-to-adr`, `delete`, and `ambiguous`. Classification is not deletion authority.

### 4. Route durable value

Before removal, route unique value through `../_shared/durable-documentation.md`:

- significant operator decision history → `$adr-writer` / `from-issue`;
- stable current boundary behavior → `$contract-writer`;
- completed repository Issue → `$issue-writer` close workflow;
- repeatable operations/debugging knowledge → the relevant runbook/reference;
- active temporary brief → keep until its task/handoff value ends.

Recommend sibling workflows rather than silently turning a broad cleanup audit into several unrelated
mutating procedures.

### 5. Pre-delete checks and recoverability

For every `delete` candidate, run the read-only method in `references/pre-delete-method.md` (parallel
when useful). Downgrade candidates with incoming references, unique content, uncertain status, or a
safer semantic action.

Then apply `references/delete-gate.md` to classify each surviving candidate:

- **recoverable** — exact regular file inside scope, tracked by Git, current contents unmodified and
  committed, no unresolved references/value;
- **gated** — untracked, staged/modified, symlink/path ambiguity, absent proven recovery, or deletion of
  ADR history;
- **blocked** — failed evidence/value checks.

### 6. Apply or report

In audit mode, report only. In apply mode:

- apply unambiguous non-delete repairs requested by the operator;
- delete recoverable candidates by exact path without a second ceremonial approval;
- present a compact exact-path decision gate only for `gated` candidates;
- re-resolve path, type, contents, references, Git state, and fingerprint immediately before mutation;
- update an unambiguous index in the same change; otherwise report it.

Never delete via glob/directory, reinterpret a bulk phrase as approval for an unseen set, or claim Git
recovery for content not proved committed.

### 7. Handoff

Use `references/output-formats.md`. Report counts, actions actually applied, blocked/gated items,
durable-value routing, and any scope/evidence that could not be checked. Do not dump document bodies or
subagent transcripts.

## Subagent contract

For large classification, pass `references/classifier-method.md`, `references/value-criteria.md`,
repo root, scope context, and coherent candidate batches. For delete safety, pass
`references/pre-delete-method.md`, one candidate, repo root, and scope context. Subagents are read-only
and return JSON; the primary agent owns classification, recoverability, and mutation.
