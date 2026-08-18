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

- `drift`: current implementation follows a different choice;
- `stale-invariant/code-defect`: implementation violates a choice that may still be intended;
- `ambiguous`: evidence cannot distinguish the two;
- `area-removed`: the decision surface no longer exists.

A stale path link alone proves link drift, not necessarily a changed architectural choice.

### Immutability

For Accepted/Superseded records, inspect `git log --follow -p` when available. Substantive edits to
Context, Options, Decision, or Consequences after acceptance are findings. Status/link metadata and
append-only review notes are allowed. State when Git history is unavailable.

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
- density: trivial reversible decision noise versus known operator decisions that were intentionally
  supposed to be preserved;
- staleness distribution and dead links;
- duplicated normative current-state prose that should have one contract owner.

## Candidate discovery from code

A reverse scan may surface consequential current forks such as persistence strategy, identity model,
deployment topology, event guarantees, or dependency commitments. Classify each as:

- `known-missing-record` only when conversation/Issue/commit/docs evidence shows a significant
  operator decision and rationale intended for ADR preservation;
- `candidate-needs-operator-history` when code shows only current state;
- `not-an-adr` when mandated, obvious, or cheaply reversible.

Do not headline a mature repository with few ADRs as defective by count alone. The audit cannot infer
historical deliberation from architecture shape.

## Finding evidence

Each finding records path, criterion, severity, exact evidence, uncertainty, and recommended action.
Use stable source pointers. `Feels stale` or `this framework is a major choice` is not evidence.
