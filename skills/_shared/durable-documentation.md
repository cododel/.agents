# Durable documentation routing

Use this reference before extracting long-lived value from an Issue, temporary brief, audit
finding, or completed task. Route each unique fact or rationale to one owner; do not copy the same
normative text across document types.

| Durable value | Canonical home |
|:--|:--|
| Product, UI, API, domain, persistence, security, or current architecture behavior that implementations must satisfy | Existing living project contract via `contract-writer`; creation of a missing contract requires operator approval |
| Significant architectural choice with real alternatives, consequences, and evidence-backed rationale | ADR after the significance gate |
| Repeatable operational procedure, recovery sequence, or production invariant | Runbook/playbook |
| Unique reproduction, diagnostic probe, failure signature, or debugging technique | Relevant troubleshooting/reference documentation or a focused code comment when local and non-obvious |
| Independently resumable deferred work | Issue until completion, then extract any rows above and close it |
| Temporary scope and acceptance agreement under review | Feature brief while active; never treat it as a durable spec or ADR |

If content has no unique durable value after the destination is verified, it may be a deletion
candidate under the normal exact-path operator gate. Plans, conversations, commits, and temporary
briefs are evidence sources or working artifacts, not automatic durable destinations.

A living contract owns normative current state and changes in place. An ADR owns decision history;
its decision invariants state when the choice still holds but do not replace the current contract.
Indexes route readers, tests and executable schemas enforce bounded surfaces, and adjacent documents
link to the normative owner instead of repeating its rules. Treat an executable artifact as the
canonical contract only when project instructions or documentation explicitly declare that role.

Write or update only the project's primary documentation language. Existing translated siblings do
not create a multilingual obligation; only the applicable project `AGENTS.md` can require one.
