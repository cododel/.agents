---
name: tavily-cli
description: "Route Tavily CLI tasks that explicitly request multi-operation orchestration across search, extract, map, crawl, and research. Use only when the user names `tavily-cli` or combines operations; use the specialized Tavily skill for a single operation. Never use for local files, Git, deployments, or code editing."
---

# Tavily CLI

Coordinate two or more Tavily operations while preserving each specialized command's boundary.

## Route

| Need | Command | Specialized skill |
|:--|:--|:--|
| Discover pages or current sources | `tvly search` | `tavily-search` |
| Extract one or more known URLs | `tvly extract` | `tavily-extract` |
| Discover site URLs without content | `tvly map` | `tavily-map` |
| Extract many pages from one site | `tvly crawl` | `tavily-crawl` |
| Produce a cited multi-source synthesis | `tvly research` | `tavily-research` |
| Search, filter, and extract with raw data isolated | search + extract | `tavily-dynamic-search` |

Use the smallest sufficient sequence. Map before crawl when site scope is unknown; extract selected
URLs instead of crawling when only a few pages matter. For a single operation, stop and use its
specialized skill.

## Shared runtime contract

Read `references/common.md` before the first command. It owns installation, authentication,
structured output, current-help lookup, and error behavior for all Tavily CLI skills.

Return the requested artifact or synthesis with source URLs. Do not paste unbounded JSON or page
content into the conversation.
