---
name: code-intelligence
description: Route code discovery through LSP, AST, or literal search according to evidence type. Use for cross-file symbol identity, definitions, references, diagnostics, call hierarchy, rename previews, code actions, or syntax-shaped structural queries. Do not use it merely to search literals, paths, configuration, or documentation.
---

# Code Intelligence

Choose the narrowest available tool that preserves the meaning of the question:

- Use LSP tooling only when it is already exposed by the active client or project for definitions,
  references, symbol identity, diagnostics, call hierarchy, and rename previews.
- Use `ast-grep` for syntax-shaped search and bounded structural transformations.
- Use `rg` for literals, paths, configuration, generated text, and documentation.

Treat rename and code-action output as an edit plan. Inspect the affected files, apply only the
scoped change, and verify the result with repository-native tests, type checks, or builds. For an AST
rewrite, first prove the structural query on representative matches and review the resulting diff.

If a preferred tool is absent or broken, use the strongest available fallback, state the loss of
precision when material, and continue when the task remains safe. Never install tooling or mutate an
MCP registry implicitly.
