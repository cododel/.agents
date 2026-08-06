# Output formats

Three primary report shapes: audit summary (before approval), gate (delete subset),
post-apply report. Each has a fixed shape so the operator can scan quickly.

## Audit summary

After classification finishes (whether inline or via classifier subagent), present:

```markdown
## Audit summary

Scope: <confirmed docs directories>
Total candidates: N

Counts by verdict:
  keep:            N
  repair:          N
  close:           N
  stale:           N
  merge:           N
  supersede:       N
  promote-to-adr:  N
  delete:          N
  ambiguous:       N

### Hand-off recommendations
- `adr-writer:from-issue` could promote these <M> issues to ADRs (the flow deletes
  the source issues after the ADR is saved, with explicit operator confirmation):
    - <path>
    - <path>
- `issue-writer:close` could sweep these <N> `[CLOSED]` issue files (it runs its
  own pre-extraction check before any `rm`, so anything ADR-worthy gets caught a
  second time):
    - <path>
    - <path>

### Repair candidates (need attention but not destructive)
| Path | Issue | Suggested fix |
|------|-------|---------------|
| <path> | filename/body status mismatch | rename to [CLOSED] or update body |

### Stale open Issues
| Path | Last reviewed | Evidence-based stale note |
|------|---------------|---------------------------|
| <path> | YYYY-MM-DD | <premise that no longer matches current evidence> |

### Supersede candidates (ADRs replaced by newer decisions)
| Path | Superseded by | Action |
|------|---------------|--------|
| <path> | <newer-adr-path> | add header `**Superseded by:** ...` and keep file |

### Ambiguous (need your review)
| Path | Verdict considered | Why ambiguous |
|------|--------------------|---------------|
| <path> | delete vs repair | unique commands in body but no incoming references — move into a runbook first? |

### Delete candidates → see Delete Review Gate below
```

Then follow with the gate (per `delete-gate.md`) only if delete candidates exist.

## Compact mode for small audits (≤ 10 files)

When the candidate set is small, the full table format is noisy. Use:

```markdown
Audit of <scope> (N files):

  keep:      <path>, <path>, <path>
  repair:    <path> — filename/body mismatch
  promote:   <path>  → fits `adr-writer:from-issue` (architectural decision)
  stale:     <path> — keep Open; update Last reviewed and add Stale note
  delete:    <path>, <path>  → closed issues; consider `issue-writer:close` instead
                              of this skill's gate (it re-checks for extractable value)

  (No ambiguous items.)
```

## Post-apply report

After deletions and other applied actions:

```markdown
## Cleanup applied

Deleted (N):
  - <path>
  - <path>

Non-delete actions applied:
  - <path>: added "Superseded by: <newer-adr>" header
  - <path>: renamed [OPEN] → [CLOSED] after verified completion
  - <path>: updated Last reviewed and added an evidence-based Stale note; kept Open

Approved paths skipped at apply time (final re-check changed the picture):
  - <path>: re-read showed updated body with new evidence; left in place

Recommended next steps:
  - Run `adr-writer:from-issue` on `docs/issues/` to promote <M> architectural items
    (it deletes the source issues itself, with operator confirmation)
  - Run `issue-writer:close` on `docs/issues/` to sweep <N> remaining `[CLOSED]`
    files (pre-extraction check + delete)
  - <Other manual follow-ups>
```

## Failure mode reports

If classification fails partway (subagent errored, files unreadable):

```markdown
## Audit incomplete

Classified successfully: N of M files.

Failed:
  - <path>: <error from subagent>

Recommendation: re-run on the failed subset, or surface specific files for manual
review.
```

If pre-delete-checker turns up surprises (unexpected references, unique content the
classifier missed):

```markdown
## Pre-delete checker downgrades

The following were marked `delete` by classification but downgraded by safety checks:

| Path | Original | Downgraded to | Reason |
|------|----------|---------------|--------|
| <path> | delete | repair | referenced from `docs/runbooks/deploy.md` line 42 |
| <path> | delete | repair | contains unique commands not preserved elsewhere — move into a runbook before delete |

These are NOT in the delete gate below — they require operator decision on the
suggested alternative.
```

Always show downgrades **before** the gate, so the operator sees what was filtered
out and can override if they disagree.
