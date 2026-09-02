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
- source and destination ref names and exact commit IDs;
- merge direction and merge base;
- staged, unstaged, and untracked state;
- applicable project instructions, merge strategy, checks, and stable contracts.

Use the destination's existing workspace when its ownership is clear. Do not silently switch an
operator-owned checkout, create another worktree, or reuse a branch checked out elsewhere. Route to
`$worktree-task` only when its isolation gate is actually satisfied.

Start the merge only when the destination is clean, or when every pre-existing change is proven
unrelated, preserved, and distinguishable from the merge. Otherwise stop before mutation. Never
stash, autostash, reset, clean, discard, or overwrite operator work automatically.

Refresh a remote-tracking ref only when the request requires current remote state. Verify the remote
and fetched ref explicitly; a local merge never implies permission to publish anything.

## Understand both sides before resolving

Inspect the common ancestor and each side's commits and diff. Trace affected registrations,
consumers, configuration, schemas, migrations, generated artifacts, tests, and living contracts.
Use merge preview facilities such as `git merge-tree` when available, but treat the preview as
advisory: it cannot prove semantic compatibility or runtime correctness.

Honor an established project merge strategy. For a non-fast-forward merge, prefer pausing before the
commit so the combined tree can be inspected and verified. A valid fast-forward may complete without
a merge commit when project policy allows it.

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

When a material fork remains:

- resolve and stage every independent mechanical path already proven safe;
- leave each product-conflicted path unmerged, including a path that also contains resolved
  mechanical hunks;
- keep the merge in progress; do not commit and do not abort;
- ask one focused question describing the exact path or symbol, each branch's evidenced intent, the
  observable consequence of each option, and a recommended option when evidence supports one;
- report the exact in-progress state so work can resume after the operator decides.

Do not turn missing repository evidence into a product choice. Research discoverable facts first;
ask only when the alternatives genuinely require operator intent.

## Verify the combined result

After all material decisions are resolved:

- prove there are no unmerged paths or genuine conflict markers and run `git diff --check`;
- inspect the combined result relative to both pre-merge tips, including semantic losses that caused
  no textual conflict;
- verify affected consumers, registrations, configuration, migrations, generated artifacts,
  cleanup paths, tests, and contracts;
- run focused checks covering behavior introduced or changed by both branches, then broader project
  checks when justified by the affected radius;
- distinguish product failures from missing dependencies, credentials, environment, sandbox, or
  harness failures;
- allow hooks to run normally, inspect any hook-produced changes, and rerun invalidated checks;
- verify the source commit is an ancestor of the result and, for a merge commit, that both parents
  are the expected commits;
- verify final status against the recorded pre-existing state.

Create the merge commit only after the required checks pass or the operator explicitly accepts the
exact verification limitation. Use the repository's commit-message convention. Do not bypass
signing, hooks, or other integrity controls without exact authorization.

## Handoff

On success, report the source and destination commits, whether the result was a fast-forward or merge
commit, the semantic resolutions, decisive verification, preserved pre-existing changes, and that no
push occurred.

When paused on a material fork, report only the resolved mechanical scope, remaining unmerged paths,
the decision needed, and the fact that the merge remains open. Never describe an environment-blocked
or partially verified merge as complete.
