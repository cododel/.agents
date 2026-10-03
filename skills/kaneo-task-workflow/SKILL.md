---
name: kaneo-task-workflow
description: "Manage work through Kaneo MCP only when Kaneo is explicitly named or project instructions declare it. Resolve scope before reads or writes; do not infer Kaneo from generic task/Issue wording or mirror Markdown Issues."
---

# Kaneo Task Workflow

## Route and select capability

Use Kaneo for an explicit current mention/proven reference, or when applicable project instructions
declare it for this scope. Otherwise follow the declared tracker; with several, use their scope
mapping and ask only about unresolved placement. Generic task/Issue wording, Markdown directories,
and available tools do not select Kaneo. In a Kaneo-declared project, requests to record/defer work
route there unless Markdown is explicitly requested; do not mirror both automatically.

Inspect the selected connector/server's live declarations. Plugin metadata does not prove that a
separate local MCP server is active or authenticated. Capabilities and schemas vary; do not invent
arguments, assume task deletion/member listing is absent, or simulate missing tools through unrelated
calls. Do not register servers or change credentials as a fallback; report the exact limit and
continue independent work.

Consult only the relevant section of [references/tool-reference.md](references/tool-reference.md)
when tool choice, parameter semantics, or connector quirks need clarification. The catalog is not a
required read for every request and never overrides the selected live schema. Use `whoami`, when
exposed, only for authentication diagnostics; never output/persist its raw token-bearing response.

## Resolve the narrowest target

- Supplied task/project ID or link: read that entity directly and verify returned identity/ownership
  before writing. Skip resolved ancestors; names, remembered IDs, and plans are selectors, not proof.
- Unknown ID: prefer supported narrow search scoped to known workspace/project and entity type;
  list workspaces/projects only for unresolved ancestors. Include archives only for archived scope.
- Task inventory: use the smallest useful filters and follow pagination; report partial pages honestly.
  Load comments, relations, labels, or members only when the requested operation needs them.
- Workflow state: read `list_project_columns` when exposed, otherwise supported project/board data.
  Use the returned status representation required by the selected write schema; IDs, slugs, and
  display names are not interchangeable across connectors or projects.

## Apply exact mutation intent

Reading or implementing a referenced task does not authorize tracker writes. Create, update, move,
status, comment, label, relation, and delete calls require explicit task-management intent for their
actual target. Re-read destructive targets and preserve unrelated fields/operator content.

For creation, resolve the project/columns, check for an obvious duplicate, and supply only known or
required fields from the live schema. Track independently useful work rather than every observation
unless requested. Retain every returned ID for multi-step writes and report partial completion.

Prefer narrow status/field/move tools when exposed. Verify destination columns before moving. A
request to close a task authorizes the verified final status expressing that intent; it does not
imply deletion, comments, time entries, or other fields. Resolve materially different final outcomes.

After any uncertain write, reconcile resulting state before retrying; use documented idempotency only
when supported. Blind retries can duplicate entities. For comments/labels/relations, inspect the
relevant reference/schema for ownership limits, nullable clearing, and relation direction.

Report resolved scope, filters/pagination, affected IDs, exact changes, and partial failures. Never
include credentials, bearer tokens, device codes, or raw authentication payloads.
