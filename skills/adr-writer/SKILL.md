---
name: adr-writer
description: "Create ADRs only for significant operator-made decisions with real alternatives and rationale, including explicit closed-Issue promotion. Use for `сделай ADR/зафиксируй решение`; never infer decisions from code or implementation summaries."
---

# ADR Writer

Preserve why the operator chose a consequential path. Creation requires an explicit ADR/promotion
request and evidenced choice, alternatives/constraint, and rationale. Code or an agent preference
cannot supply historical authority. Accepted reasoning remains immutable; changed choices need
successors, not body rewrites.

## Load the selected workflow

| Intent | Mode | Read next |
|:--|:--|:--|
| Capture a decision established in the current conversation | from-chat | `references/from-chat.md` |
| Explicitly find/promote decision history preserved in closed Issues | from-issue | `references/from-issue.md` |

Default to `from-chat`; Issue promotion is explicit, not automatic closeout. Read only the selected
mode, plus `references/adr-spec.md` before classification/writing. That shared specification owns
significance, granularity, truthful rationale, decision/record dates, lifecycle, depth, and contract
relationships. `Proposed` needs an explicit pending-record request; missing core rationale cannot
be disguised as an Accepted record.

Resolve repository/local conventions through `../_shared/repository-discovery.md`; load
`references/path-resolution.md` when selecting a write path. Use `assets/adr-template.md` only for
the fallback format and `assets/adr-readme.md` only when bootstrapping a justified ADR root. Read the
minimum local examples needed to prove conventions.

The ADR request covers resolved local files and unambiguous relationship backfills. It does not
authorize source cleanup. Before Issue backlink edits, the selected promotion method chooses retained
versus deletion-bound sources and owns exact recovery, committed provenance, unique-value, and link
gates. Never auto-commit to satisfy them.

When a current normative owner needs work, use `$contract-writer` only within authorized authoring
scope and its four-value/semantic gates. Report any real decision/ownership conflict while continuing
independent unambiguous records. Return concise paths and the selected workflow's summary; do not echo
ADR bodies.
