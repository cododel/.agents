# Create / update workflow

## 1. Prove the deferral

Establish:

- the concrete observed problem and why it matters;
- evidence and a stable grep-able locator;
- why fixing it now falls outside the active affected radius or materially increases regression or
  merge-conflict risk;
- enough independent scope that another session can resume it;
- the first next step and observable completion/verification boundary;
- whether an operator decision is still required.

For an explicit deferral, preserve the operator's stated reason and resume conditions. For automatic
technical-debt capture, derive the deferral reason from scope/risk evidence, not from guessed priority.
If the root cause is not proven, label it as a hypothesis and record the next falsifying probe; do not
write a confident diagnosis.

## 2. Discover local ownership and duplicates

Use shared repository discovery to prove one Issues root. Read its README/template and sample 1–2
recent open records. Search distinctive symptoms, identifiers, paths, and root-cause terms before
creating a file.

- Update an existing Issue when ownership/root cause clearly matches.
- Create a related new Issue when evidence proves a distinct root cause, boundary, or completion
  target; link the relationship.
- Ask only when the records are plausibly competing owners and the choice would change historical or
  operator intent.

When no Issues root exists, an explicit deferral or a passed automatic-creation gate authorizes
bootstrapping `docs/issues/` or a proven module-local equivalent with the fallback README/template.
Stop if repository or module scope is ambiguous.

## 3. Write useful resumption context

Match local convention. Otherwise use `../assets/deferred-template.md` and capture:

- title, date, `Open` status, priority, and severity;
- affected scope and stable code/runtime probes;
- problem, evidence, root cause or explicit hypothesis;
- why deferred now and the risk of leaving it unresolved;
- recommended direction without pretending an unresolved design is decided;
- resume conditions/first actions;
- completion criteria and verification;
- related contracts, ADRs, Issues, commits, or task context.

Keep priority (urgency/sequencing) and severity (impact/harm) independent. Unknown material facts use
`TODO:` rather than invented values. Do not paste logs or chat transcripts; preserve decisive excerpts
and source pointers.

For an update, add current evidence and `Last reviewed`; revise stale claims rather than appending an
unbounded diary. Change status/filename only when evidence supports the lifecycle transition.

## 4. Add one useful TODO

When a stable code seam directly exposes the deferred risk, add one concise comment, for example:

```text
TODO(issue): <why this remains unsafe/incomplete>; see docs/issues/<issue-file>.md
```

Adapt syntax and relative path to the language/repository. The comment must remain meaningful without
line-number dependence. Do not add TODOs to generated files, duplicate them across consumers, or use
a TODO as a substitute for a failing test that belongs in the current fix.

## 5. Verify

- path and filename follow local convention;
- status/body and filename agree;
- evidence locators exist and no paths/SHAs are fabricated;
- no duplicate owner remains unlinked;
- TODO link resolves when one was added;
- an established Issues index is updated only when its format is unambiguous;
- `git diff --check` and project documentation checks pass when available.

## 6. Return to the active task

Report the Issue and TODO once, update the task journal when active, and resume the original task. Do
not begin implementing the deferred Issue in the same branch/session unless the operator changes
scope.
