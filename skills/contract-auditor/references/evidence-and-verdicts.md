# Evidence and verdict semantics

## Rule verdicts

- `compliant`: implementation evidence and proportionate verification demonstrate the complete
  rule on the reviewed target.
- `partial`: part of the rule is demonstrated, but a non-contradictory gap remains.
- `violated`: current implementation or observable behavior contradicts the normative rule.
- `unverified`: evidence is unavailable, stale, ambiguous, environment-blocked, or outside the
  authorized scope.

Use these evidence levels:

- `observed`: exact current file, configuration, schema, or timestamped read-only runtime evidence;
- `executed`: exact test/probe command was run and its result recorded;
- `derived`: a bounded inference from observed evidence, explicitly labelled;
- `assumed`: not evidence; it cannot support `compliant` or a readiness claim.

Configuration proves where a path points, not what exists behind it. Local tests do not prove
production state. A previous report is a hypothesis until refreshed against the current target.

## Blocker confirmation gate

A finding can block rollout only when all of these are true:

- an exact normative rule or named material risk is identified;
- a reachable production scenario and complete code/configuration trace are shown;
- existing guards and mitigations on that path were checked and found insufficient;
- impact is `blocker` or `high`; and
- proof is either an executed deterministic reproduction/probe, or a direct deterministic
  contradiction independently confirmed by at least two review vectors when execution is
  unavailable.

`derived` evidence alone, a hypothetical path, missing runtime proof, or one unconfirmed vector
cannot produce a release blocker. Preserve a proven contract violation; otherwise classify the supported risk or evidence gap.
Such a finding remains visible but does not stop or extend the bounded audit.

For every blocking candidate, record each gate item as an explicit boolean.
No aggregate score substitutes for a missing rule, reachability trace, mitigation check, impact, or
proof requirement.

## Finding classes

- `contract-violation`: implementation contradicts an established normative rule.
- `verification-gap`: implementation may comply, but material proof is incomplete.
- `contract-drift`: credible current-state evidence and the living contract diverge; the auditor
  does not decide which should change.
- `missing-contract`: an established consequential lasting obligation is insufficiently expressed
  in local code/docs and has no suitable normative owner; all contract-writer value conditions apply.
- `rollout-blocker`: a correctness, security, compatibility, operability, or lifecycle defect can
  make rollout unsafe even when it is not direct contract prose.
- `accepted-risk`: a non-contract rollout risk explicitly accepted by the operator in current
  authority or an explicitly authoritative project record. Never infer acceptance from silence.

Use `blocker | high | medium | low` severity and separately record readiness effect as
`blocker | risk | none`. Record the proof kind and missing evidence, if any. Exclude
maintainability-only findings with no contract or rollout effect.

## Traceability requirements

Every material rule row contains:

- rule ID and normative owner;
- the rule statement or a precise paraphrase;
- exact code/config/schema evidence;
- exact test, probe, or runtime evidence;
- rule verdict and evidence level;
- any gap or conflict.

An ADR or passing tests alone neither proves compliance nor automatically implies `missing-contract`;
identify the concrete ownership gap and apply all four value conditions before reporting it.

## Named-risk closure

Give each operator-named material risk its own matrix. For a resource leak such as leaked servers,
cover at minimum:

- lifecycle ownership and terminal states;
- cleanup on success, failure, cancellation, timeout, and partial initialization;
- concurrency, races, retries, and idempotency;
- detection through logs, metrics, health state, or operator-visible inventory;
- regression/stress evidence and required production-like observation.

Use the same four rule verdicts per dimension. A confirmed live leak or broken cleanup path is a
`rollout-blocker`. Missing material concurrency or runtime proof is `unverified` and prevents a
readiness claim.

## Overall verdict precedence

The overall verdict covers the audited contract and acceptance boundary, not deployment permission.
A proven material contract violation fails that boundary regardless of severity. Its rollout effect
remains separate: only the blocker confirmation gate permits `readiness effect: blocker`.
A violation requires current evidence of an exact normative contradiction; suspicion remains unverified.

Apply in this order:

1. `NOT READY` when a material contract violation is proven, a finding satisfies the rollout
   blocker confirmation gate, or an evidenced material non-contract rollout risk remains unaccepted.
   State whether the reason is noncompliance, a confirmed rollout blocker, or pending risk acceptance;
   pending acceptance is not an evidence gap and does not itself make the risk a blocker.
2. `UNVERIFIED` when no `NOT READY` condition holds but a material rule/risk is `partial` or
   `unverified`, unresolved contract drift prevents determining the governing rule, a missing
   contract prevents comparison, required production-like evidence is absent, independent strict fan-out was unavailable, or the bounded confirmation protocol was
   not completed.
3. `READY WITH ACCEPTED RISKS` when all material contract rules and required evidence are complete,
   no violation/blocker remains, and the only remaining rollout risks were explicitly accepted.
4. `READY` when all material rules are compliant, all named risks are closed, required evidence is
   present, no rollout-relevant finding remains, and the strict confirmation protocol completed
   when required.

Explicit risk acceptance cannot waive a contract violation or unresolved conflict. Green tests
cannot raise a lower verdict. When a still-valid `NOT READY` condition and verification gaps coexist,
retain `NOT READY` and list the gaps separately. Evidence for an obsolete snapshot cannot establish the current verdict.
