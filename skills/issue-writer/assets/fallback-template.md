# [{SEVERITY}] `path/to/file.ext` — short error message or symptom

**Date:** YYYY-MM-DD
**Last refreshed:** YYYY-MM-DD
**Priority:** {P0|P1|P2|P3}
**Severity:** {Critical|High|Medium|Low}
**Status:** {Active|Investigating|Resolved}
**Scope affected:** `{scope-or-service}`
**Files:** `path/to/file.ext`
**Probe:** `unique_function_or_grep_snippet` — one-line description of what's wrong
**Discovered via:** {Code review | Production logs | Runtime error | User report | Implementation follow-up | …}

---

## Background

{2–4 sentences: what this component does, the context in which the problem appears,
and what observable behavior is wrong. Link to the trigger event (incident, log,
review) so the next reader can reconstruct the discovery.}

---

## Root Cause

{Be specific: which function, which line or grep-able snippet, which condition or
assumption is violated. If root cause is not yet known, say so explicitly and mark
status `Investigating` rather than guess.}

### Why was this mistake made?

- {Missing guard / race condition / incomplete refactor / untested edge case / …}
- {Second contributing factor, if any}

---

## Negative Consequences

1. {User-facing impact}
2. {Data integrity impact, if any}
3. {Observability impact — noisy logs, masked errors, alert fatigue, …}

---

## How to Reproduce

```
{Minimal steps, command, or script that triggers the symptom. If repro requires
production data or a specific timing window, say so.}
```

---

## Affected Files

| File | Probe | Impact |
|------|-------|--------|
| `path/to/file.ext` | `grep_snippet_or_symbol_name` | What goes wrong here |

---

## Minimal Fix

{Smallest safe change that stops the symptom. Code snippet preferred over prose.}

```diff
- old_code
+ new_code
```

---

## Recommended Solution

{The proper fix with rationale. May differ from minimal fix if a deeper refactor or
ADR-level decision is warranted. If recommended solution requires an ADR, link or
mention it in `## Related`.}

---

## Checklist

- [ ] Fix applied in `path/to/file.ext`
- [ ] Test added or existing test updated
- [ ] Verified in {staging | local repro | production after deploy}
- [ ] Local links updated if this issue was renamed (e.g. `[ACTIVE]` → `[RESOLVED]`)

---

## Related

- {Link to related issue, ADR, PR, or external incident}

<!--
About `**Probe:**`: a short, grep-able snippet that locates the bug in the source file.
Survives line-number drift caused by future edits. Examples:
  - Specific expression: `select(User.token).where(User.id == user_id)`
  - Function with missing guard: `async def _ensure_session — no expiry check`
  - Config key: `"DATABASE_URL"` in `settings.py`
Prefer probes over line-only references. Use line numbers as supporting context, not
as the sole locator.
-->
