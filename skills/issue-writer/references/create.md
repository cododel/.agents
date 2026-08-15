# Create / update workflow

This is the detailed workflow for creating a new issue or updating an existing open
one. By the time you're reading this, you've already loaded shared repository discovery and
`conventions.md` from `SKILL.md`'s shared steps.

## Step C1 — Gather facts

Collect from the user request and repository context:

- title or short summary
- priority (`Critical | High | Medium | Low`) as urgency and sequencing
- severity (`Critical | High | Medium | Low`) as impact or harm
- status (default `[OPEN]`; use `[IMPLEMENTING]` only after implementation starts)
- affected scope: app, package, service, module, or files
- discovered-via: code review, production incident, log analysis, user report,
  implementation follow-up, …
- background and evidence (what's wrong, why it matters, what was observed)
- root cause (why it happens — be specific about the line/condition/assumption)
- affected files / entry points / probes (grep-able locators)
- recommended fix (and a minimal-fix variant if the proper fix is large)
- next steps / verification checklist
- applicable living project contracts and their expected `unchanged | extend | conflict | missing`
  impact, when proven
- related issues or ADRs

Facts you can't confirm from the conversation or the repo become explicit `TODO:` values or,
when they would invalidate downstream work, questions to the user. Never derive priority from
severity or severity from priority.

### Explicit deferral intent

Recognize the semantic intent, not a keyword. When the user clearly wants to stop work on a
concrete independently resumable question, feature, or follow-up now, preserve it, and return to
it later, treat that as a request to create a **new open issue now**. Phrases such as "отложить", "давай не сейчас,
но вернёмся к этому", "зафиксируй на потом", "defer this", and "park this" are non-exhaustive
examples, not a whitelist. Do not require the user to name the skill or say "issue", and do not
treat the request as only a conversational reminder or ask for another confirmation.

Do not create an Issue for a nuance that can be handled or reported within the current task.
If the work is not being deferred or cannot be resumed independently, keep it in the current
task context instead.

Capture the complete usable context already available in the conversation and repository:

- what question, feature, or follow-up was deferred
- the current state and all established facts, constraints, decisions, rejected options,
  attempted work, and relevant artifacts
- the deferral decision: why work stops now and which constraint, tradeoff, dependency, or
  competing priority led to it
- the **resume conditions**: concrete events, evidence, prerequisites, dates, capacity, or
  decision changes that should cause the issue to be reconsidered
- the first next steps once resumed and the acceptance or completion criteria
- unresolved questions, clearly separated from established facts

Do not infer a reason or resume condition merely from the deferral intent. If the conversation
does not establish one, write an explicit `TODO:` instead of flattening the missing context into
a generic phrase such as "not a priority". Avoid making the user repeat context that is already
present in the conversation or provable from the repository.

## Step C2 — Read local examples

Before writing, check the issues directory for:

- 1-2 recent open issues — to match the prose style, header field set, and section
  ordering people actually use
- a `README.md` / `ISSUE_TEMPLATE.md` in the same directory — already covered in
  the shared discovery workflow, but re-confirm if you skipped reading it

For a newly bootstrapped directory there are no examples: use the installed fallback README
and template directly. Do not ask for examples that cannot exist yet.

If the local convention has fields not in the fallback (e.g. `**Probe:**`,
`**FSD Slice:**`, `**Last reviewed:**`), include them. If it omits sections from the
fallback, omit them too — match the local style.

## Step C3 — Update vs create

If the deferred work overlaps an existing open issue:

1. Search for related slugs and probes in the issues directory (`grep -r` on a few
   distinctive terms).
2. If this is an explicit deferral request, create the requested new issue and link a
   related existing issue when relevant. Do not silently turn "отложить" into an update.
3. Otherwise, if you find a likely match, **ask** before either creating a new file or
   modifying the existing one. The user may want a fresh issue (different root cause),
   an update (new evidence on the same bug), or a recurrence note appended.
4. For updates: bump `**Last reviewed:**`, append new evidence in a dated subsection,
   and only change `**Status:**` if the user explicitly says so.

Some projects (per their template `NOTE` comments) reserve specific sections for
automated tooling — e.g. an `## Incidents` table appended by a bot. **Respect those
NOTE comments**: don't include the section when creating, don't overwrite when updating.

## Step C4 — Write the issue

- Match the directory's existing structure when 2+ examples exist.
- When no local example or template exists, use `assets/deferred-template.md`. If the work is not
  explicitly deferred and independently resumable, do not create an Issue.
- Preserve the user's prose language (see `conventions.md` § Language rules).
- Keep filenames English kebab-case regardless of prose language.
- For an explicit deferral request, preserve the deferred context, reason, and resume conditions
  as distinct sections even when adapting them to a stronger local template.
- Include concrete code paths, function names, and line numbers **only when proven**
  from the repo or provided by the user. Use the `**Probe:**` pattern (a short,
  grep-able snippet) when the local template supports it — line numbers drift, probes
  survive.
- Leave explicit `TODO:` placeholders for unresolved facts and mention them in the
  final report.

## Step C5 — Verify the file lands

After writing, run a quick sanity check:

- File is at the expected path with the expected filename.
- Filename matches the local pattern (fallback: status tag, date, slug).
- Header fields match the local template's required set.
- No fabricated paths or line numbers.

If the issues directory has an index (`README.md` listing open issues, or an
`index.md`), update it in the same change — but only if the local convention is
unambiguous about how. If unclear, mention it in the report and let the user decide.

## Step C6 — Report back

Tell the user:

- Created or updated path
- Chosen scope and why it was proven (single-hit `find`, repo instructions, user input)
- Priority and status
- Convention used (local template, sampled from existing issues, or fallback)
- For an explicit deferral: the recorded deferral reason and resume conditions, including any
  `TODO:` values
- Any `TODO:` placeholders or facts you couldn't confirm
- Whether you updated an index, and which one
