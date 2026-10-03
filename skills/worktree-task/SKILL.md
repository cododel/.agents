---
name: worktree-task
description: "Create or prepare one isolated linked worktree and dedicated branch when isolation is explicitly requested or concretely needed for a separate base, parallel writable work, conflicting ownership, or protected checkout. Do not use for ordinary feature, fix, implementation, or long-running work in a suitable operator-selected workspace."
---

# Worktree Task

Prepare one task-owned linked worktree and dedicated branch while preserving the operator's checkout.
Use the selected writable workspace by default. Isolation needs an explicit request, another required
base, parallel writable ownership, inseparable overlap with operator changes, or a protected target.
A feature, long task, read-only review, or dirty but separable workspace does not justify a sibling.

An implementation request permits local worktree/branch creation, scoped edits, focused verification,
and coherent task-owned commits there. It does not authorize remote actions, shared/destructive
changes, or worktree/branch deletion.

## Prove ownership and route

Before Git mutation, inspect:

```bash
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git rev-parse HEAD
git worktree list --porcelain
```

Identify the primary checkout from the worktree inventory. Preserve staged/untracked/dirty operator
work; never move the primary checkout, change `core.worktree`, share a checked-out branch, or resolve
ambiguity by switching/resetting the operator's checkout.

Choose the route from actual state:

- **Existing task-owned worktree:** reuse when attached to the correct dedicated branch and base.
  Do not repurpose another task's worktree or branch.
- **Task-owned detached worktree:** create and attach the dedicated branch at its proven HEAD before
  edits, unless the operator's explicit base requires another state.
- **New worktree:** use the operator's exact path/base first, including a requested active-session
  path to recreate. Otherwise use the current task's proven branch/HEAD and an established worktree
  root or collision-free sibling such as `../<repo-name>-<task-slug>`. Ask only about material base or
  ownership ambiguity. Follow project branch rules, otherwise `<type>/<short-kebab-description>`.
- **Partial/unknown creation:** reconcile operation status, filesystem, worktree inventory, and
  branches before retrying. Recover/attach an existing task-owned result even if registration failed;
  never remove paths/branches blindly or create duplicates.

For a new checkout, use a native facility only when it preserves path, base, and branch constraints;
otherwise use Git CLI. With a new branch:

```bash
git worktree add -b <branch> <resolved-path> <base>
```

For an existing dedicated branch, prove it belongs to the task, matches the base, and is not checked
out elsewhere, then add it without recreating it. One worktree retains its dedicated branch; use
another worktree if the task requires a different branch.

After reuse, attachment, or creation, run the ownership checks from inside the actual path. Verify
its resolved path, non-empty attached task branch, HEAD, and worktree inventory before edits.

## Prepare only required capabilities

If task commands need local setup, read [references/setup.md](references/setup.md); offline/source
work may need none. Use already available user- or project-scoped MCP tools for required task calls.
A project config file is not mandatory. Test the narrow required read-only operation before dependent
implementation; a declaration/registration alone is not proof of a working call.

If a required MCP tool is unavailable, read [references/mcp-readiness.md](references/mcp-readiness.md).
Defer only dependent work and continue independent offline work. Do not improvise production access
or copy credentials to bypass a missing capability.

## Handoff

Report exact path, branch, base/HEAD, writable scope, required setup/MCP evidence, and exact blockers.
Pass confirmed scope/acceptance to builders; include a requirements/task-journal file only when one
exists or is requested. State commit authority and closed external gates. Before task-owned commits,
review staged scope and focused evidence; broaden checks only for affected risk or project policy.
Retain the worktree/branch for review until cleanup is explicitly authorized or an owning workflow
provides that authority.
