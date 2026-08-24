# MCP readiness in linked worktrees

MCP failures in a worktree are usually configuration-scope or trust problems, not missing project
code. Resolve them before replacing the tool or accessing its backing system another way.

## Common rules

- Prefer project-scoped, versioned **non-secret** server definitions for servers that every checkout
  needs. Keep credentials in user/harness credential storage or environment variables.
- A configuration tied to the primary checkout's absolute path may not load for a sibling worktree.
- Treat an active server list as evidence of registration, not proof that a specific tool call works.
  Run one narrow read-only smoke call required by the task.
- Never copy whole user configuration files between path entries. They may contain tokens, unrelated
  project history, permissions, and private state.
- Before changing syntax or scope, invoke `$find-docs` for the currently installed harness version.

## Resolve the current environment

Do not transpose one execution environment's config shape onto another. When the repository provides
a capability scaffold, use its read-only plan/verify path to discover the current adapter. Otherwise
use `$find-docs` to establish:

1. project versus user/local configuration locations;
2. whether configuration is keyed by absolute project path;
3. trust/approval behavior for a new worktree;
4. the current server-list and authentication commands;
5. supported setup hooks or ignored-file copy mechanisms.

Prefer a tracked project-scoped definition when supported. If registration is user- or path-scoped,
re-register only the same non-secret definition for the exact worktree using the environment's current
documented interface. Never infer a configuration path or command from another client. Resolve
relative commands and working directories from the worktree, enable only the servers required by the
task, and keep authentication in user-scoped credential storage.

If the required server still cannot be activated without a credential or external authorization,
record the exact missing gate and stop only the MCP-dependent branch of work.
