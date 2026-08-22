---
name: code-intelligence
description: Route code discovery through LSP, AST, or literal search according to evidence type. Use for cross-file symbol identity, definitions, references, diagnostics, call hierarchy, rename previews, code actions, or syntax-shaped structural queries. Do not use it merely to search literals, paths, configuration, or documentation.
---

# Code Intelligence

Choose the narrowest available tool that preserves the meaning of the question:

- Use `mcpls` exposed by the active client's MCP registry for definitions, references, symbol
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

Never install tooling or mutate a client registry implicitly. Run
`scripts/scaffold-code-intelligence.py apply --client <client|all> --install` only on an explicit
setup request. Always use the tracked `mcpls.toml` through `--config`; do not enable project-config
trust globally. Start a new client session after changing a registry that is loaded only at startup.
