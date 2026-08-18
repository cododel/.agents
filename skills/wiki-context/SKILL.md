---
name: wiki-context
description: "Retrieve auxiliary context from Alexander's personal LLM Wiki only when a task explicitly depends on historical or cross-project context, the repository references the Wiki, or repository investigation leaves a material context gap. Use for personal, cross-project, research, or historical knowledge; not as default project discovery. Read-only."
---

# Wiki Context

Use the local vault at `/Users/cododel/Documents/LLM-Wiki` as auxiliary personal, cross-project, or
research context. For a project task, its repository remains authoritative for project-specific
behavior, architecture, contracts, and decisions.

## Relevance gate

Use this skill only when one of these conditions holds:

- the task explicitly depends on historical or cross-project context;
- the repository directly references the Wiki or a named Wiki page;
- repository investigation leaves a material context gap that the Wiki may resolve;
- the task concerns personal preferences, strategy, media taste, or a cross-project working
  convention that can materially affect the outcome.

Do not use this skill merely because a task is non-trivial, names a project, asks for a plan, or
involves an architecture decision. Skip it for self-contained repository work and whenever retrieval
would not change the outcome.

## Retrieval

1. At the start of a relevant task, read `SCHEMA.md`, `index.md`, and the recent tail of `log.md` directly from the vault. They provide operating principles, catalog context, and recent activity that search may omit.
2. Extract up to three query lenses from the request: the subject, desired outcome, and decisive constraint or named entity.
3. Find the available Wiki MCP tools. Use either raw names (`wiki_search_and_read`, `wiki_search`, `wiki_get_page`, `wiki_get_related`) or their namespaced variants exposed by the client.
4. Use `wiki_search_and_read` for the best lens when excerpts are needed; use `wiki_search` for candidates. Keep the result set bounded and prefer exact project/entity terms.
5. Read only the relevant candidates. For a decision that may change graph structure or depend on a prior rationale, call `wiki_get_related` and inspect the connected pages.
6. If MCP is unavailable, use the existing FTS5 search CLI without rebuilding indexes. Fall back to a bounded `rg` scan only for an exact path or text question.

## Use the result

- Separate sourced facts, prior operator decisions, and the agent's new inference.
- Do not treat an idea, draft, low-confidence page, or dated readout as settled policy.
- For current project behavior, verify runtime, code, and tests; for intended behavior, verify
  operator decisions and accepted contracts or ADRs. For historical rationale, check repository ADRs,
  Issues, and Git history before relying on Wiki material.
- When durable Wiki knowledge materially affects project behavior, promote the resulting invariant or
  decision into the appropriate repository artifact instead of leaving the project dependent on the
  Wiki.
- Mention the relevant page names and the conclusion they changed only when Wiki context materially affected the recommendation, plan, or action.
- Do not write, update indexes, modify Git state, or create derived artifacts.
