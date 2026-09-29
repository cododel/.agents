# Commit composition

Apply this procedure before staging or creating commits, and when asked to propose or review their
boundaries or messages. Planning and message drafting do not authorize Git mutations. Existing
commits are not permission to amend, squash, or otherwise rewrite history.

## Choose a meaningful unit

A commit contains one coherent outcome with one reason for changing the repository. A reviewer
should be able to explain that outcome in one precise sentence, verify it at that revision, and
understand what reverting it would remove. A task, session, directory, or author is not a commit
boundary by itself.

Keep together the implementation and the artifacts needed to make that outcome correct:

- the fix and its regression coverage, when coverage is warranted;
- a behavior change and its necessary callers, configuration, documentation, and translations;
- a dependency manifest and its lockfile, or a generator/source change and required generated output;
- a schema change and code that must change atomically for that revision to work.

Separate independently useful changes that have different reasons or can be reviewed and reverted
separately. This includes unrelated bug fixes, opportunistic cleanup, and broad formatting changes.
Separate a preparatory refactor from a behavior change when the refactor is behavior-preserving,
independently verifiable, and makes the following change easier to review. Keep small necessary
refactoring with the change when splitting it only creates scaffolding with no useful review boundary.

Do not split by frontend/backend, source/tests, file count, or a desire to make every patch tiny.
Do not bundle unrelated changes just because they share a file, issue, or release. Use scoped hunks
when ownership and dependencies are clear; existing staged work belongs in a commit only when it is
within the operator-authorized scope, not merely because it is already in the index.

## Size and sequence

Choose the smallest complete, reviewable unit, not the fewest lines. There is no fixed line or file
limit. A large mechanical rename may be one coherent commit; two unrelated one-line fixes may need
two commits. For a large patch, look for independent outcomes, preparatory transformations, and
generated noise before accepting its size. If it remains inseparable, briefly explain the coupling
in the commit body instead of creating broken intermediate revisions.

A sequence may have dependencies: each commit must work on top of its predecessors without needing
a later commit to repair it. Put prerequisites first. Do not commit a failing regression test alone
followed by its fix, or separate required callers from an interface change merely to reduce size.
Do not claim every commit is independently cherry-pickable; document non-obvious ordering constraints.

For changes requiring staged rollout, follow the project's compatibility and migration rules.
An additive schema change, compatible consumer change, and later removal can be separate coherent
steps. Git atomicity does not establish deployment atomicity or make a data migration reversible.

Checkpoint timing does not relax coherence: save a completed sub-outcome, not an arbitrary snapshot
with a vague `wip` message. If the operator explicitly requests an incomplete checkpoint, preserve
that intent and disclose its exact limitations. Honor an explicit single-commit or specified-series
request within its authorized scope; an ordinary “commit the changes” does not require bundling
unrelated outcomes. Never rewrite already-created history just to improve grouping without authority.

## Write the message from the selected diff

Follow the applicable project's explicit message rules and tooling. Under the global defaults, use:

```text
<type>(<scope>): <subject>
```

- Choose the type by the outcome: `feat` adds capability, `fix` corrects behavior, `refactor` preserves
  behavior while changing structure, `perf` improves performance, `docs` changes documentation,
  `test` changes tests alone, `build` changes build/dependency machinery, `ci` changes CI, and `chore`
  covers maintenance that fits none of these. A fix with tests is still `fix`; do not use `chore` to
  disguise an unclear bundle.
- Use one stable scope describing the affected subsystem or capability. Prefer established scopes;
  do not join several scopes to accommodate unrelated work.
- Write a concise English imperative subject, starting lowercase, with no final period. Describe the
  resulting behavior or concrete change, not the activity: `fix(auth): reject expired reset tokens`
  rather than `fix(auth): update files`. Preserve exact casing of identifiers. Follow project length
  limits; otherwise favor a readable subject over an arbitrary character quota.
- Add a body only when it helps explain the problem, rationale, significant coupling, compatibility,
  or verification limitations. Do not paste a file inventory, session transcript, or unverified test
  claims. Omit agent attribution and co-authorship trailers under the global defaults.
- For a real breaking contract change, use the repository's supported breaking-change notation
  (`!` and/or `BREAKING CHANGE:`) and explain the incompatibility and required migration. Do not label
  an internal refactor as breaking merely because it touches many files.

Choose the boundary before the message. A title that needs to enumerate unrelated outcomes is a
signal to revisit grouping. Do not use a broad title to hide mixed scope.

## Form and verify the commit

1. Review staged, unstaged, and untracked changes against task ownership. For mixed work, identify
   the intended outcomes, included paths/hunks, and dependency order before staging. A short working
   note is enough; no separate approval or plan document is required for routine grouping.
2. Stage only the chosen unit. Inspect the full staged diff, including deletions, generated files,
   and required untracked inputs. Check that nothing needed remains solely in the working tree and
   that unrelated pre-existing staged work is preserved and excluded from this commit. If the index cannot be
   safely separated with available authority, stop before committing and explain the overlap.
3. Run the proportionate checks required for that unit and inspect `git diff --cached --check`.
   Verification must support the proposed revision: tests of a working tree containing later fixes
   do not prove an earlier staged commit works. For partial staging, use an available safe staged-tree
   check or an authorized isolated disposable reconstruction when needed. Otherwise disclose the
   evidence limit; do not stash, reset, or disturb operator work to obtain a clean test tree. Do not
   create new test infrastructure just to validate a trivial documentation edit.
4. Commit only within existing authority and verification requirements. Let hooks run; inspect any
   changes they produce and recheck affected evidence before retrying. Do not bypass failures or
   silently absorb hook edits from outside the chosen unit.
5. Inspect the resulting commit's message and diff, its SHA, and the remaining staged/unstaged state.
   Report what was committed, decisive checks, and what remains. Distinguish local commits from push.

## Boundary examples

| Changes present | Composition |
| --- | --- |
| Token-expiry fix, regression test, unrelated button spacing | One auth fix with its test; separate spacing change if authorized. |
| New API field, required producer and consumer changes, contract test | One feature commit when an intermediate revision would violate the contract. |
| Behavior-preserving parser extraction followed by new syntax support | Separate refactor and feature when each revision is valid and separately verifiable. |
| Dependency upgrade requiring a call-site adaptation and regenerated lockfile | One build or behavior commit, typed by its main purpose, including all required changes. |
| Broad mechanical rename plus an unrelated logic correction | Separate rename and fix; do not conceal the behavior change in mechanical noise. |
