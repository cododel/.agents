---
name: chrome-devtools-cli
description: Use Chrome DevTools CLI when a browser task needs network, console, CSS, performance, memory, Lighthouse diagnostics, or repeatable terminal-driven automation. For ordinary navigation and visual UI checks, use available Browser Use instead.
---

# Chrome DevTools CLI

Use the CLI when DevTools evidence or repeatable terminal automation materially helps the task.
For ordinary navigation, local app flows, and visual checks, use available Browser Use. If
`chrome-devtools` is unavailable, use another capability; a browser task does not authorize installation.

## Command selection

Use installed `--help` and command-specific help for supported commands, arguments, and flags.
Resolve unclear effective defaults through installed implementation or primary version-matched
documentation. An update notice does not authorize installation or daemon restart.

Read only the needed sections of [the command reference](references/cli-reference.md):

| Task | Section |
| --- | --- |
| Element actions or page navigation | [Input automation](references/cli-reference.md#input-automation), [Navigation](references/cli-reference.md#navigation) |
| Network requests | [Network](references/cli-reference.md#network) |
| Console, CSS, scripts, screenshots, or Lighthouse | [Debugging and inspection](references/cli-reference.md#debugging-and-inspection) |
| Performance traces and insights | [Performance](references/cli-reference.md#performance) |
| Heap analysis | [Memory](references/cli-reference.md#memory) |
| Viewport, device, or network emulation | [Emulation](references/cli-reference.md#emulation) |
| Authorized extension or PWA work | [Extensions](references/cli-reference.md#extensions), [Progressive web apps](references/cli-reference.md#progressive-web-apps) |
| Experimental tools | [Experimental features](references/cli-reference.md#experimental-features) |
| Needed daemon inspection or management | [Service management](references/cli-reference.md#service-management) |

If the page ID is unknown, use `list_pages`. Before any command consuming an element UID, take a
current `take_snapshot <pageId>` and use that page's latest UIDs; refresh after navigation or relevant
DOM changes. Network, console, and other non-UID diagnostics can run directly with known IDs.

## Daemon ownership and cleanup

A tool command, including `list_pages`, implicitly starts a daemon when none exists. Account for its
process and browser/profile before the first command, and record any task-created daemon, including
implicit starts. State persists across commands; do not run `start`/`status`/`stop` before every use.

Start, restart, reconfigure, or stop only a task-owned daemon. An existing session is not task-owned
merely because the CLI reaches it. `status` can inspect an existing session when needed; `start`
restarts a running daemon. Stop task-created daemons at handoff unless asked to keep them running.

Release every loaded heap snapshot with `close_heapsnapshot` after analysis, including both inputs
of a comparison. Deleting its file does not release the loaded daemon memory.

## Files and external effects

The CLI can default to unrestricted filesystem access, including output paths and `upload_file`.
Tool access does not authorize reading, writing, or uploading those files. Confirm effective
filesystem settings; CLI defaults can differ from server defaults shown in help. For required
temp-only access, configure a task-owned daemon with an explicit OS temp root (`--workspace` or
the installed equivalent) and `--allowUnrestrictedPaths=false` where supported. Do not assume the
false flag alone establishes that restriction or restart another task's daemon to enforce it.

Command availability does not authorize external effects, extension/PWA installation, or execution
of page-provided integrations. Enabling optional features follows the same task scope and ownership.
