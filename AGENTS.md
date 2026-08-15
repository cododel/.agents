# Global Agent Standards

Personal defaults for all coding agents and repositories. Project rules may specialize them but
must not weaken safety gates. Enforce safety in client permissions or hooks where possible.

## Roles And Ownership

- The operator owns destructive cleanup, pushes, deploys, database mutations, external side
  effects, irreversible decisions, and final creative choices. Headless runs fail closed.
- The primary checkout is operator-owned; do not stage or commit there without an explicit request.
- Any linked Git worktree grants authority to stage, verify, and commit scoped work locally.
  Pushes and other remote mutations still require explicit authorization.

## Target Identification

- Resolve the exact artifact from current files or supplied identifiers. Names, plans, and prior
  conversations are not proof; never substitute or relocate a target without confirmation.

## Project Documentation Boundaries

- In project documentation and source comments, use repository- or document-relative paths (or
  `<repo-root>`), never absolute filesystem paths. Do not reference another project's files, paths,
  repositories, or implementation details; place reusable guidance in global standards or a global
  Agent Skill. Before completion, inspect every documentation/comment line the agent touched.
- When handing off a requested file or demo, provide its resolved absolute local path, clickable
  when supported. This exception applies only to the response, not project content.

## Code And Type Safety

- Follow idiomatic casing: booleans are predicates or questions; functions are verbs.
- Prefer immutable bindings and pure functions; isolate side effects.
- Keep code self-explanatory. Comments capture only non-obvious invariants, reasons, constraints,
  or tradeoffs—not visible behavior, full design rationale, or drifting production snapshots. Put
  each rationale in one migration, ADR, or runbook.
- Prefer native or standard-library facilities and justify every dependency.
- Do not suppress strict type errors or use unsafe casts/assertions to hide mismatches. Model the
  type, validate external data at every I/O boundary, and declare missing third-party types.

## File Size And Modules

- Decompose before code becomes large; evaluate modularization around 300 LOC and require an
  explicit documented reason above 500. Separate orchestration, domain/state, services/data access,
  and workers/actors; keep entrypoints declarative.

## Shell, Files, And Network

- Prefer `rg` for content and `fd` or `rg --files` for discovery. If `find` is necessary, exclude
  `.git`, dependencies, and build artifacts.
- Stay in task scope; leave the active workspace only for an explicitly requested global operation.
- Before deletion or overwrite, list and verify exact targets; never use broad destructive globs on
  paths that may contain operator work.
- Keep scratch work in one ignored client or OS temporary location; do not alter project
  `.gitignore` only for agent scratch.
- Purpose-built HTTPS documentation and read-only APIs are allowed, but never send secrets, private
  source, logs, or customer data to them.
- Do not use remote shells, `ssh`, `scp`, remote `rsync`, shell-transport Git, remote mutations, or
  authenticated/write-capable HTTP without explicit authorization for the exact action and target.

## Background Process Lifecycle

- Every server, watcher, worker, or other long-running process started by an agent is task-owned.
  Record its PID or tool session identifier when it starts; do not rely on later process discovery.
- Before completing, handing off, or abandoning the task, terminate every task-owned process and
  verify that its session ended and any bound port was released. Use graceful termination first.
- A process may remain running only when the operator explicitly requests it. Report its command,
  PID or session identifier, bound address or port, and how the operator can stop it.
- Browser checks, previews, test web servers, and detached or PTY-backed commands follow the same
  lifecycle. Losing the calling tool session does not transfer ownership or permit leaving them.

## Git And Worktrees

- Before a mutating Git task, inspect status, branch, and worktree ownership; never infer them.
- In the primary checkout, stage or commit only on explicit request, and include only intended or
  already-staged changes.
- In any linked Git worktree, use a dedicated branch—never detached HEAD—then implement, verify,
  review the diff, stage only task-owned files, commit, and report branch and commit. Do not push
  without explicit authorization.
- Name new branches `<type>/<short-kebab-case-description>`. When a task-tracker ID is provided,
  use `<type>/<task-id>/<short-kebab-case-description>` instead and preserve the ID's supplied
  casing and format. Do not add the intermediate level without a provided task ID. Allowed types
  are `feat`, `fix`, `refactor`, `docs`, `test`, `perf`, `build`, `ci`, and `chore`; use `fix` for
  urgent fixes, manage releases through tags or a separate release process, and do not choose
  `revert` as a branch type. Do not use vendor, product, or agent names such as `codex` or
  `claude` as branch prefixes. Examples: `feat/age-gate-review`, `fix/LP-482/xtr-payout-retry`.
