---
name: feature-brief
description: "Run a repository-grounded requirements briefing for a large or materially ambiguous feature, preferably in native plan mode; optionally create a temporary brief. Auto-use only for unresolved product, invariant, or architecture forks, not ordinary plans or small tasks."
---

# Feature Brief

Turn an underspecified large feature into an operator-confirmed task contract without forcing a
permanent specification layer onto the repository.

## Modes

1. **Briefing** — research first, then use a small sequence of high-value operator questions to
   resolve material behavior, invariant, scope, and architecture forks. No brief file by default.
2. **Brief file** — on explicit request, or when a stable review/handoff artifact is clearly needed
   across compaction, sessions, or subagents, materialize the agreed task contract in one temporary
   document.

An implementation plan is not a feature brief. A brief describes the target and decision boundary;
the native plan describes execution. An Issue stores deferred work; a contract owns stable current
behavior; an ADR records a significant operator decision.

## Native plan-mode integration

For a large or ambiguous feature, prefer the harness's native plan mode and native question/ask tool.
If entering plan mode requires operator action, request that switch before presenting a long plain-chat
questionnaire. Inside plan mode:

- inspect the repository and current docs before asking;
- let the harness keep the implementation plan in its native plan surface;
- use this skill only to shape the requirements interview and task contract;
- use `$task-journal` when the session is compaction-prone or multi-agent.

Do not create a second natural-language plan file merely because the skill is active.

## Grounding gate

Before asking the operator:

1. resolve the exact repository, affected surface, instructions, and existing documentation;
2. inspect current behavior, nearby conventions, types/schemas/tests, and established living
   contracts;
3. use `$find-docs` for drift-prone library/framework questions and query an existing Graphify graph
   when it can cheaply expose cross-module relationships;
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

## Optional brief file

Read `references/brief.md` only when a file is requested or clearly justified for stable handoff. Use
`assets/brief-template.md` and an established project location; otherwise:

```text
<repo-root>/.agents/briefs/YYYY-MM-DD-english-kebab-slug.md
```

The file is a temporary task contract, not implementation authority or normative project
specification. `Agreed` means the operator confirmed its current material content. Material changes
return it to `Draft` until confirmed.

Do not create a brief file when the native plan and task journal already preserve all required state
and no independent review artifact is needed. Do not commit or index a fallback brief unless the
operator or project convention requires it.

## Completion and routing

Once the target contract is sufficiently clear:

- continue to explicitly requested planning or implementation without another ceremony;
- update `$task-journal` with the confirmed motivation, acceptance, decisions, and open gates when
  active;
- route established stable-boundary changes to `$contract-writer` during implementation;
- stop for a true contract conflict or new material architecture decision;
- create an ADR only after the operator has actually made a significant decision worth preserving.

Report only the confirmed target, remaining material questions, and whether a brief file was created.
Do not echo the full document or repeat the entire interview.
