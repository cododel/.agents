# Discovery: trace invalid state to its origin

The failure frame is evidence of where a violated assumption became observable, not automatic proof
that this frame owns the defect. Trace the exact data/control path backward until a focused probe can
distinguish the proposed cause from plausible alternatives.

## 1. Anchor the symptom precisely

Extract:

- exact error type/message and command/environment;
- deepest relevant application frame;
- exact expression/value that violated an expectation;
- expected shape/state versus observed shape/state;
- whether the failure is deterministic, input-dependent, timing-dependent, or environment-dependent.

Do not ask for information that the supplied artifact, repository, local logs, or a safe focused probe
can establish. Ask only for an exact missing artifact/input when no repository-local observation can
resolve it.

Prefer independent local diagnosis when the tools can exercise the reported conditions. A successful
run establishes what worked in that configuration. If the reported failure persists elsewhere,
consider both environment differences and an incorrect hypothesis. When an observation on the
operator's device could distinguish them, you may offer an interactive session. Explain what to
observe and which predictions differ. Start the session only if the operator explicitly agrees.

## 2. Find producers, boundaries, and mutations

Search for the value's creation, assignments, transformations, boundary crossings, and consumers
rather than reading from an entrypoint breadth-first. Adapt searches to the language:

```bash
rg -n -- '\b<symbol>\s*[:=]' <relevant-scope>
rg -n -- '\b<failing_fn>\s*\(' <relevant-scope>
rg -n -- 'parse|deserialize|json|request|env|getenv|database|cache|queue' <relevant-scope>
```

Common origin classes:

1. unvalidated I/O boundary or schema/version mismatch;
2. optional/default value treated as guaranteed;
3. branch, retry, or error path that skips initialization/cleanup;
4. later mutation, stale cache/state, or ownership race;
5. lifecycle/order mismatch across async, event, request, or resource boundaries;
6. environment/configuration divergence rather than product-code defect.

Treat these as search hypotheses, not probabilities or diagnoses.

## 3. Widen only along evidence edges

Start at the failing module, then follow proven callers, producers, event/schema edges, configuration,
persistence, and lifecycle ownership. Verify every decisive edge in source.

Follow the path to the component responsible for the violated guarantee. For duplicate orders,
two clicks can explain two requests. Reproduce what happens when the order boundary receives
both, and inspect transaction or balance handling if it participates in that path. Distinguish a
confirmed defect from a related risk. Report independent risks and propose a separate check.

When hypotheses diverge or the causal chain becomes unclear, summarize privately:

- observations established;
- current hypotheses and what each predicts;
- the next repository-local observation that would falsify or separate them;
- whether the next step remains local/reversible and proportionate.

Continue autonomously when a focused local observation is likely decisive. Stop to ask only when the
remaining branch requires unavailable operator input, a material product/architecture choice,
external/shared mutation, credentials, or disproportionate exploration with no falsifiable next step.
Do not use a fixed number of widening rounds or file reads as a stop condition.

## 4. Use history selectively

`git blame`, `git log -L`, and `git log -S` can explain when an assumption or boundary changed. Use
history after narrowing a relevant symbol/path; recent adjacency is a lead, not causal proof.

## 5. Confirm the causal claim

Before calling a root cause proven, connect:

1. origin or violated ownership boundary;
2. transformation/control path;
3. failing assumption;
4. focused probe/reproduction whose result changes as the cause predicts.

A symptom, correlation or isolated reproduction alone does not establish the path from the
proposed cause to the observed failure. For a deep diagnosis, reproduce the failure where it
occurs and vary the suspected cause to check its prediction against plausible alternatives.
If that observation is unavailable, identify the unverified link. Match the stopping point to
the task: a device-specific rendering condition verified on the affected device may explain how
to make a site work across platforms. For a rendering-engine investigation, that same condition
is the reproduction case. Trace the engine mechanism. Continue to a lower layer when it could
change the explanation requested, the correct repair, or its safety.

A patch that merely makes the symptom disappear is insufficient. Check that it does not suppress the
error, broaden a catch/default, weaken validation/types, leak resources, or leave another consumer on
the same invalid path. When one link remains uncertain, label the cause a hypothesis and state the
single next falsifying observation.
