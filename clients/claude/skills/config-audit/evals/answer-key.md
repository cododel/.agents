# config-audit functional-eval answer key

Twelve planted configuration defects in the fixture produced by
`make-fixture.sh`. Use per `references/functional-evals.md` §1: run a baseline
audit WITHOUT the skill (RED) and WITH it (GREEN), score each run's findings
against this key. The skill earns its context price only if GREEN catches what
RED misses.

| id | artifact | defect | phase that should catch it |
|----|----------|--------|----------------------------|
| k1 | `.claude/CLAUDE.md` | `npm run lint:all` — no such script in package.json (dead command) | 2 |
| k2 | `.claude/CLAUDE.md` | "ALWAYS run prettier / NEVER skip formatting" — always-rule that belongs in a PostToolUse hook | 2 |
| k3 | `.claude/CLAUDE.md` | 15-step release procedure inline — a workflow that belongs in a skill | 1, 2 |
| k4 | `.claude/CLAUDE.md` | `@docs/conventions.md` import does not exist (broken import) | 2 |
| k5 | `.claude/CLAUDE.md` | "We use TypeScript / source in src/" — facts derivable from the code (context waste) | 2 |
| k6 | `.claude/commands/deploy.md` | legacy command — should migrate to a skill | 1 |
| k7 | `skills/api-docs` | description "Helps with API documentation." has no triggering conditions (no "when") | 3.1 |
| k8 | `skills/api-docs` + `skills/docs-helper` | trigger collision on API-doc requests; no anti-trigger either way | 3.5 |
| k9 | `skills/docs-helper` | references `references/missing.md` — dead path | 3.4 |
| k10 | `skills/docs-helper` | mentions `/fork the session` — stale/renamed platform command | 3.4 |
| k11 | `.claude/settings.json` | `Bash(*)` — overly broad permission | 4 |
| k12 | `.mcp.json` | `weather` MCP server with no evident use (context tax) | 4 |

## Recorded baseline (2026-06, this skill's own RED/GREEN)

- **RED** (no skill, 2 runs): 9/12 both runs — consistently missed **k5** (facts-from-code), **k6** (legacy command), **k12** (unused MCP).
- **GREEN** (with skill, 2 runs): 12/12 and 11/12 — the skill closed k5/k8/k12; one run still missed k6.

The lift on k5/k12 (context-waste defects a naive audit overlooks) is what
justifies the skill. k6 remains the weakest catch — a candidate for sharpening
`references/routing-table.md`'s legacy-`commands/` emphasis if a re-run regresses.
