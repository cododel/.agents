# Shared Agent Configuration

This directory is the canonical source for personal cross-client instructions and Agent Skills.

## Canonical Sources

- `AGENTS.md` contains client-neutral personal instructions.
- `skills/<name>/SKILL.md` contains portable workflows and their resources.
- `clients/<client>/skills/` contains client-only skill sources that are linked into the
  client's required discovery path but are not advertised globally.

## Client Adapters

- Claude Code: `~/.claude/CLAUDE.md` imports the canonical instructions; portable skills and the
  Claude-only `clients/claude/skills/config-audit` are linked under `~/.claude/skills/`.
- OpenCode: `~/.config/opencode/opencode.json` loads the canonical instructions; skills are
  discovered natively from this directory.
- Codex: `~/.codex/AGENTS.md` links to the canonical instructions; skills are discovered natively.
- Gemini CLI: `~/.gemini/GEMINI.md` links to the canonical instructions; skills are discovered
  natively from this directory.
- Antigravity: skills are discovered natively from this directory; global instructions arrive
  through `~/.gemini/GEMINI.md`.
- Grok: `~/.grok/AGENTS.md` links to the canonical instructions; skills are discovered natively.
- Cursor: skills are discovered natively. Global User Rules have no documented file adapter and
  must be synchronized through Cursor's Customize UI if desired.
- Kimi: skills are discovered natively from this directory. An empty `~/.kimi/skills/` plus
  `merge_all_available_skills = false` prevents fallback duplicates from other brand roots.
  The installed client has no true global instruction file.

Do not copy app-managed plugins, bundled skills, credentials, caches, histories, or runtime
databases into this tree.
