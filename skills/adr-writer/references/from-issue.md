# From-Issue promotion workflow

Promote significant operator decisions preserved in closed repository Issues into proper ADRs. This
is an explicit audit/promotion workflow, not an automatic part of Issue closeout.

Read `candidate-criteria.md`, `adr-spec.md`, `path-resolution.md`, and the applicable local ADR/Issue
conventions before mutation.

## 1. Resolve exact scope and evidence context

Resolve one Issue root or explicit source list through shared repository discovery. Do not scan every
Issues directory when several project/module scopes are plausible. Determine:

- **same-session** — the current conversation explicitly contains the decision history; or
- **cold audit** — only the Issue and durable linked evidence may establish it.

Treat uncertain lineage as cold audit. Record the context once for the run.

## 2. Enumerate closed candidates

Follow the repository's status convention. Under the fallback, include files whose filename or body
marks them `Closed`; recognize legacy `Resolved` only when local history proves it. Filename/body
mismatches are `ambiguous` and remain untouched.

Read every candidate body in full. Search existing ADRs and contracts before classification so a new
record does not duplicate the current owner.

## 3. Classify and group by decision identity

Apply `candidate-criteria.md`:

- `promote` — complete significant operator-decision evidence;
- `skip` — no ADR-worthy decision history;
- `ambiguous` — one or more material facts require operator history;
- `merge` — several sources prove one independently supersedable decision.

Do not group by date/slug/file overlap alone. Current-state rules without decision history route to a
living contract, not an ADR.

## 4. Ask only for material unresolved decisions

An explicit `from-issue` request authorizes creation of every unambiguous promotion in the resolved
scope. Do not add a generic “approve the plan” ceremony.

Ask before writing only when one of these remains:

- missing operator choice, alternative/constraint, or rationale;
- competing ADR roots/owners/languages with no established convention;
- uncertain one-versus-several ADR granularity that changes future supersession;
- conflicting source records;
- the operator must choose `Proposed` versus no record.

Present a compact table containing only the affected candidates and exact question. Continue with an
unambiguous subset when it is independently useful and does not prejudice the unresolved choice.

## 5. Write the ADRs

For each accepted candidate/group:

1. resolve the path through local convention or the fallback;
2. use the compact ADR template and proportionate depth from `from-chat.md`/`adr-spec.md`;
3. preserve only evidenced context, alternatives/constraint, rationale, consequences, invariants, and
   revisit conditions;
4. add provenance:

```markdown
**Source issue:** `docs/issues/<file>.md`
```

or a `Source issues` list for a merged decision;

5. link the current living contract when one exists, without copying its normative rules;
6. use `Accepted` only for a completed operator choice; do not create core-rationale TODOs;
7. update an unambiguous source Issue with `Promoted to ADR: <path>` before any later cleanup so the
   relationship remains navigable while both files exist.

If generation reveals that the evidence is incomplete, reclassify the candidate as `ambiguous`; do
not fill gaps from implementation code.

## 6. Verify

For each created record:

- one decision and one coherent supersession unit;
- real alternative/constraint and specific rationale;
- no invented operator history;
- status, naming, links, and provenance match local convention;
- source Issue backlinks and existing ADR/contract relationships resolve;
- no live ADR contradiction is introduced;
- documentation checks and `git diff --check` pass when available.

## 7. Optional source-Issue cleanup

Promotion does **not** imply deletion. Keeping the closed Issue until the normal `$issue-writer` close
sweep preserves navigable provenance.

When the operator explicitly requests source cleanup in this workflow, apply the same recovery-aware
control as `$issue-writer` close after all ADRs and backlinks verify:

- exact regular file inside the confirmed Issue root;
- fingerprint and source→ADR backlink rechecked immediately before removal;
- tracked, clean, committed contents may be deleted as a reviewable local change;
- untracked, staged/modified, symlinked, path-ambiguous, or otherwise unrecoverable contents require
  an exact-path operator checkpoint;
- never use a glob, infer cleanup from promotion alone, or claim Git recovery without proof.

Update an unambiguous Issue index in the same change; otherwise report it.

## 8. Report

Return a compact summary:

- created ADR paths grouped by individual/merged decision;
- skipped and ambiguous counts, naming only material ambiguous candidates/questions;
- source Issues updated with backlinks;
- source Issues deleted or retained and why;
- unresolved contract/decision ownership, if any.

Do not echo ADR bodies or the full classification transcript.
