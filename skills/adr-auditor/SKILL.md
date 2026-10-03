---
name: adr-auditor
description: "Audit ADR corpora when the operator asks for decision-quality, drift, immutability, lifecycle, supersession, or current-contract review. Read-only by default; never infer historical decisions or create ADRs from code shape."
---

# ADR Auditor

Measure existing ADRs against `../adr-writer/references/adr-spec.md` without rewriting history or
pretending that implementation shape proves a past operator decision.

## Output boundary

The default output is a diagnosis and remediation plan. Mutation requires an explicit operator request
after the exact actions are shown. Never rewrite the reasoning body of an Accepted ADR or delete ADR
history as routine cleanup.

## Workflow

1. **Discover scope.** Preserve the exact requested paths, roots, and audit dimensions. Use
   `../_shared/repository-discovery.md`, local ADR indexes/templates, and the minimum representative
   records needed to prove conventions. Confirm scope only when several plausible ADR roots remain.
   A narrow link or immutability audit does not authorize a full corpus/code audit; related records
   may be read only to resolve the requested check, with coverage stated explicitly.
2. **Enumerate.** Record the status/date/placement/link fields relevant to the requested checks and
   any proven local convention needed to interpret them.
3. **Audit each ADR.** Apply only requested dimensions from the shared spec and
   `references/audit-criteria.md`: operator-decision
   evidence, one-decision granularity, real alternatives/rationale, consequences, self-sufficiency,
   code drift, status truth, immutability, and ADR-as-current-contract leakage.
4. **Audit the requested corpus dimensions.** Within scope, check supersession chains, live conflicts,
   placement/naming, density/noise,
   and known significant operator decisions that were explicitly intended to be preserved.
5. **Surface candidates, not invented gaps.** When reverse discovery is requested, major unrecorded
   forks visible in code may be listed as
   `candidate-needs-operator-history`: ask whether a meaningful operator decision and rationale exist.
   Do not label absence as a defect merely because the repository uses a DB/framework/auth system.
6. **Report and gate.** Use `references/output-formats.md`; route actions through
   `references/remediation.md`.

## Scale and subagents

Use inline review or coherent read-only batches according to the requested checks, corpus complexity,
available independence, and context cost. A record count alone does not force delegation. When
delegating, use `references/adr-classifier.md` and `references/audit-criteria.md`, preserve the same
scope, and integrate compact evidence. Use independent semantic judgment for rationale, drift, and
historical decision evidence; link/status scanning alone does not settle them.

## Drift semantics

- **Decision drift:** evidence establishes that the operator changed the choice. The remedy is a
  successor ADR based on that real rationale, then `Superseded` links. Different code alone proves
  implementation divergence; it does not prove the old decision was replaced.
- **Violated current invariant:** the decision may still hold while code is wrong. Route to
  implementation/contract review, not an ADR rewrite.
- **Area removed:** mark `Deprecated` when no direct successor exists.
- **Unknown history:** report ambiguity. Code can show current state, not why it was chosen.

## Contract relationship

When an ADR is the only place maintainers can find current normative behavior, classify
`adr-as-current-contract`. `$contract-writer` may establish the missing owner when current semantics
and ownership are unambiguous; otherwise it stops for the operator fork. Backfill relationship links
without copying normative prose into the ADR.

## Mutation rules

On explicit remediation request, the auditor may apply metadata/link/status/placement normalization
that leaves reasoning intact. Successors, split decisions, rationale backfills, and new operator
choices are handed to `$adr-writer`. Deletion is never part of normal ADR remediation.

Report what could not be checked, especially missing Git history or unavailable implementation
evidence. A partial audit is not a clean result.
