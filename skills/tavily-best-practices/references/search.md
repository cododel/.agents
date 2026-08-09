# Search and RAG retrieval

Make the query express one information need. Split unrelated questions and merge results with URL
deduplication. Use domain/recency constraints only when product semantics require them; an
allowlist improves authority but can reduce recall.

Choose search depth and result count from an explicit latency, cost, and recall budget. Start with
the cheaper bounded mode, then escalate only when measured quality is insufficient. Do not request
answers, images, or raw content unless the consumer uses them.

For RAG, retain title, canonical URL, retrieval timestamp, score, and the exact excerpt passed to
the model. Treat score as ranking evidence, not truth. Apply application-level authority and
freshness rules, deduplicate, then cap sources and characters/tokens per source before prompting.

Handle empty results as a normal outcome. Distinguish it from provider failure and avoid fabricating
an answer. Fetch current search parameters and response fields from official version-exact docs.
