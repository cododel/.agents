# Feature closeout mode contracts

## Common sequence

1. Freeze the original task contract and source fingerprint before reviewing the implementation.
2. Discover the exact diff plus demonstrated affected consumers, configuration, persistence, events,
   interfaces, contracts, and operator controls.
3. Build a compact acceptance matrix: requirement/invariant → implementation evidence → verification
   evidence → status.
4. Evaluate correctness, quality, and completeness independently.
5. Distinguish confirmed in-scope defects, material unknowns, environment failures, pre-existing
   failures, and independent debt.
6. Repair only confirmed defects authorized by the original implementation scope. Route independent
   debt through `$issue-writer` with a useful TODO link when appropriate.
7. Re-run only checks and review vectors invalidated by fixes; cap remediation at two rounds.
8. Review the final diff against task motivation and update `$task-journal` before handoff.

Do not require a permanent test, contract, Issue, ADR, or runbook unless that artifact has independent
maintenance value. Use `$find-docs` for current APIs and query an existing Graphify graph when it can
accelerate affected-radius discovery; verify conclusions in source.

## Quick mode

Use for a bounded, well-understood feature or fix.

- Reconstruct the target behavior and inspect the changed radius.
- Run focused reproduction/tests plus relevant type/lint/static checks.
- Inspect obvious failure paths, unsafe typing, stale comments/docs, and scope drift.
- Repair one clear in-scope defect pass, then rerun focused checks.
- Do not fan out by default, run a repository-wide audit, force a full suite, or claim release
  readiness.

Terminal status:

- `CLOSED` — target behavior and proportional verification are supported;
- `BLOCKED` — a material decision/evidence gap or confirmed defect remains.

## Full mode

Use for a large, cross-layer, compaction-prone, multi-agent, or high-autonomy feature.

### Required review vectors

Select at least two genuinely independent vectors, usually including:

1. **Task-contract coverage** — compare the frozen motivation, scenarios, decisions, invariants,
   non-goals, and acceptance to the implementation without relying on the builder summary.
2. **Affected-radius integration** — trace callers/consumers, state/data/event flow, configuration,
   persistence, cleanup, and compatibility.

Add quality/security/failure-path/QA vectors when relevant. Give reviewers read-only targets and
structured evidence outputs. Blind them to prior conclusions when independence matters.

### Verification

- Prefer focused regression/behavior tests and runtime probes for the changed surfaces.
- Add or improve permanent tests for critical behavior, bug regressions, and domain/business rules
  when the harness value justifies maintenance cost.
- Temporary tests/probes are acceptable for legacy or difficult seams when they provide stronger
  falsifiable evidence.
- Run broader suites only when affected radius or project policy warrants them; full-suite success is
  not a substitute for semantic review.
- Inspect correctness, implementation quality/security/type safety, and completeness separately.

### Repair convergence

The primary agent confirms and deduplicates findings. It may repair in-scope findings, update
unambiguous contracts, and create/update technical-debt Issues. Re-review only invalidated vectors.
After two repair rounds, stop with remaining blockers and evidence rather than consuming context in an
open-ended search for perfection.

Terminal status:

- `PREPARED` — no confirmed in-scope blocker remains and material acceptance has evidence;
- `BLOCKED` — unresolved operator fork, missing decisive evidence, or confirmed defect remains.

## Release mode

`release` is explicit and never inferred. First satisfy `full`, then add the project's actual
integration/release handoff:

- relevant full suites, builds, migration checks, and generated-artifact checks;
- upgrade/downgrade or mixed-version behavior where applicable;
- rollback/recovery and feature/action gates;
- observability, operator controls, cleanup ownership, and failure isolation;
- production-shaped evidence supplied locally or through already authorized read-only tools;
- termination of task-owned processes and a final exact fingerprint.

Then run one final independent read-only review on that fingerprint. Use `$contract-auditor` only when
living contracts materially govern the feature or the operator explicitly requests contract/rollout
compliance; otherwise use a bounded release reviewer. The terminal reviewer does not fix findings.
Use an isolated reviewer context already available in the current execution environment; do not start
or install an external orchestration runtime solely for this step. If no such context is available,
the release result is `UNVERIFIED` rather than simulated independence.
Any resulting fix requires leaving the frozen review, producing a new fingerprint, and an explicit new
release review invocation.

No deploy, push, merge, remote mutation, or shared/persistent database action is implied.

Terminal status:

- `READY` — required local/review evidence supports the handoff;
- `NOT READY` — a confirmed blocker exists;
- `UNVERIFIED` — required evidence is unavailable or cannot be trusted.

## Output discipline

Lead with terminal status and achieved behavior. Include only decisive evidence and non-obvious
motivation. List independent debt by Issue link. Do not repeat routine file paths, every command, or
reviewer transcripts.
