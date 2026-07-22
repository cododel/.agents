# Phase 0 — Inventory

Snapshot the current state *before* judging anything. The numbers taken here are
the baseline the post-audit state is compared against.

## Run the script

```bash
scripts/inventory.sh <config-dir>     # .claude or ~/.claude
```

It prints: structure, line counts of always-loaded files (project-root
`CLAUDE.md` and `CLAUDE.local.md` when auditing a project `.claude/` — usually
the largest always-loaded artifacts — plus `rules/`), per-skill SKILL.md sizes,
agent sizes, description byte weight (loaded into every session), git
last-modified dates per artifact, and the agents/hooks/commands roster.

## Inside a live session

`/context` shows the actual startup layout — what loads and how much it eats.
Record the numbers **before** the audit; compare after.

## Checklist

- [ ] Full skill list with a one-line purpose each
- [ ] Roster of agents, hooks, commands (legacy), workflows, rules
- [ ] Last-modified date per artifact (`git log -1 --format=%cs -- <path>`)
- [ ] What hasn't been used in the last month — triangulate three signals:
      typed invocations in `~/.claude/history.jsonl` (weak: captures typed
      mentions, not auto-triggers), session transcripts under
      `~/.claude/projects/*/*.jsonl` (stronger: auto-triggered Skill calls *are*
      visible there), and operator recall. Treat zero across all three as a
      question, not a verdict
- [ ] Uncommitted state (`git status`) — config drift that exists only on disk
      is config that can silently vanish

## Plugin context tax

Plugins ship their own skills and MCP tools; their descriptions load every
session exactly like local ones. Count them:

```bash
fd SKILL.md ~/.claude/plugins/cache --type f | wc -l
```

Duplicate plugin enablement (same plugin from two marketplaces in
`enabledPlugins`) duplicates every one of its skill descriptions — check
`settings.json` for the same plugin name under two `@marketplace` suffixes.
