# From-issue (promote) workflow

Scan closed issues, identify the ones that are actually architectural decisions, and
promote them to proper ADRs. The ADR becomes the canonical reference; provenance lives
in the ADR's `Source issue:` header and in git history. After the ADRs are saved, the
source issue files are deleted in a gated final step — there is no `archive/`
directory and no retention of closed issues on disk.

By the time you're reading this, you've loaded shared repository discovery, `path-resolution.md`,
and `candidate-criteria.md` from `SKILL.md`'s shared steps. The quality bar the
generated ADRs must meet — core sections, honest alternatives, decision invariants, the
significance check — lives in `references/adr-spec.md`; `candidate-criteria.md` layers
the issue-specific promote/skip specifics on top of it. When generating each ADR (Step
P6), it follows the same template and depth rules as `from-chat`.

## Why this workflow exists (and its place in the hierarchy)

`from-chat` is the primary way ADRs are produced — capture decisions the user just
articulated, with full rationale visible in the conversation. `from-issue` is the
**exception**: closed issues sometimes carry decisions worth surfacing as ADRs
(choice of package manager, "no monorepo for now", or another fork with preserved
alternatives and rationale), and without promotion these stay buried in the issues directory.
Bare current-state rules such as "balances always go through service X" route to a living
contract instead.

Because the evidence chain in `from-issue` is weaker than in `from-chat` (you have
the issue body, not the live reasoning), the workflow is **more conservative** by
design: anti-fabrication is the hard rule, and the gate is mandatory.

## Step P0 — Context quality awareness

Before classification, determine which variant of `from-issue` you're in. This
calibrates the evidence bar for Step P3.

| Variant            | Trigger                                                                 | Evidence bar                                                                                  |
|--------------------|-------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **same-chat**      | The current conversation also closed one or more of the candidate issues | Slightly relaxed: you can cross-check the body against what was actually decided in this chat. Quote the chat reasoning in the ADR if the issue body is sparse but the chat covered the rationale.    |
| **cold audit**     | Cold scan with no recent chat lineage for the candidates                | Strict: the **issue body itself** must contain an explicit Promote signal (see `candidate-criteria.md`). No reading between the lines, no extrapolation from filenames or topic shape. |

Record the variant once at the top of the run (e.g. `context: same-chat (closed
the bun-as-pm issue in this conversation)` or `context: cold audit (no recent chat
lineage)`) and surface it in the gate so the user knows which calibration was used.

When in doubt — for example, you remember a related discussion but it doesn't
clearly cover the candidate — treat it as **cold audit**. Same-chat is a positive
claim about evidence, not a vibe.

## Step P1 — Locate the source issues directory

Shared discovery should have produced a confirmed `docs/issues/` (or its monorepo
equivalent). If `find` returned multiple hits, **ask which one** to scan. Don't process
all by default — the user almost always means one specific scope.

(For locating the *target* `docs/adr/` directory, use `path-resolution.md` per
candidate after Step P3 — different ADRs may go to different scopes.)

## Step P2 — Enumerate closed issues

A file is in the candidate pool if **either**:

1. Its filename starts with `[CLOSED]`, OR
2. Its body header contains `**Status:** Closed` (case-insensitive)

For compatibility with an established local convention, also recognize legacy `[RESOLVED]`
or `[RESOLVED-100%]` filenames and `Status: Resolved`. Keep legacy naming in provenance;
do not silently migrate source files during promotion.

```bash
# By filename
find <issues-dir> -maxdepth 1 -type f \( -name '[[]CLOSED]*.md' -o -name '[[]RESOLVED*' \)

# By body status
grep -lEi '^\*\*Status:\*\*[[:space:]]+(Closed|Resolved)' <issues-dir>/*.md
```

Take the union. If a legacy `<issues-dir>/archive/` directory exists from before the
close-and-delete workflow, exclude it from the scan — those files are out of scope
for this workflow. Files with filename/body mismatches go into `ambiguous` and are
surfaced in the report (don't promote ambiguous files — they need the user's
attention first).

## Step P3 — Classify each candidate

Read each candidate's body **in full** (don't sample) and assign a verdict per
`candidate-criteria.md`:

- `promote` — a significant architectural choice with explicit alternatives or other
  evidence of the actual fork, plus concrete rationale; a bare invariant, boundary,
  policy, or current-state description is not enough
- `skip` — clear negative signal (operational fix, hygiene, doc drift, one-off
  tooling, pure ops)
