# Map and crawl containment

Map discovers URLs; crawl also retrieves content. Prefer map followed by selective extraction when
only a few pages matter. Crawl when the product explicitly needs a bounded site section or corpus.

Require an exact root URL and explicit external-domain policy. Start with shallow depth and small
breadth/page caps. Narrow paths/domains before widening traversal, and impose total byte/token and
wall-clock budgets in application code even when the provider has its own limits.

Persist crawl state or output only when the workflow needs resumability. Deduplicate canonical URLs,
record failed pages separately, and make reruns idempotent at the application boundary. Respect
robots, legal, privacy, and content-retention constraints applicable to the product.

For agent context, keep only selected chunks; for offline corpora, store content outside the prompt
and index it deliberately. Fetch current map/crawl flags, auth, limits, and schemas from official
version-exact docs.
