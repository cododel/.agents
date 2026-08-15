# Feature closeout mode contracts

## Common closeout sequence

1. Resolve and fingerprint the source target before mutation.
2. Discover applicable living contracts, linked mutable Issues, relevant ADR provenance, migration
   surfaces, tests, runbooks, and repository verification commands.
3. Classify contract impact as `unchanged`, `extend`, `conflict`, or `missing` before changing a
   durable interface or behavior.
4. Keep every change inside the feature change-set and its demonstrated affected radius.
5. Revalidate drift-prone evidence immediately before using it. Preserve operator-owned changes and
   separate product failures from harness, environment, permission, and configuration failures.
6. Use the relevant specialized skill when its trigger applies. In particular, use `$tests` for
   test changes, `$migrations` for Alembic work, `$contract-writer` for approved contract updates,
   `$issue-writer` for specific mutable Issue records, and the ADR skills only within their authority
   gates.
7. Inspect every documentation or source-comment line changed by the closeout. Never rewrite an
   Accepted ADR body or treat a plan, Issue, test, schema, or type as an implicit living contract.
8. Run proportionate focused checks first and the relevant full suite before terminal success.

## Quick mode

Perform one shallow pass. Prefer deterministic and mechanical work:

- formatting, lint, type, import, generated-file, and documentation checks already owned by the
  repository;
- focused tests already implied by the changed surfaces;
- obvious missing test registration, stale links, and mutable status/anchor drift when current
  evidence makes the correction unambiguous;
- compact inspection of contract impact and release-sensitive gaps.

Do not make semantic contract changes, create or supersede ADRs, design migrations, broaden test
architecture, or decide ambiguous Issue closure. Report those as strong-model hand-offs. Run no
contract audit and provide no readiness verdict.

Make at most one bounded discovery/fix pass. Verification may repair the implementation once when a
test directly falsifies the intended change; do not turn newly discovered independent defects into a
recursive cleanup.

## Full mode

Perform a thorough implementation closeout:

- trace the complete affected call-site, configuration, persistence, interface, and ownership radius;
- align established living contracts when the approved behavior is an `extend`; stop on `conflict`
  or unapproved `missing` ownership;
- add or repair behavior tests with RED-GREEN evidence;
- verify migrations, compatibility, failure paths, retries, cancellation, concurrency, and resource
  cleanup in proportion to risk;
- update specific mutable Issues from current evidence, close completed records, and keep priority,
  severity, status, and filenames consistent;
- inspect relevant ADRs for provenance and code drift, but never rewrite Accepted bodies; create or
  supersede an ADR only through its significance and authority gates;
- align affected runbooks and operator controls without claiming unobserved production behavior;
- run focused checks, the relevant full suite, formatting/linting, documentation checks, migration
  head checks, and diff hygiene as applicable.

Do not invoke `$contract-auditor`. Finish after implementation verification with `PREPARED` or
`BLOCKED`.

## Release mode

First perform Full mode. Then complete production preparation appropriate to the feature risk:

- upgrade and compatibility path, feature/action gates, mixed-version behavior, and rollback;
- observability, alerts, cleanup ownership, failure isolation, and operator controls;
- required production-shaped or runtime evidence supplied through repeatable `--evidence` paths;
- clean task-owned background processes and verify their termination;
- repository-required commit or explicit dirty snapshot fingerprinting.

Resolve all implementation work before the final audit. Then:

1. Freeze and record the exact final fingerprint.
2. Invoke `$contract-auditor` once in `rollout-readiness` mode on that frozen target.
3. Pass the feature scope, contracts, named risks, executed checks, runtime evidence, and exclusions;
   do not pass an expected verdict.
4. Accept the auditor's terminal verdict. Do not mutate, implement findings, add evidence-producing
   code, broaden scope, or invoke another audit afterward.

The single terminal audit is explicitly authorized by `--release`; audit findings never authorize a
fix. Missing material runtime evidence produces `UNVERIFIED`, not a speculative `READY`.

## Output discipline

Lead with the terminal status. Distinguish measured, executed, derived, and unavailable evidence.
For changed artifacts, provide a compact mapping from closeout concern to change and verification.
List unrelated observations once under independent hand-offs; do not create Issues for them unless
the operator separately authorizes deferral.
