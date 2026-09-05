---
name: contract-auditor
description: "Read-only audit of an implementation or change-set against living contracts or explicit production-readiness criteria. Use for strict contract compliance, rollout verdicts, or named-risk closure; not contract/ADR authoring or maintainability-only review."
---

# Contract Auditor

## Purpose

Prove whether current implementation satisfies its living contracts. In stricter modes, combine
that traceability with failure-path and rollout evidence without turning the audit into a general
style review or silently changing the system.

Read `../contract-writer/references/contract-spec.md` as the definition of a living contract. Never
copy or reinterpret that specification here. Read all four local references before reporting:

- `references/audit-method.md` — mode, target, discovery, fan-out, and confirmation workflow;
- `references/subagent-method.md` — shared read-only task and JSON result contract;
- `references/evidence-and-verdicts.md` — rule, finding, named-risk, and overall verdict semantics;
- `references/output-format.md` — findings-first report shape.

## Modes

| Intent | Mode | Coverage |
|:--|:--|:--|
| Check implementation against current contracts | `compliance` | Contract rules and reverse ownership check |
| Run a final cross-layer functional review | `final-review` | Compliance plus failure paths and rollout-relevant correctness |
| Decide whether production rollout is supportable | `rollout-readiness` | Final review plus compatibility, controls, observability, rollback, and required runtime evidence |
| Re-check prior findings with bounded confirmation | `repeat-review` | Overlay on one of the modes above; revalidate current state and deduplicate |

Map “strict final” plus production/rollout language to strict `rollout-readiness`. Map an explicit
repeat/re-review request to `repeat-review` over the requested base mode.

## Core workflow

1. Resolve the exact target, base, worktree, and change-set without mutating them.
2. Discover and fully read the relevant living and explicitly declared executable contracts.
3. Assign stable per-run rule IDs and reverse-check changed durable behavior for a missing owner.
4. Freeze one audit matrix, causal frontier, and explicit audit budget, then run one bounded
   discovery fan-out. Strict review requires at least two independent vectors.
5. Apply the confirmation gate to every blocking candidate, then deduplicate.
6. Apply the bounded confirmation protocol in `references/audit-method.md` to the same immutable
   snapshot. Never repeat the full search, fix findings, or restart an audit automatically.
7. Report traceability, named-risk closure, remaining gaps, hand-offs, and one overall verdict.

## Read-only boundary

- Do not edit code, contracts, ADRs, tests, Issues, dashboards, or configuration.
- Do not stage, commit, push, deploy, migrate, enqueue, or perform production/database mutations.
- Tests and read-only probes are allowed when they do not rewrite tracked sources. Record exact
  commands, scope, results, and environment limits.
- A confirmed blocker fixes the verdict at `NOT READY`. Finish only the already-launched discovery
  vectors so the report inventories coexisting blockers; do not start another vector, pass, or
  search area. Implementation and any later audit require a new operator request and a newly
  resolved target.
- A declared composite release workflow may invoke this skill once as its terminal step when the
  operator explicitly selected preparation plus final audit before any mutation. Require a newly
  frozen target, remain read-only, and return the terminal verdict to the orchestrator. Never return
  authority to fix a finding or repeat the audit.
- Report `missing-contract` with a recommendation for `$contract-writer`; this read-only audit
  does not invoke a writer with mutation authority. Creation requires a separately authorized scope.
- Zero findings is a valid outcome. Do not invent defects to fill a report or meet a finding count.
- Stop on a contract conflict for an operator decision. Hand off confirmed defects separately.

## Trigger boundary

Run this skill on explicit contract/final/rollout review requests. Recommend it before a high-risk
production rollout involving persistence, security, compatibility, resource lifecycle, or another
hard-to-reverse boundary. Do not impose it on every delivery.
