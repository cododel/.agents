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

## Claude Code

- Project-scoped servers live in tracked `.mcp.json` at the project root and naturally appear in a
  linked worktree.
- Local-scoped servers are stored in `~/.claude.json` under the absolute project path. A local server
  registered for the primary checkout therefore may be absent from a linked worktree.
- Inspect with `claude mcp list` from the worktree. Prefer promoting a non-secret shared definition to
  project scope. Otherwise re-register the same local definition for the worktree path using current
  `claude mcp` commands; do not duplicate stored credentials manually.
- Use a project `.worktreeinclude` for required ignored local files when using Claude's built-in Git
  worktree flow. If a custom `WorktreeCreate` hook replaces that flow, the hook must perform any copy
  or setup itself.

## Codex CLI / app

- User configuration lives in `~/.codex/config.toml`; project overrides and project-scoped MCP
  definitions may live in `.codex/config.toml`.
- Codex ignores project-scoped configuration in an untrusted project or worktree. Verify trust before
  diagnosing the server definition.
- Inspect with `codex mcp list` or the native `/mcp` view. Use the project's Codex local-environment
  setup script when available to prepare worktree dependencies and ignored files.
- Keep provider/auth settings that Codex does not accept project-locally in user configuration.

## OpenCode

- Project MCP definitions live under `mcp` in `opencode.json` or `opencode.jsonc`; tracked config is
  available in each worktree.
- Inspect with the current native MCP listing/status command. Resolve relative command paths and
  working directories from the worktree, not the primary checkout.
- Enable only servers needed for the task because every enabled MCP contributes tools and context.
  Authentication remains user-local where supported.

## Unknown or changed harness

Do not transpose one harness's config shape onto another. Use `$find-docs` to establish:

1. project versus user/local configuration locations;
2. whether configuration is keyed by absolute project path;
3. trust/approval behavior for a new worktree;
4. the current server-list and authentication commands;
5. supported setup hooks or ignored-file copy mechanisms.

If the required server still cannot be activated without a credential or external authorization,
record the exact missing gate and stop only the MCP-dependent branch of work.
