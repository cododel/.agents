---
name: tavily-dynamic-search
description: "Isolate raw retrieval output in an agent-controlled search, triage, and selective extraction pipeline when Tavily is explicitly requested or selected for a concrete capability or evidence gap. Generic curated-search wording alone does not select Tavily."
---

# Tavily Dynamic Search

Apply the provider-neutral retrieval procedure in `../../AGENTS.md`. This skill supplies the
Tavily-specific execution pattern only after Tavily passes the selection gate in
`../tavily-cli/references/common.md`. Search and extraction may use different suitable providers;
do not switch an already suitable discovery tool merely to run this pipeline.

## Contract

1. Read `../tavily-cli/references/common.md` and `references/workflow.md`.
2. Search broadly enough to discover candidates, but print only bounded titles, URLs, scores, and
   short snippets for triage.
3. Select sources using task-specific evidence such as authority, date, domain, and relevance.
4. Extract only selected URLs and print bounded passages that support the requested claim.
5. Preserve source URLs and disclose failed or skipped sources. Remove scratch data only when it is
   agent-created and no longer needed; never place scratch code in the repository.

Use `tavily-search` when its compact result list is sufficient. Use `tavily-research` only when
the user explicitly delegates synthesis to Tavily.