- `merge` — looks like part of a multi-issue decision worth one combined ADR
- `ambiguous` — body is thin and signal is unclear, but the topic looks architectural;
  flag for user input rather than silent skip

For each verdict, record:

- `path` — full path to the issue
- `verdict` — one of the four above
- `reason` — one sentence quoting the matched decision and rationale ("chooses a
  ledger-only write path over direct model updates because projections must remain
  reconstructable")
- `proposed_target_path` — for `promote` and `merge`, the ADR path per
  `path-resolution.md`
- `rejection_reasons_present` — boolean, helps the user see which promotions need their
  input later

Keep the table compact — the user reads it in the gate, not the issue bodies.

## Step P3.5 — Cluster pass

Individual classification reads each file in isolation, which means it cannot see
when several issues describe the **same architectural decision**. The cluster pass
fixes that by re-examining the `promote` set as a group.

**Trigger:** run whenever there are 2 or more `promote` candidates. Below that, no
clusters are possible.

**How to cluster — compute these signals across every pair of `promote` candidates:**

| Signal             | How to check                                                                     |
|--------------------|----------------------------------------------------------------------------------|
| Slug overlap       | Shared distinctive keyword in filename slug (`pool`, `auth`, `monorepo`, etc.)   |
| File overlap       | Two issues reference the same path in body (`**Files:**` or `**Affected Files:**`) |
| Scope/tag overlap  | Same `**Services affected:**`, `**Scope / Component:**`, `**FSD Slice:**`, etc.  |
| Date proximity     | Opened within the same week — often a single incident-burst                      |
| Theme repeat       | The same phrase, symptom, or rationale appears in both `## Background` sections  |

**Cluster threshold:** propose a group only when **at least 2 signals match** across
all members of the group. One signal alone is noise (random slug collision, two issues
touching the same file for unrelated reasons).

**Building groups:**

1. Compute pairwise signals across all `promote` candidates.
2. Form groups by transitive closure: A↔B and B↔C → group {A,B,C}.
3. Verify the group has a single coherent architectural theme by skimming the
   `## Background` of each. If themes diverge, split the group.
4. Keep groups small (typically 2-5). A "group" of 10 issues is suspicious — those
   probably belong as one ADR per genuine sub-decision.

**For each proposed group**, record:

- `members` — list of paths
- `signals` — which signals matched and on what value (`slug: pool`, `file: services/db.py`)
- `proposed_title` — short slug for the unified ADR
- `proposed_target_path` — single ADR path per `path-resolution.md`

Candidates not in any cluster stay as individual promotes. The cluster pass never
demotes a `promote` to `skip` — it only groups.

## Step P4 — Confirmation gate

Present the full plan and **wait for explicit approval**, even if the user's request
sounded categorical. Three explicit paths now: individual promotes, cluster
promotes, skips.

**Before the full plan, open with an explicit "Decisions required" block** — a short
numbered list of what needs the user's answer before apply can proceed. This makes
the gate scannable even when the plan is long. Don't make the user ask "what do I
need to decide?" — surface it proactively.

Typical decision points to surface:

- **Target directory** — if `docs/adr/` doesn't exist, say so and ask for
  confirmation to create it (or for an alternative path).
- **Cluster groupings** — for each proposed cluster, state what was grouped and
  why, and that `ungroup #N` splits it. Users may disagree with the grouping without
  reading the full plan.
- **Post-apply gate** — mention that source issue deletion will be asked separately
  after ADRs are saved, so the user knows it's coming and can think about it. The
  ADR-creation gate (this one) does not bundle the source-deletion approval.

```
ADR promotion plan for <issues-dir>:
Context: <same-chat | cold audit> — <one-line justification>

Decisions required from you:
  1. <e.g. "Create docs/adr/ (doesn't exist yet)? Say 'apply' to confirm, or name another path.">
  2. <e.g. "Cluster A groups issue-foo + issue-bar into one ADR. OK, or `ungroup A`?">
  3. (after apply) Source issue deletion — will ask separately, per-path.

--- Full plan ---

=== Individual promotes (N) ===

  docs/issues/[CLOSED]-2026-01-12-package-manager-bun-only.md
    → docs/adr/ADR-20260515-bun-as-only-package-manager.md
    reason: choice of package manager for monorepo, with rejected pnpm/yarn/npm
    rejection_reasons_present: yes

=== Cluster promotes (G groups from M issues) ===

  Group #1 — monorepo posture (2 issues)
    signals: slug overlap (`monorepo`, `cabinet`), scope overlap (`platform`)
    members:
      - docs/issues/[CLOSED]-2026-02-03-no-monorepo-root-contract.md
      - docs/issues/[CLOSED]-2026-02-04-cabinet-temporary.md
    → docs/adr/ADR-20260515-monorepo-postponed-and-cabinet-temporary.md
    why grouped: both describe the "we don't commit to a monorepo right now"
                  decision; cabinet-temporary is a consequence of that posture

=== Skip (K) ===

  docs/issues/[CLOSED]-2026-03-01-typo-in-readme.md   (doc drift)
  docs/issues/[CLOSED]-2026-03-15-bumped-react-version.md   (ops task)

=== Ambiguous (J) — please review ===

  docs/issues/[CLOSED]-2026-02-22-error-handling-pattern.md
    reason: body is thin but topic (error handling pattern) looks architectural

Counts: individual=N, groups=G (from M issues), skip=K, ambiguous=J
Final ADR count if applied: N + G

Reply with:
  - `apply`                     — promote everything per the plan
  - `apply except <paths>`      — same but exclude listed sources
  - `ungroup #1`                — split group #1 into individual promotes
  - `regroup #1 + <path>`       — add a path into group #1
  - `regroup #1 - <path>`       — remove a path from group #1
  - `skip group #1`             — don't promote group #1 at all
  - `cancel`                    — abort
  - free-form corrections       — adjust verdicts before applying
```

Accept `apply` / `proceed` / `да` / `go` as approval for the whole plan. Anything
unrecognized means stop and clarify.

## Step P5 — Bootstrap target directory if missing

If the target `docs/adr/` (or scope-specific equivalent) doesn't exist:

- **Ask before creating** in promote mode. Bootstrapping a doc location during a
  batch promote is a separate decision — don't bundle it with the promotion approval.
- Create it once approved, install `assets/adr-readme.md` as `README.md`, then proceed.

## Step P6 — Generate each ADR

For each individual `promote` and each cluster group:

1. Read every source issue file **in full**. Do not summarize before generation —
   the issue body is the source of context, same way the chat is in `from-chat.md`.
2. Apply the chat-mode generation steps (`from-chat.md` Steps F2–F3): pick the right
   template variant, fill it in, preserve nuance.
3. The ADR header **must include**:
   ```
   **Source issue:** <path-to-issue>
   ```
   For cluster ADRs use the plural form with all members listed:
   ```
   **Source issues:**
     - docs/issues/[CLOSED]-2026-02-03-no-monorepo-root-contract.md
     - docs/issues/[CLOSED]-2026-02-04-cabinet-temporary.md
   ```
4. For **cluster ADRs**, the body must reconcile context from multiple sources:
   - **Context and Problem Statement** — unify the problem framing across issues.
     If issues had slightly different angles on the same problem, capture all
     angles (don't pick one and drop the others).
   - **Options Considered** — pool rejected options from all source issues. If two
     issues rejected different options for the same reason, list both and cite which
     issue surfaced which rejection.
   - **Decision Outcome** — describe the unified decision. If the cluster represents
     a *posture* (e.g. "we don't commit to a monorepo right now") and the individual
     issues are consequences of that posture, lead with the posture and use the
     consequences as evidence sub-sections.
   - **Consequences & Mitigations** — union of consequences mentioned across sources.
5. Where source issue bodies have gaps (no rejected options, no rationale), do **not
   invent**. Leave a `TODO:` placeholder and surface it in the final report. For
   cluster ADRs, a TODO is acceptable even when one source covers the gap — note
   which source filled it ("rejected options sourced from `<path>`; the other
   sources didn't enumerate them, marked as TODO for verification").

   **Same-chat exception:** if Step P0 marked this run as `same-chat` and the
   current conversation explicitly covered the missing piece (e.g. the user said
   in chat why pnpm was rejected, but the issue body didn't write it down), you
   may fill the gap from chat memory — but cite the source in-line:
   `> Rationale: <text> (sourced from chat, YYYY-MM-DD)`. The cite makes the
   provenance auditable. In `cold audit` runs, do not do this — leave the TODO.
6. Save to the path approved in the gate.

## Step P7 — Delete source issues (gated)

After all ADRs in this run are saved, each source issue has done its job: its
extractable content now lives in the ADR, and the ADR's `Source issue:` header
preserves provenance. Leaving the files behind creates noise in the active issues
directory and makes the `[CLOSED]` set drift over time. There is no `archive/`
directory and there will be no back-links — back-links to deleted files aren't
useful.

Before rendering the gate, preflight every source path:

1. Resolve its canonical path and require it to remain a regular, non-symlink file inside the
   confirmed issues directory.
2. Require every target ADR to exist and contain the expected `Source issue:` or
   `Source issues:` provenance entry.
3. Record a content fingerprint for the source file. Also report whether Git tracks it and
   whether its current contents are committed. Git-backed recovery may be claimed only for a
   tracked, committed version.
4. Mark untracked or locally modified sources `keep-by-default`; they may be deleted only when
   the operator explicitly approves that exact unrecoverable state after seeing it in the gate.

The deletion is **gated** and requires explicit approval. No silent default. Render
the deletion plan as plain markdown (not wrapped in a code block):

```
Source issue deletion plan:

Each source issue below has been promoted to an ADR. Reply with your decision (or
use a bulk option). I will not delete anything until you confirm.

  docs/issues/[CLOSED]-2026-02-15-bun-package-manager.md
    one-liner: choice of Bun over npm/pnpm/yarn with explicit rejections.
    promoted to: docs/adr/ADR-20260515-bun-as-only-package-manager.md
    recovery: tracked and committed
    fingerprint: <hash>
    intent: delete

  docs/issues/[CLOSED]-2026-02-04-cabinet-temporary.md
    one-liner: cabinet classified as temporary migration input.
    promoted to: docs/adr/ADR-20260515-cabinet-temporary-migration-posture.md
    intent: delete (cluster member)

  docs/issues/[CLOSED]-2026-02-03-no-monorepo-root-contract.md
    one-liner: flat git repo, no root workspace contract.
    promoted to: docs/adr/ADR-20260515-cabinet-temporary-migration-posture.md
    intent: delete (cluster member — same ADR as above)

Reply with one or more:
  - `apply`                    — delete all listed source files
  - `apply except <paths>`     — delete the list except the named paths
  - `keep: <path>, <path>`     — leave these source files in place
  - `cancel`                   — keep all source files in place
```

Apply rules:

- Immediately before deletion, re-resolve the path, re-read it, recompute its fingerprint, and
  recheck the target ADR provenance. If anything differs from the gated state, skip that path
  and report the change; approval does not carry across changed content.
- Delete only the exact approved regular file. Prefer the platform's file deletion tool; when
  shell deletion is necessary, use a canonical quoted path with `rm -- "$path"`. Plain `rm`,
  not `git rm` — the operator stages the deletion themselves.
- For cluster ADRs with multiple sources: each member path is listed separately.
  The operator can keep some and delete others, though the usual answer is to
  delete all members together since they're merged into the same ADR.
- For `keep` paths: leave alone. Note in Step P8 that `issue-writer:close` will
  pick them up on the next sweep. (Its pre-extraction check may still flag them
  as `blocked` because the signals are still in the body — at that point the
  operator can `override` since extraction is already complete.)
- For `cancel`: skip deletion entirely. The ADRs remain; the sources remain.

## Step P8 — Final report

Use a compact summary instead of the per-ADR confirmation line (which would be noisy
for batch runs). Output this as **plain prose/markdown, not a code block** — the user
reads it directly, not as a template:

✅ ADR promotion complete.

  Individual promotes (N):
    - docs/adr/ADR-20260515-bun-as-only-package-manager.md

  Cluster promotes (G ADRs from M sources):
    - docs/adr/ADR-20260515-monorepo-postponed-and-cabinet-temporary.md
        sources: 2 issues (no-monorepo-root-contract, cabinet-temporary)

  Skipped (K) — see plan above.
  Ambiguous (J) — left untouched, need your review.

  TODO placeholders left in:
    - docs/adr/ADR-20260515-bun-as-only-package-manager.md  (rejected options)

  Source issues deleted (D): &lt;list of deleted paths&gt;
  Source issues kept (K): &lt;list, with reason if operator gave one&gt;

If the operator chose `keep` for some or all sources, surface this in the report:
"These N source issues remain in `docs/issues/` — they will be picked up by the next
`issue-writer:close` sweep, which re-checks for extractable value (the content is now
in the ADR, so the operator can `override` if the close gate flags them)."

Source issues are deleted by this workflow as the final gated step. The ADR's
`Source issue:` header preserves provenance after the file is gone. Git history is a recovery
source only when preflight proved the issue was tracked and committed; otherwise deletion
requires an explicit unrecoverable-state override. No `archive/` directory is created or
maintained.
