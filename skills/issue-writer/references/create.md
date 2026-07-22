# Create / update workflow

This is the detailed workflow for creating a new issue or updating an existing active
one. By the time you're reading this, you've already loaded `discovery.md` and
`conventions.md` from `SKILL.md`'s shared steps.

## Step C1 — Gather facts

Collect from the user request and repository context:

- title or short summary
- severity (`Critical | High | Medium | Low`) and priority (`P0–P3`)
- status (default `[ACTIVE]`; `[INVESTIGATING]` if evidence is incomplete)
- affected scope: app, package, service, module, or files
- discovered-via: code review, production incident, log analysis, user report,
  implementation follow-up, …
- background and evidence (what's wrong, why it matters, what was observed)
- root cause (why it happens — be specific about the line/condition/assumption)
- affected files / entry points / probes (grep-able locators)
- recommended fix (and a minimal-fix variant if the proper fix is large)
- next steps / verification checklist
- related issues or ADRs

Facts you can't confirm from the conversation or the repo become **questions to the
user**, not invented values. Asking is cheap; fabricating loses audit trail.

## Step C2 — Read local examples

Before writing, check the issues directory for:

- 1-2 recent active issues — to match the prose style, header field set, and section
  ordering people actually use
- a `README.md` / `ISSUE_TEMPLATE.md` in the same directory — already covered in
  `discovery.md` Step D4, but re-confirm if you skipped reading it

For a newly bootstrapped directory there are no examples: use the installed fallback README
and template directly. Do not ask for examples that cannot exist yet.

If the local convention has fields not in the fallback (e.g. `**Probe:**`,
`**FSD Slice:**`, `**Last refreshed:**`), include them. If it omits sections from the
fallback, omit them too — match the local style.

## Step C3 — Update vs create

If the user is reporting something that overlaps an existing active issue:

1. Search for related slugs and probes in the issues directory (`grep -r` on a few
   distinctive terms).
2. If you find a likely match, **ask** before either creating a new file or modifying
   the existing one. The user may want a fresh issue (different root cause), an update
   (new evidence on the same bug), or a recurrence note appended.
3. For updates: bump `**Last refreshed:**`, append new evidence in a dated subsection,
   and only change `**Status:**` if the user explicitly says so.

Some projects (per their template `NOTE` comments) reserve specific sections for
automated tooling — e.g. an `## Incidents` table appended by a bot. **Respect those
NOTE comments**: don't include the section when creating, don't overwrite when updating.

## Step C4 — Write the issue

- Match the directory's existing structure when 2+ examples exist.
- Use `assets/fallback-template.md` only when no local example or template exists.
- Preserve the user's prose language (see `conventions.md` § Language rules).
- Keep filenames English kebab-case regardless of prose language.
- Include concrete code paths, function names, and line numbers **only when proven**
  from the repo or provided by the user. Use the `**Probe:**` pattern (a short,
  grep-able snippet) when the local template supports it — line numbers drift, probes
  survive.
- Leave explicit `TODO:` placeholders for unresolved facts and mention them in the
  final report.

## Step C5 — Verify the file lands

After writing, run a quick sanity check:

- File is at the expected path with the expected filename.
- Filename matches the local pattern (status tag, priority, date, slug).
- Header fields match the local template's required set.
- No fabricated paths or line numbers.

If the issues directory has an index (`README.md` listing active issues, or an
`index.md`), update it in the same change — but only if the local convention is
unambiguous about how. If unclear, mention it in the report and let the user decide.

## Step C6 — Report back

Tell the user:

- Created or updated path
- Chosen scope and why it was proven (single-hit `find`, repo instructions, user input)
- Priority and status
- Convention used (local template, sampled from existing issues, or fallback)
- Any `TODO:` placeholders or facts you couldn't confirm
- Whether you updated an index, and which one
