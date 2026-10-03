---
name: docs-cleanup
description: "Audit and optionally apply broad cleanup across repository Issues, ADRs, briefs, incidents, and runbooks. Use for stale/duplicate docs or milestone cleanup; read-only unless the operator clearly requests cleanup/apply. Not for ADR-only audits or ordinary Issue authoring."
---

# Docs Cleanup

Classify documentation by durable value and preserve it in one canonical owner. Default to read-only
audit. Clear cleanup/apply intent authorizes only exact local actions within the confirmed scope and
the evidence/recovery gates; review/report requests do not authorize mutation.

## Load by stage

1. Resolve roots/conventions with `../_shared/repository-discovery.md`. Preserve exact requested scope;
   do not sweep a monorepo by default. Enumerate regular Markdown files, excluding archives,
   dependencies, generated output, and unrelated trees; do not follow symlinks.
2. Read `references/value-criteria.md` for classification. `delete` is a value proposal, independent
   of safety evidence and apply authority. Review inline or delegate coherent read-only batches when
   complexity/context makes that useful; count alone does not require delegation. Load
   `references/classifier-method.md` only when delegating classification.
3. Load `../_shared/durable-documentation.md` when unique value needs routing. Recommend the relevant
   writer/Issue/runbook workflow within its authority; a cleanup audit does not silently invoke
   unrelated mutations. Keep active task/handoff material.
4. For each proposed delete, load `references/pre-delete-method.md` and run its one-candidate read-only
   checks inline or through a reviewer. Incomplete/unavailable checks are `inconclusive`; untested
   booleans are `null`. A safe evidence result does not grant authority. Unresolved semantic references
   and unique value block removal; index-only links require exact same-change repair and recheck.
5. For delete candidates, load `references/delete-gate.md` to prove recovery, resolve any exact-path
   checkpoint, and perform final state/reference rechecks. Audit mode reports only. Apply mode may
   perform covered unambiguous repairs and exact recoverable deletes; never use globs/directories or
   claim recovery for unproven contents.
6. Load `references/output-formats.md` for the audit/applied result: scope, counts, actual actions,
   gated/blocked/drifted paths, routing, and incomplete evidence. Do not dump bodies or transcripts.

## Non-bypassable gates

Valid untracked/modified/unrecoverable content requires a separate recovery checkpoint; meaningful
ADR-history deletion requires explicit exact-path semantic authority. Unresolved value/scope or
invalid symlink/path/type targets are blocked, never approval bypasses. Bulk approval covers only an
already shown unchanged exact list. Remote/shared actions remain outside this local cleanup scope.

Delegated methods define their input/JSON contracts. Reviewers stay read-only; the primary agent
verifies their source evidence and owns classification, recovery, and mutation.
