---
name: feature-brief
description: "Run a repository-grounded requirements briefing for a large or materially ambiguous feature, using a structured planning surface when available; optionally record the agreed task. Auto-use only for unresolved product, invariant, or architecture forks, not ordinary plans or small tasks."
---

# Feature Brief

Turn an underspecified feature into a current agreed task without forcing a
permanent specification layer onto the repository.

## Adaptive use

Resolve material product or architecture ambiguity through repository-grounded discussion. A clear
request needs no interview. Record the task when decisions or handoffs are hard to retain, including
medium tasks; use `$task-journal` and its shared `task.md`, not a separate default brief.
An implementation plan describes execution; the task record preserves the agreed result.

## Structured planning integration

For a large or ambiguous feature, use a structured planning and question interface already exposed by
the current execution environment when available. Do not start or require another application solely
to obtain that interface. When it is unavailable, maintain a compact plan in the conversation or task
journal and ask the same focused questions directly. In either case:

- inspect the repository and current docs before asking;
- keep the implementation plan in the environment's active planning surface when one exists;
- use this skill only to shape the requirements interview and task contract;
- use `$task-journal` when requirements, decisions, or handoffs become hard to retain reliably.

Do not create a second natural-language plan file merely because the skill is active.

## Grounding gate

Before asking the operator:

1. resolve the exact repository, affected surface, instructions, and existing documentation;
2. inspect current behavior, nearby conventions, types/schemas/tests, and established living
   contracts;
3. use `$find-docs` for drift-prone library/framework questions;
4. classify each unresolved item as repository-discoverable, objective implementation choice, or
   material operator fork.

Research the first two classes. Ask only the third. Do not ask the operator to design internal details
that the agent can determine objectively.

## Briefing workflow

Read `references/briefing.md`. Ask coherent batches small enough to answer precisely. Prioritize:

- motivation and observable target state;
- users/scenarios and failure behavior;
- stable invariants and boundary ownership;
- scope and non-goals;
- material alternatives and their consequences;
- acceptance and verification expectations.

Recommend a default when evidence supports one, but do not treat it as selected. Stop interviewing
when remaining unknowns are reversible implementation details.

## Optional written task

Read `references/brief.md` when a record is useful or requested. Storage and maintenance belong to
`$task-journal`; use `assets/brief-template.md` as a content guide. Confirmed discussion establishes
agreement without a separate approval of the file. Keep unresolved proposals distinct and revise
only affected criteria when a change is confirmed.

## Completion and routing

Once the target contract is sufficiently clear:

- continue to explicitly requested planning or implementation without another ceremony;
- update `$task-journal` with the confirmed motivation, acceptance, decisions, and open gates when
  active;
- update existing normative owners; use `$contract-writer` for a new owner only under its value test;
- stop for a true contract conflict or new material architecture decision;
- create an ADR only after the operator has actually made a significant decision worth preserving.

Report only the confirmed target, remaining material questions, and whether the shared task record was created.
Do not echo the full document or repeat the entire interview.
