---
name: kaneo-task-workflow
description: "Manage work through Kaneo MCP only when Kaneo is explicitly named or project instructions declare it. Resolve scope before reads or writes; do not infer Kaneo from generic task/Issue wording or mirror Markdown Issues."
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

Select the Kaneo connector/server applicable to the request and inspect its live tool declarations.
Plugin metadata describes a declared capability; it does not prove that a separately configured local
MCP server is active or authenticated. Do not register servers or change credentials as a task-management
fallback. If the selected tool is unavailable, report the exact limit and continue independent work.

Use the narrowest discovery chain that resolves supplied names or IDs. Skip resolved ancestors:

1. For a supplied task/project ID or link, read that entity directly with the selected tool and verify
   its returned identity and ownership before a write. A known ID need not trigger workspace-wide listing.
2. For an unknown ID, prefer a supported narrow search scoped to the known workspace/project and entity
   type; otherwise call `list_workspaces` or `list_projects` only for the unresolved ancestor. Include archived
   projects only when the request concerns archived work.
3. Read columns through `list_project_columns` when exposed; otherwise use project/board data returned
   by supported reads. Inspect `list_tasks` only for the task inventory/filtering needed by the request.
   Use the project's returned status value in the form required by the selected write schema. A column
   ID, slug, and display name are not interchangeable.
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
- Before a destructive call, re-read and verify the exact task, comment, relation, or label. Do not widen
  an ambiguous deletion request.
- After a timeout or transport error on any write, reconcile the target state before retrying. Use
  documented idempotency only when the selected tool supports it; a blind retry can duplicate tasks,
  comments, labels, or relations.
- Create tasks only for work worth tracking independently. Do not turn every observation or nuance
  into a task unless the user explicitly asks.

## Perform common operations

### Read or triage tasks

Resolve the project, then call `list_tasks` with the smallest useful filters. Follow pagination;
do not claim a complete inventory from one partial page. Use `get_task` for full task context and
load comments or relations only when they affect the answer.

### Create a task

Resolve the exact project and inspect its columns before creation. Supply `title`, `description`,
`priority`, `status`, and `projectId` when required by the selected live schema; add dates and assignee
only when known. Use supported priority values and a returned status in the schema's expected form.
Check for an obvious existing task before creating a duplicate. For multiple tasks, create them one
at a time, retain every returned ID, and report any
partial completion.

### Update status, fields, or project

Use `update_task_status` for a status-only transition. Use `update_task` for field changes and send
only intended fields; the server fetches current state, merges those fields, and performs a full
update. Use `move_task` to transfer a task between projects, and verify the destination status
against the destination project's columns. Do not hard-code workflow names such as `in-progress`
or `done` across projects.

An explicit request to close a task authorizes its status transition to the verified final column
that expresses the operator's intent. It does not authorize deletion, comments, time entries, or
other field changes. If several final states express materially different outcomes, resolve that choice.

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
differs, inspect the selected live declaration and adapt without inventing arguments. Task deletion,
member listing, project columns, and other capabilities vary across connector/server versions; use
them only when exposed and authorized. Report absent capabilities instead of simulating them through
unrelated calls.

## Report results

After reads, identify the resolved workspace/project and any filters or pagination limits. After
writes, report the affected entity IDs, exact field/status changes, and any partial failures. Never
include credentials, bearer tokens, device codes, or raw authentication payloads.
