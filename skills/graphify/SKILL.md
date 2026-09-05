---
name: graphify
description: "Build a code/docs graph on explicit request, or auto-query an existing graphify-out/graph.json for cross-module tracing and review. Verify decisive edges in source; do not rebuild for ordinary local work."
---

# Graphify

Use a graph as navigation evidence; verify decisive relationships in current sources. A graph may
be stale or incomplete and does not grant authority to install tools, send a corpus, or mutate a service.

## Route by intent

- **Query:** when an existing graph can answer a code/docs question, read [references/query.md](references/query.md).
  Do not install, update, detect, or rebuild for a query. If the CLI is absent, read the JSON using
  existing tools; a saved interpreter path is optional and must be checked before executing it.
- **Setup:** only for an authorized setup task, resolve the installed tool and compare its version
  with `.graphify_version`. Use an existing isolated environment. Missing tooling during a build
  is a prerequisite to report, not permission to install or upgrade global packages.
- **Build:** an explicit graph creation request uses [references/run-protocol.md](references/run-protocol.md)
  then [references/build.md](references/build.md). Default corpus is the selected project root.
- **Update / cluster-only:** use the same staging protocol and [references/update.md](references/update.md).
  These are mutations, never inferred from a question about the graph.

The current agent performs semantic extraction with its existing capabilities. Delegate only when
independence or parallelism repays coordination under the global subagent policy. No provider keys,
external LLM backend, model router, or additional orchestration runtime is part of this procedure.

## Optional operations

Load only the reference needed by an explicit request:

- [references/github-and-merge.md](references/github-and-merge.md): remote sources or cross-graph merge;
- [references/transcribe.md](references/transcribe.md): media transcription;
- [references/exports.md](references/exports.md): optional exports and services;
- [references/add-watch.md](references/add-watch.md): adding sources or watching changes;
- [references/hooks.md](references/hooks.md): hook or repository-instruction integration.

These operations retain their own scope and external-action gates. They must not bypass staged
publication when rebuilding the core graph. For help, summarize the relevant modes without executing.

## Result

Report the published output path, relevant graph findings, and material missing evidence. Distinguish
an incomplete run from a published graph. Never claim measured time or usage from placeholder counts.
