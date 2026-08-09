---
name: kaneo-task-workflow
description: "Route and manage project work through the Kaneo MCP task tracker. Use when the user explicitly mentions Kaneo, supplies a Kaneo workspace/project/task reference, or the applicable repository AGENTS.md explicitly declares Kaneo as the task tracker. Resolve tracker scope, read tasks, and create, update, move, comment on, label, or relate tasks. Do not infer Kaneo from generic task/issue wording, Markdown issue files, or the absence of another tracker; honor explicit repository routing and other declared trackers."
---

# Kaneo Task Workflow

Use Kaneo only when current evidence routes the work there, then operate on verified workspace,
project, and task IDs. Treat Kaneo as an external system: reads may establish context, while writes
need explicit task-management intent.

## Route to the tracker

Apply this precedence within the current repository scope:

1. Route an explicit current mention of Kaneo or a proven Kaneo reference to Kaneo.
2. Otherwise, inspect the applicable `AGENTS.md`. Route to Kaneo only when it explicitly declares
   Kaneo as the tracker for the current project or subproject.
3. If repository instructions declare another tracker, use that tracker and do not call Kaneo.
4. If multiple trackers are declared, follow their documented scope mapping. Ask for the target
   only when that mapping does not decide the request.
5. If no tracker is declared and the user did not mention Kaneo, do not infer one. Continue work
   without tracker calls, or ask only when a tracker operation is necessary to satisfy the request.

The presence or absence of `issues/`, `docs/issues/`, Markdown issue records, issue templates, or
issue-like filenames is **not** evidence for or against Kaneo. A repository may use Kaneo alongside
Markdown records, use a different hosted tracker, or have no task tracker.

In a Kaneo-declared project, intents such as "отложим", "создай задачу", or "зафиксируй на потом"
route to Kaneo unless the user explicitly requests a Markdown issue file. Do not mirror the same
work into Kaneo and Markdown automatically.

## Establish exact context

Use the narrowest discovery chain that resolves supplied names or IDs:

1. Call `list_workspaces` when the workspace ID is unknown.
2. Call `list_projects` for the selected workspace when the project ID is unknown. Include archived
   projects only when the request concerns archived work.
3. Call `list_tasks` to inspect the project board, status columns, planned tasks, archived tasks,
   filters, and pagination. Status writes use the project's returned status slug/ID, not a guessed
   display name.
4. Call `get_task` before changing a task when current state or target identity is not already
   proven. Load comments, relations, or workspace labels only when the operation needs them.

Never treat a display name, task title, remembered ID, plan, or conversation as proof of the exact
target. Resolve ambiguities read-only before a write.

Use `whoami` only for authentication diagnostics. Its response can contain a live session token;
never quote, log, persist, or return the raw response. Report only the minimum non-secret identity
and session-health fields.

## Respect mutation authority

- Read-only listing and inspection may proceed when relevant to the request.
- Create, update, move, status, comment, label, relation, and delete calls require explicit
  task-management intent from the user. Merely reading or implementing a referenced task does not
  authorize status changes or comments.
- Before a destructive call, re-read and verify the exact comment, relation, or label. Do not widen
  an ambiguous deletion request.
- After a timeout or transport error on any write, read the target state before retrying. Kaneo has
  no exposed idempotency key or batch-write tool, so a blind retry can duplicate tasks, comments,
  labels, or relations.
- Create tasks only for work worth tracking independently. Do not turn every observation or nuance
  into a task unless the user explicitly asks.

## Perform common operations

### Read or triage tasks

Resolve the project, then call `list_tasks` with the smallest useful filters. Follow pagination;
do not claim a complete inventory from one partial page. Use `get_task` for full task context and
load comments or relations only when they affect the answer.

### Create a task

Resolve the exact project and inspect its columns before creation. Supply `title`, `description`,
`priority`, `status`, and `projectId`; add dates and assignee only when known. Use only the supported
priority values and a returned project status. Check for an obvious existing task before creating a
duplicate. For multiple tasks, create them one at a time, retain every returned ID, and report any
partial completion.

### Update status, fields, or project

Use `update_task_status` for a status-only transition. Use `update_task` for field changes and send
only intended fields; the server fetches current state, merges those fields, and performs a full
update. Use `move_task` to transfer a task between projects, and verify the destination status
against the destination project's columns. Do not hard-code workflow names such as `in-progress`
or `done` across projects.

### Work with comments, labels, and relations

- List comments before editing or deleting one; comment deletion is limited to the current user's
  comments.
- Prefer existing workspace labels. `create_label` can optionally attach the new label to a task.
  `delete_label` only accepts task-associated labels; workspace-level labels are rejected.
- Use relation direction precisely: for `subtask`, source is parent and target is child; for
  `blocks`, source blocks target; `related` is bidirectional.

Read `references/tool-reference.md` before the first write in a session, when choosing between
similar tools, or when exact parameters and supported filters matter.

## Handle unsupported or stale capabilities

The live MCP catalog is the source of truth. If a documented tool is unavailable or its schema
differs, inspect the live declaration and adapt without inventing arguments. The current catalog
does not expose task deletion, project deletion, project archiving, batch creation, or member
listing; report these limitations instead of simulating them through unrelated calls.

## Report results

After reads, identify the resolved workspace/project and any filters or pagination limits. After
writes, report the affected entity IDs, exact field/status changes, and any partial failures. Never
include credentials, bearer tokens, device codes, or raw authentication payloads.
