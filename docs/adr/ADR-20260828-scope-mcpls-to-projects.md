# Scope mcpls registration to projects

**Status:** Accepted

**Date:** 2026-08-28

**Scope / Component:** code-intelligence MCP registration

**Supersedes:** None

**Superseded by:** None

**Current contract:** [Project mcpls configuration](../MCPLS_PROJECT_CONFIGURATION.md)

**Related:** None

**Source issue:** None

## Context And Decision Drivers

A user-scoped `mcpls` entry was inherited by every Codex task. Each stdio consumer created an
independent `mcpls` process and child language-server tree. The shared configuration had no workspace
root, so `mcpls` derived it from an ambiguous process working directory; observed sessions fell back
to `/`. The six-server configuration could therefore inspect unrelated filesystem content and repeat
the same indexing across concurrent tasks. More memory would delay pressure without correcting
process fan-out, root ownership, or irrelevant language-server activation.

The immediate fix must work for distinct linked worktrees, preserve unrelated MCP configuration, and
remain explicit because project configuration has harness-specific trust behavior.

## Options Considered

### Keep global registration and add memory

- **Benefits:** No configuration migration and more headroom before swap pressure.
- **Costs / risks:** Preserves one stdio process tree per task, ambiguous roots, and repeated indexing.
- **Why rejected:** It masks the observed lifecycle and scope defects instead of removing them.

### Keep a global registration with one fixed root

- **Benefits:** Eliminates fallback to `/` for one checkout.
- **Costs / risks:** Cannot represent several projects or linked worktrees and still duplicates the
  fixed checkout's index across tasks.
- **Why rejected:** A user-scoped root is inherently wrong for a multi-checkout workflow.

### Add a singleton daemon or thin proxy

- **Benefits:** Could reuse one server tree for multiple tasks in the same checkout.
- **Costs / risks:** Requires verified request multiplexing, client lifecycle isolation, cancellation,
  crash recovery, and compatible LSP ownership semantics.
- **Why deferred:** It is a separate architecture with higher correctness risk and is not required to
  remove global fan-out and unsafe roots now.

### Register mcpls per project checkout

- **Benefits:** Gives each session an exact Git root and only the language servers detected for that
  checkout; configuration can be reviewed with the project.
- **Costs / risks:** Each checkout needs explicit setup and harness trust. Multiple tasks in one
  project may still create multiple `mcpls` processes.
- **Why selected:** It directly removes the global activation and root ambiguity with a small,
  auditable change while keeping worktrees independent.

## Decision

`mcpls` MCP registration is project-scoped only. The global scaffold may remove legacy registrations
but must not create user-scoped entries. Explicit project setup generates a checkout-owned config
with its canonical absolute root (required by `mcpls 0.3.9` for LSP URI initialization) and updates
only supported harness files that already exist. The normative behavior is owned by the
[Project mcpls configuration guide](../MCPLS_PROJECT_CONFIGURATION.md).

## Assumptions And Decision Invariants

- Harnesses continue to launch stdio MCP servers per consumer rather than sharing them natively.
- An exact Git checkout root remains a safer ownership boundary than a user-level working directory.
- System-level installation of `mcpls` and language-server binaries remains independent of MCP
  registration scope.

## Consequences

### Positive

- Tasks outside configured projects no longer start `mcpls` after the harness restarts.
- A configured checkout indexes from its own root and includes only detected stacks.
- Linked worktrees cannot accidentally reuse the primary checkout's root.

### Negative / Trade-offs

- Setup and trust approval are required for each project or worktree.
- Missing language servers remain an operator-managed host dependency.
- This decision does not provide a singleton: concurrent tasks in one project can still duplicate
  `mcpls` and LSP processes.

## Validation And Revisit Triggers

- Verify that global registries contain no `mcpls`, project configs use an explicit generated config,
  and real MCP/LSP smoke processes terminate with their process group.
- Revisit when a harness natively reuses MCP servers per workspace, or when a daemon/proxy proves
  isolation, cancellation, cleanup, and semantic correctness under concurrent sessions.

## References And Follow-ups

- [Codex project configuration and trust](https://developers.openai.com/codex/config-file/config-advanced/#project-config-files-codexconfigtoml)
- [Codex configuration reference](https://developers.openai.com/codex/config-reference/)
