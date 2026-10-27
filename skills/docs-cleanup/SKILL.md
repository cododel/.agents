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
5. For delete candidates, apply [document deletion](../_shared/document-deletion.md) for target
   validity, recovery, authority and final state/reference checks. Reuse step 4 evidence; the shared
   procedure does not replace this workflow's value classification.
6. Load `references/output-formats.md` for the audit/applied result: scope, counts, actual actions,
   gated/blocked/drifted paths, routing, and incomplete evidence. Do not dump bodies or transcripts.

## Historical decision deletion

Prefer `supersede` or `deprecate` over deleting ADR history. Even when Git-recoverable, deleting
meaningful ADR history requires explicit exact-path operator intent: semantic loss is distinct from
filesystem recovery. Empty/generated duplicates may be proposed, never inferred. Other intentional
immutable history also needs its scenario-specific semantic authority; ordinary cleanup is insufficient.
Remote/shared actions remain outside this local cleanup scope.

Delegated methods define their input/JSON contracts. Reviewers stay read-only; the primary agent
verifies their source evidence and owns classification, recovery, and mutation.
