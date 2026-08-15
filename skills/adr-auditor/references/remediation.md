# Remediation — turning findings into fixes

Each finding from `audit-criteria.md` routes to one remediation action. This file defines
the action set, which are safe to apply directly, and which must hand off or pass the
gate. The governing rule is `adr-spec.md` §1: **ADRs are append-only memory.** A drifted
or wrong decision is fixed by *succession*, never by rewriting an accepted ADR's body.

## Action set

| Action | Trigger (finding) | What it does | Safety |
|--------|-------------------|--------------|--------|
| `mark-superseded` | Drift: reality moved on; a successor exists or is being written | Flip old ADR `Status: Superseded`, add bidirectional `Superseded by:` / `Supersedes:` links | Append-only — gated, applied directly |
| `mark-deprecated` | The decision's whole area is gone; no single successor | Flip `Status: Deprecated`, add a one-line note pointing at what replaced the area (or "area removed") | Append-only — gated, applied directly |
| `write-successor` | Drift where the new decision already lives implicitly in code, or a decision changed | Hand off to `adr-writer` to author the new ADR; then `mark-superseded` the old one and wire links | Hand-off — never authored by the auditor silently |
| `add-link` | Broken/one-way supersession chain, missing `Related:` | Add the missing inverse link (and fix dangling targets) | Append-only — gated, applied directly |
| `flip-status` | Status untrue but decision unchanged (`Proposed`→`Accepted` for shipped work) | Update the `Status:` field only | Append-only — gated, applied directly |
| `flag-hollow` | Hollow/decorative alternatives, missing invariants, vague reasons, not self-sufficient | Record for back-fill or down-grade; do **not** invent the missing content | Recommendation — needs operator/author input |
| `split` | One ADR bundles several decisions | Hand off to `adr-writer` to author the split ADRs (+ `Related:` links); retire the bundle via succession | Hand-off — operator decides the split |
| `relocate` | Placement violates the routing convention | Move the file to the correct dir; update inbound links in the same change | Mutating — gated |
| `fill-coverage` | Reverse-coverage gap: major decision in code, no ADR | Hand off to `adr-writer` (from-chat if the user can supply rationale, from-issue if buried in a resolved issue) | Hand-off — never fabricated |
| `establish-current-contract` | ADR is the only normative owner of durable current behavior or architecture | Report `missing` and hand off to `contract-writer`; create only after separate operator approval, then backfill provenance links | Hand-off — never infer approval |
| `normalize` | Naming/ID collision, filename↔header date mismatch | Rename to the convention, resolve the collision (more specific slug, else `-2`), fix the date field | Mutating — gated |

## What the auditor may apply directly vs hand off

**Append-only, apply on approval** — these don't touch the frozen reasoning, so they're
the auditor's to make once the operator approves at the gate:

- `flip-status`, `mark-superseded`, `mark-deprecated`, `add-link`, refresh notes.

**Mutating, apply on approval** — change the filesystem but not an ADR's reasoning:

- `relocate`, `normalize`. Update inbound links in the same change so nothing dangles.

**Hand off, never do silently** — these require *new reasoning*, which only `adr-writer`
(with the user or a source issue) can legitimately produce:

- `write-successor`, `split`, `fill-coverage`, `establish-current-contract`. The auditor identifies the need and
  prepares the hand-off (which ADR, what the successor must capture, where it goes); it
  does **not** fabricate the new decision's rationale or create a missing contract
  without separate approval. Anti-fabrication is the same hard rule as the writer's.

`flag-hollow` is a recommendation only: a hollow ADR can't be repaired by invention. The
auditor surfaces it ("Option B is decorative — no real rejection reason; Invariants
section missing") for the author to back-fill from real knowledge, or to down-grade.

## The immutability guardrail (do not violate)

When a decision has changed, it is tempting to just edit the ADR. **Don't.** That is the
exact failure the spec exists to prevent — it destroys the dated snapshot. The correct
sequence is always:

1. `write-successor` (hand off to `adr-writer`) → new ADR with the new reasoning.
2. `mark-superseded` on the old ADR + bidirectional links.

The old ADR's Context / Options / Decision / Consequences are never touched. The only
marks the auditor adds to a superseded ADR are the status flip and the `Superseded by:`
link — both append-only.

## Ordering for the operator

When presenting the remediation plan, group by safety so the operator can approve in
tranches:

1. **Append-only fixes** (status flips, link repairs) — low-risk, often bulk-approvable.
2. **Mutating fixes** (relocate, normalize) — review the moves/renames.
3. **Hand-offs** (successors, splits, coverage fills, missing current contracts) — these
   become `adr-writer` or `contract-writer` runs the operator triggers next; list them as
   next steps, don't block the append-only fixes on them.

Deletion is deliberately **not** in the action set. An ADR is history; the auditor
deprecates or supersedes, it does not delete. If the operator genuinely wants an ADR file
removed (e.g. a junk/test file that was never a real ADR), that goes through the same
explicit per-path delete gate `docs-cleanup` uses — never a default action here.
