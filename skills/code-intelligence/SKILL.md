---
name: code-intelligence
description: Route code discovery through LSP, AST, or literal search according to evidence type. Use for cross-file symbol identity, definitions, references, diagnostics, call hierarchy, rename previews, code actions, or syntax-shaped structural queries. Do not use it merely to search literals, paths, configuration, or documentation.
---

# Code Intelligence

Choose the narrowest available tool that preserves the meaning of the question:

- Use `mcpls` exposed by the active project's MCP registry for definitions, references, symbol
  identity, diagnostics, call hierarchy, and rename previews.
- Use `ast-grep` for syntax-shaped search and bounded structural transformations.
- Use `rg` for literals, paths, configuration, generated text, and documentation.

Treat rename and code-action output as an edit plan. Inspect the affected files, apply only the
scoped change, and verify the result with repository-native tests, type checks, or builds. For an AST
rewrite, first prove the structural query on representative matches and review the resulting diff.

If a preferred tool is absent or broken, use the strongest available fallback, state the loss of
precision when material, and continue when the task remains safe. Pi deliberately receives shared
rules, `ast-grep`, and `rg` without an MCP extension, so do not claim LSP evidence there.
Intelephense may withhold operations such as rename or code actions without a licence; distinguish
that capability limitation from an unavailable PHP server or broken MCP transport.

Never install tooling or mutate an MCP registry implicitly. Global `mcpls` registration is forbidden
because its working directory and language scope are not project-safe. On an explicit setup request,
invoke `$setup-project-mcpls`; it generates a checkout-owned `.agents/mcpls.toml` and updates only
already-existing supported project harness files. Always pass that file through `--config`, never
enable project-config trust globally, and start a new session after changing startup-loaded config.