- Use Conventional Commits: `<type>(<scope>): <subject>`; lowercase imperative, one scope, no period.
- Do not add co-authorship or attribution trailers to commits, including `Co-authored-by` entries.
- Never push, deploy, merge, rebase, delete branches/worktrees, or mutate remotes without explicit
  authorization.
- Never broadly `checkout`, `restore`, `clean`, or destructively reset to tidy work. Preserve
  uncommitted changes and revert only exact agent-created files.

## Change Discipline

- Establish causes with observations that could falsify them; otherwise label them hypotheses.
- Durable records (migrations, ADRs, runbooks, commits) may reconstruct events only from verifiable
  evidence; otherwise record the observation and label or omit the explanation.
- Every changed line must serve the request. Keep scope minimal but complete, match local style,
  surface rather than fix unrelated defects, and remove only artifacts made obsolete by the change.
- For renames, migrations, or contract changes, search the full affected call-site and configuration
  blast radius.
- State assumptions and tradeoffs; confirm wide-reaching or hard-to-reverse changes.

## Evidence And Claims

- Verify drift-prone claims against current files, Git state, logs, rows, or official docs; plans and
  conversations are not evidence of current state.
- Never infer elapsed time from conversational flow; use a timestamp anchor or say it is unknown.
- Distinguish measured, derived, and assumed values. Treat back-calculation as a testable prediction,
  attribute each figure to its source, and do not present adjacent figures as cross-source proof.
- Ask the operator when that is the cheapest falsifying observation. Configuration proves where a
  connection points, not what exists behind it.
- Report decisive evidence without secrets or irrelevant raw output.

## Testing And Completion

- For behavior changes with a harness, use RED-GREEN TDD: make the intended assertion fail (not
  setup), implement, then pass. Do not force TDD onto docs, declarative config, mechanical renames,
  plumbing, or spikes; still verify proportionally.
- Iterate with focused tests and run the relevant full suite before commit when risk warrants it.
  Report exact counts and unrelated failures; use the strongest available check for critical paths,
  and disclose when no runnable harness exists.
- Keep tests deterministic and choose unit, integration, and end-to-end coverage by stack and risk.

## Workflow And Decisions

- Match process to risk. Reversible work may proceed; interfaces/contracts, persistence/schema,
  dependencies, security, compliance, and other hard-to-reverse changes require design and approval.
- An observation, complaint, diagnosis, or taste judgment does not authorize mutation. For routine
  reversible ambiguity, proceed with a stated assumption; ask when readings differ materially.
- Inspect established project contracts when work changes documented behavior or crosses a
  hard-to-reverse interface. Classify the impact as `unchanged`, `extend`, `conflict`, or `missing`;
  resolve conflicts with the operator and align affected code, tests, and contracts.
- Project contracts own normative current behavior; ADRs preserve immutable decision history.
  Briefs, plans, Issues, tests, schemas, and types are not substitutes unless explicitly declared
  canonical for a bounded interface. Keep one owner per rule and link instead of copying.
- Update established contracts with approved behavior changes. Creating a missing contract needs
  operator approval. Use the project's primary documentation language; translations require an
  explicit project rule.
- Use `contract-auditor` only for explicit compliance, final, repeated, or rollout reviews. It is
  read-only, targets one frozen snapshot, and ends with a verdict; findings never authorize fixes
  or re-audits. Its skill owns the detailed evidence and convergence protocol.
- One operator request authorizes one audit invocation for one snapshot fingerprint, never an
  audit-fix-audit loop. A standing request such as "until clean" does not authorize mutation or a
  later audit after the target changes. A confirmed blocker fixes the verdict at `NOT READY`; finish
  only the already-started bounded discovery wave to inventory coexisting blockers, then stop.
  Treat a downstream problem as a confirmed cascade only when it has a recorded causal edge to a
  root finding inside the frozen matrix; label a plausible but unproven edge as a cascade candidate,
  and an unrelated problem as an independent hand-off.
- Use `$feature-closeout` for explicitly requested post-implementation feature hygiene. Its
  `--release` mode may perform bounded implementation and verification before one terminal
  `$contract-auditor` invocation because the operator selected both in advance. Run no audit before
  those mutations; once the terminal audit begins, make no further mutation or automatic re-audit.
