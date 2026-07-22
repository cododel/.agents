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
[STATUS]P<0-3>-YYYY-MM-DD-english-domain-symptom-slug.md
```

Components:

- **`[STATUS]`** — see status tags below
- **`P<0-3>`** — priority, see priorities below
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

Where `STATUS-PERCENT%` is one of `[ACTIVE-25%]`, `[INVESTIGATING-60%]`, `[RESOLVED-100%]`.
The percentage reflects requirement coverage, not optimism about planned work.

Use this only when the local README explicitly calls for it. Don't impose it on a
repository that uses the simpler `[STATUS]` form.

## Status tags

| Tag                | Meaning                                                                                  |
|--------------------|------------------------------------------------------------------------------------------|
| `[ACTIVE]`         | Confirmed issue still requiring code, data, or operator action. Default for new issues.  |
| `[INVESTIGATING]`  | Evidence is incomplete or production verification is still required.                     |
| `[RESOLVED]`       | Code, config, or docs are updated and the issue is closed for current scope. Verified.   |

When status changes, **rename the file** in the same change that updates the body. Local
links (in indexes, READMEs, sibling issues) must be updated too.

## Priority levels

| Code | Severity                                                                  |
|------|---------------------------------------------------------------------------|
| `P0` | Critical — data loss, crash loop, security breach, full outage            |
| `P1` | High — major feature broken for a subset of users, no workaround          |
| `P2` | Medium — degraded behavior, workaround exists, intermittent failures      |
| `P3` | Low — edge case, cosmetic, low frequency, easy workaround                 |

Priority is rarely changed after creation; severity often is. If the local convention
distinguishes the two (e.g. has both `**Priority:**` and `**Severity:**` fields), reflect
both in the body but keep the filename `P<n>` stable.

## Language rules

- **Filenames**: English kebab-case, always. No Cyrillic, no spaces, no punctuation
  beyond hyphens.
- **Issue body**: preserve the user's language (Russian, English, etc.) unless the local
  convention clearly enforces one. Code, paths, error messages, and identifiers stay in
  their original language regardless.
- **Status tags and priority codes**: always English literals (`[ACTIVE]`, `P2`).

## Refresh notes

For long-lived or evolving issues, append a refresh line near the header when revisiting:

```markdown
**Last refreshed:** YYYY-MM-DD
```

or, when material context shifted:

```markdown
**Refresh 2026-04-30:** Re-checked — root cause unchanged, but workaround in PR #1234
removes the user-visible impact. Keeping ACTIVE until full fix lands.
```

Refresh notes preserve audit trail without rewriting history.

## Stop and ask, never invent fields

If the local convention requires a field you can't fill from evidence (e.g. `**Probe:**`,
`**FSD Slice:**`, `**Implementation:**`), either:

- Ask the user, or
- Leave an explicit `TODO:` placeholder and call it out in the final report.

Don't fabricate file paths, line numbers, function names, or commit SHAs. The audit
trail loses value the moment a single field is invented.
