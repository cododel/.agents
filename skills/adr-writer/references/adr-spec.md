# ADR quality specification

This file is the shared definition used by `adr-writer` and `adr-auditor`.

## 1. Identity and immutability

An Architecture Decision Record is a dated record of a significant **operator-made choice**. It
preserves the context, real alternatives, concrete rationale, consequences, and conditions under
which that choice should be reconsidered.

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

An ADR is usually unnecessary when the choice is cheap and reversible, mandated with no real fork,
local implementation detail, execution order, style/convention already owned elsewhere, or merely a
description of current code.

A small one-way choice may deserve an ADR; a large but routine reversible implementation may not.

## 4. Required quality

A good ADR has:

- **one decision** that can be superseded independently;
- **concrete context and forces** specific to this system;
- **real alternatives** actually considered, including status quo only when it was a viable option;
- **specific rejection/selection reasons**, not generic best-practice language;
- **a precise decision outcome** understandable without the original chat;
- **honest positive and negative consequences**;
- **material assumptions or decision invariants** that explain when the choice still holds;
- **validation or revisit triggers** proportionate to reversal cost and uncertainty;
- **valid lifecycle/status and relationship links**.

A single-option ADR is valid only when the option was genuinely mandated and the document records the
concrete constraint. Do not invent decorative alternatives.

## 5. Proportionate depth

Use the smallest document that preserves the decision. Context, alternatives, decision, rationale,
and consequences are always required. Add assumptions/invariants, validation, references, migration,
or follow-ups only when they carry decision-specific value.

Irreversible/high-cost choices need explicit assumptions, validation/revisit triggers, and rollback or
migration consequences. A reversible local precedent should not be padded with generic risk sections.

Never encode implementation completion percentages, checklists, or task status in the ADR filename or
body unless an established project convention explicitly requires a legacy field. Decision lifecycle
and implementation progress are separate concerns.

## 6. Contract relationship

The ADR explains why a choice was made. A living contract explains what current implementations must
preserve. Link the artifacts when both exist; do not copy normative current-state rules into decision
history or treat an ADR as the only long-term implementation contract.

## 7. Corpus quality

Across a corpus:

- supersession chains and links are intact;
- no two live ADRs contradict each other without succession;
- placement/naming follow project convention;
- records are neither flooded with trivial reversible choices nor missing known significant decisions
  that the operator explicitly chose and intended to preserve;
- drift is handled through a successor or deprecation, not body rewrites.

Reverse review may identify major implemented forks with no ADR as **candidates to discuss**, not as
historical facts. The next action is operator confirmation of whether a meaningful decision/rationale
exists, not automatic ADR generation.
