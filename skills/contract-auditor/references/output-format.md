# Contract audit output format

Write in the user's or project's working language. Keep identifiers and verdict labels exact.

## Findings-first report

```markdown
## Findings

1. [blocker] <short title>
   - class: `contract-violation`
   - rule/risk: `<id>` — `<contract path>`
   - confidence/proof: `<0.00-1.00>` / `<executed or two-vector deterministic confirmation>`
   - cascade: `<root | confirmed consequence through exact edge | candidate plus missing proof | independent>`
   - blocker gate: `<six explicit true/false checks>`
   - reachability: `<production entry to harmful result>`
   - mitigations checked: `<guards/fallbacks>`
   - evidence: `<current code/runtime evidence>`
   - readiness effect: `blocker`
   - hand-off: `<bounded next action; no mutation by auditor>`

No confirmed findings.  <!-- use only when the list is empty -->

## Verdict

`READY | READY WITH ACCEPTED RISKS | NOT READY | UNVERIFIED`

Target: `<worktree, head, base, staged/unstaged scope, snapshot fingerprint>`
Mode: `<mode>`; strict: `<yes/no>`; protocol: `<discovery/confirmation/conflict status>`
Budget: `<vectors, agents, passes>`
Reason: `<one evidence-based sentence>`

## Contract traceability

| Rule | Normative owner | Code evidence | Test/runtime evidence | Result |
|:--|:--|:--|:--|:--|
| `<id>` | `<path>` | `<path:line>` | `<command/result or gap>` | `compliant/partial/violated/unverified` |

## Named-risk closure

| Risk | Lifecycle | Cleanup | Concurrency | Detection | Runtime | Result |
|:--|:--|:--|:--|:--|:--|:--|
| `<risk-id>` | `<result>` | `<result>` | `<result>` | `<result>` | `<result>` | `<result>` |

## Coverage and gaps

- reviewed vectors: `<ids>`
- executed evidence: `<commands and exact results>`
- unavailable/stale evidence: `<what, why, verdict effect>`
- reverse ownership: `<missing-contract findings or none>`
- excluded as non-rollout maintainability: `<count/brief note>`

## Hand-offs

- `$contract-writer`: `<missing owner or contract conflict; separate approval required>`
- implementation/tests/operations: `<confirmed bounded work>`
```

Omit the named-risk table only when no material named risk exists. Do not omit traceability or
coverage. Keep duplicate subagent observations under one finding and state how many vectors
confirmed it. For repeat review, add a compact disposition table for prior findings:

| Prior finding | Current disposition | Evidence |
|:--|:--|:--|
| `<id>` | `confirmed/obsolete/duplicate/unverified` | `<current evidence>` |

Do not claim rollout completion, deployment, production behavior, or fixed defects. The auditor
reports evidence and hand-offs only.
