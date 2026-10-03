---
name: find-docs
description: "Resolve an unverified external API, configuration, lifecycle, or migration fact from current primary documentation for the relevant version. Use when implementation or diagnosis depends on that fact; skip facts already established by current local docs and general research."
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

## Sources and retrieval

Use suitable available native reading/search or a configured documentation capability. Respect an
explicit provider choice. Tool selection does not determine source authority: prefer official docs
or primary implementation source applicable to the relevant version. Current vendored/local docs
may already settle the question without retrieval. Community examples can explain usage but must
not override the external contract. Label training-only answers with material stale-risk.

## Workflow

1. Resolve the relevant version from lockfiles, manifests, installed tools or the operator's request.
   Distinguish current installed behavior from the target version of a requested migration.
   Do not silently substitute a nearby version.
2. Form a narrow query from the concrete implementation/debugging need. Never send proprietary code,
   private logs, credentials, or customer identifiers.
3. Retrieve the relevant section, with one focused follow-up as the normal budget. Resolve identity
   or provider failure when needed; use further queries only for a concrete remaining fact. Stop
   when it is established or further retrieval makes no progress, reporting any material gap.
4. Verify examples against the identified version and local language/runtime constraints.
5. Apply the result to repository evidence; documentation proves the external contract, not that the
   local code/config currently follows it.

When the selected provider requires library resolution, resolve its canonical ID before querying.
For an already available documentation CLI, use its installed interface; lookup alone does not
authorize installation or changing package runners/client configuration.

Verify that extraction includes the needed fragment; a successful response is not proof of complete
content. Deduplicate underlying sources: the same page through two backends is one source, and
search ranking is not evidence of correctness.

## Failure contract

- If exact-version docs are unavailable, identify the nearest source/version, verify applicability
  against the installed API/source or a focused probe, and disclose material uncertainty. A version
  mismatch alone is not a blocker; do not claim compatibility that remains unverified.
- If library identity is genuinely ambiguous and choosing one changes the answer, ask.
- If the provider is unavailable/quota-limited, fall back to official docs rather than repeating the
  same query through several wrappers.
- Never invent a signature, flag, config key, or deprecation claim to complete the task.

Return or use the verified behavior concisely, naming the version and source in the task evidence when
material. Do not paste long documentation extracts into the main context.
