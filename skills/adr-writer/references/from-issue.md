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

Follow the repository's exact status convention. Under the fallback, parse the complete `[CLOSED]`
tag and complete body value `Closed`; recognize exact legacy `Resolved` only when local history
proves it. Prefixes such as `Closed pending verification` or `[CLOSEDNESS]` do not qualify.
Filename/body mismatches are `ambiguous` and remain untouched.

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

## 5. Choose source disposition before edits

Default to **retained**. Promotion alone never authorizes source deletion. Only explicit source
cleanup covering the exact resolved scope can select **deletion-bound** sources.

For each proposed deletion-bound source, read it fully, check incoming links and unique value, and
prove its exact regular non-symlink path is in the confirmed Issue root. Before adding any backlink,
record its fingerprint, repository-relative path, and reachable committed SHA containing the exact
current contents; require clean working-tree and index state. Do not auto-commit a source or edit
its body to manufacture this gate. If recovery is not proven, keep it retained/gated while resolving
the existing recovery control; do not claim it is recoverable.

Plan where every unique non-decision item will survive and how each incoming link will resolve.
Unresolved work/value or load-bearing references block deletion. An unambiguous index-only entry may
be removed or redirected in the same change, with recheck; it is not permission to break a semantic
reference. If extraction cannot complete within the authorized scope, retain the source.

## 6. Write the ADRs

For each accepted candidate/group:

1. resolve the path through local convention or the fallback;
2. use the compact ADR template and proportionate depth from `from-chat.md`/`adr-spec.md`;
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
close sweep must re-establish its current recovery state, since backlink edits made it modified.

When the operator explicitly requests source cleanup in this workflow, apply the same recovery-aware
control as `$issue-writer` close after all ADRs, retained-source backlinks, and extraction targets verify:

- exact regular file inside the confirmed Issue root;
- original fingerprint, source Git state, exact committed provenance, incoming links, and unique
  content rechecked immediately before removal;
- tracked, clean, committed contents may be deleted as a reviewable local change;
- untracked, staged/modified, or otherwise unproven recovery requires the exact-path operator
  checkpoint; it never substitutes for value extraction or durable source provenance;
- symlink, path escape, invalid type, or unresolved scope is blocked: correct the target, then rerun
  the checks; approval cannot bypass target validity;
- never use a glob, infer cleanup from promotion alone, or claim Git recovery without proof.

Apply the planned unambiguous index repair in the same change and recheck references. If any
load-bearing link remains unresolved or state drifted, retain that source. Never stage/commit merely
to make source cleanup possible; Git mutations retain their separate checkout authority.

## 9. Report

Return a compact summary:

- created ADR paths grouped by individual/merged decision;
- skipped and ambiguous counts, naming only material ambiguous candidates/questions;
- source Issues updated with backlinks;
- source Issues deleted or retained and why;
- unresolved contract/decision ownership, if any.

Do not echo ADR bodies or the full classification transcript.
