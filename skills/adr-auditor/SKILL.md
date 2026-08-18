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

1. **Discover scope.** Use `../_shared/repository-discovery.md`, local ADR indexes/templates, and 1–2
   representative records. Confirm scope only when several plausible ADR roots remain.
2. **Enumerate.** Record status, date, placement, links, and any proven legacy filename convention.
3. **Audit each ADR.** Apply the shared spec plus `references/audit-criteria.md`: operator-decision
   evidence, one-decision granularity, real alternatives/rationale, consequences, self-sufficiency,
   code drift, status truth, immutability, and ADR-as-current-contract leakage.
4. **Audit the corpus.** Check supersession chains, live conflicts, placement/naming, density/noise,
   and known significant operator decisions that were explicitly intended to be preserved.
5. **Surface candidates, not invented gaps.** Major unrecorded forks visible in code may be listed as
   `candidate-needs-operator-history`: ask whether a meaningful operator decision and rationale exist.
   Do not label absence as a defect merely because the repository uses a DB/framework/auth system.
6. **Report and gate.** Use `references/output-formats.md`; route actions through
   `references/remediation.md`.

## Scale and subagents

Audit up to about 10 ADRs inline. For a larger corpus, delegate coherent read-only batches using
`references/adr-classifier.md` and `references/audit-criteria.md`, then integrate compact structured
findings in the primary context. Use independent semantic judgment; a cheap model may scan links and
status fields but should not be the sole judge of rationale, drift, or historical decision evidence.

## Drift semantics

- **Decision drift:** reality moved to a different choice. The remedy is a successor ADR based on real
  operator rationale, then `Superseded` links.
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
