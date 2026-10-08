---
name: worktree-finish
description: "Finish a feature in an existing task-owned linked Git worktree: pull the base branch, merge base into the working branch, resolve mechanical conflicts, then merge the synchronized feature into base and report. Refuse outside a linked worktree. Not for feature review alone, worktree creation, push, deployment, or cleanup."
---

# Worktree Finish

Complete the local integration in this exact order: update base from its remote, merge base into
the working branch, verify that result, merge the working branch into base, then report.

An explicit invocation or unambiguous request for this workflow authorizes these local pulls,
merges, necessary task-owned commits and focused verification on the resolved branches. Merely
discovering this skill grants no authority. Do not push, deploy, delete branches/worktrees, or
rewrite history unless separately requested. Creating this skill is not a request to execute it.

## Mandatory worktree gate

Before any mutation, inspect the selected checkout with:

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git rev-parse --git-common-dir
git status --short --branch
git branch --show-current
git rev-parse HEAD
git worktree list --porcelain
```

Resolve paths and prove the selected checkout is an existing **linked** worktree registered in
this repository, distinct from the primary checkout, attached to the task's working branch.
The existence of other worktrees does not qualify the primary checkout. Detached HEAD, an
unrelated worktree/branch, or ambiguous ownership does not satisfy the gate.

If the gate fails, refuse this workflow before mutation and explain the failed condition.
Do not create a worktree, switch the primary checkout, or silently substitute another checkout
to make the request qualify. An explicitly selected worktree may be inspected from another cwd.

## Resolve targets and prepare

Load [git-operations](../git-operations/SKILL.md), its
[synchronization route](../git-operations/references/sync-and-tracking.md),
[merge-branches](../merge-branches/SKILL.md), and applicable project instructions.
Before selecting checks, load [testing-evidence](../testing-evidence/SKILL.md).
These skills own Git mechanics, conflict handling and verification; apply them to every merge.

Resolve the working branch, base branch, base's remote repository/ref and local destination
checkout from the operator request or confirmed task/project evidence. Do not assume `main`,
`origin`, or that the working branch's upstream is the base. Working and base branches must differ.
Ask only about unresolved target/ownership choices that materially affect integration.

Record paths, branch names, HEADs and staged/unstaged/untracked state for both checkouts. Use the
base branch's existing checkout via `git -C <base-checkout>`; this workflow authorizes scoped
integration there, not branch switching or unrelated edits. If base is not checked out anywhere,
stop and request a destination decision; do not create or repurpose a checkout automatically.

Finish and verify task-owned feature changes in coherent local commits before starting. Preserve
unrelated operator changes. Require a clean base checkout and no pending merge/rebase/unmerged
state on either branch; follow merge-branches' index and preservation gates for the working tree.
If operator work prevents safe integration, report the blocker without stash/reset/clean/autostash.

## 1. Pull the base branch

Verify base's exact remote/ref and tracking configuration before contacting the remote. From
the base checkout, pull that explicit remote and branch with `--ff-only`, preventing an implicit
rebase or unchecked merge commit. Record the fetched remote SHA and updated local base SHA.

If fast-forward fails because base and remote diverged, inspect both histories and use
merge-branches to merge the freshly fetched remote commit into base, with its full conflict and
verification procedure. This is the controlled merge form of pull; do not rebase, reset base to
remote, or force-update it. Other pull failures block later steps until resolved.

## 2. Merge base into the working branch

Freeze the updated base SHA and working HEAD. In the task worktree, merge the exact frozen base
commit into the working branch using merge-branches. Inspect both sides and verify affected
behavior before completing any required merge commit. Prove base's frozen SHA is an ancestor
of the resulting working HEAD; record the synchronized working SHA.

For conflicts at **any** step, distinguish mechanical integration from product decisions:

- Resolve mechanical conflicts only when repository evidence determines how to preserve both
  sides' intent; follow merge-branches rather than choosing whole-file `ours`/`theirs`.
- For competing product behavior, contracts or architecture requiring operator/CEO vision,
  stop the dependent integration and present the evidenced alternatives and consequences to
  the operator or designated CEO. Do not choose for them or send a message externally without
  explicit messaging authority. A skill cannot invent a CEO decision.
- Follow merge-branches' pause procedure: preserve safe mechanical progress, leave a started
  task-owned merge uncommitted, and report unresolved paths and exact state. Do not automatically
  abort it. Resume only after the required decision arrives and recheck live branch state.

## 3. Merge the synchronized working branch into base

Immediately before integration, recheck both checkouts, ownership, status and HEADs. Base must
still equal the SHA integrated in step 2 and working HEAD must equal the verified synchronized
SHA. If either moved, invalidate dependent evidence and repeat the affected synchronization and
verification before integrating. Stop and report ongoing concurrent movement rather than retry
indefinitely. Remote changes after pull are outside this local snapshot; do not claim freshness
beyond the recorded fetch.

In the base checkout, merge the frozen synchronized working SHA via merge-branches. Use the
project's merge strategy; normally this is a fast-forward, but do not force a merge commit or
silently replace merge with squash/rebase. Verify the candidate and final result as required by
merge-branches, and prove the synchronized working commit is an ancestor of final base HEAD.
An already-contained feature is a verified no-op, not a reason to create another commit.

## 4. Report

Report the working/base branch names and checkout paths, fetched remote SHA, synchronized working
SHA and final base SHA; pull and each merge outcome; mechanical resolutions and operator/CEO
decisions actually received; decisive checks and their limits; final status and preserved operator
work. State whether integration completed or which step is blocked, and distinguish local state
from any separately authorized push/deployment. Retain the branch and worktree for review.
