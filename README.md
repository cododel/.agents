# Shared Agent Configuration

This directory is the canonical physical source for the operator's cross-client engineering policy,
portable Skills, and behavior evals. Client adapters import or link to it; project repositories add
only their own architecture, commands, conventions, and project-scoped workflows.

## Architecture

- `AGENTS.md` is the always-on **policy kernel**: autonomy boundaries, safety/ownership, engineering
  standards, verification, durable-artifact semantics, and concise handoff behavior.
- `skills/<name>/` owns scoped **guidance and operation contracts**: triggers, decision boundaries,
  required evidence and a definition of done. Keep procedures where order protects correctness;
  load command catalogs, mode details and optional methods only when the task needs them.
- `capabilities/<name>/manifest.json` owns declarative, client-neutral tool requirements and repair
  commands.
- Project `AGENTS.md` files may specialize global engineering defaults and define project facts. They
  should link to global policy instead of copying it, except when a concrete project delta must be
  explicit.
- Project Skills own stack- or repository-specific execution procedures such as test matrices,
  migrations, release commands, or domain workflows. They do not live in this global archive.
- `evals/` records expected Skill routing and agent behavior. Relevant scenarios help detect
  regressions when instructions change; structural validation does not execute model trials.

Use one canonical owner per rule. Client/system requirements remain authoritative. Explicit operator
instructions and applicable project rules refine global defaults; invoked Skills provide guidance
within that scope. External and destructive actions require authorization covering the actual action
and target, as specified in `AGENTS.md`.

## Skill Routing Model

Skills use a hybrid trigger model:

- **automatic context/enforcement helpers:** `find-docs`, `troubleshooter`, `task-journal` when
  written memory helps, `worktree-task` when concrete isolation is needed, and `feature-closeout`
  when material acceptance/integration uncertainty warrants it;
- **situational workflows:** `feature-brief`, `contract-writer`, and design/docs workflows;
- **operator-intent workflows:** ADR creation/audit, contract audit, broad documentation cleanup,
  requested Issue/TODO recording, tracker writes, and release-mode closeout. They may route from an unambiguous natural-language
  request; they do not run merely because related code or documents exist.

Automatic does not mean unconditional. Each Skill's description and internal gate defines when its
coordination cost is justified.

There are **22 active portable Skills**. The routing matrix covers exactly their entrypoints:

- Documentation and design: `adr-auditor`, `adr-writer`, `contract-auditor`, `contract-writer`,
  `design-system-extractor`, `docs-cleanup`, `humanize`, `issue-writer`.
- Engineering and verification: `chrome-devtools-cli`, `feature-brief`, `feature-closeout`,
  `figma-css-cleanup`, `git-operations`, `localization`, `merge-branches`, `troubleshooter`,
  `worktree-task`.
- Context and coordination: `find-docs`, `find-skills`, `kaneo-task-workflow`, `task-journal`,
  `yougile-workflow`.

Inactive historical Wiki sources are not active entrypoints. `task-journal` is unchanged by the
contextual-Skills update. Source files, installed plugins and actual client discovery are separate
inventories; the count above does not prove runtime loading by every client.

## Task State And Worktrees

Task memory is adaptive: atomic changes need no files; accumulated requirements or decisions can
justify records even for medium tasks. `$task-journal` owns `.tmp/tasks/<task-id>/task.md` (current
agreed intent) and `state.md` (progress/evidence) in the current checkout. Briefing and closeout reuse
them. The agent maintains the records, keeps proposals separate, and does not require a second
approval for transcribing confirmed discussion. `/.tmp/` is ignored; records persist across sessions
and are not product contracts. Preserve the operator-selected workspace by default; use
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
- `skills/<name>/SKILL.md` — portable trigger, boundaries and expected outcome.
- `skills/<name>/references/` — task-selected details, catalogs and necessary procedures.
- `skills/<name>/assets/` — fallback templates/resources.
- `capabilities/<name>/manifest.json` — tool requirements and repair commands.
- `clients/<client>/skills/` — client-only Skill sources when required.
- `evals/skill-scenarios.tsv` — portable Skill trigger contracts.
- `evals/agent-behavior.tsv` — policy-level behavior contracts.
- [Behavior probes](evals/behavior-probes.md) — concrete prompts and grading criteria for model runs.
- `scripts/check-skills.py` — structural/link/eval validator.

## Client Adapters

Client adapters should load the canonical instructions and expose portable Skills through the
client's supported discovery mechanism. Keep client-only sources under `clients/<client>/` and
verify loading with the installed client before describing an adapter as active.

Local filesystem snapshot, checked on 2026-10-03:

- `~/.codex/AGENTS.md` is a symlink resolving to this directory's `AGENTS.md`.
- Previously documented adapter files `~/.claude/CLAUDE.md`, `~/.gemini/GEMINI.md`,
  `~/.grok/AGENTS.md`, and `~/.config/opencode/opencode.json` are absent.
- Native Skill discovery and other client settings were not verified. An absent adapter file does
  not establish whether a client loads this directory through another mechanism.

Do not copy app-managed plugins, bundled Skills, credentials, caches, histories, runtime databases, or
client state into this tree.

## Code Intelligence Capability

The capability manifest records the shared `ast-grep` requirement, minimum version, and repair
command. It is declarative; the repository validator does not probe the installed tools or consume
this manifest. Code navigation guidance lives in `AGENTS.md`; there is no separate routing Skill.
This repository does not install or register an LSP bridge.

## External Skill Provenance

- `find-skills` is locally maintained, derived from `vercel-labs/skills`,
  `skills/find-skills/SKILL.md` (former installer folder hash
  `76a98a285cb0434f3d39e1a873823556330e398b`). It is no longer installer-managed;
  review upstream changes manually while retaining the local capability-gap trigger.

## Retrieval Capabilities

Use suitable retrieval tools exposed by the selected client. The shared corpus does not supply a
search-provider integration layer. Resolve extra requirements such as site crawling, bulk exports,
or SDK integration in the individual harness/project setup; native search alone does not prove those
capabilities. Primary-source and version guidance belongs to `find-docs`, with authority and evidence
boundaries in `AGENTS.md`.

## Validation

Run:

```bash
python3 scripts/check-skills.py
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

These checks validate repository structure, links, Skill entrypoint/scenario consistency and patch
whitespace. Stdlib tests also verify validator portability and three scanner regressions: non-object
JSON, an explicit subdirectory boundary and suspicious token assignments. They do not establish
that a model follows the instructions. Behavioral runs
use the prompts and grading criteria in [Behavior probes](evals/behavior-probes.md), with disposable
workspaces and recorded model/tool traces. This repository currently has no automated model-runner.
New contextual-Skill probes require two baseline and two candidate trials with identical settings in
fresh isolated sessions. Their current status is **UNTESTED**: isolation startup failed before a model
response, and automatic approval review rejected the network retry because specific authorization
for private instruction/path egress was missing. Static checks and source review are separate evidence.
