---
name: feature-closeout
description: "Review a completed feature against original motivation, behavior, affected radius, and evidence. Auto-use for large or high-autonomy handoff; explicit `quick`, `full`, and `release` modes are supported. May repair confirmed in-scope gaps; not a small-task ceremony or repository-wide cleanup."
---

# Feature Closeout

Catch the kind of incomplete, locally correct, or structurally weak implementation that can survive a
normal coding pass. Closeout judges the feature on **correctness, quality, and completeness** against
the original task contract, not against the implementing agent's latest summary.

Read `references/mode-contracts.md` completely for every invocation.

## When to run

Run automatically before handoff when one or more materially applies:

- the operator delegated a large feature with substantial implementation freedom;
- the diff crosses modules, layers, persistence, events, permissions, or stable interfaces;
- the task survived compaction, several sessions, or multiple subagents;
- acceptance depends on more than one local test or happy path;
- the operator explicitly requests closeout, final review, QA, or release preparation.

Do not run for an atomic edit whose behavior and verification are already obvious. A normal task may
still use the compact completion review in global instructions without invoking this Skill.

## Modes

- **`quick`** — compact self-review and focused evidence for a bounded change. No independent fan-out
  by default. May repair clear in-scope defects once.
- **`full`** — default for large or high-autonomy implementation. Freeze the task contract, trace the
  affected radius, run independent review/verification vectors, repair confirmed in-scope findings,
  and recheck only affected vectors through a bounded convergence cycle.
- **`release`** — explicit only. Run `full`, then add the project's integration/release checks,
  compatibility/rollback/operations evidence, and one final read-only review of the frozen result.
  Never deploy or mutate remote/shared state.

Natural language is sufficient; exact CLI-like flags are optional. If no mode is named, infer
`quick` for a bounded task and `full` for a large/high-autonomy task. Never infer `release`.
Optional user constraints such as base, scope, or evidence narrow discovery but do not permit ignoring
demonstrated consumers.

## Authority

An implementation request plus closeout authorizes local reversible fixes inside the original task
and its demonstrated affected radius. It does not authorize:

- a new product or architecture decision;
- unrelated repository cleanup;
- push, merge, deploy, or persistent/shared database mutation;
- rewriting operator-owned changes;
- creating an ADR for a choice the operator did not make.

Update or create a living contract without another gate only when the normative behavior is already
explicit and contract ownership is unambiguous. Stop when documenting it would decide unresolved
semantics. Route independent debt to `$issue-writer` instead of expanding the closeout.

## Freeze the review target

Before evaluating:

1. resolve repository/worktree, branch, HEAD, status, base, and the exact change inventory;
2. reconstruct the original motivation, target behavior, acceptance, operator decisions, non-goals,
   and material assumptions from the current conversation, active plan, brief, and `$task-journal`;
3. snapshot that task contract separately from the implementing agent's claims;
4. identify applicable living contracts and affected consumers;
5. record a source fingerprint so later fixes and rechecks cannot be confused with the first review.

If the original task contract cannot be reconstructed reliably, stop only for the missing material
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

Independent semantic review should use a model capable of the task's reasoning depth. Cheaper models
are appropriate for deterministic scans and test execution, not as the sole judge of cross-module
requirements, architecture, or security unless local evals prove them reliable.

## Completion

A successful closeout requires evidence for all material acceptance criteria and no confirmed
in-scope blocker on correctness, quality, or completeness. Update the active task journal before
handoff.

Return a concise semantic report:

- mode and terminal status;
- achieved behavior relative to the original motivation;
- non-obvious implementation choices and why they serve that motivation;
- decisive verification/review evidence;
- remaining material risks, assumptions, or deferred Issues.

Do not dump a file list, full review transcript, or routine command log.
