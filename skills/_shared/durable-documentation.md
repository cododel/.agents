# Durable documentation routing

Route unique long-lived value from an Issue, brief, audit, journal, or completed task to one canonical
owner. Do not copy the same normative rule or rationale across document types.

| Durable value | Canonical home |
|:--|:--|
| Stable product, UI, API, domain, persistence, security, module-responsibility, or current architecture behavior | Existing suitable normative owner; new contract via `$contract-writer` only when all four value conditions hold, never from accidental behavior |
| Significant operator-made choice with real alternatives, rationale, and consequences | ADR via `$adr-writer` after its decision/significance gates |
| Repeatable operational, recovery, incident, or production-control procedure | Runbook/playbook |
| Unique reproduction, failure signature, diagnostic probe, or debugging technique | Relevant troubleshooting/reference documentation, focused regression test, or one local non-obvious comment |
| Independently resumable technical debt/deferred work | Report briefly; repository Issue only on a request to record/defer it |
| Current agreed task and unresolved proposals | Shared `task.md` via `$task-journal` when written memory helps |
| Current execution state needed across compaction/sessions/subagents | Shared `state.md` via `$task-journal`, separate from agreed requirements |

A living contract owns normative current state and changes in place. An ADR owns immutable decision
history. Existing normative API/schema/docs may own bounded guarantees when their role is established by
project declarations or normative use; incidental types and example tests alone do not establish it.
Indexes route readers; they do not duplicate the owner's rules.

Before deleting a temporary or completed source artifact, extract only genuinely unique value. If the
content adds nothing beyond its canonical owners and committed implementation/history, it may be a
delete candidate. Exact tracked, clean, committed files are locally recoverable under explicit cleanup
intent; untracked, modified, ambiguous, or historical-decision content remains operator-gated.

Use the project's primary documentation language. Existing translations do not create a multilingual
obligation; require a project rule or explicit request.
