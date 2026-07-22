# Audit criteria — measuring a corpus against the spec

The definition of a good ADR lives in `../../adr-writer/references/adr-spec.md`. **Read it
first.** This file does not restate it — it adds the **review-time specifics** that only
exist when you're auditing an existing corpus against the code, rather than writing one
ADR from a fresh decision.

Every finding ties back to a spec criterion. The auditor's job is to detect *violations*
of the spec and route each to a remediation action (`remediation.md`).

## Per-ADR findings (map to `adr-spec.md` §3)

For each ADR, check the §3 criteria. Most are readable from the document alone (one
decision, real alternatives, concrete reasons, honest consequences, self-sufficiency,
invariants captured, valid status value). Three need the code or git history and are the
review-time heart of this skill:

### Drift vs code — "does the decision still hold?"

The single highest-value per-ADR check. An ADR is a claim about how the system is built;
drift is when the code no longer matches the claim.

- Pull the ADR's concrete anchors: named files/dirs in `Implementation:`, libraries,
  providers, services, config keys, invariants ("all writes go through `ledger.py`").
- Grep the codebase for each. The decision **holds** if the anchors are present and used;
  it has **drifted** if they're gone or replaced.
- Classic drift: ADR says "we use Clerk for auth", the code migrated to a homegrown
  session layer — the ADR is stale and needs a `Superseded` successor, not a body edit.
- Distinguish **drift** (reality moved on → succession) from a **stale invariant** (the
  rule is violated in code but *shouldn't* be — that's a code bug or a coverage gap, a
  finding against the code, not the ADR). State which in the evidence.
- An `Implementation:` link pointing at a path that no longer exists is automatic drift.

### Immutability respected — git history check

The spec's §1 rule: a changed decision is a *new* ADR, never a rewrite of an accepted
one. Editing `Accepted` in place is a process smell.

- For ADRs whose status is `Accepted`/`Superseded`, scan `git log --follow -p <adr>` for
  substantive body edits *after* the initial commit — rewrites of Context, Options, or
  Decision (not append-only Refresh notes, status flips, or link back-fills).
- A post-acceptance rewrite of the reasoning is a finding: the history that should have
  become a successor ADR was overwritten instead. There's no way to recover the lost
  snapshot — flag it so the pattern stops, even though the specific loss is permanent.
- Append-only changes (a `Refresh YYYY-MM-DD:` note, flipping `Status:`, adding a
  `Superseded by:` link) are **legitimate** — not findings.

### Status truth

Not just "is the status a valid lifecycle value" but "is it *true*":

- `Accepted` ADRs whose decision has drifted (per above) are **de-facto dead** → should be
  `Superseded` (a successor exists or should) or `Deprecated` (the whole area is gone).
- `Proposed` ADRs whose decision is plainly shipped in the code → should be `Accepted`.
- `Superseded` with no `Superseded by:` link, or pointing at a missing ADR → broken chain
  (also a §6 corpus finding).

## Corpus findings (map to `adr-spec.md` §6)

These are cross-file and cannot be seen one ADR at a time.

### Reverse-coverage audit — the highest-value, least-obvious check

Per-ADR auditing only sees decisions that *were* written down. The reverse audit asks:
**what did the code obviously decide that has no ADR?** Walk the major architectural
surfaces and check each has a provenance ADR:

- **Persistence** — the database, schema strategy, ORM/query layer, migration tooling.
- **Auth** — how identity and sessions work.
- **Deploy / runtime** — containerization, hosting, CI/CD, the runtime itself.
- **Framework & core libraries** — the web framework, the package manager, the language.
- **Cross-cutting policies** — error handling, logging, i18n, observability, security.

For each surface, find the deciding evidence in code (a `Dockerfile`, a `package.json`
choice, an auth middleware, a schema dir) and check whether any ADR records *why*. A
major decision visible in code with **no ADR** is a silent decision — a coverage gap. A
project with substantial architecture and near-zero ADRs is itself the headline finding.

(Don't flood: only surfaces that represent a real, non-obvious fork count. "Uses JSON for
config" is not a missing ADR; "JSONB event store instead of a separate events table" is.)

### Supersession chain integrity

- Every `Superseded` ADR has a `Superseded by:` pointing at a real ADR, and that
  successor carries the inverse `Supersedes:` back-link. Either side missing → broken
  chain.
- No `Superseded by:`/`Supersedes:` pointing at a path that doesn't exist (orphan link).
- No two live (`Accepted`) ADRs covering the same area with contradictory positions and
  neither marked superseded — that's an unreconciled conflict.

### Placement, naming, density

- **Placement** — ADRs live where the routing convention (global vs module vs infra) puts
  them. A module-scoped decision in the global dir, or vice versa, is a finding.
- **Naming / IDs** — one consistent scheme, sortable, no filename collisions
  (`date + slug` clashes), filename date and header `Date:` agree.
- **Density / cadence** — flag both extremes: a mature codebase with a handful of ADRs
  (under-documentation, decisions lost) and a pile of ADRs on trivially reversible choices
  (noise). Report the signal; the operator judges.
- **Staleness distribution** — how many ADRs point at removed modules or a dead stack and
  are candidates for `Deprecated`.

## Recording findings

The classifier (inline or subagent) records, per ADR:

- `path`
- `findings` — list of `{criterion, severity, evidence}` where `criterion` is a spec
  reference (e.g. `drift`, `immutability`, `status-untrue`, `hollow-alternatives`,
  `missing-invariants`, `not-self-sufficient`, `bundled-decisions`), `severity` is
  `high | medium | low`, and `evidence` quotes the specific signal (a code path that
  contradicts the ADR, a git commit that rewrote it, a vague rejection line).
- `recommended_action` — the remediation label from `remediation.md`.

Corpus findings are recorded separately (chain breaks, coverage gaps, conflicts), since
they span files and have no single owning ADR.

Anti-fabrication, same as the writer: a finding must quote the actual signal — a real code
path that contradicts the ADR, an actual git rewrite, an actually-vague rejection reason.
"Feels stale" is not a finding. When genuinely unsure, mark it `ambiguous` and surface it
for the operator rather than asserting drift you can't show.
