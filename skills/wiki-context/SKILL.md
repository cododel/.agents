---
name: wiki-context
description: "Retrieve relevant context from Alexander's personal LLM Wiki before a non-trivial recommendation, plan, research task, architecture decision, or work on an ongoing project when prior principles, ideas, preferences, ADRs, or decisions could change the outcome. Use for implicit personal-Wiki context, not only when the user explicitly mentions the Wiki. Read-only."
---

# Wiki Context

Use the local vault at `/Users/cododel/Documents/LLM-Wiki` as personal context. It is evidence and prior decisions, not authority that overrides the current user request.

## Relevance gate

Use this skill before a non-trivial answer when any of these can materially affect it:

- a personal preference, strategy, media taste, or working convention;
- a named project, system, product idea, technology choice, or prior decision;
- a plan, comparison, recommendation, design, or research question with meaningful trade-offs.

Skip it for simple facts, translation, formatting, a clearly self-contained local edit, or when retrieval would not change the answer.

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
- Mention the relevant page names and the conclusion they changed only when Wiki context materially affected the recommendation, plan, or action.
- Do not write, update indexes, modify Git state, or create derived artifacts.
