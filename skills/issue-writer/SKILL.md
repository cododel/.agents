---
name: issue-writer
description: "Create or update repository-local Issues for independently resumable technical debt. Use when the operator requests recording or deferring work; a linked TODO is optional when useful. Never file speculation, current-scope work, or generic observations."
---

# Issue Writer

Keep the active task focused without discarding evidence-backed technical debt. Repository Issues are
a durable engineering backlog with historical context; they do not mirror the product task tracker and
do not justify branching the current session into unrelated work.

## Modes

| Intent | Mode | Reference |
|:--|:--|:--|
| Explicitly defer/park independently resumable work | create/update | `references/create.md` |
| Agent notices separate debt without a recording request | briefly report only | No file or TODO |
| Sweep completed Issue records after extracting durable value | close | `references/close.md` |

Read `../_shared/repository-discovery.md` and `references/conventions.md` before the selected mode.
Project-local conventions override fallback paths and templates.

## Recording authority

Create or update an Issue only when the operator requests recording or deferring that work. Finding
material debt during implementation or review is not authorization to create a record or TODO.
Briefly report the evidence and impact, then continue the current task. Do not file speculative,
cosmetic, or current-scope work merely because a template exists.

Within a recording request, preserve enough evidence, scope, and completion criteria for independent
resumption. Reuse an unambiguous existing owner and distinguish proven causes from hypotheses.

## TODO linkage

Within an operator request to record/defer a code-local problem, optionally add one concise TODO at the most stable relevant
seam using the repository's comment convention and a relative link or unique slug to the Issue. The
TODO explains **why the deferred risk exists**, not the full remediation plan. Do not scatter several
TODOs or add one when no stable code seam exists, comments are prohibited, or the Issue itself is the
only useful locator.

A TODO never replaces the Issue. The Issue owns evidence, context, recommended direction, resume
conditions, and verification.

## Mutation and decisions

- Creating/updating an Issue and a linked local TODO are reversible project-local documentation edits
  covered by an explicit recording/deferral request, not by ordinary implementation alone.
- Update an unambiguous existing owner rather than creating a duplicate. Ask only when two records may
  represent different root causes/ownership or when the update would change an operator decision.
- Do not silently mark work `Closed`; completion requires evidence for its recorded criteria.
- Closing/sweeping Issues is explicit. `references/close.md` may delete exact tracked, clean,
  committed sources after value extraction; unrecoverable or ambiguous sources remain operator-gated.

## Durable-value routing

Before closing/deleting an Issue, route unique value through
`../_shared/durable-documentation.md`: current stable behavior to a living contract, significant
operator decisions to an ADR, and repeatable operational/debugging knowledge to the appropriate
runbook/reference. Do not keep closed Issues as a second documentation archive.

## Report

For create/update, mention only:

- Issue path/link and whether it was created or updated;
- one-line reason it was deferred instead of fixed now;
- TODO location when one was useful;
- unresolved material fact, if any.

For close, report the exact deletion/extraction result defined by `references/close.md`.
