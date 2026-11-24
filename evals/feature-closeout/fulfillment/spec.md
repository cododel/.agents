# Deliver completed purchases

A checkout records an already-paid purchase with a render job ID and private destination. On a scheduled tick, dispatch the playable original for that job. A preview, a result for another job or a non-playable result cannot fulfill a purchase. The render provider exposes those properties in its result record.

A channel may be paused and later resumed. Every paid purchase remains eligible until dispatch succeeds. A temporary transport failure leaves it eligible on the next tick. Log the purchase ID for diagnosis on failure. A private asset URL must stay out of diagnostic output, including error paths.

This is a single-process sequential model. Each successful send is acknowledged synchronously. The channel gate may change between ticks. The provider's result is immutable during a tick. The scheduler passes the actual pending purchase object. No network, process-crash recovery, codec inspection or concurrent delivery is in scope.
