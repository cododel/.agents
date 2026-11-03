---
name: task-finish
description: "Complete the current implementation task, verify readiness, and integrate its linked worktree into the base branch without push. Use for an explicitly requested full finish-and-integrate cycle; not closeout-only or an ordinary one-way merge."
---

# Task Finish

Thin shortcut for Full closeout followed by ordered local worktree integration.
Invoking this skill requests both stages for the current agreed task; it does not
request executing the workflow when merely creating, editing or discussing this skill.

1. Read [git-operations](../git-operations/SKILL.md) and its
   [Worktree integration route](../git-operations/references/worktree-integrate.md).
   Establish the route's linked-worktree gate, targets and ownership before repairs or
   integration. Preserve its blockers and authority boundaries; do not substitute a
   primary-checkout workflow or guess an unresolved base branch.
2. Run [feature-closeout](../feature-closeout/SKILL.md) in **Full** mode for the
   agreed task. Continue to integration only when it is `PREPARED` for the local
   handoff. Ordinary Full does not request the separate frozen final audit.
3. Execute the Worktree integration route in its prescribed order, including its
   task-owned commits, synchronization and verification. Reuse still-valid closeout
   evidence under the owning procedures.

Do not push, deploy, delete branches/worktrees or rewrite history in this workflow.
Report closeout status and the integration route's result, including decisive checks,
final branch SHAs and any blocker. Claim completion only when both stages succeeded;
state that the result is local and unpushed.
