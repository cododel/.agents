---
name: adr-writer
description: >
  Generate detailed Architecture Decision Record (ADR) documents — either from the full
  chat conversation, or by scanning resolved issues to identify and promote architectural
  decisions buried inside them. Use whenever the user asks to create an ADR, document an
  architectural decision, capture a design choice, or audit existing issues for ADR
  candidates — including short requests like "сделай ADR", "create ADR",
  "зафиксировать решение", "document this decision", "promote this resolved issue to ADR",
  "какие resolved issues стоит превратить в ADR", "find ADR candidates in docs/issues".
---

# ADR Writer

## Purpose

Produce Architecture Decision Records (ADRs) from **decisions the user has actually
made** — never from extrapolation, best practices, or pattern-matching on topic shape.

The canonical source of a decision is the conversation in which the user weighed
options and chose one. Two modes exist:

1. **From the chat (primary).** Capture an architectural decision worked out in the
   current conversation. The chat *is* the source of truth — rejected options,
   rationale, trade-offs all came out of the user's own reasoning. This is the
   default and the strongly preferred mode.
2. **From resolved issues (exception).** Scan resolved issues for a decision worth
   surfacing as an ADR. Treated as an audit operation, not a routine workflow.
   Strongest when invoked in the **same chat** that just resolved the issue — the
   chain of reasoning is still visible and the model can verify body claims against
   what was actually decided. Cold scans (no recent chat lineage) require harder
   evidence: an explicit positive signal must be quoted from the issue body, no
   reading-between-the-lines.

Either way: work from **explicit evidence**, never from generic best practices, and
**never invent rationale the user didn't articulate**. When evidence is thin, leave
a `TODO:` placeholder and surface it in the report — don't paper over the gap.

## Mode selector

Pick the mode from the user's phrasing **before** loading the detailed workflow.

| User says…                                                                           | Mode          | Read next                       |
|--------------------------------------------------------------------------------------|---------------|---------------------------------|
| "сделай ADR", "create ADR", "document this decision", "зафиксируй решение"            | from-chat     | `references/from-chat.md`       |
| "promote this resolved issue", "найди кандидаты в ADR", "find ADR candidates",        | from-issue    | `references/from-issue.md`      |
| "какие resolved issues стоит превратить в ADR", "audit issues for ADR-worthy items"  |               |                                 |

Default to **from-chat** when the request is ambiguous — and the asymmetry is
intentional. `from-chat` is the load-bearing mode; `from-issue` is an audit
operation that should be invoked deliberately, not as a fallback.

## Quality contract

`references/adr-spec.md` defines **what a good ADR is** — the irreducible core, the
immutability rule, the per-ADR and corpus quality criteria, and the significance check
(when an ADR is *not* needed). It is the single source of truth this skill *enforces* at
write-time and that `adr-auditor` *measures* against at review-time. The template and
workflows below materialise it; when in doubt about what an ADR should contain or whether
one is warranted, that file is the authority. Read it before generating.

## Shared steps (both modes)

Both workflows need the same setup pieces. Read them in this order:

1. **`references/discovery.md`** — locate the `docs/adr/` directory (or its monorepo
   equivalent). One `find` command with explicit exclusions; repo instruction files
   override.
2. **`references/path-resolution.md`** — pick the correct save path based on decision
   scope (global / module / infra). Read this only after discovery confirms which `adr/`
   directories exist.

Both modes also run the **significance check** (`adr-spec.md` §5) before producing a
file — `from-chat` against the conversation (Step F0), `from-issue` against the issue
body (via `candidate-criteria.md`).

The `from-issue` mode additionally needs:

3. **`references/candidate-criteria.md`** — issue-specific promote/skip rules layered on
   top of the significance check, so the classification step is reproducible.

## Assets

- `assets/adr-template.md` — full markdown template covering header metadata (status
  lifecycle, relationship links, `Scope / Component`), the core sections, the
  Risk-Profile-tiered enrichment sections, optional percent-status filename, refresh
  notes, and OPEN / IN-PROGRESS / CLOSED examples. Used by both modes when no stronger
  local convention is documented in the target `docs/adr/README.md`.
- `assets/adr-readme.md` — fallback project convention installed as `README.md` when the
  skill bootstraps a new ADR directory.

## Output convention (preserved from original)

The user's standing preference: **after writing the ADR file, do not echo the body
into chat**. Respond with a short Russian confirmation only:

```
✅ ADR успешно сохранен: `[path/to/the/file.md]`
```

For the `from-issue` mode in batch (multiple promotions in one run), use a compact
summary instead — see `from-issue.md` Step P8.

## Design notes

- **One quality contract, two consumers.** `references/adr-spec.md` is the shared
  definition of a good ADR. This skill enforces it at write-time; the `adr-auditor`
  skill measures an existing corpus against it at review-time (reading it via
  `../adr-writer/references/adr-spec.md`). Keeping the definition in one file is what
  stops "how we write" and "how we audit" from drifting apart — change the contract
  there, not in the template or a workflow copy.
- **ADR ↔ Spec bidirectional linking.** When a companion implementation spec exists
  (typically under `docs/superpowers/specs/`, `docs/specs/`, or a sibling design-doc
  directory), the ADR header carries `**Implementation spec:** [link]` and the spec
  carries `**Aligned with:** [ADR link]`. One-way linkage is a smell — readers
  entering through the ADR won't discover the spec. `from-chat.md` Step F3.5 enforces
  this for new ADRs; the future `spec-writer` skill is responsible for back-filling
  the ADR field when a spec is created after the ADR.
- `references/discovery.md` is duplicated from `issue-writer/` and `docs-cleanup/` by
  design. Each skill stays installable on its own; copies are the price of autonomy.
- `from-chat` and `from-issue` are split into separate references because they have
  different *sources of context* (chat vs file). Only the markdown template in
  `assets/` is shared.
- `candidate-criteria.md` is a separate file (not inlined in `from-issue.md`) because
  the same criteria are useful as a mental model when answering the question "is this
  worth an ADR?" outside the promote workflow. Keeping it separate makes it
  re-readable on its own.
- Promotion **deletes the source issue** after the ADR is saved (with explicit operator
  confirmation). The ADR becomes the canonical reference; the issue file's job is done
  once its content is extracted. Provenance lives in the ADR's `Source issue:` header
  and in git history — there is no `archive/` directory, and back-links to deleted
  files aren't useful. The operator can decline the delete at the gate, in which case
  the source remains and `issue-writer:close` handles it later.
