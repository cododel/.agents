---
name: feature-closeout
description: "Review feature completion or an intermediate alignment checkpoint against the current agreed task and evidence. Use for material acceptance/integration uncertainty or an explicit request. Full is the default; Quick checks interim alignment. May repair authorized in-scope gaps; not a small-task ceremony or repository-wide cleanup."
---

# Feature Closeout

Judge correctness, quality, and completeness against the current agreed task. Use this skill for
material acceptance/integration uncertainty or an explicit request. Task length, diff size,
compaction, and task records alone do not require closeout or independent reviewers.

## Select the mode

- **Full (default)**: completion or handoff review; load [references/full.md](references/full.md).
- **Quick**: explicit quick request or an automatic interim checkpoint when material uncertainty
  could carry a deviation into a dependent step; load [references/quick.md](references/quick.md).

Natural language is sufficient. Legacy `--release` or "release closeout" selects Full's explicitly
requested frozen final audit; briefly explain the mapping. Never infer that audit from ordinary Full.
Preserve the requested scope and demonstrated consumers. An atomic change with decisive evidence
needs only normal completion review; neither Full nor automatic Quick runs merely because a stage ends.

## Authority

An implementation request plus closeout permits reversible local repairs inside the agreed task and
its demonstrated affected radius. Review alone does not authorize product changes. Closeout grants
no authority to expand requirements, overwrite operator work, or perform external/shared mutations.

Update affected established documentation within scope. New contracts, Issues and ADRs follow their
owner skills and existing authority; closeout alone does not require additional artifacts.

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
   operator controls. Include security, concurrency, migrations, mixed-version behavior,
   rollback/recovery, feature gates and observability where affected. Map material criteria to
   implementation evidence, verification and status; no new record format is required.
3. Assess **correctness** against agreed behavior, **quality** of safety/types/maintenance, and
   **completeness** of consumers/failure paths/lifecycle/compatibility. Source, docs, parser/static
   checks, tests, and focused probes provide different evidence; a passing suite or clean diff is
   insufficient by itself.
4. Separate confirmed in-scope defects, unknowns, environment or pre-existing failures, and independent
   debt. Confirm and deduplicate findings before repairing. Never weaken acceptance/tests to match
   implementation; expectation changes need an agreed behavior change or a demonstrated check defect.
5. Repair only authorized confirmed defects within the selected procedure's limit. Use
   testing-evidence for missing checks and result reuse; re-review invalidated vectors after fixes,
   requirement or material environment changes. Review the final diff against the agreed task and
   refresh the fingerprint after source changes.

The mode does not require deployment or post-deploy smoke by itself. For required runtime evidence,
identify the applicable criterion or material risk and why it must be checked now. Preserve project
gates and agreed production acceptance; never defer them or narrow the requested result to obtain
success. Evidence of local readiness does not prove a requested deployed outcome.

For independent review, use isolated read-only contexts already available in the environment and
withhold builder conclusions when independence matters. Do not install an orchestration runtime to
simulate this evidence; missing contexts must remain visible under the selected mode's limits.

## Completion

Full success requires evidence for every material criterion in the requested result and no confirmed
in-scope blocker on correctness, quality or completeness. Quick assesses only criteria due at the
checkpoint and prerequisites of the next step; it does not certify final completion. Keep future
criteria pending and disclose any requested end state not yet verified.

Record outcomes and gaps in `state.md` when active. Return mode/status, reviewed scope, decisive
evidence and material gaps. Zero findings is valid; omit routine logs and reviewer transcripts.
