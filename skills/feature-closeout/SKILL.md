---
name: feature-closeout
description: "Close an implemented feature change-set across code, tests, living contracts, migrations, mutable Issues, ADR provenance, runbooks, and production-readiness evidence. Use explicitly as `$feature-closeout --quick`, `--full`, or `--release` after feature implementation or before release. Do not use for whole-repository debt cleanup, feature discovery, or repeated audit-fix loops."
---

# Feature Closeout

Bring the current implemented feature and its affected radius to one bounded terminal state. Read
`references/mode-contracts.md` completely for every invocation.

## Usage

```text
$feature-closeout --quick [--base <ref>] [--scope <path>...] [--commit]

$feature-closeout --full [--base <ref>] [--scope <path>...] [--commit]

$feature-closeout --release [--base <ref>] [--scope <path>...] \
  [--evidence <path>...] [--commit]

$feature-closeout --help
```

Treat this as bash-like prompt grammar, not a shell command. Parse arguments before inspecting or
mutating the project.

- Require exactly one of `--quick`, `--full`, or `--release`.
- Print this Usage block verbatim and stop for `--help`, no mode, multiple modes, an unknown flag,
  a missing value, or `--evidence` outside `--release`.
- Accept repeatable `--scope` and `--evidence` values.
- Do not invent `--repo`, manifest, state-file, or model arguments.

## Resolve the target

1. Resolve the current repository root, exact worktree, branch, HEAD, status, applicable
   instructions, and documentation index from the active workspace.
2. Resolve the primary base from repository policy; use `--base` only as an explicit override.
3. Inventory committed changes since merge-base, staged changes, unstaged changes, and relevant
   untracked files. Include only affected call sites, configuration, persistence, interfaces, and
   durable ownership seams.
4. Treat `--scope` as a narrowing constraint, never permission to ignore an affected dependency.
5. Stop with `BLOCKED` when the repository, base, feature change-set, or ownership is ambiguous.

This skill closes one feature change-set. Do not turn it into general historical debt cleanup. Hand
off independent findings outside the affected radius without fixing them.

## Select the mode

- `--quick`: run one shallow, low-risk cleanup pass suitable for a fast model. Do not run
  `$contract-auditor` or claim production readiness.
- `--full`: run a thorough implementation closeout suitable for a strong model. Do not run
  `$contract-auditor` or claim production readiness.
- `--release`: complete the full closeout and rollout preparation, then freeze the final fingerprint
  and run `$contract-auditor` exactly once as the terminal read-only step.

Modes are independent invocations. `--full` includes the useful `--quick` coverage, and `--release`
includes `--full`; no earlier mode is required and no mode invokes another automatically.

## Authority and stop gates

- Treat the selected mode as authority to make only the bounded project changes that mode permits.
- Treat `--commit` as explicit commit authority where repository rules require it. Without it,
  follow the applicable checkout and worktree policy; never infer push, merge, deploy, or database
  authority.
- Stop for a contract conflict, missing contract that needs creation approval, significant new ADR
  decision, destructive action, target drift, independent blocker, or unavailable required evidence.
- Once the terminal audit in `--release` begins, make no further project mutation. A `NOT READY` or
  `UNVERIFIED` verdict ends the invocation; never fix the finding or rerun the audit automatically.

## Report

Return the selected mode, resolved target and base, source and final fingerprints, changes made,
verification commands and exact results, contract impact, Issue/ADR dispositions, independent
hand-offs, commit status, and one terminal status:

- `CLEANED | BLOCKED` for `--quick`;
- `PREPARED | BLOCKED` for `--full`;
- `READY | NOT READY | UNVERIFIED` for `--release`.
