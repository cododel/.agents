---
name: worktree-task
description: "Create or prepare one isolated linked worktree and dedicated branch when isolation is explicitly requested or concretely needed for a separate base, parallel writable work, conflicting ownership, or protected checkout. Do not use for ordinary feature, fix, implementation, or long-running work in a suitable operator-selected workspace."
---

# Worktree Task

Create one isolated implementation workspace with one dedicated branch after proving that isolation
is needed, then prove that its development and MCP environment is usable while leaving the operator's
current workspace intact.

## Decide whether isolation is needed

Treat the checkout and branch at task start as operator-selected. If they are writable and the task
belongs to them, work there; an existing linked worktree is already the task workspace. Do not create
a sibling worktree merely because the task is a feature, fix, refactor, implementation, autonomous,
or long-running.

Use this skill only when one of these concrete conditions applies:

- the operator explicitly requests a worktree or isolated branch;
- the task requires another base or branch, or does not belong to the current branch;
- a parallel writable builder needs an independent workspace;
- dirty operator changes overlap the task so their scope cannot be safely separated;
- a protected primary/default checkout cannot accept implementation without permission or a stricter
  project rule.

Read-only explorers and reviewers do not need an isolated worktree. Do not let multiple writable
agents own the same branch or worktree unless a project workflow explicitly coordinates it.

An explicit request to work in the current workspace permits reversible scoped edits there unless a
stricter project rule prohibits it. Dirty but separable changes are not a reason to isolate: preserve
them and do not reset, stash, discard, or overwrite them. When overlap makes ownership unsafe,
isolation or operator clarification is justified.

## Authority

A direct implementation request authorizes local creation of the linked worktree, its dedicated
branch, scoped file edits, focused verification, and coherent task-owned commits there. It does not
authorize push, merge, worktree/branch deletion, remote mutation, deployment, or destructive changes
to shared state.

## 1. Prove repository ownership

After deciding that isolation is needed and before any Git mutation, record:

```bash
git rev-parse --show-toplevel
git status --short --branch
git worktree list --porcelain
git branch --show-current
git rev-parse HEAD
```

Identify the primary checkout from `git worktree list --porcelain`; do not infer it from the current
path. Preserve all dirty, staged, and untracked operator work. Never move the primary checkout,
change `core.worktree`, reuse a branch already checked out elsewhere, or repair ambiguity by
switching/resetting the operator's checkout.

Stop only when the repository boundary, base revision, or intended ownership cannot be established
without selecting a material alternative. A dirty primary checkout alone is not a blocker because a
linked worktree starts from a committed revision.

## 2. Resolve branch, base, and path

- Follow applicable project branch rules, otherwise the global `<type>/<short-kebab-description>`
  convention.
- Use the operator-supplied base when present. Otherwise use the current task's proven branch/HEAD;
  ask only when choosing among plausible bases changes the deliverable.
- Prefer an established client/project worktree root. Without one, use a collision-free sibling path
  such as `../<repo-name>-<short-task-slug>`.
- One worktree owns exactly one dedicated branch for its lifetime. If another branch is required,
  create another worktree instead of switching this one.

Create atomically:

```bash
git worktree add -b <branch> <resolved-path> <base>
```

Then verify from inside the new path:

```bash
git status --short --branch
git branch --show-current
git rev-parse HEAD
git worktree list --porcelain
```

If creation partially fails, inspect current worktree/branch state before retrying. Never blindly
remove a path or branch to make the retry pass.

## 3. Prepare the local environment

Inspect project instructions and setup conventions before installing or copying anything. Prefer, in
order:

1. a tracked project worktree/setup script;
2. a harness-native worktree setup facility;
3. an established bootstrap command from project documentation;
4. the smallest manual setup needed for the requested task.

Handle ignored local files explicitly. Copy or generate only files proven necessary for development
inside this worktree. Never copy credentials into tracked files, print secrets, or broadly mirror the
primary checkout. Symlink caches/dependency directories only when the project or harness convention
says concurrent sharing is safe.

Install dependencies only when absent or stale for the resolved lockfile. Record setup failures as
environment evidence rather than silently changing package managers or dependency versions.

## 4. Establish MCP readiness

Only after creating the isolated worktree, read `references/mcp-readiness.md`. Determine which MCP
servers the project/task expects from project instructions, configuration, and the source session.
Then, inside the worktree:

1. prove project-scoped MCP configuration is present;
2. verify the worktree is trusted where the harness gates project configuration;
3. list active servers with the harness's native inspection command/tool;
4. compare expected versus active server names and test only the minimal read-only operation needed;
5. repair path-scoped configuration using current official harness documentation through
   `$find-docs`, without copying tokens or inventing server definitions.

Do not begin an MCP-dependent implementation until the required server is visible and its narrow
read-only smoke check succeeds. If credentials need operator interaction, stop at that exact gate;
do not replace the MCP with improvised production access.

## 5. Hand off the workspace

For a builder session or subagent, provide:

- exact worktree path, branch, base, and current HEAD;
- task contract or `$task-journal` path;
- writable ownership scope and forbidden overlaps;
- setup/verification commands already proven;
- expected MCP servers and readiness result;
- commit authority and all still-closed external-action gates.

The builder may commit coherent checkpoints on this branch. Before each commit, review staged scope
and run the focused checks that prove that checkpoint's changed behavior. A full suite belongs at the
integration/release handoff when project policy does not require it earlier.

## Completion

Report the worktree path, branch, base, setup/MCP readiness, and any exact blocker. Do not delete the
worktree or branch automatically after implementation; it remains the reviewable unit until the
operator accepts and explicitly requests cleanup or a higher-level workflow owns it.
