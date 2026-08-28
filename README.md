# Shared Agent Configuration

This directory is the canonical physical source for the operator's cross-client engineering policy,
portable Skills, and behavior evals. Client adapters import or link to it; project repositories add
only their own architecture, commands, conventions, and project-scoped workflows.

## Architecture

- `AGENTS.md` is the always-on **policy kernel**: autonomy boundaries, safety/ownership, engineering
  standards, verification, durable-artifact semantics, and concise handoff behavior.
- `skills/<name>/` owns repeatable **procedures**. Detailed workflows do not belong in the global
  kernel merely because they are important.
- `capabilities/<name>/manifest.json` owns declarative, client-neutral tool requirements, project
  harness rules, probes, and repair commands. Runtime configuration generated from it belongs to the
  exact project checkout.
- Project `AGENTS.md` files may specialize global engineering defaults and define project facts. They
  should link to global policy instead of copying it, except when a concrete project delta must be
  explicit.
- Project Skills own stack- or repository-specific execution procedures such as test matrices,
  migrations, release commands, or domain workflows. They do not live in this global archive.
- `evals/` defines trigger and behavior contracts. A rule change should add or update an eval rather
  than rely only on prose review.

Use one canonical owner per rule. The intended precedence is hard global safety → current operator
request/decisions → nearest project instructions → global engineering defaults → invoked Skill/local
convention.

## Skill Routing Model

Skills use a hybrid trigger model:

- **automatic context/enforcement helpers:** `find-docs`, `troubleshooter`, `issue-writer` under its
  strict debt gate, `task-journal`, existing-graph queries through `graphify`, `worktree-task` when
  a concrete isolation need exists, and `feature-closeout` for large/high-autonomy handoff;
- **situational workflows:** `feature-brief`, `contract-writer`, design/docs/Tavily workflows;
- **operator-intent workflows:** ADR creation/audit, contract audit, broad documentation cleanup,
  tracker writes, and release-mode closeout. They may route from an unambiguous natural-language
  request; they do not run merely because related code or documents exist.

Automatic does not mean unconditional. Each Skill's description and internal gate defines when its
coordination cost is justified.

## Task State And Worktrees

Long-running task memory is untracked and worktree-specific through `$task-journal`; it is not a new
repository documentation layer. Preserve the operator-selected workspace by default; use
`$worktree-task` only when isolation is needed, such as a protected primary checkout or parallel
writable ownership.

Project-scoped non-secret MCP configuration is preferred for project-specific servers. `mcpls` is
always project-scoped because its workspace root and enabled language servers belong to one exact
checkout; it must never be registered globally. Each linked worktree is configured independently.
The worktree workflow verifies harness trust, path-scoped registration, generated setup files, and a
narrow MCP smoke call before MCP-dependent work begins.

## Canonical Sources

- `AGENTS.md` — client-neutral global policy.
- `skills/<name>/SKILL.md` — portable trigger and workflow entrypoint.
- `skills/<name>/references/` — on-demand detailed procedure.
- `skills/<name>/assets/` — fallback templates/resources.
- `capabilities/<name>/manifest.json` — supported stacks, probes, repair commands, and harness policy.
- `clients/<client>/skills/` — client-only Skill sources when required.
- `evals/skill-scenarios.tsv` — portable Skill trigger contracts.
- `evals/agent-behavior.tsv` — policy-level behavior contracts.
- `scripts/check-skills.py` — structural/link/eval validator.
- `scripts/scaffold-code-intelligence.py` — portable entrypoint for project inspection, setup,
  verification, and legacy global removal.
- `scripts/code_intelligence_scaffold/` — strict manifest, project adapters, source-preserving
  patching, and MCP verification internals.

## Client Adapters

The current installation uses one physical source with harness-specific adapters or symlinks:

- Claude Code: `~/.claude/CLAUDE.md` imports the canonical instructions; Skills are linked under
  `~/.claude/skills/`.
- OpenCode: `~/.config/opencode/opencode.json` loads the canonical instructions; Skills are
  discovered from this directory.
