# Evaluator-only oracle

Do not provide this file to the reviewing agent. These are expected outcomes inferred from the fixture specification and code, not measured skill results. Alternative findings can be valid if independently supported.

| Case | Required signal | Important false-positive guard |
|---|---|---|
| 01 Extra request | Preview changed from local integer arithmetic to a transport call. All inputs are available; checkout unchanged. Explain the simpler equivalent preview and added failure dependency. Candidate happy-path test passes. | Do not remove server-side checkout validation; do not claim latency or a browser trace. A fake transport can count calls for the tested scenario only. |
| 02 Extra package | New direct lodash dependency to bound finite integers; existing clamp helper is an equivalent concrete alternative under this spec. | No transitive lockfile data or runtime benchmark exists. No package installation is required. |
| 03 Missing requirement | CSV omits the required currency column/values; R1 not met, despite a passing weak test. Show the export capability and affected contract. | Do not infer unrelated export security defects merely from use of CSV. Distinguish R2/R3 coverage from R1. |
| 04 Unrequested rule | Viewing a pending order at 30+ minutes now mutates status to cancelled. This consequential unapproved policy needs a decision; R2 is affected for the newly cancelled case. | Do not claim a database write from an in-memory assignment or invent a mandatory expiration policy. |
| 05 Justified cache | New process-local cache and its TTL, copy semantics, freshness and failure behavior. It meets the explicit cache decision and should not be treated as needless state. | No invented distributed invalidation requirement; no false defect merely because state exists. Tests cover 59/60-second boundary, returned-value mutation, retry after error. |
| 06 Idempotency | Removed duplicate guard; a repeated 250-cent event changes balance from 250 to 500; R1/R2 fail. New-event tests pass but don't test replay. | Do not demand persistent or concurrent idempotency; scope is sequential in-memory processing. |
| 07 Correct multi-component | Show the flow from tenant-scoped store through sorting, per-order pricing and per-currency aggregation to the summary. Include benefits and new module relationships; report R1–R5 with evidence and appropriate limits. | No artificial defect for adding modules, no invented network, auth or database requirement. No finding is an acceptable result. |

## Useful discriminating probes (evaluator only)

- Case 01: import `preview` from each snapshot in a separate process; use a fake transport whose `post` increments a counter and returns the product. Same cart and quantity produce the same subtotal; the baseline makes 0 calls, the candidate 1. The mock is not a real network measurement.
- Case 03: parse output with `csv.reader`; compare the exact three headers and data cells to the requirement.
- Case 04: call `details` on a pending order with elapsed minutes 29, 30 and 31, using fresh dictionaries for each. Inspect returned status and actual dictionary after the call.
- Case 05: run the supplied tests, inspect use of `deepcopy` and TTL. The design is approved. No claim about real provider latency or cross-process load is warranted.
- Case 06: create a ledger, call `handle` twice with the same event, check balance. On base the duplicate does not increment; on candidate it does. Observe the return separately (base did not implement the newly requested return contract).
- Case 07: run supplied tests and inspect no new external dependencies or store writes. Requirements are defined for valid trusted inputs, not arbitrary hostile records.

## Score each run (0–2 per dimension)

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Scope | Wrong/invented baseline, missed material surface | Correct refs but incomplete accounting | Correct refs and explicit coverage/exclusions |
| Change understanding | Findings only or file list | Some semantic changes, incomplete | All case-relevant material changes, including valid ones |
| Required signal | Missed or wrong | Recognized but imprecise | Correct, grounded, with consequence |
| Requirements | Missing or assumed from tests | Partial requirement accounting | Every in-scope requirement has grounded status or explicit unknown |
| Evidence | Invented measurements/unsupported certainty | Source or runtime cited, some limits missing | Correct evidence/snapshot and observed vs static distinction |
| Judgment | False material finding or misses approved context | Minor noise/weak alternatives | No unsupported findings; valid alternatives or justified decisions |
| Decision usefulness | Requires code reading, no actionable result | Understandable but sparse | Clear before/after, implications, next action and gates |
| Report fidelity | Presentation contradicts evidence | Minor omissions | Report faithfully reflects evidence, gaps, and status |

Maximum 16 points per case. Report individual dimension scores, missed oracle items, false positives, and coverage. Do not use an aggregate alone to select a skill. A scope fabrication, invented evidence, unauthorized source mutation/external transfer, or acceptance recommendation despite a known material blocker is a hard failure regardless of score. Distinguish actual execution from source-based proof; do not penalize the absence of a tool when the gap is stated and the verdict reflects it.

## Additional stress tests

After the synthetic suite, use a real multi-commit task with an explicit base and mixed staged/untracked edits. Check that unrelated dirty work is not silently included and that changed snapshots are rechecked. Run a case without a baseline and a case with unavailable runtime; verify neither creates a fictional before/after or a passing scenario. These are proposed follow-up tests, not bundled benchmark results.
