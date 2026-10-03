---
name: yougile-workflow
description: Work with YouGile only through the connector explicitly selected by the operator. Require a link for an existing task and an operator-decided, verified full path for new entities; ask when context is missing.
---

# YouGile workflow

## Connection and target

Use only the connector explicitly selected by the operator for this request. Do not infer it from
available tools, repository/name matches, or another session. If absent, ask for the organization
and connection before any YouGile operation. No browser UI, REST API, CLI, alternate connector, or
workaround is permitted; report unsupported operations and ask how to proceed.

For an existing task or knowledge-base page, require the operator's link, resolve it through the
selected connector, and verify returned identity before changes. An ID, title, search hit, or
remembered ID cannot replace that link. Keep the supplied link in the final report.

## Placement and page content

Before creating an entity, resolve the complete operator-confirmed path: organization, parent
project, board, column/section where applicable, title, and requested visibility/ownership. Reuse
choices already confirmed for this task while target/circumstances remain unchanged; refresh the live
existing path without asking again.
Defaults, unanswered questions, and inferred placement are not agreement. Verify existing ancestors
and supported entity type; stop creation when either remains unverified. For unresolved connector
placement, operator creation in the UI followed by its link is a possible next step.

A knowledge-base page may be task-backed without a visible chat; a confirmed case used the task
connector's description update for its body. Inspect this route through the selected connector
rather than assuming a missing chat/failed task read proves otherwise. Preserve existing body unless
replacement was requested. If unreadable, obtain its text or an explicit replacement decision;
do not overwrite unknown content as an append or claim preservation.

## Formatting

YouGile can collapse code fences and their line breaks. Use confirmed headings, short paragraphs,
and one list item per distinct command/value. Do not use fences, indented code, plain-line runs, or
rely on inline-code styling for separation.

Use numbered items for sequences, bullets for alternatives/reference commands, and one executable
command per item. State its directory in the item or preceding heading; keep comments outside copied
command text. Use labeled bullets per account/object or visually similar value. Publish specific
passwords only with authorization for those values and that destination; otherwise point to their
source. Make URLs clickable where supported.

For a substantial write with uncertain rendering, prepare a small representative sample. Inspect
rendering through the selected connector when available; otherwise mark visual results unverified
and request confirmation only when material to acceptance.

## Writes, evidence, and skill changes

A link/read request does not authorize edits. Apply only requested fields on the verified target;
verify the response and supported resulting state through the same connector. Reconcile uncertain
writes before retrying. Report write success separately from failed reads or unavailable visual proof.
Retain returned IDs and distinguish completed, failed, and unknown steps; no unrequested compensating
deletion/recreation or whole-workflow success claim from partial results.

Confirmed operator-visible behavior is evidence for a reusable lesson, not permission to edit this
skill. Skill updates require an explicit edit request, narrow scope, and confirmed evidence. Do not
universalize a single connector error/guess or relax connector, link, placement, and authority gates.
