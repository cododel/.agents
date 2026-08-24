---
name: tavily-extract
description: "Extract clean text or Markdown from up to 20 known URLs with Tavily, including JavaScript-rendered pages and query-focused chunks. Use when the user supplies URLs or asks `прочитай/вытащи текст по ссылке`. Do not use to discover URLs or crawl a site."
---

# Tavily Extract

Use `tvly extract` only when one or more target URLs are already known.

1. Read `../tavily-cli/references/common.md` and run `tvly extract --help`.
2. Verify and quote every URL. Batch within the current CLI limit.
3. Start with basic Markdown extraction. Use query-focused chunks when only part of a page matters;
   increase extraction depth only when basic output misses dynamic content.
4. Return or save only the requested content. Report failed URLs separately from successful ones.

```bash
tvly extract "https://example.com/page" --format markdown --json
```

Use `tavily-search` when URLs are unknown and `tavily-crawl` when many pages from one site are
required.
