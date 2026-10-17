# Shared Agent Configuration

This repository is the canonical source for the operator's cross-client engineering policy, portable
Skills, and scenarios for evaluating agent behavior. Client adapters import or link to these
sources; project repositories own their architecture, commands, conventions, and project-specific
workflows.

## Repository Map

| Source | Responsibility |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Always-on policy: authority, ownership, engineering standards, evidence, and completion. |
| `skills/<name>/SKILL.md` | A portable Skill's trigger, boundaries, procedure, and expected outcome. |
| `skills/<name>/references/` | Details loaded only for the relevant stage or question. |
| `skills/<name>/assets/` | Templates and fallback resources. |
| [Shared references](skills/_shared/) | Guidance on finding repository records and maintaining durable documentation. |
| [Code intelligence manifest](capabilities/code-intelligence/manifest.json) | Declarative tool requirements and repair commands. |
| [Skill scenarios](evals/skill-scenarios.tsv) | Trigger, near-miss, required-outcome, and forbidden-outcome cases. |
| [Agent behavior scenarios](evals/agent-behavior.tsv) | Policy-level behavior cases. |
| [Behavior probes](evals/behavior-probes.md) | Concrete prompts, grading criteria, execution method, and dated evidence status. |
| [Issue triage probes](evals/issue-triage-probes.md) | Ranking, causality, repeat-review, and visual-analysis cases. |
| [Validator](scripts/check-skills.py) and [tests](tests/) | Structure checks and regression tests for repository utilities. |
| [.disabled_skills/](.disabled_skills/) | Inactive historical Wiki Skills, outside the active entrypoint matrix. |

Keep each rule in one place: policy in `AGENTS.md`, reusable procedures in Skills, and project facts
in project sources. Client/system requirements remain authoritative. Explicit operator instructions
and applicable project rules refine the defaults within their authority.

## Portable Skills

The repository has **26 portable Skill entrypoints**, matched against the scenario matrix by the
validator. This is a source inventory, not proof of installation or discovery in every client.

- Documentation and design: `adr-auditor`, `adr-writer`, `contract-auditor`, `contract-writer`,
  `design-system-extractor`, `docs-cleanup`, `humanize`, `issue-writer`.
- Engineering and verification: `chrome-devtools-cli`, `feature-brief`, `feature-closeout`,
  `figma-css-cleanup`, `git-operations`, `localization`, `merge-branches`, `troubleshooter`,
  `worktree-task`, `worktree-finish`, `testing-evidence`, `repository-test-audit`.
- Context and coordination: `find-docs`, `find-skills`, `kaneo-task-workflow`, `task-journal`,
  `yougile-workflow`, `issue-triage`.

Each Skill's description and entrypoint explain when to use it. Use context helpers when they
address a relevant uncertainty or evidence question. Review, cleanup, tracker, and external-write
workflows need the corresponding operator intent or a declared project workflow. Mentioning a topic
alone does not authorize a workflow or external action.

[Testing evidence](skills/testing-evidence/SKILL.md) describes how to choose and assess
verification; project profiles supply commands, isolation requirements, and required checks.
[Feature closeout](skills/feature-closeout/SKILL.md) checks completion when requested or when a
material question about completion remains. Small, self-contained changes with clear evidence need
no separate closeout process. [Task journal](skills/task-journal/SKILL.md) records the agreed task
and work progress under `.tmp/tasks/<task-id>/` when they become hard to retain reliably; `/.tmp/`
is ignored.

## Client Integration

Clients must expose the canonical policy and Skills through their supported loading mechanism. The
local `~/.codex/AGENTS.md` symlink resolves to this repository's `AGENTS.md` (checked 2026-10-17).
That proves the file target only; client loading and behavior need separate evidence.

There are no tracked client adapters or client-only Skills under `clients/`. The validator supports
`clients/<client>/skills/` if such sources become necessary. Empty local directories are not an
installed adapter. Check source files, installed plugins, client discovery, and runtime state
separately. Keep app-managed plugins, bundled Skills, credentials, caches, histories, and runtime
databases outside this repository.

## Capability Boundaries

The code intelligence manifest declares `ast-grep` for macOS, minimum version `0.45.0`, with `brew
install ast-grep` as its repair command. The validator does not read this manifest or check
installed tools. Navigation guidance lives in `AGENTS.md`; this repository supplies no LSP bridge.

Use retrieval tools exposed by the selected client. This repository supplies no search-provider
integration layer. Configure any additional crawling, export, or SDK support in the relevant harness
or project. [Find docs](skills/find-docs/SKILL.md) explains how to use primary sources and check
version compatibility.

For a local Kaneo MCP registration, use the stable `~/.bun/bin/bunx` launcher with
`@kaneo/mcp@latest serve`, rather than a resolved entrypoint inside a temporary `bunx-*` directory.
Pin a tested version when the compatibility policy requires it. The launch command alone does not
show whether a server is registered, authenticated, or available. Inspect the selected connector's
current tool declarations through [Kaneo workflow](skills/kaneo-task-workflow/SKILL.md). Device-flow
credentials are runtime state, not shared configuration.

## External Skill Provenance

`find-skills` is locally maintained, derived from `vercel-labs/skills`,
`skills/find-skills/SKILL.md` (former installer folder hash
`76a98a285cb0434f3d39e1a873823556330e398b`). It is no longer installer-managed; review upstream
changes manually and preserve the rule that discovery requires a concrete capability gap or an
explicit request.

## Validation

From the repository root, using Python's standard library:

```bash
python3 scripts/check-skills.py
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

The validator checks Skill metadata, agreement between entrypoints and scenarios, local links inside
`skills/` and `clients/`, client-neutral runtime sources, and that locally maintained `find-skills`
stays out of installer management. It does not check links in this README, capability
installation, native discovery, or model behavior. The tests check validator portability and how the
session scanner handles non-object JSON, explicit subdirectory boundaries, and suspicious token
assignments. `git diff --check` checks patch whitespace.

See [Behavior probes](evals/behavior-probes.md) for the trial method and dated results. This
repository has no automated model-runner. Older contextual trials remain untested or unverified as
recorded there. The clarification screening on 2026-10-17 records 24 candidate-only trials that
passed criteria fixed before execution. Those trials provide no baseline comparison or proof of
general reliability; the migration-stage scenario remains untested. Local trial artifacts under
`.tmp/` are not versioned. Structural checks and prose scenarios do not establish behavioral
success.
