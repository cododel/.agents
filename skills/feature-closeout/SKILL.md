---
name: feature-closeout
description: "Review a completed feature against current agreed motivation, behavior, affected radius, and evidence. Use for material acceptance/integration uncertainty or an explicit request; explicit `quick`, `full`, and `release` modes are supported. May repair confirmed in-scope gaps; not a small-task ceremony or repository-wide cleanup."
---

# Feature Closeout

Catch the kind of incomplete, locally correct, or structurally weak implementation that can survive a
normal coding pass. Closeout judges the feature on **correctness, quality, and completeness** against
the current agreed task, not against the implementing agent's latest summary.

Read `references/mode-contracts.md` completely for every invocation.

## When to run

Use closeout when material acceptance or integration uncertainty warrants a structured review, or
when explicitly requested. Choose checks for concrete risks such as cross-layer behavior, lifecycle,
compatibility, or incomplete acceptance evidence. Task length, diff size, compaction, and the presence
of task records alone do not require this skill or independent reviewers.

An atomic change with decisive evidence needs only normal completion review. Do not create records
or fan out merely to complete a template.

## Modes

- **`quick`** — compact self-review and focused evidence for a bounded change. No independent fan-out
  by default. May repair clear in-scope defects once.
- **`full`** — for substantive acceptance/integration review. Freeze the task contract, trace the
  affected radius, select useful review/verification vectors, independently where warranted,
  repair confirmed in-scope findings,
  and recheck only affected vectors through a bounded convergence cycle.
- **`release`** — explicit only. Run `full`, then add the project's integration/release checks,
  compatibility/rollback/operations evidence, and one final read-only review of the frozen result.
  Never deploy or mutate remote/shared state.

Natural language is sufficient; exact CLI-like flags are optional. If no mode is named, choose
`quick` or `full` according to the material acceptance/integration risks. Never infer `release`.
Optional user constraints such as base, scope, or evidence narrow discovery but do not permit ignoring
demonstrated consumers.

## Authority

An implementation request plus closeout authorizes local reversible fixes inside the current agreed task
and its demonstrated affected radius. It does not authorize:

- a new product or architecture decision;
- unrelated repository cleanup;
- push, merge, deploy, or persistent/shared database mutation;
- rewriting operator-owned changes;
- creating an ADR for a choice the operator did not make.

Update existing guarantees when agreed behavior changes. Create a new owner only when all
contract-writer value conditions hold. Stop only when documenting it would choose unresolved semantics.
Report independent debt; invoke `$issue-writer` only on a request to record/defer it.

## Freeze the review target

Before evaluating:

1. resolve repository/worktree, branch, HEAD, status, base, and the exact change inventory;
2. reconstruct the current agreed motivation, target behavior, acceptance, operator decisions, non-goals,
   and material assumptions from confirmed discussion and `task.md` when present; use `state.md`
   for progress, not as a replacement requirements source;
3. snapshot that task contract separately from the implementing agent's claims;
4. identify applicable living contracts and affected consumers;
5. record a source fingerprint so later fixes and rechecks cannot be confused with the first review.

If the current agreed task cannot be reconstructed reliably, stop only for the missing material
operator decision. Do not replace it with what the code happens to implement.

## Review model

Evaluate three independent dimensions:

- **Correctness:** does observed behavior satisfy the frozen task contract?
- **Quality:** is the implementation safe, typed, maintainable, idiomatic, and free of unjustified
  shortcuts or vulnerabilities?
- **Completeness:** are affected consumers, failure paths, cleanup, data/migration behavior,
  contracts, and acceptance evidence covered proportionally?

Use source, tests, focused runtime probes, current docs, and repository history as evidence. A passing
suite does not settle quality or completeness. A clean diff does not prove target behavior.

## Independent review and repair

In `full` and `release`, use independent read-only subagents when they can inspect distinct vectors
without inheriting the builder's conclusions. Typical vectors are:

- requirement and invariant coverage;
- affected-radius/data-flow and cross-module integration;
- failure paths, security, concurrency, resource lifecycle, and migration compatibility;
- implementation quality, type safety, and regression risk;
- focused QA and test-evidence adequacy.

Use isolated reviewer contexts already exposed by the current execution environment. Do not start,
install, or require an external orchestration runtime solely to satisfy review independence. If the
required independent contexts are unavailable, continue the useful inline review but apply the
selected mode's evidence limit honestly.

Choose only relevant vectors; do not launch a generic checklist swarm. The primary agent deduplicates
findings, confirms them against the frozen target, and repairs confirmed in-scope defects. After a
repair, re-run the focused checks and only the review vectors invalidated by that repair. Stop after at
most two repair/recheck rounds; remaining blockers become an explicit handoff, not an unbounded
audit-fix loop.

## Completion

A successful closeout requires evidence for all material acceptance criteria and no confirmed
in-scope blocker on correctness, quality, or completeness. Record criterion-level outcomes and
evidence gaps in `state.md` when task memory is active.

Return a concise semantic report:

- mode and terminal status;
- achieved behavior relative to the current agreed motivation;
- non-obvious implementation choices and why they serve that motivation;
- decisive verification/review evidence;
- remaining material risks, assumptions, or deferred Issues.

Do not dump a file list, full review transcript, or routine command log.
