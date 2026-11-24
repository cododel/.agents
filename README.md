# .agents

Engineering standards, reusable agent skills and optional tooling for frontend visual review. [AGENTS.md](AGENTS.md) covers authority, Git ownership and verification. Individual project repositories own their architecture, commands and product requirements.

## Get started

Clone the repository into an ordinary directory with Git. If you already have a checkout, open its root and skip the clone.

```sh
git clone https://github.com/cododel/.agents.git engineering-skills
cd engineering-skills
```

The policy and skills are Markdown and can be read directly. To use them with a coding agent, give it the path to `AGENTS.md` and the relevant `SKILL.md` in this checkout. For example, ask it to “Read `capabilities/visual-code-review/SKILL.md` and prepare a desktop and mobile comparison of the changed screen.” From a different project, supply the absolute path to the skill. Keep the checkout together so relative links to shared guidance, scripts and assets resolve.

For automatic discovery in a client that accepts skill roots, select the checkout's `skills/` directory. Optional capabilities can be invoked by path. Policy loading is a separate client setting. Preserve existing instructions when adding a reference to `AGENTS.md`.

## Close an engineering task

Use [feature-closeout](skills/feature-closeout/SKILL.md) to finish the agreed task. Supply its requirements and the baseline and target when known. The agent checks the implementation, repairs confirmed gaps within its authority and rechecks the affected behavior. For substantial changes, a local visual report explains the final behavior, architecture, decisions, repairs and remaining gaps. Small changes can be handed off directly in the response. Request a read-only assessment when the implementation must remain untouched.

## Set up manual visual review

[Install ui-evidence](capabilities/visual-code-review/ui-evidence.md#install) to compare frontend screenshots in a local HTML report. The macOS/Linux setup uses the launcher, screen template and dependency lockfile from this checkout. It downloads the CLI and Chromium into a user directory outside the frontend project and requires no agent configuration or hooks.

For frontend acceptance, capture the baseline before editing or attach ui-evidence to two running builds. A one-off comparison can keep its configuration and report outside the app. Keep a screen definition in the project when the team will reuse it. The [visual review skill](capabilities/visual-code-review/SKILL.md) describes how to prepare the evidence and report missing coverage.

## Skills and repository map

The packages under [skills/](skills/) each have a `SKILL.md` describing when to use them, the procedure and the expected result. The [scenario matrix](evals/skill-scenarios.tsv) covers these top-level skill packages. The manual visual review capability is documented above.

| Area | Sources |
| --- | --- |
| Planning and delivery | [Feature brief](skills/feature-brief/SKILL.md), [Git operations](skills/git-operations/SKILL.md), [localization](skills/localization/SKILL.md), [feature closeout](skills/feature-closeout/SKILL.md), [task finish](skills/task-finish/SKILL.md) |
| Investigation and verification | [Troubleshooting](skills/troubleshooter/SKILL.md), [testing evidence](skills/testing-evidence/SKILL.md), [test-suite audit](skills/repository-test-audit/SKILL.md), [adversarial review](skills/adversarial-review/SKILL.md), [Chrome DevTools CLI](skills/chrome-devtools-cli/SKILL.md), [Redis](skills/redis/SKILL.md) |
| Architecture and documentation | [ADRs](skills/adr/SKILL.md), [contract authoring](skills/contract-writer/SKILL.md), [contract audit](skills/contract-auditor/SKILL.md), [documentation cleanup](skills/docs-cleanup/SKILL.md), [external documentation lookup](skills/find-docs/SKILL.md) |
| Writing and design | [Bug reports](skills/bug-report/SKILL.md), [pull requests](skills/pr-writer/SKILL.md), [Markdown preview](skills/markdown-preview/SKILL.md), [prose editing](skills/humanize/SKILL.md), [design system extraction](skills/design-system-extractor/SKILL.md), [Cododel post covers](skills/cododel-post-covers/SKILL.md) |
| Task coordination | [Task journal](skills/task-journal/SKILL.md), [issue triage](skills/issue-triage/SKILL.md), [deferred issues](skills/issue-writer/SKILL.md), [Kaneo](skills/kaneo-task-workflow/SKILL.md), [process friction audit](skills/process-friction-audit/SKILL.md), [skill evolution](skills/skill-evolution/SKILL.md) |
| Shared resources | [Cross-skill guidance](skills/_shared/), [macOS code intelligence manifest](capabilities/code-intelligence/manifest.json), [inactive Wiki skills](.disabled_skills/) |
| Evaluation | [Agent behavior scenarios](evals/agent-behavior.tsv), [behavior probes and recorded outcomes](evals/behavior-probes.md), [issue triage probes](evals/issue-triage-probes.md), [skill evolution probes](evals/skill-evolution-probes.md) |

## Validate the checkout

Run from the repository root. The Python checks use the standard library. The full set needs Git and [Bun](https://bun.com/docs/installation). The preview tests also need permission to listen on loopback.

```sh
python3 scripts/check-skills.py
python3 -m unittest discover -s tests -p 'test_*.py'
bun test tests/report-preview.test.ts
git diff --check
```

The [structure check](scripts/check-skills.py) matches `skills/*/SKILL.md` against the scenario matrix and checks local references in the skill tree. The [tests](tests/) exercise the validator, the session scanner and the Markdown preview server. For ui-evidence, [verify a first comparison](capabilities/visual-code-review/ui-evidence.md#verify-a-first-comparison). The [behavior probes](evals/behavior-probes.md) describe how to evaluate what an agent actually does and record the limits of each trial.
