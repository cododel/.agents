---
name: config-audit
description: >
  Phased audit of a Claude Code configuration (project `.claude/` or global
  `~/.claude/`): inventory, instruction routing, CLAUDE.md pruning, skill
  triggering/freshness/collisions, hooks-agents-settings, trigger + functional
  evals, and the end-to-end workflow loop. Produces a timestamped P0–P3 findings
  report; every fix passes an explicit operator gate. Manual invocation only —
  run /config-audit.
disable-model-invocation: true
---

# Config Audit

## Purpose

Return precision and autonomy to the agent — not "tidy the files". The context
window is the only scarce resource: every artifact in `.claude/` either costs
context permanently (CLAUDE.md, skill descriptions, MCP tool schemas), on demand
(skill bodies, references), or not at all (hooks, `disable-model-invocation`
skills). An overloaded context is not "slightly slower" — it is degradation:
rules drown, skills stop triggering, the model ignores its own instructions.

Three questions for **every** file under review:

1. **Right place?** — routing: CLAUDE.md / rules / skill / hook / agent / settings.
2. **Worth its context price?** — "if I delete this line, will errors appear?"
3. **Verifiable?** — can we prove the artifact changes behavior? An untested
   skill is a hope, not a tool. This is TDD applied to configuration itself —
   skill-driven development (SDD): the same test-first discipline, with skills
   and config as the unit under test.

## Scope

`$ARGUMENTS` may name the target: a project root (audits its `.claude/`),
`global` (audits `~/.claude/`), or empty — ask which; default to the current
project. The audit is read-only end to end; fixes happen only after the Phase 8
operator gate.

## Workflow

Phases run in order. Load each reference only when its phase starts. Dispatch
noisy research (reading dozens of skill files, grepping session history) to
Explore subagents — the orchestrator works with their conclusions, not raw file
dumps.

| Phase | What | Read |
|---|---|---|
| 0 | Inventory snapshot — structure, sizes, dates, usage | `references/inventory.md` |
| 1 | Routing — every instruction in its right home | `references/routing-table.md` |
| 2 | CLAUDE.md pruning and truth-checking | `references/claude-md-audit.md` |
| 3 | Skills: triggering, structure, content, freshness, collision matrix | `references/skills-audit.md` |
| 4 | Agents, hooks, settings, MCP and plugins | `references/infra-audit.md` |
| 5 | Trigger evals — should / should-not / near-miss | `references/trigger-evals.md` |
| 6 | Functional evals — baseline, assertions, pressure | `references/functional-evals.md` |
| 7 | End-to-end workflow loop | `references/workflow-audit.md` |
| 8 | Report, prioritization, gate, cadence | `references/report-format.md` |

Phases 5–6 spawn real `claude -p` sessions and cost real tokens and minutes.
Confirm with the operator before running them; offering to defer them to a
follow-up session is the right default when the audit is exploratory.

A partial audit is legitimate: when the operator names a specific symptom, jump
straight to the matching phase via the red-flags table below — but say so in the
report ("phases 5–7 not run"), never let a partial audit read as a full one.

## Operator gate

Nothing is modified without confirmation. The Phase 8 report lists findings
P0–P3 with a one-sentence fix each; the gate mechanics and the P0/P1-vs-P2/P3
split live in `references/report-format.md`. Hand-offs to `issue-writer` (P2/P3
deferrals) and other siblings are *textual recommendations in the report* — the
operator runs them next; don't invoke a sibling skill directly mid-audit.
Deletions follow the standard discipline: list and verify targets, then ask.

## Output

Save the report to `reviews/<YYYY-MM-DD>-config-audit.md` (global config:
`~/.claude/reviews/`; project: `docs/reviews/` or the project's own convention).
Timestamped reports make the next audit comparable — progress over feelings.

## Red flags — quick diagnosis without a full audit

| Symptom | Diagnosis | Phase |
|---|---|---|
| Claude ignores a CLAUDE.md rule | File bloated, the rule drowns | 2 (prune / convert to hook) |
| Claude asks what CLAUDE.md already answers | Ambiguous wording | 2 |
| Skill doesn't fire on an obvious request | Description not pushy / request too simple to trigger | 5 |
| Wrong skill fires | Trigger collision | 3 (collision matrix) |
| Skill fires, output no better | Skill doesn't earn its price; no baseline eval | 6 |
| "Done", but tests are red | No verification loop / completion gate | 7 |
| Tests get fitted to the implementation | TDD in one context; split writer/implementer | 7 |
| Session degrades mid-task | Kitchen-sink context; research not in subagents | 7 |
| Same instruction pasted by hand a third time | SDD gap: that should be a skill | 1 |
| Claude bypasses a process rule "because urgent" | Loophole in wording; the *why* is missing | 6 (pressure test) |

## Composes with

- `issue-writer` — P2/P3 findings become tracked issues (file-based deferral).
- `adr-writer` — when an audit decision is architectural ("staging gated by
  hook, not prose"), capture it as an ADR.
- `docs-cleanup` — that skill audits *docs* (issues, ADRs, runbooks); this one
  audits *config* (`.claude/`). Same shape, different target — don't cross them.

## Design notes

- Manual-only (`disable-model-invocation: true`): an audit is expensive and
  operator-initiated by design; nothing here should auto-trigger. This also
  makes its description context-free between invocations.
- Cadence (full / spot / triggered) and the incident-as-config-bug framing live
  in `references/report-format.md` — the audit treats each "Claude did the wrong
  thing" incident as a config bug, not just its consequences.
- Deterministic measurement lives in `scripts/` (`inventory.sh`,
  `trigger-eval.sh`); the functional-eval fixture lives in `evals/` — prose
  doesn't re-derive what code can measure or what a fixture can prove.
