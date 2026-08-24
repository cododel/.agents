---
name: tavily-dynamic-search
description: "Run a programmatic Tavily search→filter→extract workflow with results isolated from the main context. Use for curated key details without raw-HTML noise (`найди и отфильтруй`). Do not use for plain result lists (`tavily-search`), known URLs, site crawling, or full research reports (`tavily-research`)."
---

# Tavily Dynamic Search

Use a programmatic search → triage → selective extraction workflow so raw result bodies remain in
a scratch data file or subprocess and only curated evidence enters the main context.

## Contract

1. Read `../tavily-cli/references/common.md` and `references/workflow.md`.
2. Search broadly enough to discover candidates, but print only bounded titles, URLs, scores, and
   short snippets for triage.
3. Select sources using task-specific evidence such as authority, date, domain, and relevance.
4. Extract only selected URLs and print bounded passages that support the requested claim.
5. Preserve source URLs and disclose failed or skipped sources. Remove scratch data only when it is
   agent-created and no longer needed; never place scratch code in the repository.

Use `tavily-search` when its compact result list is sufficient and `tavily-research` when Tavily
should perform the synthesis.
