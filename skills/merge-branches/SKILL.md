---
name: merge-branches
description: "Safely merge one Git branch or ref into another on explicit request, resolve mechanical conflicts without dropping either side's behavior, and stop on product, contract, or architecture forks. Not for rebase, cherry-pick, history repair, push, or generic Git diagnosis."
---

# Merge Branches

Merge the requested source into the exact destination while preserving the behavior and intent of
both lines of development. Treat a textually clean merge as a candidate result, not proof that no
functionality was lost.

## Scope and authority

Use this skill only for an explicit merge request. The request must identify, or make unambiguous,
the source, destination, and merge direction. Do not choose a conventional destination when more
than one is plausible.

The request authorizes the local merge, conflict resolution, focused verification, and the merge
commit when one is required. It does not authorize rebase, cherry-pick, branch-history repair, push,
deployment, destructive cleanup, or mutation of shared data. Follow stricter repository rules when
present.

For multiple explicitly requested merge pairs, process them sequentially. Give every pair its own
preflight, resolution, and verification; do not let a failed pair contaminate the next destination.

## Establish the merge target

Before mutation, resolve and record:

- repository root, current worktree, active branch, and all linked worktrees;
- requested source and destination ref names and merge direction;
- staged, unstaged, and untracked state;
- applicable project instructions, merge strategy, checks, and stable contracts.

If the request requires current remote state, verify the requested remote and fetched ref and
refresh that ref **before** freezing source/destination commit IDs or computing their merge base.
A cached remote-tracking name does not prove freshness. Then record the exact source and
destination SHAs and merge base; use those frozen commits for inspection and execution. A local
merge does not authorize publication.

Use the destination's existing workspace when its ownership is clear. Do not silently switch an
operator-owned checkout, create another worktree, or reuse a branch checked out elsewhere. Route to
`$worktree-task` only when its isolation gate is actually satisfied.

Before an ordinary merge, require the index to equal destination HEAD (`git diff --cached --quiet`)
and no pre-existing merge or unmerged entries. Unrelated unstaged or untracked changes may remain
only when proven preserved and distinguishable from the merge; pre-existing staged changes cannot
be silently included in its commit. Stop before mutation if these conditions cannot be established.
Never stash, autostash, reset, clean, discard, or overwrite operator work automatically.

## Understand both sides before resolving

Inspect the common ancestor and each side's commits and diff. Trace affected registrations,
consumers, configuration, schemas, migrations, generated artifacts, tests, and living contracts.
Use merge preview facilities such as `git merge-tree` when available, but treat the preview as
advisory: it cannot prove semantic compatibility or runtime correctness.

Honor an established project merge strategy. For a non-fast-forward merge, prefer pausing before the
commit with `--no-commit` so the combined tree can be inspected and verified. That flag does not
pause a fast-forward: verify the source tree and affected behavior before advancing the destination.
Do not force `--no-ff` merely to obtain a pause when a fast-forward is permitted. If the source is
already contained in the destination, report the no-op without creating a commit.

Immediately before execution, confirm destination HEAD still equals its recorded SHA and merge the
exact frozen source SHA, rather than a branch name that may have moved. If either intended target
changes, refresh the affected inspection and checks before proceeding.

## Classify and resolve conflicts

Resolve a conflict mechanically only when repository evidence determines one combined result without
choosing product behavior. Typical cases include independent imports, registrations, routes,
configuration fields, non-overlapping moved code, ordering or formatting changes, and generated
artifacts that can be recreated from authoritative inputs.

For every mechanical conflict:

1. inspect the base, source, and destination versions rather than only the marker block;
2. integrate both behaviors at the correct post-merge ownership boundary;
3. update dependent imports, registrations, types, configuration, tests, or generated outputs;
4. stage the path only after all conflicts in that path are resolved.

Never accept `ours` or `theirs` for an entire file merely to clear markers. Do not hand-edit a
generated artifact when a canonical generator exists. Do not rewrite historical migrations merely
to collapse a graph; follow an established merge-head pattern when it is unambiguous.

Preserving functionality does not mean blindly resurrecting every deleted line. Accept a deletion
only when current code, history, contracts, or an operator decision proves it intentional and
compatible with the other branch. Treat uncertain modify/delete conflicts and clean merges that may
silently remove still-required behavior as semantic conflicts.

## Stop on a material fork

A material fork exists when plausible resolutions produce different observable behavior or stable
ownership. This includes competing business rules, API or schema semantics, authorization,
data-lifecycle behavior, migration ordering, configuration precedence, and incompatible architectural
boundaries.

When a material fork is discovered before mutation, stop without starting the merge. If it is
discovered after a task-owned non-fast-forward merge has begun:

- resolve and stage independent mechanical paths already proven safe;
- preserve genuinely unmerged product-conflicted paths, including a path that also contains
  resolved mechanical hunks;
- leave the merge uncommitted and do not abort it automatically; a textually clean path may still
  contain a semantic fork, but do not fabricate conflict markers or index stages for that path;
- ask one focused question describing the exact path or symbol, each branch's evidenced intent, the
  observable consequence of each option, and a recommended option when evidence supports one;
- report the exact in-progress state so work can resume after the operator decides.

For a pre-mutation stop, ask the same focused question and report that no merge was started. If a
fork is found after a fast-forward already completed, report the advanced HEAD and the limitation;
do not invent an in-progress merge or rewind it without authority.

Do not turn missing repository evidence into a product choice. Research discoverable facts first;
ask only when the alternatives genuinely require operator intent.

## Verify the combined result

Before creating a non-fast-forward merge commit, after all material decisions are resolved:

- prove there are no unmerged index entries (`git ls-files --unmerged`) or genuine conflict
  markers; inspect `git diff --cached --check` for the candidate index and `git diff --check` for
  remaining working-tree changes;
- inspect the combined result relative to both pre-merge tips, including semantic losses that caused
  no textual conflict;
- verify affected consumers, registrations, configuration, migrations, generated artifacts,
  cleanup paths, tests, and contracts;
- run focused checks covering behavior introduced or changed by both branches, then broader project
  checks when justified by the affected radius;
- distinguish product failures from missing dependencies, credentials, environment, sandbox, or
  harness failures.

Create the merge commit only after the required checks pass or the operator explicitly accepts the
exact verification limitation. Use the repository's commit-message convention. Do not bypass
signing, hooks, or other integrity controls without exact authorization.

Allow hooks to run normally. Inspect hook-produced changes; they invalidate any check whose inputs
changed. If a hook stops the commit, recheck the candidate index and affected behavior before
retrying. If a hook changes the committed result, verify that result and disclose any new failure
instead of claiming the earlier checks cover it.

After the commit or fast-forward, verify the frozen source commit is an ancestor of the result.
For a merge commit, verify the first parent is the recorded destination SHA and the second is the
frozen source SHA. Verify final HEAD and status against the recorded pre-existing state. These
post-mutation checks supplement the candidate verification; they do not replace it.

## Handoff

On success, report the source and destination commits, whether the result was a fast-forward or merge
commit, the semantic resolutions, decisive verification, preserved pre-existing changes, and that no
push occurred.

When paused on a material fork, report the resolved mechanical scope, unresolved semantic choices,
any genuinely unmerged paths, and whether no merge was started or a task-owned merge remains open.
Never describe an environment-blocked or partially verified merge as complete.
