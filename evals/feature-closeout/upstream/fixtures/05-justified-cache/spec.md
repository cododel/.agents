# Task: reduce calls to the public catalog service
- R1: Public catalog results may be reused for up to 60 seconds after each successful fetch. After 60 seconds they must be fetched again.
- R2: Two reads within that period through the same Catalog instance must reuse the cached result.
- R3: Do not cache errors. Catalog results are public and identical for all callers. Callers must not be able to mutate the cached result through a returned object.
- Approved decision: use an instance-local in-memory cache. The application owns one Catalog instance, uses sequential reads and supplies a monotonic clock; no cross-process, multi-instance, concurrent or persistent-cache guarantee is required.