- Codex: `~/.codex/AGENTS.md` links to the canonical instructions; Skills are discovered natively.
- Gemini CLI: `~/.gemini/GEMINI.md` links to the canonical instructions; Skills are discovered from
  this directory.
- Antigravity: Skills are discovered from this directory; global instructions arrive through the
  Gemini adapter.
- Grok: `~/.grok/AGENTS.md` links to the canonical instructions; Skills are discovered natively.
- Cursor: Skills are discovered natively; User Rules are synchronized through Cursor configuration
  where no file adapter is available.
- Kimi: Skills are discovered from this directory; local configuration prevents duplicate fallback
  discovery from other brand roots.

Do not copy app-managed plugins, bundled Skills, credentials, caches, histories, runtime databases, or
client state into this tree.

## Code Intelligence Capability

`code-intelligence` keeps portable LSP/AST policy in `~/.agents`. Its manifest describes supported
stacks, exact detection evidence, host probes and repair commands. The explicit-only
`$setup-project-mcpls` Skill generates a checkout-owned `.agents/mcpls.toml` and updates only existing
supported project harnesses. See [the project configuration contract](docs/MCPLS_PROJECT_CONFIGURATION.md)
and [the accepted decision](docs/adr/ADR-20260828-scope-mcpls-to-projects.md).

The tracked LSP set covers Python (`basedpyright`), TypeScript and JavaScript
(`typescript-language-server`), PHP (`intelephense` 1.18.5), Rust (`rust-analyzer`), C/C++
(`clangd`), and Swift (`sourcekit-lsp`). PHP activation is deferred until a `*.php` file is inside a
project identified by Composer, PHPStan, Psalm, or PHPUnit markers. Intelephense requires Node.js 20+
and its free tier does not expose every semantic operation; premium-only operations must not be
reported as MCP transport failures. The shared `ast-grep` component also parses PHP for structural
search and bounded rewrites.

The supported project harnesses are:

| Harness | Project-scoped adapter |
| --- | --- |
| Root MCP config | Existing `mcp.json`; source-preserving `mcpServers.mcpls` update |
| Codex | Existing `.codex/config.toml`; `cwd = ".."` targets the checkout root |

Inspect and configure it explicitly:

```bash
python3 scripts/scaffold-code-intelligence.py validate
python3 scripts/scaffold-code-intelligence.py inspect-project --root <git-root>
python3 scripts/scaffold-code-intelligence.py setup-project --root <git-root>
python3 scripts/scaffold-code-intelligence.py verify-project --root <git-root>
python3 scripts/scaffold-code-intelligence.py unconfigure-global --client all
```

`inspect-project` is read-only. `setup-project` never installs binaries or creates missing harness
files. It preserves unrelated entries, environment values, comments, and rejects foreign collisions.
Detected stacks remain configured when their LSP is missing, with the exact repair command reported.
`unconfigure-global` exists only to remove legacy user-scoped entries; no command can add one.

## External Skill Provenance

- `find-skills` is externally managed by `.skill-lock.json`. Update it through the owning installer;
  do not hand-edit it.
- `graphify` is derived from the installed `graphifyy` package. The pinned version lives in
  `skills/graphify/.graphify_version`; local portability overlays keep its trigger and worker/tool
  instructions client-neutral without changing graph semantics.
- Tavily Skills are locally maintained routing/production wrappers. Resolve CLI flags from current
  `tvly <command> --help` and SDK contracts from current official documentation.

To review a Graphify update:

1. install the intended `graphifyy` version in an isolated tool environment and record
   `graphify --version` in `skills/graphify/.graphify_version`;
2. diff its `skill-agents.md` and references against the local snapshot, separating upstream graph
   semantics from client-specific worker/tool wording;
3. copy reviewed semantic changes, reapply the documented client-neutral portability overlays, then
   run the validator and client discovery smoke tests.

## Validation

Run:

```bash
python3 scripts/check-skills.py
python3 scripts/scaffold-code-intelligence.py validate
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```
