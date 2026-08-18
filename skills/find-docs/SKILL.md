---
name: find-docs
description: "Auto-retrieve current, preferably exact-version official docs when work depends on drift-prone library, framework, SDK, CLI, cloud, MCP, or harness behavior. Not for general research or stable language concepts."
---

# Current Documentation Lookup

Prevent API guessing and stale-library reasoning with the smallest relevant documentation pull.

## Trigger

Invoke automatically when the task depends on:

- exact API signatures, configuration keys, CLI flags, lifecycle behavior, or migration guidance;
- a library/framework/harness version not already verified in current repository evidence;
- a runtime error whose meaning depends on current vendor behavior;
- setup of MCP, worktrees, permissions, hooks, providers, or cloud services;
- uncertainty between neighboring versions or recently changed behavior.

Do not invoke for general programming concepts, business logic, ordinary local refactoring, or facts
already proven by vendored/current project documentation.

## Source order

1. configured current-docs/MCP provider available in the harness;
2. official vendor documentation or primary source for the exact version;
3. an installed docs CLI/provider already declared by project/global configuration;
4. Context7 CLI as a last local launcher fallback;
5. training knowledge only when no current source is available, explicitly labeled stale-risk.

Prefer primary sources. Community examples may explain usage but must not override official contracts.

## Workflow

1. Resolve the exact installed/requested version from lockfiles, manifests, CLI output, or the
   operator. Do not silently substitute a nearby version.
2. Form a narrow query from the concrete implementation/debugging need. Never send proprietary code,
   private logs, credentials, or customer identifiers.
3. Query one provider/source, then at most one focused follow-up for the unresolved detail. Pull only
   the relevant section rather than an entire manual.
4. Verify examples against the identified version and local language/runtime constraints.
5. Apply the result to repository evidence; documentation proves the external contract, not that the
   local code/config currently follows it.

When the configured current-docs provider supports library resolution, resolve the canonical library
ID first. If no provider is configured and Context7 CLI is available, use an ephemeral launcher
without global installation, preferring the project's existing package runner; otherwise use:

```bash
npx ctx7@latest library <name> "<focused query>"
npx ctx7@latest docs <resolved-library-id> "<focused query>"
```

Do not install or choose Bun/npm/pnpm merely for this skill when another configured source is
available.

## Failure contract

- If exact-version docs are unavailable, disclose the nearest source/version before using it.
- If library identity is genuinely ambiguous and choosing one changes the answer, ask.
- If the provider is unavailable/quota-limited, fall back to official docs rather than repeating the
  same query through several wrappers.
- Never invent a signature, flag, config key, or deprecation claim to complete the task.

Return or use the verified behavior concisely, naming the version and source in the task evidence when
material. Do not paste long documentation extracts into the main context.
