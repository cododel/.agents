# SDK boundary and reliability

Keep one application-owned adapter between domain code and the Tavily SDK. Accept a typed request,
return a validated domain result, and translate provider exceptions into a small stable local error
taxonomy. This prevents SDK field or exception drift from spreading across the codebase.

Use a long-lived client according to current official lifecycle guidance. Prefer the async client
for concurrent I/O, close it deterministically, and propagate cancellation. Bound concurrency with
a semaphore or worker pool rather than launching one request per input without a cap.

Set explicit per-operation timeouts based on product latency budgets. Retry only transport errors,
timeouts, and rate limits when the current exception/status contract marks them transient. Use
bounded exponential backoff with jitter and server retry hints. Do not retry invalid input, auth,
forbidden, exhausted quota, or deterministic empty results.

Record metrics at the adapter: endpoint, latency, status/error class, attempts, requested and
returned counts, and usage/request identifiers when the current response provides them. Redact API
keys, user secrets, and raw content. Validate response shape before domain code consumes it.

Test with a fake adapter or recorded contract fixture owned by the project; keep a small opt-in live
smoke for provider compatibility when appropriate. Fetch current SDK methods and exceptions before
writing code.
