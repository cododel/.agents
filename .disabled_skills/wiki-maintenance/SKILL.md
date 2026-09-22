---
name: wiki-maintenance
description: "Diagnose and repair a confirmed, scoped structural issue in Alexander's personal LLM Wiki, including wikilinks, frontmatter, tags, sources, index coverage, log entries, or safe migrations. Use when the user asks to fix, repair, migrate, or clean a specific Wiki defect. Requires a read-only inventory and exact approval before mutation."
---

# Wiki Maintenance

Operate on `/Users/cododel/Documents/LLM-Wiki`. Follow its `AGENTS.md` and `SCHEMA.md`; use `$wiki-context` when the issue may depend on an existing decision or a related page.

## Diagnose first

1. Capture vault Git status and identify the exact problem through the existing health, lint, MCP, and source-aware resolver surfaces.
2. Inventory all matches and classify active references separately from immutable raw sources, archived material, dated readouts, and historical logs.
3. Decide whether the issue is a typo, ambiguity, semantic link change, frontmatter/schema violation, index gap, orphan, or a requested migration. Do not replace links mechanically just to remove a warning.
4. Propose the precise transformation, file set, validation, and direct `origin/main` delivery. Call out dirty or untracked files that remain excluded.

## Approval and repair

Wait for exact approval before editing. A migration, deletion, raw-source change, schema change, or archival action needs its own explicit scope; never infer it from a generic request to clean the Wiki.

- Preserve raw bodies, historical evidence, and existing semantic links unless their approved meaning changes.
- Do not invent directory-to-README shortcuts or weaken the shared resolver to silence ambiguities.
- Modify `SCHEMA.md` only when the user explicitly changes the Wiki contract; log its rationale separately.
- Keep the repair narrow. Record normal navigation and history changes only when they are part of the approved scope.

## Verify and deliver

Run the affected focused checks followed by `wiki_health.ts` and `wiki_lint.ts`. Distinguish existing warnings from new defects. Before staging, verify vault, `main`, `HEAD`, `origin/main`, status, and the exact approved diff.

Stage only approved files or hunks, run `git diff --cached --check`, create one Conventional Commit, and push it to `origin/main`. On divergence, a failed push, or unexpected files in the cached diff, stop without merge, rebase, reset, or broad cleanup.
