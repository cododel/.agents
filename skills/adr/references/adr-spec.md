# ADR quality specification

This file is the shared definition used by ADR recording and audit procedures.

## 1. Identity and immutability

An Architecture Decision Record is a dated record of a significant **operator-made choice**. It
preserves the context, real alternatives, concrete rationale, consequences, and conditions under
which that choice should be reconsidered.

Keep the actual decision date separate from the record-creation date. Use evidenced dates; an old
Issue's open/close date or today's recording date does not establish when the operator decided.
When the decision date is unknown, say so and retain available source provenance.

An ADR is not current-state documentation, a feature specification, implementation plan, progress
tracker, code review, or a reconstruction of what the code seems to have decided.

Once `Accepted`, its decision reasoning is immutable. Allowed later edits are relationship/status
metadata and concise append-only review notes that do not rewrite history. A changed choice requires a
new successor ADR; the old record becomes `Superseded` or, when the whole area disappears without a
direct successor, `Deprecated`.

## 2. Operator-decision gate

Create an ADR only when evidence shows that the operator:

- understood a material fork or hard constraint;
- selected or explicitly proposed one path;
- established enough rationale to preserve honestly.

Code, dependencies, commits, and implementation shape can confirm that a decision was implemented;
they cannot prove who chose it or why. An auditor may surface an **ADR candidate for operator
confirmation**, but absence of a record is not a defect unless an actual decision and rationale can be
shown.

## 3. Significance gate

An ADR is usually warranted when the choice has one or more of:

- high reversal cost or long-lived persistence/data consequences;
- a stable interface, module/service ownership, or cross-system boundary;
- security, compliance, privacy, or failure-isolation consequences;
- a new external dependency or platform commitment with credible alternatives;
- a precedent likely to shape future implementation;
- substantial rejected alternatives whose rationale would otherwise be lost.

An ADR is usually unnecessary for a routine local implementation detail, execution order,
style/convention already owned elsewhere, or merely a description of current code. Reversibility
alone does not fail the gate: a reversible choice can establish a meaningful precedent or carry
substantial alternative rationale worth preserving. A mandatory choice can qualify when a concrete
consequential constraint explains the single option, as required below.

A small one-way choice may deserve an ADR; a large but routine reversible implementation may not.

## 4. Required quality

Record one independently supersedable choice and its concrete, evidenced reason. A reader should
understand both without the original conversation. A single-option decision names the constraint
that required it. Preserve a material trade-off when omitting it would change the meaning.

## 5. Proportionate depth

One paragraph can be the complete decision body. Include alternatives, consequences, assumptions
or links where they explain the choice or when to reconsider it. Use separate headings only as
needed. For irreversible or high-cost choices, explain material assumptions, validation or revisit
triggers, and rollback or migration consequences.

Never encode implementation completion percentages, checklists, or task status in the ADR filename or
body unless an established project convention explicitly requires a legacy field. Decision lifecycle
and implementation progress are separate concerns.

## 6. Contract relationship

Before creating a record, identify what enduring decision rationale it adds beyond the current owner
and task memory. If it only restates behavior, skip it. State the chosen outcome briefly; leave detailed
algorithms, formulas, acceptance checklists, and rollout procedures with their current owners. Include
historical detail only when necessary to understand the trade-off, clearly as decision-time context.

The ADR explains why a choice was made. A living contract explains what current implementations must
preserve. Link the artifacts when both exist; do not copy normative current-state rules into decision
history or treat an ADR as the only long-term implementation contract.

## 7. Corpus quality

Across a corpus:

- supersession chains and links are intact;
- no two live ADRs contradict each other without succession;
- placement/naming follow project convention;
- records are neither flooded with trivial choices nor missing known significant decisions
  that the operator explicitly chose and intended to preserve;
- drift is handled through a successor or deprecation, not body rewrites.

Reverse review may identify major implemented forks with no ADR as **candidates to discuss**, not as
historical facts. The next action is operator confirmation of whether a meaningful decision/rationale
exists, not automatic ADR generation.
