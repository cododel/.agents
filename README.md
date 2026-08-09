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

## External Skill Provenance

- `find-skills` is externally managed by `.skill-lock.json`. Update it through the installer that
  owns the lock entry; do not hand-edit the installed skill.
- `graphify` is a vendor snapshot from the installed `graphifyy` package. Its pinned source version
  is recorded in `skills/graphify/.graphify_version`; the `SKILL.md` body and every file under
  `references/` mirror that version. The local frontmatter `description` is intentionally narrower
  and is the only trigger override.
- Tavily skills are locally maintained routing and production wrappers. CLI flags come from
  `tvly <command> --help`; SDK signatures, response schemas, and framework integrations come from
  current official documentation rather than copied references.

To review a Graphify update:

1. Upgrade or install the intended `graphifyy` version in an isolated tool environment and record
   `graphify --version` in `skills/graphify/.graphify_version`.
2. Locate that environment's `site-packages/graphify/` directory. Diff its `skill-agents.md`
   against `skills/graphify/SKILL.md`, allowing only the documented `description` override, and run
   a recursive diff between its `skills/agents/references/` and
   `skills/graphify/references/` directories.
3. Copy reviewed vendor changes as one versioned snapshot, reapply only the trigger override, then
   run the repository skill validator and client discovery smoke tests. Never edit an installed
   package or client cache as the source of truth.
