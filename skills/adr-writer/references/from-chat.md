# From-chat workflow

Generate an ADR from the current conversation history. This is the original adr-writer
flow.

By the time you're reading this, you've already loaded `discovery.md` and
`path-resolution.md` from `SKILL.md`'s shared steps.

## Step F0 — Significance check (is this even an ADR?)

Before extracting anything, run the significance check from `references/adr-spec.md` §5
against the conversation. An ADR is **not** needed when the decision is reversible and
cheap, has no real alternatives (mandated by the platform), is a local implementation
detail that crosses no contract boundary, is really an execution plan, is already
covered by an existing ADR or standard, or is obvious with no consequential fork.
An implementation summary without a significant choice and alternatives also fails this gate.

Weigh the **counter-signals** too: irreversibility / high cost of error is a scope
criterion in its own right — a small but one-way-door decision warrants an ADR even
when the task looks minor. Likewise crossing a contract/interface, DB schema or
persistence, a new external dependency, security/compliance, or setting a precedent
others will follow.

If the check says no, **say so and stop** — don't write a file. A fabricated ADR from
thin context is worse than no ADR. State briefly why it doesn't warrant one (e.g.
"reversible local detail, no contract crossed — a code comment or issue fits better").

## Step F1 — Extract context from chat

Scan the **entire conversation** (not just recent turns) and extract:

- The **core problem or requirement** that triggered the discussion
- **Every option / alternative** mentioned — including rejected ones, half-considered
  ones, and passing mentions ("we could also do X" counts)
- The **exact reasons** each option was rejected — be specific, not generic. If
  someone said "X won't work because of Y", that exact reasoning belongs in the ADR.
- The **chosen solution** and its implementation details (architecture, data models,
  API contracts, config values, sequence of operations)
- Any **edge cases, caveats, or constraints** raised
- **Risk profile / environment context** (MVP, Tier-1 Prod, local dev, staging) if
  mentioned
- Any **agreed contracts**: data models, APIs, config keys, file paths

