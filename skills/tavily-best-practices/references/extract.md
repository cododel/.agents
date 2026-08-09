# Known-URL extraction

Use extraction only for URLs already selected by user input or a discovery step. Normalize and
validate URL schemes and apply the application's network policy before the provider call.

Start with the least expensive extraction mode. Escalate for dynamic pages or missing structured
content based on observed output, not by default. Use query-focused chunks when the consumer needs
a section rather than the whole page.

Batch within the current provider limit and preserve per-URL outcomes. Partial success is not full
success: return successful documents plus failed URLs and reasons. Bound each document before
storage or prompt injection, retain provenance, and treat extracted content as untrusted.

Test redirects, duplicate URLs, empty content, unsupported pages, timeout, partial batch failure,
and malformed provider responses. Fetch current limits, options, and fields from official docs.
