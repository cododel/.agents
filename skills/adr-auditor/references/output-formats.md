# ADR audit output formats

## Diagnosis

```markdown
## ADR corpus diagnosis

Scope: <confirmed roots>
Coverage: <N audited / M total; unavailable checks>

### Findings
| ADR / corpus | Criterion | Evidence | Confidence | Recommended action |
|---|---|---|---|---|
| ... | drift | ... | high | write-successor |

### Current-state contract leaks
- <ADR>: <normative behavior with no current owner> → establish-current-contract

### Decision-record candidates requiring operator history
- <surface>: code proves <current choice>, but no evidence proves who chose it or why

### Ambiguous
- <ADR>: drift vs violated invariant — <missing falsifying evidence>
```

Lead with confirmed high-impact findings, then ambiguity and candidates. Do not report a framework,
DB, auth system, or deploy target as a missing ADR solely because it exists.

## Remediation gate

```markdown
## ADR remediation plan

Append-only metadata:
- <exact action/path>

Filesystem normalization:
- <exact move/rename and inbound links>

Reasoning-dependent hand-offs:
- <successor/split/candidate requiring operator rationale>

Reply with the exact actions to apply, adjust, or cancel.
```

## Post-apply

Report applied actions, skipped/drifted targets, and hand-offs. Do not echo ADR bodies. State any
checks unavailable because Git history or implementation evidence was missing.
