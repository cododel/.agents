# Create / update workflow

## 1. Establish the work and recording authority

Identify the observed defect, agreed improvement, requested capability, or accepted limitation being
recorded, its source, affected scope, and why it matters. Establish enough context for another
session to resume: unresolved decisions, the next useful action, and observable completion or
reconsideration conditions. Preserve stated deferral reasons; do not invent one when none was given.

Proceed on a request to record/defer this work or confirmed acceptance of a material limitation under
AGENTS. Discovering debt alone permits a concise report, not an Issue or TODO. An operator may defer
in-scope work even when the agent could fix it now; no technical-risk justification is required.
For a defect, separate observed symptoms from established causes and hypotheses. If the cause is
unknown, say so; record a distinguishing probe when one is supported, not a mandatory invented cause.

## Accepted limitations

Distinguish work postponed for later implementation from an accepted limitation whose repair may never
be worthwhile. For the latter, record the decision source, rationale and considered alternative,
operating limits, material edge cases/consequences, how leaving those limits would be detected, and
who revisits the decision under what condition. Use evidence or label uncertainty; unknown impact is
not proven acceptable. Do not invent an implementation deadline or assert that the defect was fixed.

Reuse one suitable Issue or existing decision owner. Route a significant agreed architectural choice
to `adr` only when its criteria fit; no mandatory Issue-plus-ADR pair. A simple implementation
that already meets requirements does not need a debt record. Temporary missing work remains in the
active task unless the operator actually changes acceptance or defers it.

Keep local lifecycle conventions. Under the fallback, an Issue with accepted unresolved debt stays
`Open`, with its disposition in the body; it is not a closure candidate merely because risk was
accepted. For an accepted limitation, use reconsideration conditions and the next assessment instead
of promising repayment. Revisit implementation only under the current authorized scope.

## 2. Discover local ownership and duplicates

Look for an existing local record or list that already owns the work. For a standalone Issue,
use the established Issues root and its conventions. Inspect examples when the format or
ownership is unclear. Search for the same outcome before adding a record.

- Update an existing Issue when it owns the same work and completion target.
- Create a related new Issue for a distinct completion target, boundary, or established defect cause;
  link the relationship.
- Ask only when the records are plausibly competing owners and the choice would change historical or
  operator intent.

When a standalone Issue is needed and no Issues root exists, an explicit recording/deferral request authorizes
bootstrapping `docs/issues/` or a proven module-local equivalent with the fallback README/template.
Stop if repository or module scope is ambiguous.

## 3. Write useful resumption context

For ordinary deferred work, a short entry can identify the affected place, the desired outcome
and how the next person will recognize completion. An existing list can carry this in one bullet.
For a standalone file, follow local conventions or use the compact fallback template.

Preserve an explicitly stated deferral reason. Add evidence, priority, a dependency, or a first
investigation step when it changes how someone resumes the work. For a defect, distinguish an
observed symptom from a suspected cause. Use the accepted-limitation guidance above when applicable.

## 4. Optional useful TODO

Within the recording request, when a stable code seam directly exposes the deferred risk, optionally
add one concise comment, for example:

```text
TODO(issue): <why this remains unsafe/incomplete>; see docs/issues/<issue-file>.md
```

Adapt syntax and relative path to the language/repository. The comment must remain meaningful without
line-number dependence. Do not add TODOs to generated files, duplicate them across consumers, or use
a TODO as a substitute for a failing test that belongs in the current fix.

## 5. Verify

- path and filename follow local convention;
- for standalone Issues, the complete body status is valid; filename status agrees only where local convention encodes it;
- evidence locators exist and no paths/SHAs are fabricated;
- no duplicate owner remains unlinked;
- TODO link resolves when one was added;
- an established Issues index is updated only when its format is unambiguous;
- `git diff --check` and project documentation checks pass when available.

## 6. Return to the active task

Report the Issue and TODO once, update the task journal when active, and resume the original task. Do
not begin implementing the deferred Issue in the same branch/session unless the operator changes
scope.
