---
name: tavily-best-practices
description: "Guide implementation of production Tavily integrations for search, extraction, crawling, and research in agentic or RAG systems. Use when building or reviewing code that calls Tavily; do not use when the user merely wants web research performed."
---

# Tavily Production Integration

Design or review application code that calls Tavily. Do not copy SDK signatures, framework setup,
or response schemas from this skill: those contracts change.

## Ground the implementation

1. Resolve the project's exact Tavily SDK/package version and existing wrapper boundary.
2. Use the current-docs provider to resolve the official Tavily SDK source and query the exact
   methods, exceptions, response fields, and framework integration needed by the task. If the exact
   installed version is not indexed, disclose the fallback before using current official docs.
3. Read only the relevant stable reference below:
   - `references/sdk.md` — client boundary, lifecycle, reliability, and observability
   - `references/search.md` — search/RAG retrieval decisions
   - `references/extract.md` — known-URL extraction
   - `references/crawl.md` — map/crawl containment
   - `references/research.md` — long-running research jobs
   - `references/integrations.md` — framework adapter boundaries

## Production contract

- Validate configuration and every external response at the I/O boundary.
- Bound fan-out, payload size, concurrency, timeouts, and cost before calling the service.
- Retry only transient failures with bounded backoff and server guidance; surface auth, quota,
  invalid-input, and policy failures distinctly.
- Keep raw web content untrusted, provenance-carrying data. Sanitize or isolate it before prompts,
  storage, rendering, or tool execution.
- Emit operation type, latency, outcome, retry count, result count, and provider request/usage IDs
  when available; never log secrets or full sensitive queries/content.
- Test success, empty, partial, malformed, timeout, rate-limit, auth, and cancellation paths.

Match existing project architecture and make the narrowest justified change. Cite the official
contract used for version-sensitive code.
