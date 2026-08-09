# Isolated search and extraction patterns

Use Python standard library or `jq` to keep raw Tavily JSON outside the main context. The exact
fields and flags come from the installed CLI help, not this reference.

## Single-pass pattern

Run `tvly search ... --json` as a subprocess or pipe, parse JSON, and print only a bounded triage
record per result: index, title, URL, score, and a short snippet. Do not print `raw_content`.

## Multi-pass pattern

1. Save search JSON as task-scoped scratch data in the OS temporary directory.
2. Print a compact triage view.
3. Choose source indices from that view; do not assume rank alone proves authority.
4. Call `tvly extract` only for chosen URLs.
5. Filter extracted Markdown by headings, paragraphs, code blocks, dates, or domain-specific terms;
   print enough surrounding context to avoid misleading fragments.

Use deterministic bounds for sources and output. Deduplicate by canonical URL when combining
queries. Catch command failures and malformed JSON explicitly; do not turn an empty/partial result
into a successful answer. Keep scratch data separate from scratch code: a short one-off parser may
run inline, while reusable code belongs in an established project script only when requested.
