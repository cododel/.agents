# ADR quality spec — what makes an ADR good

This file is the **single source of truth** for what a good Architecture Decision
Record is. It has two consumers, by design:

- **`adr-writer` enforces it at write-time** — the template materialises it, the
  `from-chat` / `from-issue` workflows gate against it before producing a file.
- **`adr-auditor` measures against it at review-time** — it scores an existing
  corpus by the same criteria and proposes fixes.

One definition, two applications. Keeping it in one file is what stops "how we write
ADRs" and "how we judge ADRs" from drifting apart. When you change what a good ADR is,
change it here — not in the template or a workflow copy.

It is also re-readable on its own: when someone asks "is this even worth an ADR?" or
"why does this ADR feel hollow?", this file answers without loading a workflow.

## 1. What an ADR fundamentally is

An ADR is a **dated, immutable snapshot of a decision and the reasoning behind it, as
of the moment the choice was made.** It captures why the system looks the way it does:
what forces were in play, which position was taken, what was rejected and honestly why,
and what consequences were accepted.

It is emphatically **not** documentation of the current system. Current-state docs
drift as the code changes; an ADR must not. Its value is precisely that it is frozen —
a reader years later can reconstruct "what did they know, what did they weigh, why this
and not that" at that point in time.

### The immutability rule (the easiest thing to get wrong)

The most destructive mistake is treating an ADR as a living design doc and "updating"
it when the decision changes. That erases exactly the value the document exists to
preserve. The rule:

- **A decision changed → write a NEW ADR.** The old one becomes `Superseded`, and the
  two records carry reciprocal supersession links; the old ADR's *body* is never rewritten.
- **The only legitimate edits to an accepted ADR** are append-only: a `Refresh
  YYYY-MM-DD:` note (re-verified, still in use, minor drift noted), a status field
  change, or back-filling a relationship link. Never a rewrite of context, options,
  or rationale.
- **Editing `Accepted` instead of issuing a successor is a process smell** — and a
  thing the auditor checks against git history.

## 2. The irreducible core

Four things must be present, or it isn't an ADR. Everything else (Section 4) is
enrichment that earns its place by Risk Profile.

1. **Context and the forces that made the decision necessary.** Not just "the problem"
   — the *forces*: constraints, priorities, the trigger that surfaced this now rather
   than earlier. (Drivers/Forces can be a distinct section in fuller ADRs, but the core
   requirement is that the forces are present somewhere, not flattened into a topic
   sentence.)
2. **The decision itself, as a position taken.** A clear "we chose X" — not a survey,
   not a maybe. Enough detail that someone can act on it without re-running the
   discussion.
3. **The rejected alternatives, with honest, specific reasons.** At least two real
   options weighed, each with a concrete rejection reason tied to *this* context. Vague
   rejections ("less elegant", "more scalable") are the single most common ADR failure
   mode — they destroy the document's value. If there genuinely were no alternatives,
   that is a *named single-option ADR* with the reason no alternative existed — see
   Section 5.
4. **The consequences accepted.** Both sides. What we gain, *and* what debt, risk, or
   limitation we knowingly take on. Consequences that are all-upside are suspect —
   honest decisions have costs.

## 3. Per-ADR quality criteria

These are the checks `adr-writer` aims to satisfy and `adr-auditor` scores against.
Each is a yes/no a reader (or the auditor) can answer from the document plus the code.

- **One decision.** The ADR captures a single fork, not several bundled together.
  Multiple unrelated decisions → multiple ADRs, optionally `Related:`-linked.
- **Valid status.** The status is one of the lifecycle values and is *true*: no
  `Accepted` ADRs that are de-facto dead, no `Proposed` ADRs long since shipped.
- **Alternatives are real.** ≥2 genuine options with concrete, context-specific
  rejection reasons — or an explicit, justified single-option marker. Decorative
  options ("Option B: do it badly") don't count.
- **The decision still holds.** The code still reflects the ADR, or reality has moved
  on. Drift — ADR says "we use Clerk", code migrated to a homegrown auth — means the
  ADR is stale and needs a `Superseded` successor.
- **Reasons are concrete.** Rejection and selection reasons are tied to this system's
  forces, not general-purpose platitudes that would apply to any project.
- **Immutability respected.** The ADR wasn't rewritten in place when the decision
  evolved; changes went out as successors. (Auditor verifies via git history.)
- **Consequences are honest.** Negatives, risks, and trade-offs are stated, not just
  benefits.
- **Self-sufficient.** Understandable without the originating conversation. No "as we
  discussed above", no references to ephemeral context ("the option Vasily mentioned").
