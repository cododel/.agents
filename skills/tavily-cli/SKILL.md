---
name: tavily-cli
description: "Coordinate multiple Tavily CLI operations when explicitly requested or selected for concrete retrieval needs. Combining generic search and reading does not select Tavily. Use specialized skills for single operations; Research requires explicit delegation."
---

# Tavily CLI

Coordinate two or more Tavily operations after the selection gate in `references/common.md`.
Combining search and reading is not by itself a reason to choose Tavily.

## Route

| Need | Command | Specialized skill |
|:--|:--|:--|
| Discover pages or current sources | `tvly search` | `tavily-search` |
| Extract one or more known URLs | `tvly extract` | `tavily-extract` |
| Discover site URLs without content | `tvly map` | `tavily-map` |
| Extract many pages from one site | `tvly crawl` | `tavily-crawl` |
| Explicitly delegate synthesis to Tavily | `tvly research` | `tavily-research` |
| Search, filter, and extract with raw data isolated | search + extract | `tavily-dynamic-search` |

Use the smallest sufficient sequence. Map before crawl when site scope is unknown; extract selected
URLs instead of crawling when only a few pages matter. For a single operation, stop and use its
specialized skill.

## Shared runtime contract

Read `references/common.md` before the first command. It owns installation, authentication,
structured output, current-help lookup, and error behavior for all Tavily CLI skills.

Return the requested artifact or synthesis with source URLs. Do not paste unbounded JSON or page
content into the conversation.
