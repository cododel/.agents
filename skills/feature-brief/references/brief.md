# Brief file workflow

Create a brief only when its stable review value exceeds the duplication cost: explicit operator
request, long multi-session work, several subagents, a large acceptance surface, or a need to review
the target contract independently from the implementation plan.

## 1. Resolve content and path

Read the full relevant conversation, repository evidence, existing contracts, active task journal, and
native plan. Reuse established facts; do not fork them into competing versions.

Prefer a proven project convention. Otherwise use:

```text
<repo-root>/.agents/briefs/YYYY-MM-DD-english-kebab-slug.md
```

Keep the original path and date when revising. Do not add an index or `.gitignore` entry merely for the
fallback. Keep one active brief per feature.

## 2. Write the target contract

Use `../assets/brief-template.md`, preserve the operator's language, and keep it concise. Include only:

- motivation and intended outcome;
- observable scenarios/behavior;
- scope and non-goals;
- facts, confirmed decisions, and material assumptions;
- stable invariants/contract impact;
- acceptance criteria and unresolved material questions.

Do not include file-by-file implementation steps, estimates, generic risks, or boilerplate sections
with no task-specific value. Link to the native plan or task journal only when a stable local pointer
exists; do not copy their content.

## 3. Agreement and change control

Write new or materially revised content as `Draft`. Mark `Agreed` only after the operator confirms the
current material content. Typographical and evidence-pointer fixes do not revoke agreement; a change
to behavior, scope, invariant, constraint, or acceptance does.

Agreement confirms the feature target, not every implementation detail and not remote/destructive
authority. When implementation uncovers a new material fork, return only the affected section to
operator review rather than restarting the entire briefing.

## 4. Handoff

At implementation completion, compare observable behavior to acceptance and route durable value:

- stable current behavior to an existing/new living contract when justified;
- significant operator decisions to an ADR when requested/worth preserving;
- independently resumable follow-up debt to an Issue;
- execution state only to the task journal or native plan.

Do not delete, archive, or promote the brief merely because implementation ended. It may remain as
working context until operator acceptance; an explicit cleanup may remove an exact tracked, clean,
committed brief after durable-value review, while untracked/modified content remains gated.
