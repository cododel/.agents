---
name: feature-closeout
description: "Close an implementation task before finalization when material completion uncertainty remains or closeout is requested: check agreed acceptance, fix unambiguous authorized gaps, clarify material choices and recheck until PREPARED. Full closes the task; Quick checks interim alignment. Not a findings-only audit or broad cleanup."
---

# Feature Closeout

Bring the current agreed implementation task to completion before finalization. Check correctness,
quality and completeness, repair authorized gaps, clarify material choices and recheck. Use this skill
for material completion uncertainty or an explicit request; atomic work with decisive evidence needs
only compact normal completion. Task length, diff size, compaction and task records alone require
neither a separate ceremony nor independent reviewers. Read-only review requests grant no repair authority.

## Select the mode

- **Full (default)**: completion or handoff process; load [references/full.md](references/full.md).
- **Quick**: an explicitly requested interim checkpoint; load [references/quick.md](references/quick.md).
  Handle ordinary implementation uncertainty directly without introducing a separate checkpoint mode.

Natural language is sufficient. Legacy `--release` or "release closeout" explicitly requests
preparation followed by the separate frozen final audit documented in Full; briefly explain the
mapping. That read-only audit is outside the repair loop, not a new mode or an automatic next step.
Preserve the requested scope and demonstrated consumers. An atomic change with decisive evidence
needs only normal completion review; neither Full nor automatic Quick runs merely because a stage ends.

## Authority

An implementation request plus closeout permits reversible local repairs inside the agreed task and
its demonstrated affected radius. Fix confirmed unambiguous authorized defects immediately rather
than merely listing them. Ask the operator about material unresolved choices and continue independent
work. Review alone does not authorize product changes. Closeout grants no authority to expand
requirements, overwrite operator work, or perform external/shared mutations.

Update affected established documentation within scope. New contracts, Issues and ADRs follow their
owner skills and existing authority; closeout alone does not require additional artifacts.

## Common completion invariants

These rules own the shared procedure for all modes. Use
[testing-evidence](../testing-evidence/SKILL.md) when its scope applies; project-required gates remain required.
Closeout checks acceptance and closes authorized gaps, without an automatic fresh suite run or repository-wide test audit:

1. Establish the current agreed task, applicable contracts and actual changes. Use confirmed
   discussion or `task.md` for acceptance and `state.md` for progress/evidence. Resolve checkout
   identity where needed to distinguish the reviewed changes. Stop the affected path for a missing
   material decision; never substitute the implementation for agreed requirements. A separate source
   fingerprint is required only for the explicitly requested frozen final audit in Full.
2. Trace demonstrated consumers, interfaces, data/events, configuration, persistence, cleanup, and
   operator controls. Include security, concurrency, migrations, mixed-version behavior,
   rollback/recovery, feature gates and observability where affected. Map material criteria to
   implementation evidence, verification and status; no new record format is required.
3. Assess **correctness** against agreed behavior, **quality** of safety/types/maintenance, and
   **completeness** of consumers/failure paths/lifecycle/compatibility. Source, docs, parser/static
   checks, tests, and focused probes provide different evidence; a passing suite or clean diff is
   insufficient by itself.
4. Separate confirmed in-scope defects, unknowns, environment or pre-existing failures, and independent
   debt. Confirm and deduplicate findings; immediately repair unambiguous authorized defects and
   clarify material alternatives with the operator. Never weaken acceptance/tests to match
   implementation; expectation changes need an agreed behavior change or a demonstrated check defect.
5. After repairs, run missing or invalidated checks; reuse evidence only while relevant code,
   configuration and environment remain compatible. Review the final diff against the agreed task.
   Repeat Full until `PREPARED` or a concrete blocker prevents further authorized progress. Do not finalize with a repairable
   findings list. Keep Quick bounded to its checkpoint; it never certifies final completion.

Assess the agreed agent deliverable and prerequisites due at this handoff. Operator release work
is not an automatic prerequisite for local closeout. Keep separately assigned later verification
pending/unverified when relevant; local checks do not establish another environment's outcome.
For runtime evidence required by a current criterion or material risk, explain why local evidence
is insufficient and report the gap. Preserve project gates and agreed acceptance; missing permission
or environment does not defer a required check. Never invent a deferral or narrow acceptance.

For independent review, use isolated read-only contexts already available in the environment and
withhold builder conclusions when independence matters. Do not install an orchestration runtime to
simulate this evidence; missing contexts must remain visible under the selected mode's limits.

## Completion

Full success requires evidence for every material criterion within the agreed completion boundary
and no confirmed in-scope blocker on correctness, quality or completeness. Resolve obvious authorized
gaps and repeat assessment before finalizing; report a concrete unmet decision, prerequisite, evidence,
authority or agreed resource limit when it prevents further progress. Quick assesses only
criteria due at the checkpoint and prerequisites of the next step; it does not certify final
completion. Keep future criteria pending and disclose any requested end state not yet verified.

Record outcomes and gaps in `state.md` when active. Return mode/status, reviewed scope, decisive
evidence and material gaps. State the boundary with the verdict (for example, `Full — PREPARED for
local handoff`) and distinguish current blockers from agreed later verification. Zero findings is
valid; omit routine logs and reviewer transcripts.
