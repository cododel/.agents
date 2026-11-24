# ADR fallback template

Use local ADR conventions when present. Otherwise save as:

```text
ADR-YYYYMMDD-<english-kebab-decision-slug>.md
```

Do not encode implementation percentage or task progress in the fallback filename.

---

# {Decision title}

**Status:** {Proposed | Accepted | Superseded | Deprecated}
**Decision date:** {evidenced YYYY-MM-DD | Unknown}
**Recorded:** YYYY-MM-DD

{What was decided and the concrete reason. One paragraph can be sufficient. Include relevant
constraints and trade-offs where they explain the choice.}

{When applicable, link the source Issue, current contract and superseding or superseded ADR.
For high-cost or irreversible decisions, include the assumptions, validation or revisit triggers,
and rollback or migration consequences.}