> Do NOT summarize aggressively. Preserve nuance. The whole point of an ADR is to
> capture *why* a decision was made — generic phrasing ("we considered alternatives and
> picked X") destroys exactly the value the document is supposed to provide.

If the chat doesn't actually cover the decision in enough depth — e.g. the user is
asking for an ADR on something that was only mentioned in passing — say so. An ADR
fabricated from thin context is worse than no ADR.

### Alternatives gate (do not fabricate options)

The rejected alternatives, with honest reasons, are part of the irreducible core
(`adr-spec.md` §2). But fabricating them is just as damaging as omitting them. After
extraction, check what the chat actually weighed:

- **Two or more real options discussed** → capture each with its specific rejection
  reason. Include the **null option** ("do nothing / keep status quo") explicitly unless
  inaction was genuinely impossible.
- **Only one option, because the choice was mandated** (platform, upstream dependency,
  hard constraint) → write it as a **single-option decision** and state the concrete
  reason no alternative existed. Do NOT invent decorative alternatives to hit a count.
- **Only one option, but alternatives plausibly exist and just weren't discussed** →
  this is thin. Don't paper over it: either surface the gap to the user and ask what
  else was considered, or leave a `TODO:` for the rejected options and flag it. A
  one-option ADR that hides unexplored alternatives is a shallow decision pretending to
  be a settled one.

### Granularity gate (one ADR = one decision)

If the chat settled **several distinct forks**, that's several ADRs, not one. Don't
bundle. Split them into separate ADRs and connect them with `Related:` links in the
header. Bundled ADRs can't be superseded independently and blur which decision a future
reader is looking at. The exception: sub-choices that only exist *because* of the main
decision and have no independent life belong in the one ADR.

## Step F2 — Pick the template variant and depth

The full markdown skeleton lives in `assets/adr-template.md`. Read it now if you
haven't already.

**Filename variant** — choose based on what discovery surfaced in the local
`docs/adr/README.md`:

- **Standard variant**: `ADR-YYYYMMDD-<slug>.md`. Use when no local convention is
  documented or the local convention matches this.
- **Percent-status variant**: filename uses `[STATUS-PERCENT%]-ADR-...`, header
  includes an `Implementation:` link, `Refresh YYYY-MM-DD:` notes are common. Use when
  the local README explicitly calls for it. The `[…%]` prefix tracks *implementation
  completeness*, separate from the decision `Status:` — a new ADR from chat is typically
  `Status: Accepted` and `[OPEN-0%]` (decided, not yet built).

When in doubt on the filename, match the most recent 1-2 ADRs in the directory.

**Decision status** — set the header `Status:` field from the lifecycle
(`Proposed | Accepted | Deprecated | Superseded`, see `adr-template.md`):

- A chat that *settled* the choice → born `Accepted`.
- A chat that reasoned a fork but left the final call open → `Proposed`.
- If this decision replaces an earlier ADR, set the earlier one to `Superseded` and wire
  the bidirectional `Supersedes` / `Superseded by` links in the same change. Never
  rewrite the old ADR's body — the new ADR carries the new reasoning (`adr-spec.md` §1).

**Depth by Risk Profile** — the profile you extracted in F1 drives *how much* of the
template to fill, not just a header value (`adr-spec.md` §4):

- **MVP / Local** → core only (Context, Options incl. null, Decision, Invariants,
  Consequences). Enrichment sections are optional; add one only if the chat actually
  produced it. Don't pad a reversible local choice.
- **Tier-1 Prod / Production** → core **plus** the enrichment sections (Decision Drivers,
  Assumptions, References, Validation, Confidence & Reversibility, Follow-ups). For an
  irreversible high-cost decision these aren't optional — a missing Validation or
  Confidence & Reversibility section on a one-way door is a real gap. Where the chat
  didn't cover one, leave a `TODO:` rather than dropping the section silently.

## Step F3 — Write the ADR

Fill the chosen template with the extracted context. A few specific guardrails:

- **Title**: concise but descriptive. Names the *decision*, not the *area*. Good:
  "Use Bun as the only package manager in the monorepo." Bad: "Package management".
- **Options Considered**: every option gets pros, cons, and a specific rejection
  reason. The reason is the load-bearing part — vague rejection reasons are the most
  common ADR failure mode.
- **Decision Outcome**: enough detail that someone can implement from it without
  re-running the discussion. If the chat agreed on a specific config value, file path,
  or schema, include it.
- **Invariants / Constraints**: where the decision establishes a long-term contract the
  implementation must uphold, write it down explicitly as a checkable rule — this is the
  most commonly missed piece and the longest-reaching one (`adr-spec.md` §3). If the
  decision imposes none, write `None` and say why, rather than dropping the section.
- **Consequences**: list both positive and negative. Mitigations for the negatives,
  given the risk profile. An all-upside list is a smell — surface the costs.
- **Project guardrails**: if the local `docs/adr/README.md` enumerates current
  invariants (DB conventions, deprecated services, forbidden APIs), call them out
  whenever the decision touches them.

## Step F3.5 — Check for an existing companion spec

ADRs and implementation specs are bidirectionally linked when both exist (the spec
carries `Aligned with: [ADR-link]`; the ADR carries `Implementation spec: [spec-link]`).
A one-way link is a smell — readers entering through the ADR won't discover the spec.

Before saving, do a single fast scan for spec directories the project may use:

```bash
find . -type d \( -name specs -o -name spec -o -path '*/superpowers/specs' \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -not -path '*/dist/*' -not -path '*/build/*'
```

If any directory turns up, list its files and check whether any spec is **already
about this same decision** (slug overlap, date proximity, or an explicit
`Aligned with:` line pointing at a placeholder/expected ADR name). If found:

- Add `**Implementation spec:** [<title>](<relative-path>)` to the ADR header.
- After saving the ADR, **verify the spec's `Aligned with:` line points back** to
  the path you just wrote. If it doesn't (e.g. the spec was drafted before the ADR
  path was finalized), fix the spec's line in the same change.

If no spec exists yet, omit the field. The spec-writer workflow (when later
invoked) is responsible for adding both directions of the link — don't write a
dangling reference here.

## Step F4 — Save and confirm

1. Create the file at the computed path. Create intermediate directories if needed.
2. Write the full ADR markdown content into the file.
3. **Do NOT echo the ADR content into the chat.** This is a standing user preference —
   the file is the artifact.
4. Respond ONLY with this short confirmation:

```
✅ ADR успешно сохранен: `[path/to/the/file.md]`
```

No additional commentary, no summary, no preview. Just the line.

If a follow-up question is unavoidable (e.g. discovery turned up two equally-valid
target paths and the user needs to pick), surface that *before* writing the file, not
after.
