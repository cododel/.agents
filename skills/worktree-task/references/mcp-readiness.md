# MCP readiness in linked worktrees

Read this when a required MCP tool is unavailable in the worktree. Inspect the live tool surface first;
configuration scope and trust are possible causes, not a diagnosis. Resolve the cause before replacing
the tool or accessing its backing system another way.

## Common rules

- Respect established project- or user-scoped configuration. An already available user-scoped tool can
  satisfy the task without adding project configuration. Keep credentials in established credential storage.
- A configuration tied to the primary checkout's absolute path may not load for a sibling worktree.
- Treat an active server list as evidence of registration, not proof that a specific tool call works.
  Run one narrow read-only smoke call required by the task.
- Never copy whole user configuration files between path entries. They may contain tokens, unrelated
  project history, permissions, and private state.
- Before changing syntax or scope, invoke `$find-docs` for the currently installed harness version.

## Resolve the current environment

Do not transpose one execution environment's config shape onto another. When the repository provides
a capability scaffold, use its read-only inspect/verify path to discover the current adapter. Otherwise
use `$find-docs` to establish:

1. project versus user/local configuration locations;
2. whether configuration is keyed by absolute project path;
3. trust/approval behavior for a new worktree;
4. the current server-list and authentication commands;
5. supported setup hooks or ignored-file copy mechanisms.

If an authorized repair requires path-scoped registration, reuse only the same non-secret definition
for the exact worktree using the environment's current documented interface. Do not add a project
definition merely to satisfy this skill. Never infer a configuration path or command from another client. Resolve
relative commands and working directories from the worktree, enable only the servers required by the
task, and keep authentication in user-scoped credential storage.

If the required server still cannot be activated without a credential or external authorization,
record the exact missing gate and stop only the MCP-dependent branch of work.
Continue independent offline work; no MCP readiness check is needed for a task with no MCP dependency.
