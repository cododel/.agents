# Contract workflow

## 1. Discover the owner

Read repository instructions and documentation indexes, then use the shared discovery reference.
Confirm a contract through explicit project declarations, a local contract/spec convention, or a
representative living current-state document. Read the complete relevant contract before deciding
impact.

Treat current architecture documentation as a contract when the project declares it a maintainer
boundary or its content normatively owns current process, service, persistence, or extension
boundaries. Never classify an ADR as the current contract merely because it contains invariants.

## 2. Resolve language

Use this precedence:

1. applicable project `AGENTS.md`;
2. explicit documentation index or local convention;
3. dominant adjacent maintainer documentation;
4. ask when several languages remain co-equal.

Write only the primary language. Multilingual output requires an explicit project `AGENTS.md`
instruction; translated siblings or a language switcher alone do not authorize it.

## 3. Classify impact

- `unchanged`: the established contract already permits the work; do not edit it.
- `extend`: current behavior gains or narrows a normative rule; update the established owner in
  place as part of approved behavior work.
- `conflict`: the requested behavior contradicts the owner; stop for an operator decision.
- `missing`: durable current behavior needs an owner and none exists; propose scope and path, then
  wait for explicit creation approval.

Do not call an ADR-only description `unchanged`. Do not create a contract for incidental details
whose maintenance value is unclear.

## 4. Resolve a create path

Follow the proven local convention first. Without one, use an area-based file under the existing
documentation root:

- UI behavior: `docs/UI_CONTRACT.md`;
- current architecture boundaries: `docs/ARCHITECTURE.md`;
- another stable area: `docs/<AREA>_CONTRACT.md`, with an English ASCII area token.

Do not invent a parallel contracts directory or multilingual filename. If the documentation root
or area is ambiguous, include the candidates in the approval request and stop.

## 5. Write or update

Match a proven local format. Otherwise copy `assets/contract-template.md`, remove unused optional
fields, and organize normative bullets by stable surface. Use present tense and testable wording.
Keep implementation paths only when they define a public boundary or durable ownership seam.

For updates, inspect the full affected contract blast radius. Remove superseded current-state rules
in the same edit; living contracts do not preserve history in their body. Preserve rationale in an
existing/new ADR only when the decision independently passes the ADR significance gate.

## 6. Link provenance

If a related ADR exists, add `Decision provenance` to the contract and `Current contract` to the
ADR. Backfill only the ADR relationship field; do not rewrite an Accepted ADR body. If adding the
link would conflict with a local ADR convention, follow that convention and report the unresolved
one-way link.

## 7. Verify

- Compare every changed contract rule with current implementation and focused tests.
- Confirm acceptance checks are observable and do not invent unimplemented behavior.
- Search touched docs for duplicated normative text; leave one owner and links elsewhere.
- Confirm no decision-history sections or unrequested translations were added.
- Run the repository's documentation checks and `git diff --check` when available.

Report exact paths, language evidence, impact, provenance links, and any missing verification.
