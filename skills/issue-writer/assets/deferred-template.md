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

## Recommended Direction

{Evidence-backed direction. Keep unresolved product/architecture decisions explicit.}

## Resume Conditions And First Actions

1. {Concrete trigger or prerequisite for resuming}
2. {First investigation/implementation action}

## Completion Criteria

- [ ] {Observable behavior or debt-removal outcome}
- [ ] {Required verification}

## Related

- {Linked TODO location, contract, ADR, Issue, commit, or `None`}
