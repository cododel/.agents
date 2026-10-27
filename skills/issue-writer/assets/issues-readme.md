# Repository Technical-Debt Issues

This directory stores deferred, independently resumable engineering work close to the code it affects.
It is not a duplicate product tracker and not an archive for every observation.

Create an Issue only when the operator requests recording/deferment of evidence-backed independently
resumable work or confirms acceptance of a material limitation owned by an Issue.
Discovering debt alone calls for a brief report. Include a
source/locator, context, the observed problem or requested outcome, stated deferral reason, supported
direction, resume condition, and verification boundary. Include causes or hypotheses only for defects
and distinguish unknown from inapplicable information. A linked code TODO is optional when a stable
seam benefits from an in-place warning.

## Naming and lifecycle

Use stable filenames: `YYYY-MM-DD-<english-kebab-slug>.md`.

- body status: `Open`, `Implementing`, `Closed`;
- priority: `Critical`, `High`, `Medium`, `Low` for urgency/sequencing;
- severity: `Critical`, `High`, `Medium`, `Low` for defects or evidenced harmful limitations; omit when inapplicable and mark applicable unknown values;
- body language follows project documentation unless explicitly requested otherwise; filenames remain English kebab-case.

The body is the single status owner; status or priority changes do not rename the file. Closing an
Issue retains the source by default. Authorized cleanup may remove it after completion, durable-value,
reference, and recovery checks. Preserve unique current behavior, significant decisions, or repeatable
operational knowledge with a suitable canonical owner before removal. Untracked or modified content
remains separately gated because its recovery is not proven.
