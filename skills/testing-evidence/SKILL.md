---
name: testing-evidence
description: "Use when changing behavior and planning verification, writing/editing/reviewing tests, diagnosing test failures, or selecting/running/interpreting checks. Provides meaningful TDD and evidence-quality decisions; project profiles supply commands and required gates. Does not initiate a suite-wide audit."
---

# Testing Evidence

Own the portable testing procedure. Read the applicable project testing profile for commands,
isolation and required final gates; those requirements are not silently relaxed by global defaults.
Agreed acceptance defines done. Tests provide falsifiable evidence, not replacement requirements.

## Choose protection before implementation

For an observable behavior change, default to **RED → GREEN → REFACTOR**. Establish the intended
observable result independently of current implementation, find existing protection, and extend it
before adding a duplicate. A new permanent test needs a realistic failure, observable assertion,
independent expected-result basis and the production boundary that would actually fail. These can
be clear in the test/group itself; no form per assertion, test quota or required coverage growth.

Run a focused check on the defective/missing behavior before implementing. RED must express that
gap, not import, collection, fixture, timeout setup or missing-service noise. Reuse a trustworthy
existing failure. After the fix obtain GREEN, then refactor within the authorized scope and verify
invalidated protection. Never change acceptance or expectations merely to get green.

For behavior-preserving refactors, use existing tests first; strengthen/add only for a demonstrated
gap. Preparatory refactoring may establish a necessary seam; RED/GREEN is followed by proportional
cleanup, not a compulsory large refactor. Choose evidence by risk and claim, not changed filename.
Exploration/prototypes may precede tests: before production promotion establish independent acceptance
and integration/error evidence. Read [experiments.md](references/experiments.md) when a temporary PoC
or interactive operator demo resolves uncertainty more cheaply. Do not copy exploratory code as oracle.
Documentation, mechanical/trivial changes or disproportionate/unavailable seams may use a temporary
probe or source/static/UI evidence. Explain material RED/permanent-test limits; do not manufacture RED
or destructively revert operator work. Critical money/access/persistence/lifecycle risks still need
evidence at their responsible boundary, or an explicit gap.

## Judge the actual guarantee

Read assertions plus decisive setup/helpers and the subject. A double may provide inputs/external
responses, but must not implement the guarantee being tested. Real decisions over fake input and
mocked interaction contracts are valid; they do not prove the dependency's own side effects.
Reproduce the causal error phase: deferred flush/commit, lost acknowledgement after commit,
callback arrival, race overlap or shutdown drain is not interchangeable with an immediate throw.

Schemas, API payloads, architecture/import boundaries, snapshots, SQL commands, exact literals and
interaction/order assertions can protect real contracts. Reject incidental pins and self-confirming
expected algorithms, not assertion formats. A contract may already live in a schema/API/source rule;
a new Markdown contract is not required. Read [test-design.md](references/test-design.md) when
choosing a boundary/oracle, assessing doubles/timing, duplicates or legacy test value.

## Execute and interpret proportionately

Use focused risk-appropriate checks during iterations. Broaden for demonstrated affected consumers,
integration boundaries, relevant changes/failures or project policy. Preserve meaningful serial,
cross-OS/backend/runtime variations when they expose different risks; do not require them universally.
No automatic full suite, mutation campaign or fresh infrastructure per iteration.

Before handoff identify one canonical final evidence set: project-required gates, affected behavior,
relevant build/static checks and integration checks. Reuse current adequate results, run missing or
invalidated parts, and do not rerun merely because closeout starts. A focused subset cannot replace
a project-required full suite. Read [execution-evidence.md](references/execution-evidence.md) when
selecting/running/interpreting checks, reusing results or assembling final evidence.

Report material checks as **passed / failed / skipped / not-run**, with actual selection and limits.
Empty collection/setup failure is not behavioral success. Match claims to the observed boundary;
passing tests are not complete acceptance. After a dependent failure, an old green is stale until
the failure is resolved and suitable fresh evidence exists. Unknown dependency relevance is not green.

## Review without automatic cleanup

For a scoped test-value review, use retain/strengthen/consolidate/retire/investigate with evidence,
unique guarantee/removal risk and a specific next action. Never delete from a score, test count,
heuristic, coverage or absence of historic failures. Review-only intent does not authorize edits;
replacement/overlap must preserve distinct layers, inputs and timing/platform guarantees still
required. Retiring an obsolete requirement needs cancellation evidence and no dependent consumers
or remaining obligations, not artificial replacement; actual deletion needs separate authorization.
Use [repository-test-audit](../repository-test-audit/SKILL.md) for requested repository/suite audits,
not for an ordinary regression fix. Reuse existing task memory only when useful.
