# Issue conventions: filename, status, priority, language

This file covers the conventions that apply to **both** modes (create and close). Read
it after `discovery.md` and before `create.md` / `close.md`.

## Local convention always wins

If the target directory has a `README.md`, `ISSUE_TEMPLATE.md`, `CONTRIBUTING.md`, or
similar file (see `discovery.md` Step D4), it defines the convention. The patterns below
are the **fallback** — used only when no local convention exists, or to fill gaps the
local convention doesn't cover.

When following local convention, sample 2-3 existing files in the directory to confirm
the documented rules match actual practice.

## Filename pattern (fallback)

```
[STATUS]-YYYY-MM-DD-english-domain-symptom-slug.md
```

Components:

- **`[STATUS]`** — see status tags below
- **`YYYY-MM-DD`** — original issue date (today for new issues; **never change** when
  status or priority is updated — date encodes when the issue was first opened)
- **`slug`** — English kebab-case, 3-7 words, `domain-symptom` shape (e.g.
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
repository that uses the simpler `[STATUS]` form.

## Status tags

| Tag                | Meaning                                                                                |
|--------------------|----------------------------------------------------------------------------------------|
| `[OPEN]`           | Deferred work is independently resumable but implementation has not started. Default. |
| `[IMPLEMENTING]`   | Scoped implementation is actively in progress.                                        |
| `[CLOSED]`         | Completion criteria are met and verified for the recorded scope.                       |

Incomplete evidence or investigation does not introduce another lifecycle state: keep the
Issue `Open` and record the uncertainty explicitly. Recognize `ACTIVE`, `INVESTIGATING`, and
`RESOLVED` only when reading an established local or legacy convention; do not emit them in
the fallback format.

When status changes, **rename the file** in the same change that updates the body. Local
links (in indexes, READMEs, sibling issues) must be updated too.

## Priority and severity

Use the same literals for two independent fields:

- `Priority: Critical | High | Medium | Low` records urgency and sequencing.
- `Severity: Critical | High | Medium | Low` records impact or harm.

Do not derive either field from the other. Keep both in the body and out of the filename so
priority can change without renaming the Issue. Recognize `P0` through `P3` only where an
established local or legacy convention requires them.

## Language rules

- **Filenames**: English kebab-case, always. No Cyrillic, no spaces, no punctuation
  beyond hyphens.
- **Issue body**: preserve the user's language (Russian, English, etc.) unless the local
  convention clearly enforces one. Code, paths, error messages, and identifiers stay in
  their original language regardless.
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
