# Repository Technical-Debt Issues

This directory stores deferred, independently resumable engineering work close to the code it affects.
It is not a duplicate product tracker and not an archive for every observation.

Create an Issue when evidence proves material work that should not widen the current task. Include a
stable locator, context, root cause or explicit hypothesis, deferral reason, recommended direction,
resume condition, and verification boundary. Add one linked code TODO when a stable seam benefits from
an in-place warning.

## Naming and lifecycle

Use `[STATUS]-YYYY-MM-DD-<english-kebab-slug>.md` unless local convention says otherwise.

- status: `OPEN`, `IMPLEMENTING`, `CLOSED`;
- priority: `Critical`, `High`, `Medium`, `Low` for urgency/sequencing;
- severity: `Critical`, `High`, `Medium`, `Low` for impact/harm;
- body language follows the project/author; filenames remain English kebab-case.

Status changes update both body and filename. Before removing a closed Issue, extract unique current
behavior, significant decisions, or repeatable operations/debugging knowledge into their canonical
owner. An explicit close sweep may remove an exact tracked, clean, committed source; untracked or
modified content remains separately gated because its recovery is not proven.
