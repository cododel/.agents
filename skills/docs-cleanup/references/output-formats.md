# Output formats

Keep reports compact and separate audit findings from applied mutation.

## Audit or pre-apply summary

```markdown
## Documentation cleanup

Mode: audit | apply
Scope: <confirmed roots>

Counts:
  keep=N repair=N close=N stale=N merge=N supersede=N
  promote-to-adr=N delete-candidate=N ambiguous=N

Durable-value routing:
- <path> → contract / ADR candidate / runbook / Issue close

Recoverable deletes:
- <path> — tracked, clean, committed; no unique value/references

Gated or blocked:
- <path> — <untracked/modified/ADR history/ambiguous value/etc.>
```

In audit mode, stop there. In apply mode, apply recoverable actions and show the exact decision block
from `delete-gate.md` only when gated candidates remain.

## Post-apply report

```markdown
## Cleanup applied

Applied:
- <semantic repair/merge/supersession>

Deleted (recoverable):
- <path>

Held/gated:
- <path> — <reason and required decision>

Skipped after final recheck:
- <path> — <drift/evidence change>

Next durable workflow:
- <path> → `$contract-writer` / `$adr-writer` / `$issue-writer`
```

Do not list unchanged `keep` files individually in large audits unless the operator requests the full
classification. Do not repeat subagent reasoning or long excerpts.

## Incomplete audit

State the number classified, exact unreadable/failed subset, and which conclusions therefore remain
unverified. Never present a partial classification as a clean corpus result.
