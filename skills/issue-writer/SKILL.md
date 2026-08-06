---
name: issue-writer
description: "Create, update, or close repository-local Markdown issue records for deferred, independently resumable work. Use for `создай/напиши issue`, `отложим`, `defer this`, `park this`, or `sweep closed`, including deferral intent without the word issue. Do not create an Issue for every observation, work being completed now, hosted trackers, or broad read-only docs classification (`docs-cleanup`)."
---

# Issue Writer

## Purpose

Manage the lifecycle of issue tracking documents in the location and format proven by the
current repository. Two distinct modes:

1. **Create / update** an issue only for deferred work that another session can resume
   independently from the captured decision context and resume conditions.
2. **Close** closed issues by extracting any documentation value (architectural
   decisions → ADRs; operational procedures → runbooks; unique repros/commands → relevant
   docs) and then deleting the source files. Closed issues are not retained in an
   archive — once their content is extracted, the file's job is done.

Work from repo evidence, not similar-looking guesses.

## Mode selector

Pick the mode from the user's **intent** before loading the detailed workflow. The phrases in
the table are non-exhaustive examples, not literals to match.

| User intent and example wording                                                                                                      | Mode    | Read next                |
|-------------------------------------------------------------------------------------------------------------------------------------|---------|--------------------------|
| Defer independently resumable work: "create issue", "track this for later", "напиши issue", "зафиксируй на потом"                | create  | `references/create.md`   |
| Stop a concrete question/feature now and preserve it for later: "отложим это", "вернёмся к этому позже", "defer this", "park this"   | create  | `references/create.md`   |
| Sweep closed work: "close issues", "sweep closed", "delete closed", "почисти issues", "архивируй closed"                      | close   | `references/close.md`    |

Archive-style trigger phrases route to `close` for muscle-memory compatibility — the
operation itself is delete-after-extraction, not move-to-archive. The close gate makes
this explicit and surfaces any item with extractable value before any `rm`.

If the request is ambiguous (e.g. just "issues are a mess" — sounds more like a docs
audit), confirm intent with the user first. The `docs-cleanup` skill is a better fit for
broad audits; this skill is for the two narrow lifecycle operations above.

If work is being implemented now or a finding is only an incidental nuance, do not create
an Issue. Continue the current work or report the observation inline unless the operator
explicitly chooses to defer it as an independent task.

## Shared steps (both modes)

Before branching into a mode, both workflows need the same two pieces of context. Read
them in this order:

1. **`references/discovery.md`** — locate the issues directory in the current repo or
   monorepo scope. One `find` command, with explicit exclusions, is the source of truth;
   repo instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `docs/README.md`)
   override it when present.
2. **`references/conventions.md`** — filename pattern, status tags, priority levels, and
   language rules. The mode-specific reference assumes you've already read this.

Then branch into `create.md` or `close.md` per the selector above.

## Assets

- `assets/fallback-template.md` — full markdown template for a new issue when the target
  directory has no stronger local format. Used by `create.md`.
- `assets/deferred-template.md` — fallback template for an explicitly deferred question,
  feature, or follow-up. Used by `create.md`.
- `assets/issues-readme.md` — fallback local convention installed as `README.md` when the
  skill bootstraps a new issues directory.

## Report back

After any operation, report:

- For **create**: created path, chosen scope (and why it was proven), priority and status,
  convention used (local or fallback), any placeholders or unresolved facts.
- For **close**: counts of `deleted / blocked-needs-extraction / ambiguous`, the list of
  deleted paths, per-blocked-item reason (which extraction was suggested), any index/README
  updates made, and any items left untouched.

## Design notes

- `references/discovery.md` is duplicated in `adr-writer/` and `docs-cleanup/` by
  intention. The trio shares the same discovery problem (locate `issues/`, `adr/`, etc.)
  but each skill must remain installable on its own — copies are the price of autonomy.
- The two modes split into separate `references/` so that triggering "create" doesn't
  also pull close details into context (and vice versa). Progressive disclosure is the
  reason the body of `SKILL.md` is short.
- Close runs through an explicit operator gate before any `rm` — the request can sound
  categorical, but the model never deletes files without the user confirming the plan.
- The close workflow includes a **mandatory pre-extraction check**: any closed issue
  whose body holds extractable value (rejected options, invariants, unique repros, ops
  procedures) is `blocked` from deletion until either the value is extracted into its
  proper home (ADR / runbook / troubleshooting doc) or the operator explicitly overrides.
  Closing an issue must always extract documentation value first — the archive directory
  is gone, so anything worth keeping must move to its real home before the file dies.
