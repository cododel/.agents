---
name: issue-writer
description: "Create or update repository-local Issues for independently resumable technical debt. Explicitly or auto-use for proven material debt outside the active radius; add one useful linked TODO. Never file speculation, current-scope work, or generic observations."
---

# Issue Writer

Keep the active task focused without discarding evidence-backed technical debt. Repository Issues are
a durable engineering backlog with historical context; they do not mirror the product task tracker and
do not justify branching the current session into unrelated work.

## Modes

| Intent | Mode | Reference |
|:--|:--|:--|
| Explicitly defer/park independently resumable work | create/update | `references/create.md` |
| Agent proves separate material debt during another task | create/update automatically | `references/create.md` |
| Sweep completed Issue records after extracting durable value | close | `references/close.md` |

Read `../_shared/repository-discovery.md` and `references/conventions.md` before the selected mode.
Project-local conventions override fallback paths and templates.

## Automatic creation gate

Create or update an Issue without another operator prompt only when **all** are true:

1. repository/runtime evidence proves a concrete defect, debt, or missing safeguard;
2. resolving it now is outside the accepted affected radius or would materially widen regression or
   merge-conflict risk;
3. the work is independently resumable with a concrete locator, first next step, and completion
   boundary;
4. the impact is material enough that losing the context would be costly;
5. no existing open Issue already owns it, or the matching owner is unambiguous and can be updated;
6. the record does not require choosing unresolved product behavior or architecture.

Otherwise keep the observation in the active task, report it as a hypothesis, or ask only for the
material decision. Do not create Issues for cosmetic preferences, speculative improvements, every
review note, or a bug that the current task should simply fix.

## TODO linkage

For an automatically deferred code-local problem, add one concise TODO at the most stable relevant
seam using the repository's comment convention and a relative link or unique slug to the Issue. The
TODO explains **why the deferred risk exists**, not the full remediation plan. Do not scatter several
TODOs or add one when no stable code seam exists, comments are prohibited, or the Issue itself is the
only useful locator.

A TODO never replaces the Issue. The Issue owns evidence, context, recommended direction, resume
conditions, and verification.

## Mutation and decisions

- Creating/updating an Issue and a linked local TODO are reversible project-local documentation edits
  covered by an implementation or explicit deferral request.
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
