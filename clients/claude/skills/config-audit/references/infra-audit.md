# Phase 4 — Agents, hooks, settings, MCP/plugins

## Agents (`.claude/agents/*.md`)

- [ ] Each has a minimally sufficient `tools` list (a reviewer must not have
      `Write`; a researcher needs `Read, Grep, Glob`)
- [ ] `model` chosen per task: rough work (search, data gathering) — cheap
      model; reasoning — the main one
- [ ] Description written for **delegation**: Claude must understand when to
      hand a task to this agent
- [ ] No agents duplicating skills: if context isolation isn't needed, it
      should be a skill

## Hooks (`settings.json` / `hooks/`)

- [ ] Every hook fires on a test run (manually run the scenario that should
      trigger it; for stdin-JSON hooks, pipe a fixture JSON through the script)
- [ ] Dangerous-operation guards are `PreToolUse` (deny via exit code 2), not
      text instructions
- [ ] Post-edit formatting/linting is `PostToolUse`, not a CLAUDE.md line
- [ ] `Stop` hooks gate completion where sessions run unattended (note: Claude
      Code overrides a Stop hook after 8 consecutive blocks — it is a *soft*
      gate, design unattended runs so they don't lean on it as a hard stop)
- [ ] Hook scripts are fast — a slow hook on every edit kills session tempo
- [ ] **Precedence**: as of this writing, settings `deny` rules win and `ask`
      rules prompt even when a PreToolUse hook returned "allow", so a hook can
      only auto-allow what no `ask` rule covers — but this interplay has shifted
      across releases. Verify the current deny/hook/ask precedence against the
      hooks + permissions docs at audit time (skills-audit §3.4: docs, not
      memory), then design hook+permissions together, not separately

## Settings

- [ ] `settings.json` (shared) vs `settings.local.json` (personal, gitignored)
      separation intact
- [ ] Permissions allowlist reflects real frequent commands; no overly broad
      grants (`Bash(*)` is a finding, always)
- [ ] Declared autonomy is executable: if prose grants the agent freedom in some
      zone (e.g. agent-owned worktrees) but an `ask` rule still prompts there,
      the prose is a dead letter — wire the exception as a hook or narrow the rule
- [ ] `skillOverrides` used to mute third-party (plugin) skills instead of
      editing their files
- [ ] Plugins: each enabled plugin earns its skill-description tax; the same
      plugin enabled from two marketplaces doubles it
- [ ] MCP servers: every connected server is actually used; unused ones
      disconnected (their tool descriptions are a permanent context tax)
