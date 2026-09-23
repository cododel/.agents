---
name: git-operations
description: Guide Git staging, commits, branch synchronization, pushes, remote verification, and transport failure recovery. Use for a requested Git operation or Git state diagnosis; route worktree, merge, and PR maintenance to their specialized skills.
---

# Git operations

This skill supplies an operating procedure, not permission. Apply the current request and the
applicable `AGENTS.md` files first. A skill never expands authority to commit, switch branches,
push, rewrite history, change remotes, or use another credential.

## Case routes

The request or an observed Git state can activate a route at any point. Read the matching case
directly before acting on it; leave other case files unloaded.

| Signal in the task or checkout | Route |
| --- | --- |
| Stage or commit local work | Use the common procedure below and applicable `AGENTS.md`. |
| Push, create a remote branch, or rewrite a remote ref | [Remote publication](references/remote-publication.md) |
| Sandbox/DNS, network, SSH agent, or HTTPS access failure; proposed transport/account change | [Transport failures](references/transport-failures.md) |
| Fetch, pull, divergence, or a stale upstream marker such as `[⇡]` | [Synchronization and tracking](references/sync-and-tracking.md) |
| Create or change a worktree | `$worktree-task` |
| Merge branches | `$merge-branches` |
| Maintain an open PR through comments, conflicts, or CI | `$autopilot` |

## Start

1. Identify the selected checkout and task scope. Before a Git mutation, inspect repository root,
   branch, HEAD, status, and `git worktree list --porcelain`. Include untracked files in the review.
2. For remote operations, identify the named remote, destination repository and branch, current
   remote branch SHA (or its absence), transport, and intended write identity. Treat configured
   access as evidence of availability, not authorization. Never print raw credential-bearing URLs
   or credential-helper output; report only a sanitized host and repository path.
3. State the exact remote target and method before a remote write. If the method or account changes,
   return to the authorization check before writing.

## Execute and verify

- Keep staging and commits scoped to requested work. Inspect the exact staged diff before commit;
  do not use a broad add, reset, clean, or force operation to make status look tidy.
- Run the smallest authorized Git operation. A failed or ambiguous remote write requires state
  reconciliation before any retry.
- Verify the resulting local SHA, remote branch SHA when published, and tracking state when relevant.
  A command's success message alone does not prove all three.

## Handoff format

Report, in this order and without secrets:

1. **Target:** checkout, branch, destination repository/branch, and transport if remote.
2. **Action:** what ran and whether it succeeded, failed, or remains uncertain.
3. **Evidence:** local SHA, remote SHA and tracking relation when applicable.
4. **Remaining:** only concrete blockers or checks still needed. Say explicitly when work was local
   only, pushed, or merely fetched; do not equate a push with deployment.

Use project conventions for commit messages, branch names, and permissions. The specialized skills
in the route table remain the owners of their case-specific procedures.
