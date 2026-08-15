# Output formats

Three report shapes: diagnosis (after the audit), remediation gate (before applying),
post-apply report. Fixed shapes so the operator scans fast.

## Diagnosis report

After the per-ADR and corpus audits finish (inline or via subagent):

```markdown
## ADR corpus diagnosis

Scope: <confirmed ADR directories>
Total ADRs: N   (Accepted: a · Proposed: p · Superseded: s · Deprecated: d · no/invalid status: x)

### Health summary
  drifted from code:        N
  status untrue:            N
  hollow alternatives:      N
  missing decision invariants: N
  ADR as current contract:     N
  bundled decisions:        N
  immutability violations:  N   (rewritten after acceptance — history already lost)
  clean:                    N

### Per-ADR findings (highest severity first)
| ADR | Finding | Evidence | Action |
|-----|---------|----------|--------|
| ADR-20251101-auth-clerk | drift (high) | `Implementation:` → `lib/clerk.ts` is gone; auth now in `lib/session/*` | write-successor + mark-superseded |
| ADR-20250903-db-choice | hollow (med) | only one option; no rejected alternatives, no reason none existed | flag-hollow |
| ADR-20260112-cache | status-untrue (med) | `Proposed` but shipped in `cache/redis.ts` | flip-status → Accepted |

### Corpus findings
- **Broken chains (N):**
    - ADR-…-old: `Status: Superseded` but no `Superseded by:` link
    - ADR-…-new: supersedes ADR-…-old in prose but no `Supersedes:` field
- **Coverage gaps (N) — major decisions in code with no ADR:**
    - Persistence: PostgreSQL + JSONB event store (`db/events.sql`) — no ADR
    - Deploy: Fly.io with multi-region config (`fly.toml`) — no ADR
- **Conflicts (N):** ADR-…-a and ADR-…-b both `Accepted`, contradict on <area>, neither superseded
- **Naming/placement (N):** <path> — module decision in the global dir; <path> — filename date ≠ header Date
- **Missing current contracts (N):** <ADR> is the only normative owner for <behavior>
  (→ `contract-writer`, separate creation approval)

### Ambiguous (need your review)
| ADR | Unclear between | Why |
|-----|-----------------|-----|
| ADR-… | drift vs stale-invariant | code violates the invariant — ADR wrong, or code bug? |
```

## Compact mode for small corpora (≤ 10 ADRs)

```markdown
ADR audit of <scope> (N ADRs):

  clean:       ADR-a, ADR-b
  drift:       ADR-c  → successor + supersede (auth moved Clerk → homegrown)
  hollow:      ADR-d  → flag for back-fill (no real alternatives)
  status:      ADR-e  → flip Proposed→Accepted (shipped)
  chain break: ADR-f  → add Superseded-by link to ADR-g

  Coverage gaps: DB choice, deploy target — no ADR (→ adr-writer)
  (No ambiguous items.)
```

## Remediation gate

After the diagnosis, present the plan grouped by safety (per `remediation.md`). **Wait for
explicit approval.** Nothing mutates before it.

```markdown
## Remediation plan — approve before I touch anything

### Tranche 1 — append-only (low risk, bulk-approvable)
  flip-status:     ADR-e  Proposed → Accepted
  mark-superseded: ADR-c  → Superseded, link to (successor, Tranche 3)
  add-link:        ADR-f ↔ ADR-g  bidirectional Superseded-by / Supersedes

### Tranche 2 — mutating (review the moves/renames)
  relocate:  ADR-h  docs/adr/  → docs/adr/billing/  (module-scoped)
  normalize: ADR-i  rename to fix filename/header date mismatch

### Tranche 3 — hand-offs (these become your next writer runs)
  write-successor: ADR-c — new auth ADR (homegrown session); I wire links after
  split:           ADR-j bundles {caching, rate-limiting} → two ADRs
  fill-coverage:   DB choice, deploy target → from-chat if you can supply the why
  establish-current-contract: ADR-k owns current auth behavior alone → contract-writer after approval

Reply: apply tranche 1 | apply 1+2 | apply except <ADR> | adjust <…> | cancel
```

ADR deletion is **not** offered here — the auditor supersedes/deprecates, it doesn't
delete history. A genuine junk file goes through an explicit per-path delete confirmation,
never a default.

## Post-apply report

```markdown
## Audit remediation applied

Append-only fixes (N):
  - ADR-e: Status Proposed → Accepted
  - ADR-c: Status → Superseded, added `Superseded by: ADR-…-new`
  - ADR-f ↔ ADR-g: wired bidirectional supersession links

Mutating fixes (N):
  - ADR-h: moved to docs/adr/billing/, updated 2 inbound links

Recommended next steps (hand-offs you trigger):
  - `adr-writer` (from-chat): author the homegrown-auth successor, then I/you supersede ADR-c
  - `adr-writer`: split ADR-j into caching + rate-limiting ADRs
  - `adr-writer`: backfill coverage ADRs for the DB and deploy decisions
  - `contract-writer`: establish the missing current auth contract after separate approval
  - Back-fill ADR-d's missing alternatives/decision invariants (needs real rationale — can't be invented)

Skipped (with reason):
  - ADR-k: marked ambiguous (drift vs code-bug) — left for your call
```

## Failure-mode report

If the audit can't complete (subagent errored, files unreadable, no git history for the
immutability check):

```markdown
## Audit incomplete

Audited successfully: N of M ADRs.
Failed / partial:
  - <path>: <reason> (e.g. "not in git — immutability check skipped, other checks ran")

Recommendation: re-run on the failed subset, or surface specific ADRs for manual review.
```

Always show what was *not* checked — a silent partial audit reads as a clean bill of
health when it isn't one.
