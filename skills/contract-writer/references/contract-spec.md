# Living contract specification

## Identity

A living project contract is normative current-state documentation. It says what product, UI, API,
domain, persistence, security, or architecture behavior implementations must satisfy now. It is
edited in place when that behavior changes and has no decision lifecycle.

A contract is not:

- an ADR: dated, immutable decision history with alternatives, rationale, and consequences;
- a feature brief: a temporary operator-agent agreement under review;
- a plan or Issue: execution order or deferred work;
- a test, schema, or type merely because it checks or shapes one surface;
- an index or README that routes readers to the normative owner.

An executable schema, API description, or type surface may be canonical for its bounded interface
only when project instructions or documentation explicitly declare it so. That declaration does not
silently make it the product or architecture contract for adjacent behavior.

## Ownership and overlap

Keep each normative rule in one owner. Split contracts by stable responsibility, not by every
feature: for example, UI behavior belongs in a UI contract and process/service boundaries in a
current architecture contract. When a rule touches both, choose the primary owner and link from the
other document.

Duplication is not harmless reinforcement. Repeated normative prose creates multiple editable
truths. Indexes summarize destinations; ADRs link for provenance; tests and schemas enforce the
owner's rules.

## Content

A contract contains:

- a clear current scope;
- normative present-tense behavior or boundaries;
- failure, unavailable, security, or compatibility behavior where material;
- observable acceptance checks or concrete verification rules;
- optional `Decision provenance` links to related ADRs.

A contract does not contain:

- options considered or rejected alternatives;
- why one design won over another;
- a chronology of incidents, discussion, or implementation;
- decision status (`Proposed`, `Accepted`, `Superseded`) or completion percentages;
- copied rationale or requirements already owned elsewhere.

Small local implementation details belong in code and tests. Create a durable contract only when
the behavior or boundary has enough maintenance value to guide future changes.

## Language and naming

Use the primary documentation language established by applicable project `AGENTS.md`, then by an
explicit docs index/convention, then by the dominant adjacent maintainer documentation. If several
languages are co-equal and no primary language can be proven, ask.

Use language-neutral filenames. Do not add a language suffix or create/update translated siblings
unless project `AGENTS.md` explicitly requires multilingual documentation. Existing translations
alone are not such a requirement.

## ADR relationship

When both artifacts exist, link them without moving normative text into the ADR:

- contract header: `Decision provenance: <ADR links>`;
- ADR header: `Current contract: <contract link>`.

An ADR's decision invariants define conditions under which the recorded choice still holds. They do
not answer whether current behavior is fully documented. If behavior exists only in an ADR and
tests, classify the living-contract impact as `missing`.
