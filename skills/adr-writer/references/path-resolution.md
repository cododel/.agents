# ADR path resolution

Follow an explicit project ADR index/README and representative local records first.

## Fallback routing

| Scope | Fallback path |
|:--|:--|
| Whole-system or cross-cutting decision | `docs/adr/ADR-YYYYMMDD-<slug>.md` |
| One independently owned app/package/service | `<module>/docs/adr/ADR-YYYYMMDD-<slug>.md` |
| Infra/operations with an established separate docs root | `<infra-docs-root>/adr/ADR-YYYYMMDD-<slug>.md` |

Use a short English kebab-case slug that names the decision. Make collisions more specific before
using a numeric suffix. Match a proven legacy filename convention when it already exists, but never
introduce implementation-percent naming as the fallback.

Choose module-local placement only when one module clearly owns the decision. Use global placement for
shared/cross-cutting behavior. If two canonical homes remain co-equal and choosing one establishes a
new durable convention, ask the operator.

An explicit ADR or `from-issue` request authorizes creation of the resolved local directory and
fallback README when ownership is clear; mention a newly created root in the handoff. Ask only when
several canonical homes remain plausible. Never invent a parent outside the repository's documentation
structure.
