# Kaneo MCP Tool Reference

Use the live MCP declarations as the source of truth. This reference captures the official Kaneo
MCP surface and its currently exposed schemas so an agent can select tools without rediscovering
the entire catalog.

## Contents

- Session and discovery
- Projects
- Tasks
- Comments
- Labels
- Task relations
- Operational constraints

## Session and discovery

### `whoami`

Return the current cached Kaneo session and user. Takes no arguments. Use only for authentication
diagnostics and redact the session token from all output.

### `list_workspaces`

List workspaces accessible to the signed-in user. Takes no arguments. Workspace objects provide
the ID needed by project and label tools.

## Projects

### `list_projects`

- `workspaceId` (required string)
- `includeArchived` (optional boolean)

List projects in a workspace.

### `get_project`

- `id` (required string)

Get one project by ID.

### `create_project`

- `workspaceId` (required string)
- `name` (required string)
- `slug` (required string)
- `icon` (required string)

Create a project in a workspace.

### `update_project`

- `id` (required string)
- `name`, `slug`, `icon`, `description` (optional strings)
- `isPublic` (optional boolean)

Apply only supplied project fields.

## Tasks

### `list_tasks`

- `projectId` (required string)
- `assigneeId`, `status` (optional strings)
- `priority` (optional: `no-priority`, `low`, `medium`, `high`, `urgent`)
- `dueAfter`, `dueBefore` (optional date strings)
- `page`, `limit` (optional numbers)
- `sortBy` (optional: `createdAt`, `priority`, `dueDate`, `position`, `title`, `number`)
- `sortOrder` (optional: `asc`, `desc`)

The response can contain project columns with `id`, `slug`, `name`, `isFinal`, and their tasks,
plus planned tasks, archived tasks, and pagination. Use returned column slugs/IDs for status calls.

### `get_task`

- `taskId` (required string)

Get one task by ID.

### `create_task`

- `projectId` (required string)
- `title` (required string)
- `description` (required string; use an empty string only when the user provides no useful body)
- `status` (required string from the target project's columns)
- `priority` (required: `no-priority`, `low`, `medium`, `high`, `urgent`)
- `startDate`, `dueDate` (optional strings)
- `userId` (optional string)

### `update_task`

- `taskId` (required string)
- `title`, `status`, `projectId` (optional strings)
- `description` (optional string or null)
- `priority` (optional: `no-priority`, `low`, `medium`, `high`, `urgent`)
- `startDate`, `dueDate` (optional strings or null)
- `userId` (optional string or null)
- `position` (optional number)

The MCP fetches the current task, merges supplied fields, and then performs a full update. Send only
intended changes and use `null` only to clear a nullable field deliberately.

### `update_task_status`

- `taskId` (required string)
- `status` (required string from the current project columns)

Prefer this tool for status-only transitions.

### `move_task`

- `taskId` (required string)
- `destinationProjectId` (required string)
- `destinationStatus` (optional string from the destination project columns)

Inspect the destination project first. Omitting `destinationStatus` delegates status choice to the
server and may not express the user's intended workflow state.

## Comments

### `list_task_comments`

- `taskId` (required string)

### `create_task_comment`

- `taskId` (required string)
- `content` (required string)

### `update_task_comment`

- `commentId` (required string)
- `content` (required string)

Only update a comment after resolving its exact ID.

### `delete_task_comment`

- `commentId` (required string)

Only the current user's comments can be deleted. Re-read the comment before deletion.

## Labels

### `list_workspace_labels`

- `workspaceId` (required string)

### `create_label`

- `workspaceId` (required string)
- `name` (required string)
- `color` (required string)
- `taskId` (optional string)

Create a workspace label and optionally attach it to one task.

### `attach_label_to_task`

- `labelId` (required string)
- `taskId` (required string)

### `detach_label_from_task`

- `labelId` (required string)

The MCP detaches the label from its current task.

### `delete_label`

- `id` (required string)

Only task-associated labels can be deleted. The API rejects workspace-level labels whose `taskId`
is null.

## Task relations

### `create_task_relation`

- `sourceTaskId` (required string)
- `targetTaskId` (required string)
- `relationType` (required: `subtask`, `blocks`, `related`)

Direction matters: `subtask` means source parent → target child; `blocks` means source blocker →
target blocked; `related` is bidirectional.

### `get_task_relations`

- `taskId` (required string)

List all subtask, blocking, and related relations involving a task.

### `delete_task_relation`

- `id` (required relation ID)

Resolve the relation ID with `get_task_relations` before deletion.

## Operational constraints

- There is no exposed batch mutation. Preserve returned IDs and stop on partial failure unless the
  user asked for best-effort continuation.
- There is no exposed idempotency key. After an uncertain write result, read before retrying.
- There is no exposed task delete, project delete, project archive, or member-list tool.
- Project names and task titles are selectors for humans, not stable identity. Write calls use IDs.
- Workflow statuses are project-defined. Never assume one project's slugs apply to another.
- Dates are accepted by the MCP as strings. Preserve an explicit timezone/offset; if a date is
  materially ambiguous, ask rather than inventing one.

## Source provenance

- Official Kaneo MCP package: <https://github.com/usekaneo/kaneo/tree/main/packages/mcp>
- Official MCP README and tool inventory:
  <https://github.com/usekaneo/kaneo/blob/main/packages/mcp/README.md>
- Kaneo functional and API documentation: <https://docs.kaneo.app/>

The official HTTP task documentation is incomplete for some request bodies. Prefer the live MCP
input schema whenever it is more specific than the general HTTP documentation.
