---
name: wiki-write
description: "Propose and deliver a source-grounded write to Alexander's personal LLM Wiki: capture material, create an idea, note, readout, draft, concept, entity, comparison, or query, or explicitly update an existing page. Use when the user asks to save, add, develop, or update Wiki knowledge. Requires exact scope confirmation before every write."
---

# Wiki Write

Work in `/Users/cododel/Documents/LLM-Wiki`. `AGENTS.md` and `SCHEMA.md` are the live contract; read them rather than copying their rules into this skill.

## Before proposing a write

1. Use `$wiki-context`, then inspect the relevant processed pages and raw sources. Search before creating a page; prefer an explicit update when the topic already exists.
2. Classify the content: raw source, dated evidence, early idea, note, draft, or durable knowledge. Do not store short-lived reference facts unless the schema explicitly treats the value as tracked knowledge.
3. Present the exact proposed scope: source material and assets, new or updated pages, meaningful backlinks, `index.md`, `log.md`, optional visibility override, validation, and the intended commit plus push to `origin/main`.
4. Wait for an explicit confirmation of that scope. A request to save material establishes intent but is not confirmation to create files, update shared navigation, commit, or push.

## After confirmation

1. Preserve source material first. For substantial input create the appropriate `raw/` source with all schema-required provenance, body-only SHA256, and `processed_to`; never silently rewrite a raw body. Use the schema's canonical inline source heading for short material.
2. Create or update only the approved processed page. Preserve existing wikilinks, distinguish source facts from synthesis, and set lifecycle or visibility metadata only when justified.
3. Search for related pages through MCP. Add at least two substantive outbound wikilinks where the page type requires them; add reverse links only when the relationship is real.
4. Update `index.md` and append the agreed concise `log.md` entry. Do not alter `SCHEMA.md` during ordinary ingest.
5. Run the existing `wiki_health.ts` and `wiki_lint.ts`, then refresh FTS5. Report pre-existing warnings separately from regressions introduced by this scope.

## Scoped delivery

Immediately before Git mutation, re-check the vault path, `main`, `HEAD`, `origin/main`, status, and approved path set. Stop on divergence or ambiguous upstream; never merge, rebase, reset, or absorb another person's changes.

- Stage only approved paths or explicit hunks in shared navigation; never use broad staging.
- Inspect the cached path set and run `git diff --cached --check`.
- Create one Conventional Commit such as `docs(wiki): record <topic>`.
- Push only that commit to `origin/main`. If the push fails, report the state and leave history intact.
