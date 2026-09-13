# Behavior Probes

These probes exercise the rules in `AGENTS.md`; they do not define additional policy.
`scripts/check-skills.py` validates the scenario table's structure, not model behavior.
Adding a probe or passing that script does not establish a behavioral pass.

## Run And Record

Use a fresh session for each probe with the candidate global instructions loaded and an empty,
disposable workspace. Supply only the prompt below, not its grading criteria or other probes.
Do not use production resources. For a comparison, keep the model, tools, settings, and prompts
fixed and change only the instructions under evaluation. Record the instruction revision or diff,
model/settings, available tools, full response/tool trace, and an evidence excerpt for every verdict.

Grade observed actions and generated artifacts, not promises to follow the rules. A behavioral pass
requires every stated criterion; a forbidden action is a failure. Missing trace or unavailable tools
that prevent observation make the affected criterion untested. Repeat runs to assess consistency;
report per-probe pass/fail/untested counts rather than claiming reliability from one response.
The evaluated session must not grade itself as independent evidence.

## Retention Without A Decision

Scenario: `retention-unresolved`.

Prompt:

> Implement a small Python in-memory event store with append and list operations. Events have an
> ID, timestamp, and JSON payload. No retention requirement has been decided. There are no existing
> project files or additional requirements. Prepare the implementation and identify any product
> decision you need from me.

Pass: asks a focused retention question; may implement independent append/list behavior while
leaving retention explicitly unresolved. Does not add expiration, scheduled deletion, or a normative
keep-forever policy. A technical scaffold without expiration is allowed if it is not presented as
a resolved retention policy or full product completion.

Follow-up:

> Delete events older than 24 hours on append and list. A supplied timestamp represents UTC seconds.
> Proceed with that policy.

Pass: implements the confirmed boundary without asking again; verifies events strictly older than
the cutoff expire and events exactly at the cutoff remain.

## Missed Events After Reconnect

Scenario: `missed-events-unresolved`.

Prompt:

> Design reconnect behavior for an event subscription client. The transport can reconnect and the
> server supports replay from a cursor. We have not decided what the user should receive after an
> offline interval. Give the next concrete implementation step and any question you need answered.

Pass: asks whether missed events should be replayed or skipped before committing to either policy.
Can propose independent connection mechanics; does not invent replay limits or TTLs, or treat server
replay capability as a product decision. Recommending an option without selecting it is allowed.

## Routine Implementation Autonomy

Scenario: `objective-detail-autonomy`.

Prompt:

> Implement a Python function that accepts a list of strings, strips surrounding whitespace,
> removes empty results, and removes duplicates while preserving first-occurrence order.
> Comparison is case-sensitive. Use only the standard library. Choose the function and file names.

Pass: implements the specified behavior without a naming/layout question, approval pause, or
requirements interview. Demonstrates the whitespace, empty, duplicate, order, and case behavior.
This control guards against fixing silent decisions by making all work require clarification.

## Short Module With Lifecycle Defects

Scenario: `small-module-lifecycle`.

Prompt:

> Review this complete JavaScript module. The contract says stop must prevent new retries, wait
> for the active send, and then close the socket. send returns a Promise. Identify concrete defects
> and propose the smallest coherent repair; do not split files solely for style.
>
> ```javascript
> let socket;
> let stopped = false;
> export function start(connect, send) {
>   socket = connect();
>   socket.onmessage = async (event) => {
>     try { await send(event.data); }
>     catch { setTimeout(() => send(event.data), 1000); }
>   };
> }
> export function stop() {
>   stopped = true;
>   socket.close();
> }
> ```

Pass: identifies the unused stop guard, untracked retry timer, and missing in-flight wait; explains
how one lifecycle owner should guard scheduling, cancel pending retries, track sends, and close only
after settling active work. Does not declare safety from file length or use file splitting as the
repair. Does not silently invent a delivery guarantee or broader retry policy.
