# ADR Writer

Preserve why the operator chose a consequential path. Within authorized implementation or
documentation work, record a significant agreed decision without a separate ADR request when its
choice, alternatives/constraint, and rationale are evidenced and worth retaining beyond task memory.
An explicit ADR/promotion request also authorizes scoped recording. Read-only review, diagnosis, or
planning alone does not authorize ADR writes. Code or an agent preference cannot establish agreement.

## Load the selected workflow

| Intent | Mode | Read next |
|:--|:--|:--|
| Capture a decision established in the current conversation | from-chat | [from-chat](from-chat.md) |
| Preserve a decision from an in-scope closed Issue, or run a requested promotion sweep | from-issue | [from-issue](from-issue.md) |

Default to `from-chat`. Task or Issue closure never requires an ADR; skip routine choices and records
that add no enduring rationale. A retrospective promotion sweep requires an explicit request.
Read only the selected mode, applying the entrypoint's shared specification. `Proposed` needs an
explicit pending-record request; missing core rationale cannot be disguised as an Accepted record.

Resolve repository/local conventions through `../../_shared/repository-discovery.md`; load
[path-resolution](path-resolution.md) when selecting a write path. Use [adr-template](../assets/adr-template.md) only for
the fallback format and [adr-readme](../assets/adr-readme.md) only when bootstrapping a justified ADR root. Read the
minimum local examples needed to prove conventions.

Scoped recording covers resolved local files and unambiguous relationship backfills. It does not
authorize source cleanup or mass revision of old ADRs. Before Issue backlink edits, the selected
promotion method chooses retained versus deletion-bound sources and owns exact recovery, committed provenance, unique-value, and link
gates. Never auto-commit to satisfy them.

When a current normative owner needs work, use `$contract-writer` only within authorized authoring
scope and its four-value/semantic gates. Report any real decision/ownership conflict while continuing
independent unambiguous records. Return concise paths and the selected workflow's summary; do not echo
ADR bodies.
