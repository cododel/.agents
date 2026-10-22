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

## Approach and stages

For a large task, assess whether a connected but incomplete implementation helps resolve its main
uncertainty. Compare only relevant alternatives: direct implementation, completing a necessary
component, validating a critical dependency, or a broader skeleton. Choose independently from current
evidence, integration risk, dependencies and feedback value. None is preferred by this skill; neither
size nor duration alone selects a skeleton. A material choice can be noted briefly in existing state,
not a new report or approval ceremony. Reconsider when evidence changes the rationale.

For the chosen approach, keep the next observable outcome and completion boundary in `state.md`,
referencing agreed acceptance. Name necessary dependencies and remaining obligations. Component
completion can be the right next outcome; relate it to the overall task instead of treating local
activity as proof of global progress. Use parallel work where useful without imposing a fixed number
of active stages.

If a broad skeleton is chosen, it may precede complete implementations of individual nodes; a
separate throwaway prototype is not mandatory. Identify mocks, simplified behavior and known failures,
then deepen and stabilize the implementation against final acceptance. Investigate critical feasibility
and safety assumptions early when they could invalidate the path. Testing depth and claims belong to
`testing-evidence`, not this journal.

Classify new work as needed now, a later required obligation, or outside scope. Reorder implementation
independently while preserving requirements and authority. If work no longer resolves a relevant
uncertainty or closes a dependency, reassess the approach; do not automatically switch to a skeleton
or open another audit. Show useful reproducible results with their limits when available; continue
independent authorized work unless operator feedback is a prerequisite.

## Updates and resumption

For sustained multi-stage work, keep one current outcome list in the existing implementation plan
or `state.md`; link to its owner from the other records instead of maintaining copies. Use stable IDs,
observable completion conditions, status, remaining gaps and material dependencies/decisions. Build
the initial list from known requirements and evidence; label unknowns without launching a new audit
or rerunning checks merely to populate it. Separate local deliverables from later operator actions.

Keep completed outcomes with concise evidence references. Record added or reopened outcomes and
their requirement source; technical substeps and defects within the same acceptance stay under that
outcome. Preserve identity when splitting or merging rows so decomposition cannot masquerade as
progress or silently reset the baseline. Counts describe this list, not equal units of effort.

At meaningful milestones, summarize changes against that baseline and the next observable result.
If no outcome closed, identify the material gap reduced. Record a useful forecast's basis, uncertainty
and significant revisions; when an estimate is unsupported, name the checkpoint needed to form one.
Apply the global convergence rule when successive stages fail to reduce the gap; updating the list
is not itself implementation progress. This procedure adds no separate report or approval stage.

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

When several dependent steps are difficult to follow, use an available `update_plan` as a short
view of the active stage and next actions. It is optional for atomic work and cannot replace the
records' requirements or evidence. Update at material changes, not every tool call; reconcile after
resumption. No detailed duplicate plan or replacement infrastructure is needed when unavailable.
Completed step counts are not a completion percentage.

## Delegation and completion

Give delegates relevant requirements, constraints, sources, and acceptance references. Keep primary
record ownership with the coordinating agent; delegates return evidence without concurrently rewriting
these files. Record assignments only while useful.

At closeout, compare the current agreed criteria with implementation and verification, recording
supported, failed, and unverified outcomes in `state.md`. Do not force closeout or independent review
solely because records exist. Keep the files across responses and completion for resumption/operator
inspection; do not automatically delete, commit, or promote them to project documentation.
