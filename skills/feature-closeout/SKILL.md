---
name: feature-closeout
description: "Review a completed feature against current agreed motivation, behavior, affected radius, and evidence. Use for material acceptance/integration uncertainty or an explicit request; explicit `quick`, `full`, and `release` modes are supported. May repair confirmed in-scope gaps; not a small-task ceremony or repository-wide cleanup."
---

# Feature Closeout

Judge correctness, quality, and completeness against the current agreed task. Use this skill for
material acceptance/integration uncertainty or an explicit request. Task length, diff size,
compaction, and task records alone do not require closeout or independent reviewers.

## Select the mode

- **`quick`**: bounded self-review with proportional evidence; load [references/quick.md](references/quick.md).
- **`full`**: substantive acceptance/integration review; load [references/full.md](references/full.md).
- **`release`**: explicit only; satisfy Full, then load [references/release.md](references/release.md)
  for the frozen release review. Load both Full and Release procedures.

Natural language is sufficient. When unnamed, choose Quick or Full by material risk; never infer
Release. User constraints narrow discovery without excluding demonstrated consumers. An atomic
change with decisive evidence needs only normal completion review.

## Authority

An implementation request plus closeout permits reversible local repairs inside the agreed task and
its demonstrated affected radius. Review alone does not authorize product changes. New semantics or
architecture, unrelated cleanup, rewriting operator work, push/merge/deploy, and remote/shared
persistent mutations remain outside this authority.

Update existing guarantees when agreed behavior changes; use `$contract-writer` for a new owner only
under its value test. Record independent debt through `$issue-writer` only on a request to record or
defer it. ADR recording requires operator intent and an actual significant operator-made decision.

## Common review invariants

These rules own the shared procedure for all modes. Use
[testing-evidence](../testing-evidence/SKILL.md) for check adequacy, boundary/oracle quality and result
identity; project-required gates remain required. Closeout adds acceptance review, not an automatic
fresh suite run or repository-wide test audit:

1. Resolve repository/worktree, branch, HEAD, status, base, and exact change inventory. Freeze the
   current motivation, behavior, acceptance, decisions, non-goals, and material assumptions from
   confirmed discussion or `task.md`; `state.md` supplies progress/evidence, never acceptance.
   Identify applicable contracts and record a source fingerprint separately from builder claims.
   Stop the affected branch for a missing material requirement/decision; never substitute what the
   implementation happens to do.
2. Trace demonstrated consumers, interfaces, data/events, configuration, persistence, cleanup, and
   operator controls. Map each material criterion to implementation evidence, verification, and
   status without requiring a file for atomic work.
3. Assess **correctness** against agreed behavior, **quality** of safety/types/maintenance, and
   **completeness** of consumers/failure paths/lifecycle/compatibility. Source, docs, parser/static
   checks, tests, and focused probes provide different evidence; a passing suite or clean diff is
   insufficient by itself. Use `$find-docs` when external semantics remain unverified.
4. Separate confirmed in-scope defects, unknowns, environment or pre-existing failures, and independent
   debt. Confirm and deduplicate findings before repairing. Never weaken acceptance/tests to match
   implementation; expectation changes need an agreed behavior change or a demonstrated check defect.
5. Repair only authorized confirmed defects within the selected mode's limit. Re-run only checks and
   vectors invalidated by fixes, requirement changes, or material environment changes. Review the
   final diff against the frozen motivation and refresh the fingerprint after source changes.

For independent review, use isolated read-only contexts already available in the environment and
withhold builder conclusions when independence matters. Do not install an orchestration runtime to
simulate this evidence; missing contexts must remain visible under the selected mode's limits.
Do not require permanent tests, contracts, Issues, ADRs, or runbooks without independent maintenance
value.

## Completion

Success requires evidence for every material acceptance criterion and no confirmed in-scope blocker
on correctness, quality, or completeness. Record outcomes and gaps in `state.md` when active.
Return mode/status, achieved behavior, decisive evidence, material gaps, and useful non-obvious
choices. Zero findings is valid; omit routine logs, file inventories, and reviewer transcripts.
