# Phase 8 — Report, prioritization, gate, cadence

## Findings table

| Priority | Criterion | Examples |
|---|---|---|
| P0 | Actively harms accuracy | Trigger collisions, lies in CLAUDE.md, dead commands, rotten references |
| P1 | Wastes context | Bloated CLAUDE.md, unused skills without disable-model-invocation, surplus MCP servers, duplicate plugin enablement |
| P2 | Unrealized value | Advice-rules that should be hooks, missing verification loops, no baseline evals, prose autonomy with no enforcement |
| P3 | Hygiene | Missing examples in skills, drifted reference versions, naming, uncommitted config |

Each finding: one row, one-sentence concrete fix. End the report with the three
fixes having the highest effect-to-effort ratio.

**Also report what is healthy.** An audit that only lists defects invites
"fixing" sound design (e.g. internally-gated skills don't need
`disable-model-invocation`; advice+enforcement layering is not duplication).
Naming considered-and-rejected changes protects them from the next auditor.

## The gate

P0/P1 — offer to fix inside the review session, each as its own scoped
conventional commit. P2/P3 — hand to `issue-writer` as file-based deferrals;
don't inflate the audit session. Nothing is changed without confirmation; for
deletions, list and verify targets first.

## Report file

`reviews/<YYYY-MM-DD>-config-audit.md`, committed. Include: inventory numbers
(before), findings table, what-is-healthy list, eval results if phases 5–6 ran,
and which phases were skipped. The next audit diffs against it — progress over
feelings.

## Cadence

- **Full audit** — every 60–90 days, report saved with a timestamp.
- **Spot audit** — after each major Claude Code release (features migrate:
  commands→skills, slash commands get renamed — e.g. `/fork` → `/branch` —
  config rots from platform change, not only project change).
- **Triggered audit** — after any "Claude did the wrong thing" incident. Each
  such case is a configuration bug: find which artifact should have prevented
  it and fix *it*, not just the consequences.

## Artifact lifecycle (appendix)

```
Repeated an instruction by hand 2+ times
        → skill draft (via skill-creator)
        → trigger evals (should / should-not, near-misses)
        → functional eval with baseline (RED-GREEN)
        → production (.claude/skills/)
        → review cadence (this skill)
        → unused for N weeks → disable-model-invocation or deletion
```

Configuration is code. Code has tests, review, versioning, and death. So does
`.claude/`.
