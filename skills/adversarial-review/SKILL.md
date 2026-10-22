---
name: adversarial-review
description: "Investigate complex algorithms, business workflows, or vulnerabilities in owned systems through counterexamples and reproducible evidence. Use for adversarial acceptance or authorized security research; not ordinary implementation checks, a known-error diagnosis, or a formal contract/rollout audit."
---

# Adversarial Review

Try to falsify consequential guarantees within a defined scope. Produce reproducible findings and
bounded conclusions, including a useful negative result when no defect is found. Finding counts,
agent counts and green checks do not establish acceptance or security.

## Select the profile and authority

- **acceptance**: assess algorithms, business rules, state transitions and recovery against agreed
  behavior. Read [acceptance](references/acceptance.md).
- **security**: investigate how an actor could violate a protected property through reachable
  inputs or actions. Read [security](references/security.md).
- Combine profiles only when the request or concrete risk calls for both; retain the distinct
  correctness and exploitability claims. Natural language is sufficient to select a profile.

Resolve scope from the request and project sources. Ask early only for material missing decisions
about expected behavior, targets, permitted actions or acceptance; continue independent work.
Do not demand a new questionnaire when those decisions are already available.

Research authorizes inspection and permitted disposable probes, not product changes. If the request
also authorizes repairs, fix confirmed unambiguous in-scope defects and recheck them. Neither profile
grants production access, external attacks, dependency installation, publication or deployment.
Respect stricter project and environment boundaries. Record unavailable required evidence as a gap.

## Reuse existing owners

Load [testing-evidence](../testing-evidence/SKILL.md) before designing or interpreting verification.
It owns oracle quality, controls, causal error phases, doubles, execution evidence, RED/GREEN and
evidence reuse. Use the project's testing profile for commands and isolation; do not reproduce those
procedures here. If the dependency is unavailable, report it rather than claiming to have applied it.

Use [contract-auditor](../contract-auditor/SKILL.md) for an explicitly requested formal contract or
rollout audit; its frozen read-only verdict is not an invitation to enter this skill's repair loop.
Reading contracts as sources here does not invoke that audit or import its mandatory fan-out,
confirmation matrix and stop-on-blocker procedure. If both are requested, keep their phases explicit.
[feature-closeout](../feature-closeout/SKILL.md) owns completion of the overall implementation task.
This investigation can supply evidence to it without automatically invoking another audit.

## Establish a bounded investigation

Identify the research target; use testing-evidence for result identity and evidence invalidation.
The files and runtime state a probe depends on must remain identifiable during execution. Pause
affected probes or use an authorized isolated snapshot when concurrent changes make this impossible;
unrelated work need not stop. Do not require a whole-repository freeze for a scoped investigation.

Extract the important guarantees and their sources, actual entrypoints, decision owners, persistent
states, external effects and recovery paths. Distinguish agreed intent from implementation and test
expectations. Missing specification is not permission to invent product rules; a protected property
may also have an evidenced trust/ownership basis, as described in the security profile.

Choose scenarios by consequence, reachability, uncertainty and affected boundaries. Include critical
cross-owner paths, not just individually correct components. Keep the required outcomes and explicit
exclusions visible; a concise response suffices for a small investigation. Reuse task state when present.
Bound broad exploration by the agreed scope and available resources; ask about material tradeoffs
instead of silently narrowing required coverage. Do not require exhaustive state-space exploration.

Project scenarios, resource budgets, harness commands, model choices and team rosters belong in the
project/run context, not this skill. Do not introduce a new harness solely to satisfy the workflow.

## Investigate and challenge

Apply the selected profile to generate concrete counterexamples and test them using testing-evidence.
Trace the real entrypoint through the responsible boundary to observable consequences. Distinguish
an invalid operation accepted from a valid operation wrongly rejected. Exercise meaningful rule
interactions and failure/recovery paths rather than inflating a checklist with similar examples.

Delegate independent research or verification when it materially improves coverage or confidence.
Choose assignments by risk and ownership, with separate write/resource boundaries; no fixed roster
or model is required. Supply requirements and raw artifacts, initially withholding prior verdicts
where independent assessment matters. Share prior findings afterward for confirmation and deduplication.
Keep ordinary work with the primary researcher. Select independent confirmation when consequence
or uncertainty warrants it, or the agreed acceptance requires it; tool availability alone is not a
reason to add a reviewer. Disclose unavailable required independence rather than labeling self-review
independent. Resolve disagreement through evidence and requirement sources, not majority vote.

Do not expand the investigation merely because another area exists. Follow a newly exposed dependency
when it can change a material conclusion; make additions to the agreed scope visible.

## Findings and closure

Keep findings and coverage together in the response or existing record; use a durable register when
needed to retain multi-stage work. No separate report or prescribed table is required. Each material
finding should connect:

- the guarantee or protected property and its basis;
- affected version, conditions, actor where relevant, and observable consequence;
- reproduction and evidence under testing-evidence, with causal location and confirmation limits;
- repair direction, affected consumers and a concrete closure condition.

Keep statuses distinct: confirmed defect, hypothesis, unresolved requirement, evidence gap, supported
allowed behavior, and not reproduced on the stated version. Check execution status is separate:
a successful diagnostic probe may demonstrate a defect. Deduplicate by cause and repair ownership
without discarding distinct consequences. Prioritize impact, reachability and repair dependencies.

In research-only work, return findings and evidence-backed repair directions, ordered when dependencies
matter; unresolved hypotheses need the next distinguishing observation, not a speculative repair plan.
For authorized repairs, use testing-evidence for the repair/check cycle and evidence reuse. Retain the
original finding and assess its closure, including affected legitimate paths. This closes the scoped
finding, not the overall implementation task; do not restart unrelated discovery after each repair.

Report investigation coverage separately from its implications:

1. **Investigation:** complete within the stated scope, or incomplete with the specific remaining
   coverage, evidence, decision or access gap. A finished report does not close unperformed required
   research. Confirmed defects alone do not prevent completion of the remaining agreed investigation.
2. **Findings and implications:** state confirmed violations and remaining uncertainty. Give a scoped
   acceptance conclusion only when acceptance was requested and its criteria are defined; support it
   only with evidence for all required criteria and no unresolved blocker. Otherwise report the
   blockers/gaps without inventing a gate. A security-only search does not require an acceptance
   verdict. Overall task completion and formal rollout verdicts remain with their owners above.

Stop when the agreed investigation/repair outcomes have evidence or a concrete blocker prevents
progress. No defect quota or automatic repeated sweep. Cleanup follows project ownership rules;
report retained task-owned resources and material simulation limits. A completed investigation,
local acceptance, and readiness to deploy are different claims.
