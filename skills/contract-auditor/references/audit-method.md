# Contract audit method

## 1. Select the mode

- `compliance`: map normative rules to implementation and verification evidence.
- `final-review`: add cross-layer correctness, negative paths, retries, cancellation, concurrency,
  and resource cleanup where relevant.
- `rollout-readiness`: add migrations, compatibility, feature flags, rollback, observability,
  operational controls, and production-like evidence required by the risk profile.
- `repeat-review`: layer on the requested mode, load prior findings as hypotheses, and revalidate
  them against current state.

The words `strict`, `final`, or `всесторонний` activate the strict protocol when they request an
independent final assessment. Production/rollout language selects `rollout-readiness`.

## 2. Resolve the target

An explicitly named checkout, worktree, revision, diff, or base wins. Otherwise:

1. confirm the repository root, current worktree, branch, HEAD, and `git status`;
2. resolve the primary branch from project instructions, then remote default branch, then an
   unambiguous local `main` or `master`; ask if no unique base can be proven;
3. use the merge-base with that primary branch;
4. inventory committed changes since merge-base, staged changes, unstaged changes, and relevant
   untracked files;
5. expand only through affected call sites, configuration, persistence, public interfaces, and
   resource ownership seams needed to test the changed behavior end to end.

Record exact target and base hashes. For an uncommitted target, also record deterministic hashes of
the staged diff, unstaged diff, and relevant untracked-file manifest. Together these values are the
snapshot fingerprint. Inspect staged and unstaged state separately when either may contain the real
implementation. Do not assume the visible checkout is the review target when the request or prior
findings name another worktree.

## 3. Discover contracts and known risks

Read applicable project instructions and documentation indexes, then use
`../../_shared/repository-discovery.md` from the sibling skill corpus.

- Fully read every living contract whose scope intersects the target or blast radius.
- Include OpenAPI, schema, or type surfaces only when project instructions or documentation
  explicitly declare them canonical, and only for their declared interface.
- Treat README/index text as routing, not an implicit normative owner.
- Treat Accepted ADRs as provenance, not current contracts.
- Treat tests as verification, not ownership, unless the project explicitly declares otherwise.
- Reverse-check every changed durable behavior or architecture boundary for one normative owner.
  No owner is `missing-contract`, never implicit compliance.

Build a compact inventory with `contract_path`, `scope`, and stable per-run rule IDs. When the
contract has no native IDs, use `<relative-path>#<section-slug>:<ordinal>`. Give every subagent the
same inventory and IDs.

Known risks come from the operator prompt and relevant open Issues, incidents, and contracts.
Runtime logs, dashboards, or production rows enter scope only when available through authorized
read-only access and relevant to the target. Record their timestamp/freshness; do not broaden into a
full operations audit silently.

## 4. Plan one fan-out wave

Run independent vectors by concern, not one agent per file.

Required strict vectors:

1. `contract-traceability` — rule ownership, implementation mapping, tests, and reverse coverage;
2. `failures-rollout` — failure paths, concurrency, lifecycle cleanup, and rollout blockers.

Add vectors only when the target warrants them:

- `executable-evidence` — declared schemas/types/OpenAPI plus their consumers and tests;
- `migration-compatibility` — upgrade/downgrade, mixed versions, backfill, flags, and rollback;
- `observability-lifecycle` — ownership, cleanup, cancellation, metrics, alerts, and operator view;
- `named-risk:<id>` — independent closure proof for each operator-named material risk.

Ordinary audits run one bounded parallel wave and no automatic full repeat. Strict review always
uses at least two independent subagents, even for a small diff. If the platform cannot provide that
independence, continue the useful inline review but the overall verdict cannot exceed `UNVERIFIED`.

Before launching, record a finite audit budget in the matrix: `max_vectors`, `max_agents`,
`max_discovery_passes=1`, `max_confirmation_passes=1`, and whether one conflict-resolution pass is
available. The strict default is at most four vectors with one agent per vector. Group named risks
into those vectors; exceed the default only when the operator explicitly names more independent
risks, and freeze the higher bound before discovery. Subagents never spawn audit subagents.

