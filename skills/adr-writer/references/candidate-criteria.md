# Candidate criteria: which closed issues belong as ADRs?

This file defines the rules for deciding whether a closed issue should be **promoted**
to an ADR or **skipped** (and left for `issue-writer:close` to sweep, which runs its
own pre-extraction check before any `rm`). It's
read by `from-issue.md` Step P3 and is also useful as a standalone mental model when
the user asks "is this worth an ADR?"

It is the **issue-specific layer** on top of the general significance check in
`references/adr-spec.md` §5 ("when is an ADR needed at all?"). The spec defines the
general bar — reversible/local/mandated decisions don't warrant an ADR; irreversibility,
contract crossings, schema, new dependencies, security, and precedent do. This file
translates that bar into concrete promote/skip signals you can quote from an issue body,
and adds the anti-fabrication discipline specific to working from a file rather than a
live conversation. When the two ever seem to disagree, the spec is the authority.

## First principle: no fabrication

ADRs are records of decisions the user **actually made**. The primary way to produce
them is `from-chat`, where the rationale is articulated live and the model
transcribes. `from-issue` is an audit exception — and it inherits the same anti-
fabrication rule: never invent rejected options, never invent rationale, never
extrapolate a decision from topic shape. If the body doesn't say it (and in
same-chat runs, the chat didn't say it either), it doesn't go in the ADR.

Bias yourself toward `skip`. A missed ADR candidate costs the user one question;
a fabricated ADR pollutes the architectural record and is much harder to detect
later.

## Context quality affects the evidence bar

`from-issue.md` Step P0 classifies the run as **same-chat** (chain of reasoning
visible in the current conversation) or **cold audit** (no recent lineage). The
bar shifts:

- **Same-chat runs** — the issue body is the primary evidence, but if the chat
  *also* covered the rationale, you may cite it inline in the generated ADR
  (`Rationale sourced from chat, YYYY-MM-DD`). Slight relaxation of the
  "must-be-in-body" rule because the lineage is verifiable.
- **Cold audit runs** — the issue body alone must carry the load. No filling
  gaps from imagined context, no "I remember this was discussed somewhere." If
  the body is thin, the verdict is `skip` or `ambiguous`, not `promote with TODO`.

When unsure which variant applies, treat the run as **cold audit**.

## The bar: would a future engineer want to find this as an ADR?

ADRs answer "why does this system look the way it does?" If the closed issue's body
contains a non-trivial answer to that question, it's a candidate. If it just contains
"we fixed a bug, here's the patch", it's not.

## Promote — clear positive signals

Mark for promote only when the issue records a **significant choice plus its rationale**.
An invariant, boundary, policy, or current architecture statement by itself belongs in a
living project contract and is not an ADR signal.

- **Non-trivial trade-off with rejected options.** The issue body discusses two or
  more approaches and explains why one was chosen and others rejected. The rejection
  reasons are the load-bearing part.
- **Decision invariant tied to a significant choice.** The issue explains which
  architectural choice established a lasting condition, what alternative was rejected,
  and why. A bare rule such as "balances always go through `services/ledger.py`" is
  current-state contract material, not enough to promote.
