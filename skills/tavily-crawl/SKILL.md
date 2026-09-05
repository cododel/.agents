---
name: tavily-crawl
description: "Crawl and extract many pages from one site with Tavily. Use for `crawl`, `скачай документацию`, entire docs sections, bulk page extraction, or saving a site as local Markdown. Do not use for one/few known URLs (`tavily-extract`) or URL-only discovery (`tavily-map`)."
---

# Tavily Crawl

Use `tvly crawl` for bounded multi-page extraction from one site.

1. Apply the selection gate and runtime contract in `../tavily-cli/references/common.md`, then
   run `tvly crawl --help`.
2. Confirm authentication, root URL, path/domain scope, and whether output is context for reasoning
   or a requested local corpus.
3. Start shallow with a small page limit. Use instructions and per-source chunks for agent context;
   use `--output-dir` for an explicitly requested full-page download.
4. Inspect partial failures and stop before widening depth, breadth, or external-domain scope.

```bash
tvly crawl "https://docs.example.com" --instructions "API authentication" --limit 20 --json
```

Use `tavily-map` first when the site structure is unknown and `tavily-extract` when only a few URLs
are needed.
