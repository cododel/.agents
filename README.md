# Shared Agent Configuration

This directory is the canonical physical source for the operator's cross-client engineering policy,
portable Skills, and behavior evals. Client adapters import or link to it; project repositories add
only their own architecture, commands, conventions, and project-scoped workflows.

## Architecture

- `AGENTS.md` is the always-on **policy kernel**: autonomy boundaries, safety/ownership, engineering
  standards, verification, durable-artifact semantics, and concise handoff behavior.
- `skills/<name>/` owns repeatable **procedures**. Detailed workflows do not belong in the global
  kernel merely because they are important.
- `capabilities/<name>/manifest.json` owns declarative, client-neutral tool requirements, probes, and
  repair commands.
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

## Kaneo MCP

Kaneo is a user-scoped, project-agnostic MCP capability. Its client registration must invoke the
stable `~/.bun/bin/bunx` launcher with `@kaneo/mcp@latest serve`; never persist a resolved package
entrypoint under an OS temporary `bunx-*` directory. Pin a tested package version only when a
deliberate compatibility policy is needed. The server's device-flow credentials are runtime state,
not shared-agent configuration.

## Canonical Sources

- `AGENTS.md` — client-neutral global policy.
- `skills/<name>/SKILL.md` — portable trigger and workflow entrypoint.
- `skills/<name>/references/` — on-demand detailed procedure.
- `skills/<name>/assets/` — fallback templates/resources.
- `capabilities/<name>/manifest.json` — tool requirements, probes, and repair commands.
- `clients/<client>/skills/` — client-only Skill sources when required.
- `evals/skill-scenarios.tsv` — portable Skill trigger contracts.
- `evals/agent-behavior.tsv` — policy-level behavior contracts.
- `scripts/check-skills.py` — structural/link/eval validator.

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

`code-intelligence` routes syntax-shaped discovery and bounded structural rewrites through
`ast-grep`, while literal, path, configuration, and documentation searches use `rg`. Its manifest
records the shared `ast-grep` requirement and repair command. LSP tooling may still be used when the
active client already exposes it, but this repository does not install or register an LSP bridge.

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
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```
