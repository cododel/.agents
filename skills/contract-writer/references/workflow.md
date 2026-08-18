# Contract workflow

## 1. Discover the normative owner

Read repository instructions and documentation indexes, use shared discovery, and inspect relevant
current-state documents completely. Prove ownership through explicit project declarations,
established contract conventions, or repeated normative use—not filename similarity alone.

Inspect code, tests, schemas, event flows, and ADRs to establish current behavior. They are evidence,
not automatic replacement owners.

## 2. Resolve language and path

Use, in order:

1. project/directory `AGENTS.md`;
2. explicit docs index/template/convention;
3. dominant adjacent maintainer docs;
4. a compact area-based fallback under the proven docs root;
5. operator decision only when several durable choices remain co-equal.

Fallbacks when no stronger convention exists:

- UI boundary: `docs/UI_CONTRACT.md`;
- architecture/module boundaries: `docs/ARCHITECTURE.md`;
- another stable area: `docs/<AREA>_CONTRACT.md`.

Do not invent a parallel hierarchy or multilingual family without evidence.

## 3. Classify impact and authority

- `unchanged`: do not edit.
- `extend`: update the established owner as part of requested behavior work.
- `conflict`: stop for an operator decision; do not silently make code match either side.
- `missing`: apply the value test. Create an owner autonomously when behavior, scope, language, and
  path are unambiguous. Ask only when the document itself would decide one of those.

A missing contract discovered during a feature does not require documenting the whole surrounding
legacy area. Capture only the stable boundary and proven rules needed to prevent the identified drift.

## 4. Write or update

Match local format; otherwise use `../assets/contract-template.md`. Remove unused optional sections.
Use present-tense normative bullets and concise acceptance anchors.

For updates:

- inspect the full affected rule/consumer radius;
- remove or replace superseded current-state text in the same edit;
- do not preserve historical rationale in the body;
- keep one owner and replace copied normative text elsewhere with links when touched.

For retroactive creation, distinguish proven behavior from desired behavior. Do not make an accidental
implementation quirk normative merely because it exists; the value must come from operator intent,
established consumers, compatibility, or a clear ownership invariant.

## 5. Link provenance

Backfill `Decision provenance` / `Current contract` when a related ADR exists and local convention
permits it. Relationship fields may be appended to an Accepted ADR; its decision body remains
immutable. Do not create an ADR solely to make the contract look complete.

## 6. Verify

- compare every changed normative rule with current implementation and operator decisions;
- identify focused tests/probes or executable contracts that enforce each material rule;
- ensure ownership/exclusions are not contradicted by other touched documentation;
- check links, language, and absence of copied decision history;
- run project docs checks and `git diff --check` when available.

Report gaps where behavior is intended but not yet enforced; a written contract does not make the code
compliant.
