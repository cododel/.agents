# Task: introduce a read-only order summary service
- R1: List orders for the caller's tenant only, sorted by order ID.
- R2: For each order, show its ID, currency and total in cents (sum of quantity × unit_price_cents).
- R3: Include the count of returned orders and the sum per currency; never combine different currencies.
- R4: An empty tenant returns zero orders, no summaries and an empty per-currency map.
- R5: Do not write to the order store or add external services or dependencies.
This fixture defines single-process, trusted input records with valid integer amounts and tenant IDs. The caller's tenant ID is already authenticated by the host. No new authentication, DB, concurrency or external integration is in scope.