- **Decision invariants captured.** Where the recorded choice depends on a lasting
  constraint, that decision invariant is written down explicitly rather than left
  implicit in the prose. Decision invariants explain when the decision still holds;
  they do not replace the living project contract that owns current-state behavior.

## 4. Enrichment, tiered by Risk Profile

Beyond the core, these sections add rigour. They are **required for Tier-1 / Production**
decisions and **optional for MVP / Local** ones — the depth of the document should match
the cost of being wrong. A lightweight ADR for a reversible local choice should not be
padded out with all of them; a Tier-1 irreversible one should not omit them.

- **Decision Drivers / Forces** — the forces and priorities that shaped the choice,
  stated separately from the problem description. (Core requirement is that forces are
  present; this is the section that makes them explicit.)
- **Assumptions** — what is taken as given. When an assumption breaks, the ADR is up for
  review. In solo work these otherwise stay implicit in someone's head.
- **Decision Invariants / Constraints** — the lasting conditions under which the
  recorded decision remains valid. They preserve decision meaning, not current-state
  documentation; a living project contract remains the normative owner when one exists.
- **References** — sources, prior art, the research that produced the decision. An ADR is
  often born from an agent's research; losing the provenance is a real cost.
- **Validation** — how we'd know the decision was right, and what would falsify it.
  Forces the decision to be falsifiable rather than a matter of taste.
- **Confidence & Reversibility** — how sure we are and how reversible the choice is. Ties
  directly to when a future revisit is warranted.
- **Follow-ups** — the issues / ADRs this decision spawns. Closes the loop with
  file-based issues.

## 5. The significance check — when an ADR is NOT needed

Not every choice warrants an ADR. Writing one for a non-decision pollutes the record
with noise as surely as omitting a real one loses history. Run this check **before**
generating — in `from-chat` against the conversation, in `from-issue` against the issue
body (where `candidate-criteria.md` adds the issue-specific promote/skip specifics on
top of this).

**An ADR is NOT needed when the decision is:**

- **Reversible and cheap to undo.** Low cost of being wrong, easy rollback.
- **Without real alternatives** — mandated by the platform/framework, no genuine fork.
- **Local — an implementation detail** that doesn't cross a module / interface /
  contract boundary.
- **Only a description of implementation or current state.** Without a significant choice,
  alternatives, and rationale to preserve, it belongs in a living project contract,
  ordinary documentation, or code according to the project's declared ownership.
- **An order of execution** → that's a plan, not an ADR. Plans and ADRs are orthogonal:
  a plan sequences work, an ADR records a fork. Don't encode a plan as an ADR.
- **Already covered** by an existing ADR or a documented standard/convention — don't
  restate the standard.
- **Obvious** — the agent proposed it, it was accepted immediately, and there's no
  consequential fork to record.
- **Style / formatting** under the control of a linter or convention.

**Counter-signals — an ADR IS warranted even on something small** when the decision
involves any of:

- **Irreversibility / high cost of error.** This is a scope criterion in its own right,
  independent of how big the task looks. A small but irreversible fork deserves an ADR;
  a large but trivially reversible one may not.
- **Crossing a contract or interface boundary.**
- **Persistence or a DB schema** — anything that outlives a deploy and is costly to
  change later.
- **A new external dependency.**
- **Security / compliance.**
- **A precedent others will follow** — the first instance of a pattern that will be
  copied.

When the significance check says no, the right move is to *say so* and not write a file —
a fabricated ADR from thin context is worse than no ADR.

## 6. Corpus-level criteria

A file-based ADR set is only a *graph of decisions* if it hangs together. These are the
checks `adr-auditor` applies across the whole corpus (not per-file):

- **Supersession chains are intact.** Every `Superseded` ADR links to its successor and
  vice versa; no orphans pointing at nothing.
- **Coverage.** No silent decisions — major choices visible in the code (DB, auth,
  deploy, framework) each have a provenance ADR. The reverse audit: pick what the code
  obviously decided and check there's a record.
- **No duplicates / conflicts.** Not two un-reconciled ADRs covering the same area with
  contradictory positions and neither marked superseded.
- **Placement.** ADRs live where the routing convention says (global vs module vs infra).
- **Naming / IDs.** One consistent scheme, no collisions, sortable.
- **Density / cadence.** Neither too sparse (under-documentation — decisions get lost)
  nor flooded with trivia (noise on reversible choices). Both are smells.
- **Staleness distribution.** How many ADRs point at removed modules or a dead stack and
  are waiting to be marked `Deprecated`.
