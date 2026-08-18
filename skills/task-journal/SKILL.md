---
name: task-journal
description: "Maintain one compact untracked task-state journal for long, compaction-prone, multi-agent, batch, or multi-session work. Auto-use when context loss is material; not for short tasks, transcripts, plans, or implementation authority."
---

# Task Journal

Preserve the smallest durable snapshot needed to resume the current task correctly after context
compaction, session interruption, or subagent fan-out. The journal is working memory, not a plan,
Issue, product document, decision record, or final report.

## Activation gate

Create one journal when any of these is true:

- the task is likely to cross a context-compaction or session boundary;
- requirements, operator decisions, or acceptance criteria are numerous enough to be forgotten;
- work has several research/implementation/verification phases;
- subagents need a shared task contract or handoff target;
- a large batch must be resumed without re-reading the entire conversation;
- the operator explicitly asks for persistent task memory.

Do not create one for a short, atomic, easily restated task. Do not keep several journals for one
primary task.

## Resolve the path

For a Git repository, prefer a worktree-specific untracked location:

```bash
git_dir="$(git rev-parse --absolute-git-dir)"
journal_path="$git_dir/agent-tasks/<english-kebab-slug>.md"
printf '%s\n' "$journal_path"
```

Create the parent directory if needed. This resolves under the linked worktree's Git metadata when
inside a worktree and under the repository Git directory in the primary checkout, so it does not
pollute `git status` or collide across worktrees. Prove the current session and delegated agents can
read/write the resolved path. If a client sandbox blocks direct Git-metadata access, use one stable
client/OS scratch path keyed by repository and worktree instead of moving the journal into tracked
project files.

Outside Git, use the same stable scratch strategy and include a repository/session identifier in the
path. Never place the journal in tracked project documentation unless the operator explicitly
requests a deliverable.

Pass the exact resolved journal path to subagents that need it. Never infer a sibling worktree's
journal path.

## Initial snapshot

Copy `assets/journal-template.md` and fill only established information. The initial snapshot should
capture:

- mission and operator motivation;
- target observable behavior and acceptance boundary;
- constraints and non-goals;
- operator decisions versus agent assumptions;
- current phase and exact repository/worktree target;
- open material gates/questions;
- evidence already established;
- next actions and verification state.

Use concise source pointers rather than pasted logs, code, or conversation excerpts. Do not store
secrets, credentials, private customer data, or large generated output.

## Update protocol

Rewrite the journal compactly at semantic boundaries instead of appending a chronological diary.
Keep `Mission And Motivation` stable across phase changes unless the operator explicitly changes the
task goal. Record phase-specific objectives, newly discovered risks, audit findings, and corrective
work in `Current State`, while replacing superseded status, phase, HEAD, verification state, and next
actions.
Update it:

1. after a material operator decision, correction, or scope change;
2. before context compaction, session transfer, or subagent delegation;
3. after a failed experiment or verification result changes the approach;
4. when an assumption becomes evidence or is invalidated;
5. before a major implementation-to-review or review-to-handoff transition.

Do not update after every command, file read, or routine edit. Remove resolved questions and obsolete
next steps. Keep rejected paths only when they prevent repeating a costly mistake or encode an
operator decision.

## Size and fidelity

- Target at most about 150 lines or 2,000 tokens. Compress before exceeding it.
- Preserve exact operator decisions and acceptance requirements; summarize repository evidence.
- Never fabricate a missing decision from the apparent implementation direction.
- If the current conversation contradicts the journal, the current operator instruction wins and
  the journal must be corrected immediately.
- The journal records authorization state only as a reminder. Before a gated action, verify the
  authorization from surviving operator instructions and current state.

## Subagent handoff

Give each subagent only the sections relevant to its bounded role plus the exact journal path. Record
its assignment and final evidence under `Subagent handoffs`; do not paste full transcripts. The
primary agent integrates conflicting conclusions and owns updates to the main task contract.

## Completion

Before final handoff, set `Status` to `Ready for operator review`, summarize verification and known
remaining risks, and remove stale work-in-progress entries. Keep the journal until the operator has
accepted the task or the owning worktree/session is intentionally cleaned up. Do not promote it to a
repository artifact or cite it as proof of implementation state.
