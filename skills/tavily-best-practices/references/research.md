# Long-running research jobs

Treat research as an asynchronous job even when the SDK offers a blocking convenience. Persist the
provider request ID with the local job, make polling resumable, and define terminal success, failure,
timeout, and cancellation states.

Bound the research question, expected dimensions, output schema, citation requirements, and maximum
wait before starting. Poll with bounded intervals and a deadline; avoid duplicate job creation on
client retries by using an application idempotency record.

Validate structured output and citations before publishing. Preserve provider citations and label
application inferences separately. Never present a timed-out, failed, or partial job as a completed
report.

Observe queue time, execution time, poll attempts, terminal state, usage, and abandoned jobs. Test
resume-after-restart, duplicate start, timeout, cancellation, malformed output, and missing sources.
Fetch current models, status values, methods, and response fields from official docs.