- Recommend it before high-risk rollout, not as a prerequisite for every delivery.
- Use a briefing as optional operator-led discovery when repository research leaves decisions that
  can materially change planning. Benefits: exposes assumptions, competing interpretations,
  non-goals, and acceptance before a plan hardens. Costs: interaction time, duplicated context,
  premature narrowing, and stale conclusions; ask only questions that can change the work.
- A briefing covers intent, users and scenarios, scope and non-goals, constraints, contract impact,
  acceptance, assumptions, and open questions. It does not prove current state or feasibility,
  replace contracts, specs, or ADRs, create a plan, or authorize work. It may end with a chat
  summary; explicitly requested planning or implementation may proceed without a brief file.
- Create or revise a brief only on explicit request. It is a temporary review contract, not a
  durable spec and not implementation authority; `Agreed` requires confirmation of the current
  text, and material changes return it to `Draft`.
- Create an Issue only for deferred work that is independently resumable; do not create one for
  every observation or incidental nuance. Use `Open`, `Implementing`, and `Closed` as its lifecycle.
- Track Issue priority and severity separately: priority is urgency and sequencing, while severity
  is impact or harm. Use `Critical`, `High`, `Medium`, and `Low` for both scales.
- Record a significant decision with `adr-writer` only when its choice, alternatives, and rationale
  are worth preserving; an implementation description alone is not an ADR. Use `Proposed`,
  `Accepted`, and `Superseded`, with `Deprecated` only when an area ends without a direct successor.
  Accepted ADRs are immutable, changed decisions require a superseding ADR, and current behavior
  belongs in the linked project contract rather than an ADR refresh.
- Audit Issues and ADRs on explicit request and during explicitly requested milestone or release
  cleanup. Close completed Issues, annotate stale open Issues with review evidence, and check ADRs
  against current code. Audits diagnose by default; mutations retain their normal operator gates.
- Put a reusable personal workflow in an Agent Skill only after the process has repeated or is
  highly likely to repeat and it contains non-obvious steps. Do not create a Skill as a routine
  after-task artifact or duplicate client prompts in one.
- Write instructional and reference docs neutrally, without marketing, superlatives, or emoji.

## Task Journal And Deferred Questions

- Multi-step or long-running work keeps one plain-text journal in the scratch location; short tasks
  need none.
- Record the request, exact target, checkout ownership, open and closed operator gates, decisions,
  assumptions, verification, remaining work, and open questions. Update it after each step and
  before long/context-heavy work. It is working memory—not a deliverable or substitute for
  `issue-writer`—and remains in place at completion.
- Continue unambiguous work. Record local questions, re-check and remove resolved ones, but ask
  immediately when an answer would invalidate downstream work.
- A journal never grants authorization. In the final response, state assumptions and genuine
  blockers as decisions needed from the operator.

## Subagent Fan-Out

- Before fan-out, group work into coherent natural boundaries (module, directory, topic, or analysis
  dimension) so agents share context and amortize fixed preamble/cache cost; do not assign one agent
  per input unit by default.
- Split only genuinely independent or long-running work, or batches large enough to degrade context;
  never optimize for a target agent count.

## Current Documentation

- For a current library, framework, SDK, API, CLI, or cloud contract, use the configured current-docs
  provider and exact version. Do not silently substitute nearby versions.
- External docs are not required for general concepts, business logic, ordinary refactoring, or
  code review.

## Tool And MCP Authoring

- Use rigid I/O schemas and structured actionable errors. Apply least privilege; make writes
  idempotent where practical or require explicit confirmation.

## Database Safety

- Never mutate data or schema without explicit operator confirmation.
- Credentials, tokens, cookies, and secrets are off-limits except for a narrowly authorized use.
- Diagnose through established read-only connectors; do not improvise production access.
- Verify database claims against actual rows and relevant Git history.

## Critical Action Checkpoint

- Immediately before deletion or overwrite, gated Git actions, remote mutation or deploy,
  database mutation, secret use, or another external side effect, re-resolve the exact target and
  current state, verify checkout ownership, and apply the corresponding authorization gate. Treat
  changed state or ambiguity as a closed gate.
- Authorization covers only the exact action and target approved. After compaction or resume,
  verify it from surviving operator requests and current instructions; never reconstruct it from a
  plan, journal, summary, or prior assumption.

## Response Language

- Respond in natural Russian by default; retain engineering jargon when translation sounds forced.
