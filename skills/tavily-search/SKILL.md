---
name: tavily-search
description: "Search with Tavily when explicitly requested, suitable native search is unavailable, evidence is insufficient, or an additional retrieval backend or Tavily-specific filter is needed. Ordinary find/look-up wording alone does not select Tavily."
---

# Tavily Search

Use `tvly search` for source discovery after the selection gate in
`../tavily-cli/references/common.md`. Identify the concrete retrieval need; ordinary search wording
alone is insufficient. No provider is a mandatory first choice for semantic discovery.

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
raw results. The agent performs synthesis; use `tavily-research` only for explicit user delegation
of synthesis to Tavily. Deduplicate underlying sources when combining providers.
