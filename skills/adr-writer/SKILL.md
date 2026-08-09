---
name: adr-writer
description: "Create a detailed ADR for a significant decision with real alternatives and rationale, or promote such a decision from closed issues. Use for `create/write an ADR`, `сделай ADR`, `зафиксируй архитектурное решение`, or requests to find/promote ADR candidates. Do not use for implementation summaries or to audit an existing ADR corpus; use `adr-auditor` for audits."
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
2. **From closed issues (exception).** Scan closed issues for a decision worth
   surfacing as an ADR. Treated as an audit operation, not a routine workflow.
   Strongest when invoked in the **same chat** that just closed the issue — the
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
| "promote this closed issue", "найди кандидаты в ADR", "find ADR candidates",        | from-issue    | `references/from-issue.md`      |
| "какие closed issues стоит превратить в ADR", "audit issues for ADR-worthy items"    |               |                                 |

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

1. **`../_shared/repository-discovery.md`** — locate and prove the ADR root and scope.
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
  this for new ADRs. A temporary feature brief is not an implementation spec and must
  not receive this durable link. When a durable spec is created later, its owning
  workflow is responsible for back-filling both directions.
- Repository discovery and durable-value routing are shared across this coordinated skill set;
  ADR significance, path resolution, and evidence gates remain local.
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
