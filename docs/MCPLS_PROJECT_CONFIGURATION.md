# Project mcpls Configuration Contract

**Scope:** MCP registration and generated LSP configuration for one Git checkout

**Decision provenance:** [ADR-20260828: Scope mcpls registration to projects](adr/ADR-20260828-scope-mcpls-to-projects.md)

## Responsibilities

- `mcpls` and language-server binaries **may** be installed system-wide, but an MCP registration named
  `mcpls` **must not** be user-scoped or global.
- Each registration **must** belong to exactly one canonical `git rev-parse --show-toplevel` root.
- Setup **must** be explicitly invoked through `$setup-project-mcpls`; ordinary semantic lookup must
  not mutate configuration or install dependencies.
- The setup scaffold **must** generate `<repo-root>/.agents/mcpls.toml` with the canonical absolute
  Git root, an explicit `--config`, and only stacks detected from both project markers and source
  files. `mcpls 0.3.9` cannot initialize an LSP from `roots = ["."]` because it passes the relative
  path to URI conversion; setup therefore writes the absolute checkout root.
- Setup **must not** pass `--trust-project-config`, create absent harness files, grant harness trust,
  stage, commit, or terminate processes from existing sessions.

## Supported Stacks And Harnesses

The manifest is the executable inventory for Python, TypeScript/JavaScript, PHP, Rust, C/C++, and
Swift markers, file patterns, versions, probes, and repair commands.

Setup may change only these already-existing harness files:

- root `mcp.json`, where `mcpServers.mcpls` invokes the resolved `mcpls` binary with
  `--config .agents/mcpls.toml`;
- `.codex/config.toml`, where `[mcp_servers.mcpls]` uses the same arguments and `cwd = ".."` because
  relative paths in a project config resolve from its containing `.codex` directory.

Codex loads project configuration only for trusted projects. Setup reports this gate but does not
bypass it. Each linked worktree is configured as a separate canonical root.

## Behavioral Invariants

- Marker-only or source-only evidence does not activate a language server.
- Discovery ignores VCS metadata, dependencies, virtual environments, caches, and build output.
- Existing unrelated MCP entries, fields, environment values, and comments are preserved.
- An existing entry named `mcpls` is migrated only when its command is actually `mcpls`; another
  server under that name is a conflict and causes no writes.
- An existing `.agents/mcpls.toml` is changed only when it has the scaffold ownership marker.
- A missing language-server binary does not remove a detected stack. Setup writes the stack, performs
  no installation, and reports the manifest's exact repair command.
- Repeated setup with unchanged inputs leaves every managed and harness file byte-identical.
- Moving a checkout invalidates its generated absolute root; rerun setup after a move.

## Failure And Unavailable Behavior

- `/`, the user's home directory, and non-Git roots are rejected before mutation.
- Missing or incompatible `mcpls 0.3.9`, malformed harness configuration, foreign collisions, or an
  unowned generated file fail closed before writes.
- When neither supported harness file exists, setup creates nothing and reports which file must be
  added before retrying.
- Removing global registration does not stop already-running processes or immediately reduce swap;
  restart the harness to prevent new global sessions.

## Operation And Verification

From the shared agents repository:

```bash
python3 scripts/scaffold-code-intelligence.py inspect-project --root <git-root>
python3 scripts/scaffold-code-intelligence.py setup-project --root <git-root>
python3 scripts/scaffold-code-intelligence.py verify-project --root <git-root>
python3 scripts/scaffold-code-intelligence.py unconfigure-global --client all
```

`verify-project` checks exact generated and harness content, performs an MCP handshake and tool
inventory, makes a Python semantic request when Python is configured, and terminates the spawned
process group. The configuration scopes processes and indexes; it does not deduplicate concurrent
tasks in the same checkout.
