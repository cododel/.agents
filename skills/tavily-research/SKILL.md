---
name: tavily-research
description: "Delegate a bounded cited research report to Tavily only when the user explicitly requests Tavily Research or delegation of synthesis to Tavily. Generic research/compare requests and unavailable native search do not trigger this skill."
---

# Tavily Research

Use Tavily Research only when the user explicitly delegates synthesis to Tavily, including a
named comparative research run. A generic request to investigate/compare or to search via Tavily
is insufficient. Missing native search does not authorize delegation; use a suitable retrieval
provider and retain agent-controlled analysis.

1. Read `../tavily-cli/references/common.md` and run `tvly research run --help`.
2. Frame a bounded research question with the requested comparison dimensions and output needs.
3. Choose the current model/stream/structured-output options from CLI help. For asynchronous work,
   retain the request ID and use the documented `status` or `poll` subcommand.
4. Verify completion, preserve citations, and distinguish the generated synthesis from your own
   inferences. Report timeout or failed status instead of presenting partial output as complete.
5. Check key claims against the cited sources before adopting them in the final answer. Preserve
   disagreements and unverifiable claims; a completed report does not establish its correctness.

```bash
tvly research run "research question" --json
```

Use `tavily-search` for a source list and `tavily-dynamic-search` for an agent-controlled
search/filter/extract pipeline.
