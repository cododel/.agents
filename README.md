# .agents

Universal engineering policy, reusable Skills, and scenarios for evaluating agent behavior.
Project repositories own their architecture, commands, conventions, and project-specific workflows.

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
in project sources. Project `AGENTS.md` files should link to global rules instead of copying them;
repeat only what is needed to make a project-specific difference explicit. Explicit operator
instructions and applicable project rules refine the defaults within their authority.

Not every harness reads `~/.agents/AGENTS.md` automatically. If needed, symlink its supported
global instruction path to `~/.agents/AGENTS.md`.

## Portable Skills

The repository has **28 portable Skill entrypoints**, matched against the scenario matrix by the
validator.

- Documentation and design: `adr-auditor`, `adr-writer`, `contract-auditor`, `contract-writer`,
  `design-system-extractor`, `docs-cleanup`, `humanize`, `issue-writer`.
- Engineering and verification: `chrome-devtools-cli`, `feature-brief`, `feature-closeout`,
  `adversarial-review`, `figma-css-cleanup`, `git-operations`, `localization`, `merge-branches`, `troubleshooter`,
  `worktree-task`, `worktree-finish`, `testing-evidence`, `repository-test-audit`.
- Context and coordination: `find-docs`, `find-skills`, `kaneo-task-workflow`, `task-journal`,
  `yougile-workflow`, `issue-triage`, `process-friction-audit`.

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

## External Skill Provenance

`find-skills` is locally maintained, derived from `vercel-labs/skills`,
`skills/find-skills/SKILL.md` (source folder hash
`76a98a285cb0434f3d39e1a873823556330e398b`). Review upstream changes manually and preserve the
rule that discovery requires a concrete capability gap or an explicit request.

## Validation

From the repository root, using Python's standard library:

```bash
python3 scripts/check-skills.py
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

The validator checks Skill metadata, agreement between entrypoints and scenarios, local links in
Skills, and source portability. It does not check links in this README or model behavior. The tests
check validator portability and how the session scanner handles non-object JSON, explicit
subdirectory boundaries, and suspicious token assignments. `git diff --check` checks patch whitespace.

See [Behavior probes](evals/behavior-probes.md) for the trial method and dated results. This
repository has no automated model-runner. Older contextual trials remain untested or unverified as
recorded there. The clarification screening on 2026-10-17 records 24 candidate-only trials that
passed criteria fixed before execution. Those trials provide no baseline comparison or proof of
general reliability; the migration-stage scenario remains untested. Local trial artifacts under
`.tmp/` are not versioned. Structural checks and prose scenarios do not establish behavioral
success.
