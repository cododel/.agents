# From-Issue promotion workflow

Preserve significant agreed decisions from closed repository Issues. An in-scope Issue may supply
evidence during authorized implementation or documentation work, including an authorized extraction/removal
workflow. Closure alone neither proves a significant decision nor requires an ADR. A retrospective
promotion sweep requires an explicit request; read-only review never authorizes promotion.

Read `candidate-criteria.md`, `adr-spec.md`, `path-resolution.md`, and the applicable local ADR/Issue
conventions before mutation.

## 1. Resolve exact scope and evidence context

Resolve one Issue root or explicit source list through shared repository discovery. Do not scan every
Issues directory when several project/module scopes are plausible. Determine:

- **same-session** — the current conversation explicitly contains the decision history; or
- **cold audit** — only the Issue and durable linked evidence may establish it.

Treat uncertain lineage as cold audit. Record the context once for the run.

## 2. Enumerate closed candidates

Follow `../../issue-writer/references/conventions.md` for the repository's status convention.
Under the stable-name fallback, require the exact body status `Closed`; filenames carry no status.
Require matching filename/body statuses only under an established status-prefixed convention.
Missing or conflicting required statuses are `ambiguous` and remain untouched; loose prefixes
such as `Closed pending verification` or `[CLOSEDNESS]` do not qualify.

Read every candidate body in full. Search existing ADRs and contracts before classification so a new
record does not duplicate the current owner. Reconcile the current chat and Issue evidence by
decision identity as well; one decision receives one ADR regardless of source count.

## 3. Classify and group by decision identity

Apply `candidate-criteria.md`:

- `promote` — complete significant operator-decision evidence;
- `skip` — no ADR-worthy decision history;
- `ambiguous` — one or more material facts require operator history;
- `merge` — several sources prove one independently supersedable decision.

Do not group by date/slug/file overlap alone. Current-state rules without decision history route to a
living contract, not an ADR.

## 4. Ask only for material unresolved decisions

Apply the entrypoint's recording authority within the resolved scope. Do not expand a specific
Issue into an unrequested sweep or add a generic “approve the plan” ceremony.

For optional recording, skip ambiguous candidates and continue independent work; retain sources
whose unique value is unresolved. For requested promotion, ask before writing when one of these remains:

- missing operator choice, alternative/constraint, or rationale;
- competing ADR roots/owners/languages with no established convention;
- uncertain one-versus-several ADR granularity that changes future supersession;
- conflicting source records;
- the operator must choose `Proposed` versus no record.

Present a compact table containing only the affected candidates and exact question. Continue with an
unambiguous subset when it is independently useful and does not prejudice the unresolved choice.

## 5. Choose source disposition before edits

Default to **retained**. Promotion alone never authorizes source deletion. Only explicit source
cleanup covering the exact resolved scope can select **deletion-bound** sources.

For each proposed deletion-bound source, use the value/reference and recovery checks in
[document deletion](../../_shared/document-deletion.md) before adding any backlink. This workflow
additionally requires a reachable committed SHA and repository-relative path retrieving the exact
source bytes for durable ADR provenance. Record the original fingerprint and keep working-tree and
index contents clean. If provenance/recovery is unproven, retain/gate the source; recovery approval
cannot replace durable source provenance.

Plan where each unique non-decision item will survive. If extraction cannot complete within the
authorized scope, retain the source. Choose disposition before edits; the writing step below owns
retained-source backlinks and deletion-bound provenance.

## 6. Write the ADRs

For each accepted candidate/group:

1. resolve the path through local convention or the fallback;
2. match the local format; load `../assets/adr-template.md` only for the fallback, using the
   proportionate depth defined by `adr-spec.md` without loading the separate chat workflow;
3. preserve only evidenced context, alternatives/constraint, rationale, consequences, invariants, and
   revisit conditions;
4. add provenance according to the selected disposition. For a retained source:

```markdown
**Source issue:** `docs/issues/<file>.md`
```

or a `Source issues` list for a merged decision;

   for a deletion-bound source, use durable Git provenance rather than a dangling working-tree link:

```markdown
**Source issue at commit:** `<reachable-committed-sha>:docs/issues/<file>.md`
```

   Verify that `git show <sha>:<repo-relative-path>` retrieves the exact source bytes. Keep the
   actual decision date separate from the record date; unknown decision dates remain explicit;

5. link the current living contract when one exists, without copying its normative rules;
6. use `Accepted` only for a completed operator choice; do not create core-rationale TODOs;
7. add `Promoted to ADR: <path>` only to retained source Issues. Keep deletion-bound sources untouched
   so backlink edits cannot invalidate their clean-source gate. The ADR and planned index repairs
   carry their durable provenance.

If generation reveals that the evidence is incomplete, reclassify the candidate as `ambiguous`; do
not fill gaps from implementation code.

## 7. Verify

For each created record:

- one decision and one coherent supersession unit;
- real alternative/constraint and specific rationale;
- no invented operator history;
- status, naming, links, and provenance match local convention;
- retained source Issue backlinks and existing ADR/contract relationships resolve;
- deletion-bound source provenance resolves to the exact bytes in the recorded reachable commit;
- no live ADR contradiction is introduced;
- documentation checks and `git diff --check` pass when available.

## 8. Optional source-Issue cleanup

Use the disposition selected before edits. Keeping a source preserves navigable provenance; a later
cleanup must re-establish its current recovery state, since backlink edits made it modified.

Only after explicitly requested source cleanup and verification of the ADRs, retained-source backlinks
and extraction targets, apply [document deletion](../../_shared/document-deletion.md). Its final
recheck must also verify this workflow's original source fingerprint and exact committed provenance.
A retained-source backlink changes recovery state; never treat the previous clean-source check as
current. Promotion alone, or approval of recovery risk, cannot bypass these provenance requirements.

## 9. Report

Return a compact summary:

- created ADR paths grouped by individual/merged decision;
- skipped and ambiguous counts, naming only material ambiguous candidates/questions;
- source Issues updated with backlinks;
- source Issues deleted or retained and why;
- unresolved contract/decision ownership, if any.

Do not echo ADR bodies or the full classification transcript.