- **Choice of data model, provider, framework, package manager, language, or
  runtime.** ("Use Bun, not npm/pnpm/yarn", "PostgreSQL JSONB for events, not a
  separate table", "Telegram Bot API directly, not aiogram-style framework").
- **Cross-cutting policy chosen for stated reasons.** Authentication, error handling,
  logging, i18n, deployment, security, or observability can be ADR-worthy when the issue
  preserves the actual fork and rationale. The current policy itself belongs in a
  living project contract.
- **Rationale for keeping a legacy approach.** "We considered migrating X to Y;
  decided to keep X for the next 12 months because Z." Future engineers will absolutely
  want to find this when they wonder "why is this still here?"
- **"By design" decisions.** Issues whose resolution is "this is intentional, here's
  why" rather than a code change.

## Skip — clear negative signals

Skip when the issue is one of:

- **Operational fix.** "Service was down, restarted it, added an alarm." Add the
  postmortem somewhere else; not ADR material.
- **Hygiene / cleanup.** Renamed file, removed dead code, normalized imports.
- **Doc drift.** Updated README to match code that already worked that way.
- **One-off tooling.** A throwaway script written to backfill data once.
- **Pure ops task.** Bumped a dependency, rotated a secret, added a CI check.

## Hard requirement: at least one explicit positive signal

A `promote` verdict requires a visible significant choice and rationale in the issue
body — quoted in the `reason` field. "Topic sounds architectural", a bare invariant,
or a current cross-cutting policy is not enough. When those statements have durable
current-state value, route them to `$contract-writer` instead of discarding them.

This is calibrated against the real failure mode: classifiers, especially under a
push-against-undertriggering description, tend to find architectural-shaped reasons
everywhere. The bar forces the signal to be in the document, not in the model's
interpretation of the document.

## Borderline rule: default to `skip with note`, not `promote with question`

When you cannot quote a clear positive signal but the topic seems architectural,
**default to `skip` with a brief note** in the verdict reason ("topic looks
architectural but body lacks explicit rejected options or invariant — not enough to
ground an ADR"). The user can override individual skips in the gate.

This is the opposite of "promote with a question" — and intentionally so. Most
closed issues are not ADRs. False-positive promotes generate noise the user has
to filter in the gate; false-negative skips generate one unanswered question. The
asymmetry favors caution.

The narrow exception: if the issue is genuinely between `promote` and `skip` and
neither feels right, return `ambiguous` with a short reason. The orchestrator
surfaces ambiguous items separately so the user can disambiguate without scanning
the whole skip list.

## Weak formatting alone is not a reason to skip

If the body is sparse but **a positive signal is still visibly present** (a
rejected option appears, an invariant is named, a framework is chosen with a
rationale phrase), promote it. The ADR generation step can read the body in full
plus related code and reconstruct the missing structure — sparse formatting doesn't
disqualify a real architectural decision.

The combination matters: positive signal + sparse formatting → promote with a
`TODO:` for the missing sections. Sparse formatting + no signal → skip.

## Anti-patterns: things that often look like ADR candidates but are not

These topics frequently *sound* architectural and trip up classifiers. Skip them
unless the issue body contains an explicit positive signal beyond "this is about
the topic":

- **Bug fix for an existing pattern.** "Fixed race in `service.py`" is not an ADR
  even if the service is important. The ADR would be "we use service-X-with-tx-wrapper
  for all writes" — which already exists or doesn't.
- **Tooling tweak.** Bumped dependency, added a CI step, configured pre-commit
  hook. A rule it enforces may belong in a living contract; an ADR still requires a
  significant choice, alternatives, and rationale.
- **Reverted change.** A revert with rationale "didn't work" is not an ADR. The
  ADR would be "we don't use approach X because Y," which needs the actual reasoning
  on Y written out.
- **Performance fix.** Specific optimization (added index, batched queries). A policy
  such as "all list endpoints paginate" belongs in a living contract unless the issue
  also records the significant choice and rationale that warrant an ADR.
- **Documentation fix.** Updated README to match reality. Not architectural.
- **One-off debugging session.** Even when long, even when fascinating. A resulting
  current-state invariant belongs in a living contract; only a significant decision
  with alternatives and rationale belongs in an ADR.

## Cluster signals (regrouping vs 1:1 promote)

Some architectural decisions are spread across **multiple closed issues** —
different angles or different consequences of the same posture. Individual
classification cannot see this (each file is read in isolation). Detection happens
in the **cluster pass** after individual classification — see `from-issue.md`
Step P3.5.

Cluster signals operate at the file-set level, not per-file. They include:

- **Slug overlap** — shared distinctive keyword in filename slugs
- **File overlap** — multiple issues reference the same source path
- **Scope/tag overlap** — same `Services affected:`, `Scope / Component:`, `FSD Slice:`, etc.
- **Date proximity** — opened within a single week (incident-burst pattern)
- **Theme repeat** — same phrase or rationale appears in multiple `## Background`
  sections

A group requires **at least 2 signals** across all proposed members. One signal is
noise. See `from-issue.md` for the full clustering procedure and gate UX.

## Specific borderline cases

- **Bug fix that revealed an architectural gap** → the gap becomes an ADR, not the
  fix. Skip the fix-issue itself; if the gap was never written up separately, mark
  the original issue as `ambiguous` so the user can decide whether to draft the
  gap-ADR by hand.
- **Issue with both a fix and a deferred decision** → the deferred decision is the
  ADR candidate. If the issue contains both, mark `ambiguous` and recommend in the
  reason "split into a deferred-decision ADR + skip the fix part."

## How to record the classification

For each candidate, the classifier output (in `from-issue.md` Step P3) records:

- `path` — path to the closed issue
- `verdict` — `promote` | `skip` | `merge` | `ambiguous`
- `reason` — one sentence quoting the specific positive/negative signal that matched
- `rejection_reasons_present` — boolean (helps the user see at a glance which
  promotions will need their input to fill in rejected options)

This lets the user scan the table in the gate and disagree on individual items
without re-reading every issue.
