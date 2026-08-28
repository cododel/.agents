---
name: setup-project-mcpls
description: Configure mcpls for one Git checkout. Use only when the operator explicitly invokes $setup-project-mcpls; never infer this setup from ordinary code-intelligence work.
---

# Set Up Project mcpls

Configure one checkout without changing any user-scoped MCP registry.

1. Resolve the shared agents repository from this Skill's location and the target checkout with
   `git rev-parse --show-toplevel`.
2. Run:

   ```bash
   python3 <shared-agents-root>/scripts/scaffold-code-intelligence.py setup-project --root <git-root>
   ```

3. Report detected stacks, changed existing harnesses, missing language servers with the emitted
   repair commands, and any trust/restart note. When setup succeeds, run `verify-project` for the same
   root if the configured binaries are available.

The scaffold owns `<git-root>/.agents/mcpls.toml`, records the canonical absolute checkout root, and
may update only an existing root `mcp.json` and/or existing `.codex/config.toml`. It must not create
a harness file, install a binary, enable project-config trust, mutate a global registry, terminate
unrelated processes, stage, or commit the
target repository. A foreign entry named `mcpls` or an unowned `.agents/mcpls.toml` is a hard stop.

Treat every linked worktree as a distinct project root. Re-running setup for unchanged inputs must
leave all files byte-identical. This workflow scopes sessions; it does not promise a singleton across
multiple tasks in the same project.
