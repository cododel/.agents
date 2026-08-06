# ADR markdown template

This is the fallback template used when the local `docs/adr/README.md` doesn't define
its own. When a local README exists, **its convention wins** — sample 2-3 existing
ADRs in the directory to confirm.

The template *materialises* the quality contract in `references/adr-spec.md` — read that
first if you haven't. The spec says what a good ADR is; this file is its concrete shape.

Two filename variants below; pick per local convention.

---

## Filename: standard variant

```
ADR-YYYYMMDD-<slug>.md
```

- `YYYYMMDD` = today's date (or original decision date if reconstructing one). No hyphens
  in the filename date — `YYYYMMDD` sorts correctly; the `Date:` header field uses the
  human-readable `YYYY-MM-DD` form. Keep both consistent (same calendar day).
- `<slug>` = English kebab-case, 3-7 words, names the *decision*
  (`bun-as-only-package-manager`, not `package-management`).
- **Collision rule.** `date + slug` is not guaranteed unique — two ADRs can land on the
  same day about nearby topics. If `ADR-YYYYMMDD-<slug>.md` already exists, disambiguate
  by making the slug more specific (preferred — `…-redis-cache` vs `…-redis-queue`), or
  fall back to a `-2` suffix (`ADR-YYYYMMDD-<slug>-2.md`) only when the slugs are
  genuinely about distinct decisions that resist renaming. Never silently overwrite.

## Filename: percent-status variant (used by some long-running projects)

```
[STATUS-PERCENT%]-ADR-YYYYMMDD-<slug>.md
```

Where `STATUS-PERCENT%` is one of:

- `[CLOSED-100%]` — fully implemented per spec, all material requirements verified
- `[IN-PROGRESS-X%]` — partially implemented; X reflects requirement coverage
- `[OPEN-X%]` — not implemented, postponed, or implemented via a materially different
  architecture; X reflects requirement coverage, not optimism

This `[…%]` prefix tracks **implementation completeness** and is orthogonal to the
decision-lifecycle `Status:` field below (which tracks whether the decision is still in
force). A decision can be `Status: Accepted` and `[OPEN-0%]` at once: decided, not yet
built. Use the prefix only when the local README explicitly calls for it.

When the implementation status changes, **rename the file** and update local links in
the same change.

---

## Header (required)

```markdown
# ADR: <Title — concise but descriptive, names the decision>

**Date:** YYYY-MM-DD
**Scope / Component:** `module/submodule`     <!-- the area the decision governs; `N/A` if repo-wide -->
**Risk/Strictness Profile:** MVP | Production | Staging | Tier-1 Prod | Local
**Status:** Proposed | Accepted | Deprecated | Superseded
**Implementation:** <link to relevant code file/dir, or `N/A — design only`>
```

`Scope / Component` names whatever the project uses to partition itself — an FSD slice
(`auth/session`), a service (`billing-api`), a Laravel/Django module (`payments`), a
package, or `N/A` for a repo-wide decision. FSD slices are just one example of the
format, not a requirement; don't impose FSD vocabulary on a project that isn't FSD.

### Status lifecycle

The `Status:` field tracks whether the decision is still in force. It is a lifecycle,
not a one-shot label — this is what lets an ADR correctly "die" without anyone rewriting
its body (see `adr-spec.md` §1, the immutability rule).

- **Proposed** — the decision is drafted but not yet committed to. Use when the fork is
  identified and reasoned but not finally chosen.
- **Accepted** — the decision is in force. New ADRs written from a chat that already
  settled the choice are usually born `Accepted`.
- **Deprecated** — the decision is being phased out but no single successor replaces it
  (e.g. the whole subsystem is going away). No `Superseded by` pointer required.
- **Superseded** — a newer ADR replaces this decision. Requires a `Superseded by:`
  pointer to that ADR. **Never edit a superseded ADR's body** to reflect the new
  decision; the successor carries the new reasoning.

### Relationship links (when applicable)

ADRs form a graph, not a pile of files. When a decision relates to another ADR, record
it in the header. Links are **bidirectional** — the same rule as ADR↔Spec: a one-way
link is a smell. If you write one side, write the other in the same change.

```markdown
**Supersedes:** [ADR-20260101-old-decision](./ADR-20260101-old-decision.md)
**Superseded by:** [ADR-20260601-new-decision](./ADR-20260601-new-decision.md)
**Related:** [ADR-20260315-adjacent-decision](./ADR-20260315-adjacent-decision.md)
```

