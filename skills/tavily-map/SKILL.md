---
name: tavily-map
description: "List URLs and site structure with Tavily without extracting page content. Use to find a page on a known domain, enumerate pages, or `построй карту сайта`. Do not use when page content is needed (`tavily-extract` or `tavily-crawl`)."
allowed-tools: Bash(tvly *)
---

# Tavily Map

Use `tvly map` to discover URLs on a known site without loading page content.

1. Read `../tavily-cli/references/common.md` and run `tvly map --help`.
2. Confirm authentication, the root URL, and whether external domains belong in scope.
3. Start with shallow, bounded discovery. Narrow by instructions or path/domain patterns before
   increasing depth or limit.
4. Return the relevant URL set and selection rationale; do not imply that page content was read.

```bash
tvly map "https://docs.example.com" --instructions "authentication docs" --json
```

Follow with `tavily-extract` for a few chosen pages or `tavily-crawl` for a bounded section.
