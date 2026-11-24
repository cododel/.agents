# Repository Technical-Debt Issues

This directory stores deferred, independently resumable engineering work close to the code it affects.
It is not a duplicate product tracker and not an archive for every observation.

Create an Issue only when the operator requests recording/deferment of evidence-backed independently
resumable work or confirms acceptance of a material limitation owned by an Issue.
Discovering debt alone calls for a brief report. An ordinary entry identifies the affected
area, the intended outcome and how to recognize completion. Preserve the stated deferral
reason and any evidence or constraint needed to resume. A linked code TODO is optional.

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
