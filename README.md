# Shared Agent Configuration

This directory is the canonical physical source for the operator's cross-client engineering policy,
portable Skills, and behavior evals. Client adapters import or link to it; project repositories add
only their own architecture, commands, conventions, and project-scoped workflows.

## Architecture

- `AGENTS.md` is the always-on **policy kernel**: autonomy boundaries, safety/ownership, engineering
  standards, verification, durable-artifact semantics, and concise handoff behavior.
- `skills/<name>/` owns repeatable **procedures**. Detailed workflows do not belong in the global
  kernel merely because they are important.
- `capabilities/<name>/manifest.json` owns declarative, client-neutral tool requirements and the
  smallest client deltas needed to expose them; tracked configuration beside it remains the runtime
  source for that capability.
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

Project-scoped non-secret MCP configuration is preferred for project-specific servers so linked
worktrees inherit it. Project-agnostic host capabilities such as `mcpls` may instead be registered
user-scoped when every client invocation points to tracked configuration in this canonical
`~/.agents` tree. The worktree workflow still verifies harness trust, path-scoped local registration,
ignored setup files, and a narrow MCP smoke call before MCP-dependent work begins.

## Canonical Sources

- `AGENTS.md` — client-neutral global policy.
- `skills/<name>/SKILL.md` — portable trigger and workflow entrypoint.
- `skills/<name>/references/` — on-demand detailed procedure.
- `skills/<name>/assets/` — fallback templates/resources.
- `capabilities/<name>/manifest.json` — declarative requirements and client deltas.
- `capabilities/<name>/mcpls.toml` — tracked, explicitly selected runtime configuration.
- `clients/<client>/skills/` — client-only Skill sources when required.
- `evals/skill-scenarios.tsv` — portable Skill trigger contracts.
- `evals/agent-behavior.tsv` — policy-level behavior contracts.
- `scripts/check-skills.py` — structural/link/eval validator.
- `scripts/scaffold-code-intelligence.py` — portable entrypoint for capability validation and
  client-delta scaffolding.
- `scripts/code_intelligence_scaffold/` — strict contract, client adapters, JSONC patching, and MCP
  verification internals.

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

`code-intelligence` keeps portable LSP/AST policy and configuration in `~/.agents`. Its manifest
describes only missing host tools and client deltas; it does not replace native Skill discovery or
existing client imports and links. Every MCP adapter registers the absolute `mcpls` binary with the
absolute tracked `mcpls.toml` path.

The tracked LSP set covers Python (`basedpyright`), TypeScript and JavaScript
(`typescript-language-server`), PHP (`intelephense` 1.18.5), Rust (`rust-analyzer`), C/C++
(`clangd`), and Swift (`sourcekit-lsp`). PHP activation is deferred until a `*.php` file is inside a
project identified by Composer, PHPStan, Psalm, or PHPUnit markers. Intelephense requires Node.js 20+
and its free tier does not expose every semantic operation; premium-only operations must not be
reported as MCP transport failures. The shared `ast-grep` component also parses PHP for structural
search and bounded rewrites.

The supported client deltas are:

| Client | User-scoped adapter |
| --- | --- |
| Codex | Native `codex mcp get/add/remove` registry shared by CLI, desktop, and IDE |
| Antigravity | Current `~/.gemini/config/mcp_config.json`; legacy paths remain untouched |
| Grok Build | Native `grok mcp list/add/remove/doctor`, independent of Claude imports |
| Claude Code | Native `claude mcp add/remove --scope user`, inspected through `~/.claude.json` |
| Kimi Code | `$KIMI_CODE_HOME/mcp.json`, defaulting to `~/.kimi-code/mcp.json` |
| OpenCode | Highest-priority global JSON/JSONC config; both v1 and v2 MCP shapes |
| Pi | Shared rules plus `ast-grep` and `rg`; LSP is unsupported without a third-party extension |

Inspect and configure it explicitly:

```bash
python3 scripts/scaffold-code-intelligence.py validate
python3 scripts/scaffold-code-intelligence.py plan --client all
python3 scripts/scaffold-code-intelligence.py apply --client all --install
python3 scripts/scaffold-code-intelligence.py verify --client all
python3 scripts/scaffold-code-intelligence.py unconfigure --client all
```

`plan` is read-only. `apply` does not install anything without `--install`, never installs language
servers, and changes only the selected clients' `mcpls` entries. With `--client all`, absent clients
are skipped and every detected client is preflighted before any registry change. Replacing a
conflicting entry requires `--replace`; removing one with unexpected parameters requires `--force`.
OpenCode JSONC edits preserve unrelated source text, comments, and trailing commas. Pi never gains an
MCP extension through this scaffold. A known language-server repair remains explicit and is emitted
as a command hint in both human and JSON plan output. For PHP the pinned repair command is
`npm install --global intelephense@1.18.5`.

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
