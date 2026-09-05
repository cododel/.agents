---
name: tavily-extract
description: "Extract known URLs with Tavily for batch Markdown/text, difficult pages, or an explicit Tavily request. Prefer suitable native reading for ordinary single-page requests; a supplied URL alone does not select Tavily. Not site discovery or crawling."
---

# Tavily Extract

Use `tvly extract` for known URLs when requested explicitly or when batch output or extraction
needs justify it. Suitable native reading is preferred for an ordinary page. Apply the selection
gate in `../tavily-cli/references/common.md`; batch extraction needs no prior failed native call.

1. Read `../tavily-cli/references/common.md` and run `tvly extract --help`.
2. Verify and quote every URL. Batch within the current CLI limit.
3. Start with basic Markdown extraction. Use query-focused chunks when only part of a page matters;
   increase extraction depth only when basic output misses dynamic content.
4. Return or save only the requested content. Report failed URLs separately from successful ones.

```bash
tvly extract "https://example.com/page" --format markdown --json
```

Discover unknown URLs with a suitable search tool; use `tavily-search` when its gate applies.
Use `tavily-crawl` when many pages from one site are required.