- `Supersedes` / `Superseded by` are inverse fields — issuing a successor means adding
  `Superseded by` to the old ADR *and* `Supersedes` to the new one, plus flipping the old
  one's `Status:` to `Superseded`.
- `Related` is for decisions that touch but don't replace each other (e.g. two ADRs that
  together split one large area — see the granularity guard in `from-chat.md`).

When a companion implementation spec exists (e.g. under `docs/superpowers/specs/`,
`docs/specs/`, or a sibling design-doc directory) and references this ADR via an
`Aligned with:` line, **add a back-link** so the relationship is discoverable from
either direction. ADR↔Spec bidirectional linking is the convention; a one-way link
is a smell. Place it directly under `Status:`:

```markdown
**Implementation spec:** [<spec-title-or-date>](<relative-path-to-spec>)
```

If the ADR is being created **before** any spec exists, omit the field. When the
spec is later created (e.g. via `spec-writer`), that workflow adds both the
`Aligned with:` line in the spec and back-fills this field in the ADR — don't
write a dangling reference now.

For ADRs reconstructed from a closed issue (promote mode), add:

```markdown
**Source issue:** `docs/issues/[CLOSED]-2026-01-12-foo.md`
```

For ADRs revisited later, append a refresh note near the header (don't rewrite history):

```markdown
**Refresh 2026-04-30:** Re-verified — chosen option still in use; minor drift on API
naming (current `bot_ledger.credit()` vs ADR-spec `Ledger.add_credit()`).
```

For OPEN/IN-PROGRESS ADRs whose chosen design diverges from current implementation, add
a Note clarifying the gap:

```markdown
**Note:** Chosen option (X with lease model) NOT implemented. Current implementation uses
Y instead — see `services/y.py:42-180`. This ADR remains the design of record.
```

---

## Body sections — core (required, in this order)

These four sections are the irreducible core (`adr-spec.md` §2). Every ADR has them,
regardless of Risk Profile.

```markdown
## 1. Context and Problem Statement

[What's the problem? Why does it matter? What constraints and current-state facts
shape the decision? Include the trigger (incident, scaling pain, new requirement)
that surfaced this decision now rather than earlier. Name the forces in play — the
priorities and pressures that push toward one answer — not just the topic. For
Tier-1 / Production decisions, split these out into a dedicated Decision Drivers
section below.]

## 2. Options Considered

[Every option discussed — including rejected ones, passing mentions, and the null
option. Each gets the same shape:]

### Option A: <Name>

- **Description:** [How it works / what it is]
- **Pros:** [Specific benefits, not generic]
- **Cons & Reason for Rejection:** [Why it was rejected. Be highly specific. If the
  conversation produced an exact reasoning ("X won't work because of Y"), preserve
  that exact reasoning here. Generic rejection reasons are the most common ADR failure
  mode.]

### Option B: <Name>

[Same shape.]

### Option N: Do nothing / keep the status quo

[The null option, stated explicitly. "Leave it as-is" is almost always available and
is a real alternative — record why action beats inaction. Omit only when inaction is
genuinely impossible (e.g. a required external migration), and say so.]

[Continue for every option. If there genuinely was only one viable option — the choice
was mandated by the platform, an upstream dependency, or a hard constraint — do NOT
fabricate decorative alternatives. State it as a single-option decision and give the
concrete reason no alternative existed. See `from-chat.md` and `adr-spec.md` §5.]

## 3. Decision Outcome

**Chosen Option:** <Name from above>

[Detailed explanation of the implementation: architecture, data models, API contracts,
config values, sequence of operations, file paths — whatever was agreed upon. Enough
detail that someone can implement from this without re-running the discussion.]

[For percent-status ADRs, also include a brief reason this option was NOT rejected —
the symmetric counterpart to the rejection reasons in Section 2.]

## 4. Invariants / Constraints

[The long-term contract this decision imposes — what the implementation must uphold for
the decision to hold. State each as a checkable rule, not a vague aspiration: "all
balance mutations go through `services/ledger.py`", "no `os.getenv` outside config
loaders", "events are append-only, never updated in place". This is the most commonly
missing piece and the one with the longest reach — it's what a future reader (and the
auditor) checks the code against. If the decision genuinely imposes no lasting
constraint, write `None` and say why.]

## 5. Consequences & Mitigations

- **Positive:** [What we gain — be specific about which problems from Section 1 are
  addressed and how.]
- **Negative / Risks:** [Technical debt, known limitations, open questions, blast
  radius if the decision turns out wrong. An all-positive consequences list is a smell —
  honest decisions have costs.]
- **Mitigations:** [How the negatives are addressed given the Risk Profile in the
  header. "Staged rollout, monitor metric M, rollback by reverting commit." Be concrete.]
```

---

## Body sections — enrichment (tiered by Risk Profile)

These sections add rigour proportional to the cost of being wrong. **Required for
Tier-1 / Production** decisions; **optional for MVP / Local** ones. Don't pad a
reversible local choice with all of them, and don't omit them from an irreversible
Tier-1 one. (See `adr-spec.md` §4.)

```markdown
## Decision Drivers / Forces

[The forces and priorities that shaped the choice, stated separately from the problem.
"Must stay within the t3.large connection limit", "team has no Kafka experience",
"sub-100ms p99 is a product requirement". These are the criteria the options were
judged against.]

## Assumptions

[What's taken as given. When one of these breaks, this ADR is up for review. "Traffic
stays under 10k req/s", "we remain single-region", "Stripe remains our processor". In
solo work these otherwise live only in someone's head.]

## References

[Sources, prior art, the research that produced the decision — links, benchmarks, docs,
related ADRs. An ADR is often born from research; losing the provenance is a real cost.]

## Validation

[How we'd know the decision was right, and what would falsify it. "If error rate on the
new path exceeds the old by >5% over a week, the decision was wrong." Forces the choice
to be falsifiable rather than a matter of taste.]

## Confidence & Reversibility

[How sure we are (low / medium / high) and how reversible the choice is (one-way door vs
easily rolled back). Ties directly to when a future revisit is warranted — a low-confidence
one-way door deserves a Validation trigger and an early Refresh.]

## Follow-ups

[The issues / ADRs this decision spawns. "Needs a migration issue for the existing rows",
"a follow-up ADR on the caching layer this unblocks". Closes the loop with file-based
issues — capture these as real issue files via issue-writer, not inline TODOs.]
```

---

## Optional: Implementation Status section (for OPEN / IN-PROGRESS ADRs)

When the decision is documented but not fully implemented, append:

```markdown
## Implementation Status

- ✅ <Requirement that's actually implemented>
- ✅ <Another implemented requirement>
- ❌ <Requirement that's NOT implemented> (uses <alternative> instead, see `path/to/alt.py`)
- ❌ <Another gap>
```

This is what drives the percent-status in the filename: count `✅ / (✅ + ❌)`.

---

## Optional: Verification Requirements (for projects that gate on it)

When the local README requires verification before marking CLOSED, append a small
verification block:

```markdown
## Verification

- [ ] All Section 3 requirements present in code with file paths and line numbers
- [ ] Tests cover the new behavior
- [ ] Migrations / config / env-template updated
- [ ] Cross-cutting effects on neighboring services reviewed
```

---

## Anti-patterns to avoid

- **Vague rejection reasons.** "Option B was less elegant." → useless. Replace with the
  actual concern raised: "Option B requires per-tenant connection pools, which doubles
  RDS pool count and pushes us past the t3.large connection limit."
- **Missing or fabricated options.** Don't write an ADR with only one option *without
  saying why* — and don't invent decorative alternatives to hit a count. If only one was
  genuinely viable, mark it a single-option decision and give the concrete reason no
  alternative existed (`adr-spec.md` §2, §5).
- **Bundling decisions.** One ADR, one decision. If you're documenting several forks at
  once, split them and `Related:`-link instead.
- **Editing a live decision into a dead one.** When the decision changes, issue a
  successor with `Status: Superseded` links — never rewrite an accepted ADR's body
  (`adr-spec.md` §1).
- **Echoing the chat.** The ADR is for someone who wasn't in the conversation. Don't
  reference "as we discussed above" or "the option Vasily mentioned." Promote the
  reasoning, drop the conversational frame.
- **Inventing precision.** Don't fabricate file paths, function names, or config keys
  that weren't actually mentioned. Use `TODO:` placeholders for facts you don't have.
