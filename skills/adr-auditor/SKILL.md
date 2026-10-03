---
name: adr-auditor
description: "Audit ADR corpora when the operator asks for decision-quality, drift, immutability, lifecycle, supersession, or current-contract review. Read-only by default; never infer historical decisions or create ADRs from code shape."
---

# ADR Auditor

Audit existing decision history within the exact requested paths and dimensions. Default to read-only
diagnosis; remediation needs explicit authorization covering the shown actions. Never rewrite
Accepted reasoning or delete ADR history as routine cleanup. Code divergence does not establish a
changed operator choice.

## Workflow

1. Resolve scope using `../_shared/repository-discovery.md` and proven local indexes/templates. Read
   related records only to resolve the requested check; a narrow link/immutability request does not
   expand into a corpus or code audit.
2. Use `../adr-writer/references/adr-spec.md` as the quality/lifecycle specification and
   `references/audit-criteria.md` for the requested checks. Preserve their decision-authority,
   drift-versus-violation, acceptance-baseline, and immutability coverage rules. Excluded or incomplete
   checks are reported honestly, never as `clean`.
3. Review inline or delegate bounded read-only batches when complexity/context makes that useful;
   count alone does not force delegation. Load `references/adr-classifier.md` only when delegating.
   Give reviewers the same scope and criteria; integrate source evidence, not conclusions alone.
4. Check corpus relationships/conflicts/density or reverse candidates only when requested. Code can
   surface `candidate-needs-operator-history`; it cannot invent missing decisions or rationale.
5. Load `references/output-formats.md` to report findings, uncertainty, exact coverage, and hand-offs.
   Load `references/remediation.md` when proposing or applying specific actions. It owns permitted
   metadata/link/status/placement repairs and writer hand-offs; it never permits routine deletion.

For `adr-as-current-contract`, recommend `$contract-writer` under its value and authoring gates.
Diagnosis does not authorize a writer. A partial audit is not a clean corpus result.