Freeze the contract inventory, rule IDs, vectors, named risks, scope exclusions, and snapshot
fingerprint before discovery. Any later confirmation uses these exact IDs and scope; do not add
search areas or reinterpret rules between phases.

### Cascade boundary

A cascade is a finite downstream consequence of one root defect through an exact control-flow,
data-flow, persistence, ownership, or resource-lifecycle edge. Record `root_finding_id`,
`causal_parent`, `causal_edge`, and `depth` for every claimed cascade consequence. Follow it only
inside the frozen causal frontier and audit budget. Deduplicate consequences that share one root
cause instead of inflating the finding count.

When a shared root is plausible but one causal edge is still missing, classify the observation as a
`cascade-candidate`, name the proposed root and missing proof, and keep it separate from confirmed
cascade consequences. Without either a demonstrable edge or a bounded falsifiable edge hypothesis,
classify it as an independent finding. If it is outside the frozen matrix, report an out-of-scope
hand-off and do not inspect it further. Changing code, contracts, configuration, or the snapshot
ends cascade analysis; it never starts a new recursive audit.

Pass each agent the resolved method paths, repository root, snapshot fingerprint, exact target/base
hashes, change inventory, contract inventory with rule IDs, known risks, and scope exclusions. Do
not include the expected answer or prior conclusions. Use `subagent-method.md` as the result schema.

## 5. Integrate and verify

- Re-open current files for every `blocker` or `high` finding and every proposed
  `contract-violation`, `contract-drift`, `missing-contract`, or `rollout-blocker`.
- Run the strongest focused read-only checks available. Distinguish product failures from harness,
  environment, permission, and configuration failures.
- Apply the blocker confirmation gate from `evidence-and-verdicts.md`. A candidate below the gate is
  a risk or verification gap, never a release blocker and never a reason to extend the audit.
- Include non-contract findings only when they create correctness, security, or operability risk
  for the rollout. Exclude style and maintainability-only observations.
- Deduplicate by `<class>|<rule-or-risk-id>|<root-cause>|<affected-surface>`, not prose similarity.
- Treat earlier review findings as hypotheses. Mark each `confirmed`, `obsolete`, `duplicate`, or
  `unverified` against the current target.

## 6. Confirm strict and repeat review

Use at most one full discovery pass, one candidate-confirmation pass, and one optional
conflict-resolution pass over the frozen matrix and snapshot. A clean streak is not required and
must not be simulated by repeating the full search.

1. Recompute the snapshot fingerprint after every vector and before integration or confirmation.
   If it changed, stop with `UNVERIFIED`; never continue or silently adopt the new target.
2. Complete the already-launched discovery wave. Do not add vectors, rules, or search areas after
   launch.
3. Confirm only `blocker`/`high` candidates and disputed prior findings with the strongest bounded
   read-only evidence. If there are no candidates, re-open only the material traceability rows
   needed to validate integration; do not rerun discovery.
4. Once one finding satisfies the blocker gate, fix the overall verdict at `NOT READY`. Collect
   results from the already-launched discovery vectors to inventory coexisting blockers, but start
   no new test, vector, or pass.
5. Use the optional third pass only to resolve conflicting independent evidence. It cannot discover
   new surfaces or reset the audit.

Any implementation hand-off ends this audit invocation. After a fix, only a new operator request
may authorize a new audit with a newly resolved fingerprint; a standing "until clean" instruction
does not. The sole exception is an explicitly declared composite release workflow that performed no
earlier audit, completed all mutations first, froze a new fingerprint, and invokes this audit once
as its terminal read-only step. If time, context, tool availability, independence, or required
evidence prevents this bounded protocol, report completed work and return `UNVERIFIED`.

## 7. Decide and report

Apply `evidence-and-verdicts.md`, then render `output-format.md`. Lead with confirmed findings. A
green test suite never overrides a contradicted contract, missing material runtime evidence, or an
unclosed named risk.
