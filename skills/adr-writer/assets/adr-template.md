# ADR fallback template

Use local ADR conventions when present. Otherwise save as:

```text
ADR-YYYYMMDD-<english-kebab-decision-slug>.md
```

Do not encode implementation percentage or task progress in the fallback filename.

---

# {Decision title}

**Status:** {Proposed | Accepted | Superseded | Deprecated}
**Date:** YYYY-MM-DD
**Scope / Component:** {system, service, module, or boundary}
**Supersedes:** {link or `None`}
**Superseded by:** {link or `None`}
**Current contract:** {link or `None`}
**Related:** {links or `None`}
**Source issue:** {link or `None`}

## Context And Decision Drivers

{The concrete problem, constraints, and forces that made a choice necessary.}

## Options Considered

### {Option A}

- **Benefits:** {context-specific benefits}
- **Costs / risks:** {context-specific costs}
- **Why selected or rejected:** {actual operator rationale}

### {Option B}

- **Benefits:** {context-specific benefits}
- **Costs / risks:** {context-specific costs}
- **Why selected or rejected:** {actual operator rationale}

{Add status quo or a single-option constraint only when it was genuinely part of the decision.}

## Decision

{The selected path and enough stable detail to understand the decision without the originating chat.
Link to the current contract for normative behavior rather than copying it.}

## Assumptions And Decision Invariants

- {Condition under which this decision remains valid, or `None` with reason}

## Consequences

### Positive

- {Benefit}

### Negative / Trade-offs

- {Cost, limitation, or new risk}

## Validation And Revisit Triggers

- {Evidence that would support/falsify the decision or trigger reconsideration}

## References And Follow-ups

- {Research, Issue, migration, contract, or related ADR link; omit section if empty}
