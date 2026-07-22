---
name: troubleshooter
description: >
  Diagnose tracebacks, stack traces, panics, logs, crashes, and runtime errors down to the
  exact root cause and propose a minimal patch. Use whenever the user wants an error
  investigated rather than blindly patched — including "разберись с ошибкой", "почему
  падает", "что упало", "разбери стектрейс", "вот traceback", "отладь это", "почему
  крашится", "найди причину", "разбери лог", "что кидает исключение", "debug this", "why is
  this failing", "fix this crash", "diagnose this exception", "trace this bug", "what's
  throwing", "find the root cause". Investigation starts read-only. If the user explicitly
  asked to fix the failure, apply the proven minimal patch after diagnosis; otherwise present
  it for approval. Confirmed bugs may be tracked with issue-writer and architectural causes
  documented with adr-writer when the user requests it.
---

# Troubleshooter

Diagnose before fixing. Prove the root cause from actual code and runtime behavior, name the
incorrect assumption (not the symptom), and propose the smallest patch that fixes it.
Investigation starts read-only. Diagnosis must precede any patch, even when the user already
asked for a fix.

## Default mode and the gate

The skill **always starts read-only**: investigate, prove the root cause, propose a patch.
What happens to that patch is the gate:

| After diagnosis…                                      | Action                                                                 |
|-------------------------------------------------------|------------------------------------------------------------------------|
| User asked only to diagnose / explain                 | Present the report and **stop**. Do not touch files.                   |
| User explicitly asked to fix the failure              | Apply the proven minimal diff after diagnosis, within that scope.      |
| User approves a subsequently proposed patch           | Apply that diff and nothing broader.                                   |
| Bug worth tracking, or fix deferred                   | Recommend `issue-writer`; invoke it only when requested.               |
| Root cause is an architectural decision / recurring class | Recommend `adr-writer`; invoke it only when requested.             |

An explicit request such as "fix this crash" authorizes the minimal patch needed for the
diagnosed failure; it does not authorize adjacent refactors. A diagnosis-only request does not
authorize writes. If the requested scope or the proven patch is broader than the user could
reasonably expect, present the diff and confirm before writing.

## Read-only boundary

Use these boundaries while investigating and deciding whether an execution step is covered by
the user's request:

**Safe read-only** — static file reads; repository search; reading logs, config, dependency
manifests; `git log` / `git blame` / `git show` (history only); inspecting types; and fetching
public official documentation through an already configured read-only documentation or web
tool. Do not send source code, logs, credentials, or private identifiers to an external service.

**Treat as stateful — require the user's fix request or specific approval:** running a test
suite or repro script, migrations, package installs or ephemeral package launchers, formatters,
starting servers, authenticated network calls, and anything touching a database or filesystem
state. *"Just running the existing tests" is not guaranteed read-only* — a suite can mutate a
database, spawn services, or write fixtures. If execution would sharpen a diagnosis-only task,
show the exact command and ask before running it.

## Workflow

1. **Read the failure.** Extract error type, exact message, the failing *application* frame
   (file:line), and separate framework/library frames from the project frame that holds the
   wrong assumption. If the artifact is incomplete and the failing target can't be proven from
   the given identifiers or repo files, **stop and ask** for the missing traceback, log, path,
   or command — don't guess from a similar-looking frame.

2. **Trace the bad state to its origin.** This is where the value is, and it's the easiest
   step to flail in. Follow **`references/discovery.md`** for the concrete how: grep
   orientations, scoping, and the navigation from failing line → upstream source of the bad
   state. For framework-specific mechanics (where bad state hides in Django / Next.js /
   Laravel), load the matching file under `references/playbooks/` *only when the stack
   applies* — don't pull all of them into context.

3. **Name the root cause.** Explain why the observed state reaches the failing line, tied to
   concrete code references and the runtime/framework behavior involved. Name the incorrect
   assumption in the code, not just the symptom.

4. **Propose or apply the minimal fix.** Use a focused diff at the best boundary for
   the bad state. Avoid broad catch-all `try/except` unless the actual fix *is* translating a
   known boundary error into a domain outcome. Name the focused test or check that would prove
   the fix. Before applying an approved diff, re-read every target file and ensure the proposed
   context is still current; if it changed, stop and re-evaluate rather than applying a stale
   patch. Run stateful verification only when the user's request or a later approval covers it.

## Investigation budget

A repo-aware agent can read half the project chasing one error. Cap it:

- **One failure at a time.** Diagnose the error in the traceback first; note unrelated
  failures, don't chase them.
- **Bounded search.** At most ~3 rounds of widening search and ~10–15 file reads before you
  must either (a) have the root cause traced end-to-end, or (b) **stop, state the current best
  hypothesis and exactly what's missing, and ask.** Surfacing a narrowed hypothesis early
  beats silently reading the whole repo.
- **Stop when proven.** Once the bad state traces from origin → failing line with concrete
  references, you're done investigating. More reading past that is budget waste, not rigor.

## Report format

Write the final report in the user's language:

- **Root Cause:** why it crashed, technically — the mechanism, not the message.
- **Diagnosis:** the incorrect assumption in the code.
- **Proposed Patch:** minimal diff or code block, plus why it fixes the root cause.
- **Verification:** read-only evidence gathered, and the focused test/check that would confirm
  the fix (described, not run).
- **Next step:** whether the requested fix was applied, approval is needed, or a separately
  requested `issue-writer` / `adr-writer` follow-up is appropriate.

When the investigation hit the budget without a proven root cause (case (b) above), don't dress
the skeleton up as a solved case. **Root Cause** becomes the narrowed hypothesis plus the exact
evidence still missing — phrased as a hypothesis, not a verdict. **Proposed Patch** is omitted: a
patch against an unproven cause is a guess, and there's nothing proven to fix yet. **Next step**
recommends tracking the unresolved diagnosis with `issue-writer` when useful; do not create the
issue unless the user asked to track it. A surfaced gap beats a fabricated cause.

## Design notes

- **Read-only-first, intent-aware apply:** the skill's value is the diagnosis. An explicit fix
  request carries the proven minimal patch through to apply; diagnosis-only requests stop at
  the report, and unexpectedly broad fixes get a separate gate.
- **`references/discovery.md` carries the "how"** so the SKILL.md body stays short. The
  navigation problem (failing line → source of bad state) is the same shape across stacks; the
  stack playbooks only add framework-specific hiding spots, loaded on demand (progressive
  disclosure) so a Python bug never drags the Laravel playbook into context.
- **Composition is declared, not implied:** a confirmed diagnosis is an input to `issue-writer`
  (log the bug) or `adr-writer` (the root cause was an architectural decision). The skill ends
  by routing, matching the rest of the ecosystem rather than terminating in a report.
