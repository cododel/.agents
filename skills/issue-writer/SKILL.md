---
name: issue-writer
description: "Record or update repository-local deferred work on an operator request, or review an existing Issue for current relevance/completion and close completed Issues within explicit lifecycle scope. A linked TODO is optional; discovered debt alone does not authorize a record or sweep."
---

# Issue Writer

Preserve evidence-backed independently resumable work without silently expanding the active task.
Recording/deferral and lifecycle cleanup are separate operator intents; discovering debt alone permits
a brief report, not an Issue, TODO, or sweep.

## Load the selected mode

| Intent | Mode | Reference |
|:--|:--|:--|
| Explicitly record/defer/park independently resumable work | create/update | `references/create.md` |
| Agent notices separate debt without a recording request | briefly report only | No file or TODO |
| Check whether a selected existing Issue is still relevant or complete; review lifecycle candidates | review, read-only | `references/close.md` |
| Explicitly close/sweep completed Issue records after extracting durable value | close/apply | `references/close.md` |

For an authorized recording or lifecycle request, resolve roots through
`../_shared/repository-discovery.md`, read `references/conventions.md`, and load only the selected
mode reference. Local conventions override fallbacks. Load `assets/deferred-template.md` only for
fallback Issue authoring and `assets/issues-readme.md` only for authorized bootstrap; review/close
never creates a missing Issues root.

## Essential boundaries

An explicit operator deferral may remove work from the active scope; preserve the stated reason and
resume conditions without inventing a technical-risk prerequisite. Reuse an unambiguous existing
owner; label uncertain causes as hypotheses. A useful code TODO is optional within the recording
request, explains why the risk remains, and never replaces the Issue's resumption evidence.

Review is read-only. Close/apply needs explicit lifecycle scope and evidence that recorded completion
criteria are met. Its method owns exact status parsing, unique-value extraction, inbound links,
clean-source recovery/provenance, and final rechecks. Valid unrecoverable sources need an exact-path
checkpoint; invalid targets or unresolved value/scope are blocked. Never auto-commit to satisfy
recovery or infer remote tracker authority.

Load `../_shared/durable-documentation.md` before extracting/removing unique value. Keep decision
history and current guarantees with their canonical owners under the relevant authoring gates.

Report the created/updated Issue, deferral reason, optional TODO, and material uncertainty; then resume
the active task. For review/close, use the selected method's compact retained/deleted/extraction result.
