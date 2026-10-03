# Contract workflow

## 1. Discover the normative owner

Read repository instructions and documentation indexes, use shared discovery, and inspect relevant
current-state documents completely. Prove ownership through explicit project declarations,
established contract conventions, or repeated normative use—not filename similarity alone.

Inspect code, tests, schemas, event flows, and ADRs to establish current behavior. They are evidence,
not automatic replacement owners.

Keep discovery/impact read-only. Identifying a missing owner does not authorize writing one; apply
the findings only within an explicit authoring request or authorized behavior work that covers the
guarantee change.

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

When no contract root exists, a new owner is justified only if all four value conditions hold and
the repository's docs root, language, module scope, and placement convention are proven. Within
authorized authoring work, bootstrap the smallest area document under that established structure;
do not create a contract merely because `docs/contracts/` is absent. If only a suitable existing
API/schema/document needs an update, use it. Ask only for a genuinely unresolved canonical-home
choice, not a missing conventional folder.

## 3. Classify impact and authority

- `unchanged`: do not edit.
- `extend`: in authorized behavior/authoring work, update the established owner.
- `conflict`: if the operator already confirmed the changed guarantee, update the existing owner and
  disclose any implementation gap. Otherwise stop affected authoring for the unresolved decision;
  do not silently make code match either side.
- `missing`: apply all four value conditions. Within authorized work, create an owner when behavior,
  scope, language, and the proven documentation path are unambiguous. In discovery/impact mode,
  report the justified gap without writing. Ask only when the document would decide a material fork.

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
