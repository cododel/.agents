# {Short technical-debt or deferred-work title}

**Date:** YYYY-MM-DD
**Last reviewed:** YYYY-MM-DD
**Priority:** {Critical|High|Medium|Low}
**Severity:** {Critical|High|Medium|Low}
**Status:** Open
**Scope affected:** `{scope-or-service}`
**Probes:** `{stable path, symbol, command, event, or error signature}`
**Discovered via:** {Implementation | Debugging | Review | Operator deferral | …}

## Problem And Impact

{Concrete observed problem and why losing or ignoring it matters.}

## Evidence

- {Verified observation and source pointer}

## Root Cause / Current Hypothesis

{Proven root cause, or explicitly labeled hypothesis plus the next falsifying observation.}

## Why Deferred

{Why fixing now is outside the active affected radius or would materially widen risk/conflicts, or
the operator's explicit deferral reason.}

## Accepted Limitation

{Omit for ordinary deferred work. Decision source/owner, alternative and rationale, operating limits,
material edge cases and consequences, detection and reconsideration trigger. Acceptance is not repair.}

## Recommended Direction

{Evidence-backed direction. Keep unresolved product/architecture decisions explicit.}

## Resume Conditions And First Actions

1. {Concrete trigger for implementation or reconsidering an accepted limitation; no invented deadline}
2. {First investigation/implementation action}

## Completion Criteria

- [ ] {For planned repair: observable behavior or debt-removal outcome; for accepted limitations, do not promise repair—state what would justify revising the decision}
- [ ] {Required verification}

## Related

- {Linked TODO location, contract, ADR, Issue, commit, or `None`}
