# Closed-Issue ADR candidate criteria

Use this only for explicit `from-issue` promotion. The question is not whether an Issue sounds
architectural; it is whether the surviving evidence proves a significant **operator-made decision**
with enough rationale to record honestly.

## Evidence context

- **Same-session evidence:** the current conversation may supplement the Issue when it explicitly
  contains the operator's choice, alternatives/constraint, and rationale. Record document/date
  provenance without pretending the chat is durable by itself.
- **Cold audit:** the Issue and linked durable sources must carry the decision evidence. Do not infer
  history from implementation shape, filename, dependency choice, commit adjacency, or model memory.

When uncertain, use the cold-audit bar.

## Verdicts

### `promote`

All are true:

1. evidence proves the operator chose or explicitly proposed a path;
2. the choice passes the significance gate in `adr-spec.md`;
3. at least one real alternative or a concrete mandatory constraint is known;
4. selection/rejection rationale is specific enough to preserve without invention;
5. the decision is not already owned by an equivalent live ADR.

Sparse formatting is acceptable; missing load-bearing rationale is not. An `Accepted` ADR may not use
`TODO:` as a substitute for the decision, alternatives/constraint, or rationale.

### `skip`

Use when the record is only:

- a bug fix, incident action, cleanup, routine dependency bump, CI/config tweak, or one-off script;
- current behavior, responsibility, invariant, or policy without a preserved decision fork;
- an implementation detail that is cheap/reversible or already mandated by a living convention;
- a topic that appears architectural only from its filename or affected files.

Route non-obvious current-state semantics to `$contract-writer` when they have durable value.

### `ambiguous`

Use when evidence suggests a real significant decision but lacks one load-bearing historical fact,
such as who selected the path, what alternative/constraint existed, or why it was selected. Ask one
compact operator question for that fact. Do not create an Accepted ADR until it is resolved; create a
`Proposed` record only when the operator explicitly requests a pending decision document.

### `merge`

Several Issues may feed one ADR only when they are evidence for **one independently supersedable
choice**. Shared files, dates, tags, or words are discovery leads, never grouping proof. Merge when:

- each source concerns the same decision outcome;
- their contexts/alternatives/consequences are complementary rather than contradictory;
- splitting would duplicate the same rationale;
- one future successor could replace the whole choice coherently.

Otherwise keep separate candidates or mark the relationship ambiguous.

## Classification output

For each source return:

- `path`;
- `verdict`: `promote | skip | ambiguous | merge`;
- one-sentence evidence-grounded reason;
- selected decision and rationale source pointers;
- proposed ADR owner/path when unambiguous;
- missing material fact, if any.

False-positive ADRs create permanent historical fiction. Prefer a precise `skip` or `ambiguous` over
an architectural-looking document whose rationale was reconstructed by the agent.
