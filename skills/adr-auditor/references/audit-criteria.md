# ADR audit criteria

Read `../../adr-writer/references/adr-spec.md` first. This file adds review-time checks that require
code, Git history, and corpus context.

## Per-ADR checks

### Decision authority and rationale

- Does the record attribute a real operator decision rather than present implementation as history?
- Are alternatives and selection/rejection reasons concrete and evidenced?
- If only one option exists, is the hard constraint explicit rather than decorative?
- Is the ADR one independently supersedable decision?

Thin or invented-looking rationale is `hollow-alternatives` / `unsupported-rationale`, not something
the auditor may repair by writing better prose.

### Drift versus violated invariant

Extract concrete anchors from the decision, contracts, dependencies, services, data model, and
invariants. Verify them in current source/config/runtime evidence.

- `drift`: evidence establishes a changed operator choice, with current implementation traced
  separately;
- `stale-invariant/code-defect`: implementation violates a choice that may still be intended;
- `ambiguous`: evidence cannot distinguish the two;
- `area-removed`: the decision surface no longer exists.

A stale path link alone proves link drift, not necessarily a changed architectural choice.
When implementation follows another approach but no changed operator choice is evidenced, report
`stale-invariant/code-defect` if the intended choice is established, otherwise `ambiguous`.

### Immutability

For Accepted/Superseded records in the requested immutability scope, establish the acceptance
baseline from evidence, then inspect `git log --follow -p` and any current staged/unstaged changes.
Substantive edits to Context, Options, Decision, or Consequences after acceptance are findings.
Status/link metadata and append-only review notes are allowed. Report one exact check status:

- `clean`: the acceptance baseline and complete relevant history/current diff were checked;
- `violated`: a substantive post-acceptance rewrite is evidenced;
- `skipped-no-git`: required repository history is unavailable;
- `not-checked`: the check is outside requested scope or was not performed; explain which;
- `not-applicable`: the record has not reached an immutable lifecycle state;
- `unknown-acceptance-baseline`: available evidence cannot establish when acceptance began.

Record the reason and coverage (baseline commit/date when known, history range/current diff checked,
and any missing interval). Never encode a partial or skipped check as `clean`.

### Status truth and relationships

- `Proposed` plus implemented code does not automatically prove operator acceptance; flag for
  confirmation unless history shows the decision.
- `Accepted` plus proven decision drift needs a successor/deprecation path.
- `Superseded` must link to a real successor and vice versa.
- `Deprecated` should mean the area ended without a direct replacement.

### ADR used as current contract

Report `adr-as-current-contract` only when maintainers need normative current behavior/ownership from
the ADR and no declared living/executable contract owns it. Do not demand a contract for every ADR.

## Corpus checks

- supersession chains and relationship links;
- contradictory live ADRs in the same decision area;
- placement/naming against local convention;
- density: trivial decision noise versus known significant operator decisions that were intentionally
  supposed to be preserved;
- staleness distribution and dead links;
- duplicated normative current-state prose that should have one contract owner.

## Candidate discovery from code

A reverse scan may surface consequential current forks such as persistence strategy, identity model,
deployment topology, event guarantees, or dependency commitments. Classify each as:

- `known-missing-record` only when conversation/Issue/commit/docs evidence shows a significant
  operator decision and rationale intended for ADR preservation;
- `candidate-needs-operator-history` when code shows only current state;
- `not-an-adr` when the shared significance gate fails; reversibility alone does not disqualify a
  meaningful precedent or substantial alternatives whose rationale must survive.

Do not headline a mature repository with few ADRs as defective by count alone. The audit cannot infer
historical deliberation from architecture shape.

## Finding evidence

Each finding records path, criterion, severity, exact evidence, uncertainty, and recommended action.
Use stable source pointers. `Feels stale` or `this framework is a major choice` is not evidence.
