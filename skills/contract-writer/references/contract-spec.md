# Living contract specification

## Identity

A living contract is lightweight normative current-state documentation for a stable boundary. It says
what a product/UI/API/domain/persistence/security/module/architecture surface guarantees, owns, does
not own, or requires implementations to preserve now. It changes in place when current behavior
changes.

A contract is not:

- an ADR with dated alternatives, rationale, and immutable decision history;
- a feature brief or plan for one implementation;
- an Issue for deferred work;
- a test, schema, or type merely because it checks or constrains one example;
- a complete specification of existing code;
- an index/README that only routes to the owner.

## Value test

A contract earns its maintenance cost when the rule is stable and at least one is true:

- responsibility or exclusion is non-obvious from local code;
- behavior spans several components, event hops, or lifecycle phases;
- future edits can pass local tests while violating the semantic intent;
- compatibility, ordering, idempotency, failure, security, or ownership semantics matter;
- the project already treats the surface as a documented contract.

Do not retroactively specify an entire legacy project. Document touched or discovered behavior when
its drift risk is concrete. A concise contract for one stable boundary is preferable to a feature-by-
feature documentation layer.

## Ownership and overlap

Keep one normative owner per rule. Split by stable responsibility, not by every feature or file. When
a rule touches several surfaces, choose the primary owner and link from the others.

Project instructions may declare an executable schema/API/type/test canonical for a bounded
interface. That declaration does not make it the owner of adjacent business, UI, or architecture
semantics.

## Required content

Include only material sections:

- scope and responsible boundary;
- explicit responsibilities and exclusions;
- normative present-tense behavior/invariants;
- material failure, unavailable, security, compatibility, ordering, or lifecycle behavior;
- observable acceptance/verification anchors;
- optional links to decision provenance and related executable contracts.

Do not include rejected options, why one design won, incident chronology, implementation progress,
percent completion, task status, or copied requirements owned elsewhere.

## Wording

Use testable normative language (`must`, `must not`, `owns`, `does not own`, `when X, Y occurs`). Avoid
implementation choreography unless a concrete path/protocol itself is the stable boundary. Record
observable rules and semantic ownership, not a snapshot of every class/function.

## Language and naming

Use applicable project instructions, then an explicit documentation convention, then dominant
adjacent maintainer documentation. If several languages/locations remain truly co-equal and choosing
one creates a durable project convention, ask.

Use stable, language-neutral filenames unless project convention says otherwise. Create translations
only by project rule or explicit request.

## ADR relationship

When both exist, link without duplicating content:

- contract: `Decision provenance: <ADR>`;
- ADR: `Current contract: <contract>`.

The ADR records why the operator chose a path. The contract records what future implementations must
preserve. A contract may exist without an ADR when current behavior is clear but historical choice was
never explicitly recorded.
