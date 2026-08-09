---
name: find-docs
description: "Retrieve current, preferably version-exact documentation, API references, and code examples for a named library, framework, SDK, CLI, or cloud service. Use for API syntax, configuration, migrations, setup, CLI usage, library-specific debugging, `документация по X`, or `как настроить X`. Do not use for general web research."
---

# Documentation Lookup

Use Context7 without a global install. Prefer `bunx ctx7@latest`; fall back to
`npx ctx7@latest` when Bun is unavailable.

## Workflow

1. Form a focused query from the user's intent without secrets, personal data, or proprietary code.
2. Unless the user supplied `/org/project` or `/org/project/version`, resolve first:

   ```bash
   bunx ctx7@latest library <name> "<focused query>"
   ```

3. Select the exact project by name, relevance, source reputation, coverage, and version. Then query:

   ```bash
   bunx ctx7@latest docs <library-id> "<focused query>"
   ```

Use one resolution and at most two focused documentation queries per question. Prefer an exact
indexed version when the operator named one. If it is unavailable, disclose that before using
current official versioned docs; never silently substitute a nearby release.

## Failure contract

If resolution is ambiguous, ask. If Context7 has no good source, quota is exhausted, or the result
does not answer the question, say so and fall back to official vendor documentation. Use training
knowledge only last and label it potentially stale. Never expose Context7 authentication values.

Answer with the verified syntax or behavior and identify the version/source actually used.
