---
name: tavily-research
description: "Produce a comprehensive multi-source Tavily research report with citations. Use for in-depth investigation, comparisons, market analysis, literature reviews, `исследуй`, or `сравни`. Do not use for quick source discovery (`tavily-search`) or search/filter/extract workflows (`tavily-dynamic-search`)."
allowed-tools: Bash(tvly *)
---

# Tavily Research

Use Tavily research for a substantive multi-source synthesis, not a quick lookup.

1. Read `../tavily-cli/references/common.md` and run `tvly research run --help`.
2. Frame a bounded research question with the requested comparison dimensions and output needs.
3. Choose the current model/stream/structured-output options from CLI help. For asynchronous work,
   retain the request ID and use the documented `status` or `poll` subcommand.
4. Verify completion, preserve citations, and distinguish the generated synthesis from your own
   inferences. Report timeout or failed status instead of presenting partial output as complete.

```bash
tvly research run "research question" --json
```

Use `tavily-search` for a source list and `tavily-dynamic-search` for an agent-controlled
search/filter/extract pipeline.
