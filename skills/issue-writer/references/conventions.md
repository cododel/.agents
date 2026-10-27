# Issue conventions: filename, status, priority, language

This file covers the conventions that apply to **both** modes (create and close). Read
it after shared repository discovery and before `create.md` / `close.md`.

## Local convention always wins

If the target directory has a `README.md`, `ISSUE_TEMPLATE.md`, `CONTRIBUTING.md`, or
similar file found during discovery, it defines the convention. The patterns below
are the **fallback** — used only when no local convention exists, or to fill gaps the
local convention doesn't cover.

Use the stable-name fallback below for newly bootstrapped Issue roots. Preserve existing roots'
documented or evidenced naming/lifecycle conventions, including the previous status-prefixed
fallback. This change does not authorize migrating existing files or mixing naming schemes; if an
existing root has no resolvable convention, clarify it before creating or renaming records.

When following local convention, inspect enough relevant existing files to establish whether the
documented rules match actual practice. Resolve discrepancies rather than treating a fixed sample
size as proof.

## Bootstrap when no issues root exists

In create mode, an explicit request for a repository-local Issue authorizes creating
`docs/issues/`, or `<scope>/docs/issues/` when one module is proven to own the deferral. Install
`../assets/issues-readme.md` as its `README.md` and use `../assets/deferred-template.md` for the first
Issue. Ask instead when the repository boundary or module scope is ambiguous or local instructions
declare a different tracker/location. Bootstrap is part of the authorized recording request, never
an automatic response to discovered debt. In review/close mode, report that there is no confirmed root and
stop; never bootstrap an empty directory for a sweep.

## Filename pattern (fallback)

```
YYYY-MM-DD-english-domain-symptom-slug.md
```

Components:

- **`YYYY-MM-DD`** — original issue date (today for new issues; **never change** when
  status or priority is updated — date encodes when the issue was first opened)
- **`slug`** — concise English kebab-case with enough domain/symptom identity to avoid collisions (e.g.
  `auth-token-leak-on-logout`, `migrations-fail-on-empty-db`)

Filenames stay in English even when issue prose is in another language. This keeps
`grep`, `find`, and CI tooling stable across contributors.

### Optional pattern: percent-status (used by some long-running projects)

Some repositories track implementation drift over time and use a richer prefix:

```
[STATUS-PERCENT%]-...-slug.md
```

Where `STATUS-PERCENT%` is a locally defined legacy form such as `[ACTIVE-25%]` or
`[RESOLVED-100%]`.
The percentage reflects requirement coverage, not optimism about planned work.

Use this only when the local README explicitly calls for it. Don't impose it on a
repository with another naming convention.

## Status

Under the stable-name fallback, the body is the single status owner:

| Value | Meaning |
|-------|---------|
| `Open` | Deferred work is independently resumable but implementation has not started. Default. |
| `Implementing` | Scoped implementation is actively in progress. |
| `Closed` | Completion criteria are met and verified for the recorded scope. |

Keep the filename unchanged when status or priority changes. Incomplete evidence or investigation
keeps the Issue `Open`, with uncertainty recorded explicitly. Parse the complete body status value:
`Closed pending verification` is not `Closed`; a missing or conflicting status is ambiguous.

For established status-prefixed conventions, preserve their exact syntax and synchronize filename,
body and affected links when that convention requires it. Recognize `ACTIVE`, `INVESTIGATING`,
`RESOLVED` and percent-status forms only under an evidenced local or legacy convention.
Never discover completed candidates through a loose prefix match.

## Priority and severity

Use the same literals for two independent fields:

- `Priority: Critical | High | Medium | Low` records urgency and sequencing.
- `Severity: Critical | High | Medium | Low` records impact or harm.

Do not derive either field from the other. Keep applicable fields in the body, not the filename.
Severity applies to defects or evidenced harmful limitations; omit it when inapplicable and mark
applicable unknown values explicitly. Recognize `P0` through `P3` only where an established local
or legacy convention requires them.

## Language rules

- **Filenames**: English kebab-case, always. No Cyrillic, no spaces, no punctuation
  beyond hyphens.
- **Issue body**: follow the project's documentation language unless the operator explicitly requests
  another language; if none is established, use the request's language. Code, paths, error messages,
  and identifiers retain their original language.
- **Status, priority, and severity values**: always use the English literals above.

## Refresh notes

For long-lived or evolving issues, append a refresh line near the header when revisiting:

```markdown
**Last reviewed:** YYYY-MM-DD
```

or, when material context shifted:

```markdown
**Stale note:** Re-checked on YYYY-MM-DD; the named dependency no longer exists, but the
completion criteria have not been verified. Keeping the Issue Open pending operator review.
```

Use `Stale note` only with evidence. It annotates an `Open` Issue and never acts as a fourth
status. Review notes preserve audit trail without rewriting history.

## Stop and ask, never invent fields

If the local convention requires a field you can't fill from evidence (e.g. `**Probe:**`,
`**FSD Slice:**`, `**Implementation:**`), either:

- Ask the user, or
- Leave an explicit `TODO:` placeholder and call it out in the final report.

Don't fabricate file paths, line numbers, function names, or commit SHAs. The audit
trail loses value the moment a single field is invented.
