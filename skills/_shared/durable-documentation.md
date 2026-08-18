# Durable documentation routing

Route unique long-lived value from an Issue, brief, audit, journal, or completed task to one canonical
owner. Do not copy the same normative rule or rationale across document types.

| Durable value | Canonical home |
|:--|:--|
| Stable product, UI, API, domain, persistence, security, module-responsibility, or current architecture behavior | Existing or justified missing living contract via `$contract-writer`; create autonomously when behavior/ownership are explicit, ask when the document would decide semantics |
| Significant operator-made choice with real alternatives, rationale, and consequences | ADR via `$adr-writer` after its decision/significance gates |
| Repeatable operational, recovery, incident, or production-control procedure | Runbook/playbook |
| Unique reproduction, failure signature, diagnostic probe, or debugging technique | Relevant troubleshooting/reference documentation, focused regression test, or one local non-obvious comment |
| Independently resumable technical debt/deferred work | Repository Issue until completion |
| Temporary feature target under review | Feature brief while active, only when its handoff/review value justifies a file |
| Current execution state needed across compaction/sessions/subagents | Untracked `$task-journal`, never project documentation |

A living contract owns normative current state and changes in place. An ADR owns immutable decision
history. Tests, schemas, types, and executable specs enforce bounded surfaces and become canonical only
when project instructions explicitly assign that role. Indexes route readers; they do not duplicate
the owner's rules.

Before deleting a temporary or completed source artifact, extract only genuinely unique value. If the
content adds nothing beyond its canonical owners and committed implementation/history, it may be a
delete candidate. Exact tracked, clean, committed files are locally recoverable under explicit cleanup
intent; untracked, modified, ambiguous, or historical-decision content remains operator-gated.

Use the project's primary documentation language. Existing translations do not create a multilingual
obligation; require a project rule or explicit request.
