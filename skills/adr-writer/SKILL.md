---
name: adr-writer
description: "Create ADRs only for significant operator-made decisions with real alternatives and rationale, including explicit closed-Issue promotion. Use for `сделай ADR/зафиксируй решение`; never infer decisions from code or implementation summaries."
---

# ADR Writer

Preserve **why the operator chose one consequential path over real alternatives**. The agent may
research options and identify an ADR candidate, but an ADR records a decision the operator actually
made; it never upgrades the implementing agent's preference into architecture history.

## Modes

| Intent | Mode | Read next |
|:--|:--|:--|
| Capture a decision established in the current conversation | from-chat | `references/from-chat.md` |
| Explicitly find/promote decision history preserved in closed Issues | from-issue | `references/from-issue.md` |

Default to `from-chat`. Treat `from-issue` as an explicit audit/promotion workflow, not a routine close
step.

## Quality contract

Read `references/adr-spec.md` before writing. It is shared with `$adr-auditor` and owns:

- the operator-decision and significance gates;
- one-decision granularity;
- evidence requirements for alternatives and rationale;
- immutable Accepted records and succession;
- proportionate context, consequences, assumptions/invariants, and revisit evidence.

Do not fabricate a rejected option, selection reason, confidence, or historical discussion. Ask for a
missing load-bearing decision fact or leave an explicit `TODO:` only when the operator still wants a
`Proposed` record. An `Accepted` ADR must be self-sufficient and must not contain unresolved core
rationale.

## Discovery and path

Read, in order:

1. `../_shared/repository-discovery.md`;
2. `references/path-resolution.md`;
3. the applicable local ADR README/template and 1–2 recent representative ADRs.

Project convention wins. The fallback is intentionally small and uses
`assets/adr-template.md`; it has no implementation percentage or task-progress lifecycle.

## Contract relationship

A living contract owns normative current behavior; an ADR owns dated decision history. When both
exist, link them bidirectionally without copying rules. When a stable current contract is missing,
`$contract-writer` may create one autonomously only if behavior and ownership are already explicit;
otherwise report the unresolved semantic gate.

## Authority and mutation

- ADR creation requires an explicit operator request. A `from-issue` request authorizes unambiguous promotions in its resolved scope; ask only for missing decision history, conflicting ownership, or material grouping choices.
- The ADR may be born `Accepted` only when the operator made the choice. Use `Proposed` only when the
  operator explicitly wants a pending decision record.
- Never rewrite the reasoning body of an Accepted ADR. Changed decisions require a successor and
  bidirectional `Supersedes` / `Superseded by` links.
- Directory/file creation and relationship-link backfills are local reversible edits covered by the
  ADR request. Promotion does not imply source cleanup; when cleanup is explicitly requested,
  `from-issue` may remove exact tracked, clean, committed sources and gates unrecoverable ones.

## Output

After writing, do not echo the ADR body. Respond in one concise line with the repository-relative path,
for example:

```text
ADR сохранён: `docs/adr/ADR-20260818-use-event-outbox.md`
```

For batch promotion, use the compact summary defined by `references/from-issue.md`.
