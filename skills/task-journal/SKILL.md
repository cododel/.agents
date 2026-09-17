---
name: task-journal
description: "Preserve the current agreed task separately from working state when requirements, decisions, phases, or context switches are hard to retain. Use adaptively, including medium tasks; skip atomic work."
---

# Task Journal

Own the storage and maintenance procedure for one task's working memory. The records preserve the
current agreed target across context changes; they are not product contracts or new authorization.

## When records help

Create records when decisions, requirements, phases, handoffs, or interruptions make intent hard to
retain, or when requested. Start midway if complexity grows. A medium task may benefit; a long task
label alone does not require ceremony. Skip atomic, easily restated changes. Subtasks do not get their
own pairs automatically.

## Location and ownership

Use the current checkout's `.tmp/tasks/<task-id>/task.md` and `state.md`. Choose a unique descriptive
ID; inspect an existing directory before reusing it and never overwrite another task. Exclude
`/.tmp/` from Git, adding the scoped ignore entry when absent under this policy. Do not stage records.
When project writes are unavailable, disclose one stable OS-temp directory keyed by checkout/task.
Pass exact resolved paths to delegates; do not infer a sibling checkout's records.

The agent creates and maintains both files without repeated approval. File ownership does not grant
permission to change agreed requirements or perform gated actions. Keep secrets and large logs out.
For a resumed legacy journal, transfer only that task's established information and preserve the old
source until the new records are checked. Do not bulk-migrate old journals or briefs.

## Two distinct records

Use `assets/task-template.md` for `task.md` and `assets/journal-template.md` for `state.md`; omit empty
sections and keep only useful detail.

- `task.md`: current agreed objective and motivation, observable behavior, material constraints,
  non-goals, acceptance criteria, and compact confirmed requirement changes with decision provenance.
  Clearly separate agreed content from unresolved proposals while briefing.
- `state.md`: current target/phase, implemented state, verification evidence and limitations,
  material assumptions/questions, active assignments, and next actions. Reference acceptance criteria
  in `task.md` rather than copying them.

A direct request or confirmed discussion can establish agreement; do not request a separate approval
of its transcription. The initial request may have been superseded. Preserve the latest agreed target,
not the first wording or the implementation's latest summary.

## Updates and resumption

Update at meaningful changes, not after every tool call:

- Confirmed requirement changes update only affected criteria in `task.md`, with a short note of what
  changed and its decision source. Proposals remain separate until resolved; unchanged agreement stands.
- Implementation findings update `state.md`; they do not authorize weaker acceptance or new invariants.
- Changes to requirements, code, or environment mark only dependent evidence/assignments stale.
- Before a handoff or context boundary, refresh state, evidence pointers, and next actions.

After resuming, read both files and verify the live checkout and relevant runtime state. Records are
reminders, not proof that code, tests, or authorization remain current. Reconcile discrepancies with
surviving operator decisions; ask only about a missing material decision.

Keep records compact by replacing obsolete progress and resolved questions, not by deleting agreed
criteria. Preserve only rejected approaches needed to prevent repeating a significant mistake.
No transcript, duplicate implementation plan, or mandatory line/token quota is needed.

## Delegation and completion

Give delegates relevant requirements, constraints, sources, and acceptance references. Keep primary
record ownership with the coordinating agent; delegates return evidence without concurrently rewriting
these files. Record assignments only while useful.

At closeout, compare the current agreed criteria with implementation and verification, recording
supported, failed, and unverified outcomes in `state.md`. Do not force closeout or independent review
solely because records exist. Keep the files across responses and completion for resumption/operator
inspection; do not automatically delete, commit, or promote them to project documentation.
