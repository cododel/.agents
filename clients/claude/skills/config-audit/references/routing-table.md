# Phase 1 — Routing audit: every instruction in its right home

Run every piece of instruction through this table. Findings of this phase — the
"move from X to Y" list — are usually the highest-impact part of the whole audit.

| Knowledge type | Home | Context price | Misplacement symptom |
|---|---|---|---|
| Conventions/commands needed **every** session | `CLAUDE.md` | Permanent, every session | CLAUDE.md grew into a procedures document |
| Rules for specific paths/languages | `.claude/rules/*.md` (path-scoped) | Only when matching files are touched | Language guidelines bloat CLAUDE.md |
| Domain knowledge & "sometimes" procedures | `.claude/skills/<name>/SKILL.md` | Description always, body on demand | The same instruction gets pasted into chat by hand |
| Side-effect workflow, manual-only | Skill with `disable-model-invocation: true` | **Zero** until `/name` is typed | A deploy skill auto-fires when nobody asked |
| Action that must happen **always, no exceptions** | Hook (`settings.json`) | Zero (determinism outside context) | "ALWAYS run lint" lives in CLAUDE.md — and Claude sometimes forgets |
| Isolating noisy work (research, audit, review) | Subagent (`.claude/agents/*.md`) | Separate context window | Main session stuffed with grep dumps and logs |
| Access to external systems | MCP (`.mcp.json`) | Tool descriptions permanently | MCP server connected "just in case", unused |

## Distinguishing rules

- **CLAUDE.md holds facts and standing rules, not procedures.** Procedures → skills.
- **Advice → CLAUDE.md, guarantee → hook.** CLAUDE.md is advisory by nature. A
  rule that keeps being violated is not a reason to write it in caps — it's a
  reason to make it a `PreToolUse`/`PostToolUse` hook (exit code 2 blocks).
- **Skill vs subagent:** a skill runs in the current context, a subagent in an
  isolated one. If the task's intermediate output (logs, search, reading dozens
  of files) isn't needed in the main session — it's a subagent.
- **`commands/` is legacy.** Everything moves to `skills/` — a skill with
  `disable-model-invocation: true` plus `$ARGUMENTS` fully covers old commands.
- **A "global rule" that isn't path-scoped is CLAUDE.md content by another
  name** — and if it duplicates a skill description or MCP server instructions,
  the same guidance is being paid for two or three times every session. Keep
  exactly one always-on copy of any instruction.
