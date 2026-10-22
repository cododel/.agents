# Acceptance profile

Use for complex algorithmic or business behavior whose correctness is not established by an ordinary
happy-path check. The output is evidence for agreed outcomes, not a substitute specification.

## Build scenarios from the guarantee

For a consequential operation, identify the caller and inputs, decision owner, durable fact, external
effect and permitted outcomes. Where concurrency exists, locate the point at which the decision
becomes effective. For important intermediate states, identify a reachable automatic or authorized
operator exit; an intentionally terminal state is not a recovery defect.

Select relevant disruptions: retries, competing decisions, boundary times, partial persistence,
unknown external outcomes, restart and cancellation. Use testing-evidence to establish the actual
failure phase and overlap. An internal recovery helper does not establish that the deployed entrypoint
can reach it. External delivery guarantees must account for what can actually be known after response loss.

Check combinations of rules as well as individual rules: priority with eligibility, rounding with
limits, expiry with reservation, or cancellation with a late result. Derive combinations from actual
dependencies and consequences; do not require a Cartesian product of every input.

## Algorithms and independent expectations

Choose a suitable oracle under testing-evidence. Useful options include a small reference solution,
exhaustive enumeration of small inputs, conservation/bounds properties, and input transformations
with an independently justified relation between outputs. Examples: reordering independent inputs
preserves a total; allocating value preserves the specified sum and per-item limits.

State the property’s assumptions. Monotonicity, order independence and uniqueness are not universal
requirements. A copied production formula is not an independent reference, and agreement between
two implementations may share a bug. Small-input proof does not establish large-input performance.

## Integration and acceptance boundary

Trace critical paths across consumers and owners, including valid rejected requests and UI/API
disagreements where relevant. Verify recovery through real registration/wiring and compatibility of
affected consumers, not only isolated functions. Assess capacity only against agreed profiles and
thresholds; report the environment and avoid extrapolating local measurements to production.

Apply the entrypoint's scoped conclusion rules. A bounded negative search supports only the scenarios
actually examined, even when they belong to a larger implementation task.
