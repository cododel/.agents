---
name: tavily-search
description: "Run a quick Tavily web search returning ranked results, snippets, and metadata. Use for current facts, articles, sources, or `найди/поищи/look up` requests that need no deep synthesis. Do not use for known URLs, site-wide extraction, or detailed research reports."
allowed-tools: Bash(tvly *)
---

# Tavily Search

Use `tvly search` for source discovery or a bounded factual lookup when no URL is known.

1. Read `../tavily-cli/references/common.md` and run `tvly search --help`.
2. Turn the request into a concise search query; split materially different questions instead of
   building one long prompt.
3. Bound results, apply recency or domain filters only when the request justifies them, and request
   raw content only when it avoids a later extraction step.
4. Parse JSON into a compact list of title, URL, relevant snippet, and score/metadata needed for
   selection. Cite or return the source URLs.

```bash
tvly search "query" --max-results 5 --json
```

Use `tavily-extract` for selected full pages, `tavily-dynamic-search` when filtering must isolate
raw results, and `tavily-research` for a comprehensive synthesis.
