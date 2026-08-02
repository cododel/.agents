---
name: find-docs
description: "Retrieve current, preferably version-exact documentation, API references, and code examples for a named library, framework, SDK, CLI, or cloud service. Use for API syntax, configuration, migrations, setup, CLI usage, library-specific debugging, `документация по X`, or `как настроить X`. Do not use for general web research."
compatibility: Requires network access and either Bun/bunx or Node.js/npm/npx; CONTEXT7_API_KEY is optional.
---

# Documentation Lookup

Retrieve current documentation and code examples using the Context7 CLI. Use `bunx` as the
default launcher: it avoids a global install and is faster in repeated local benchmarks.

```bash
bunx ctx7@latest <command>
```

If Bun is unavailable, use `npx ctx7@latest` as the fallback. Never install `ctx7` globally
just to answer a documentation question.

## Workflow

Two-step process: resolve the library name to an ID, then query docs with that ID.

```bash
# Step 1: Resolve library ID
bunx ctx7@latest library <name> <query>

# Step 2: Query documentation
bunx ctx7@latest docs <libraryId> <query>
```

You MUST call `library` first to obtain a valid library ID UNLESS the user explicitly provides
an ID in the format `/org/project` or `/org/project/version`.

Command budget: one `library` resolution plus up to two focused `docs` queries per question. If
that is insufficient, use the best verified result and state what remains unresolved.

## Step 1: Resolve a Library

Resolves a package/product name to a Context7-compatible library ID and returns matching libraries.

```bash
bunx ctx7@latest library react "How to clean up useEffect with async operations"
bunx ctx7@latest library nextjs "How to set up app router with middleware"
bunx ctx7@latest library prisma "How to define one-to-many relations with cascade delete"
```

Always pass a `query` argument — it is required and directly affects result ranking. Use the user's intent to form the query, which helps disambiguate when multiple libraries share a similar name. Do not include any sensitive or confidential information such as API keys, passwords, credentials, personal data, or proprietary code in your query.

### Result fields

Each result includes:

- **Library ID** — Context7-compatible identifier (format: `/org/project`)
- **Name** — Library or package name
- **Description** — Short summary
- **Code Snippets** — Number of available code examples
- **Source Reputation** — Authority indicator (High, Medium, Low, or Unknown)
- **Benchmark Score** — Quality indicator (100 is the highest score)
- **Versions** — List of versions if available. Use one of those versions if the user provides a version in their query. The format is `/org/project/version`.

### Selection process

1. Analyze the query to understand what library/package the user is looking for
2. Select the most relevant match based on:
   - Name similarity to the query (exact matches prioritized)
   - Description relevance to the query's intent
   - Documentation coverage (prioritize libraries with higher Code Snippet counts)
   - Source reputation (consider libraries with High or Medium reputation more authoritative)
   - Benchmark score (higher is better, 100 is the maximum)
3. If multiple good matches exist, acknowledge this but proceed with the most relevant one
4. If no good matches exist, clearly state this and suggest query refinements
5. For ambiguous queries, request clarification before proceeding with a best-guess match

### Version-specific IDs

If the user mentions a specific version, use a version-specific library ID:

```bash
# General (latest indexed)
bunx ctx7@latest docs /vercel/next.js "How to set up app router"

# Version-specific
bunx ctx7@latest docs /vercel/next.js/v14.3.0-canary.87 "How to set up app router"
```

The available versions are listed in the `library` output. Use an exact indexed version when
available. If it is unavailable, disclose that before using another version or fall back to the
official versioned documentation; never silently substitute the closest release.

## Step 2: Query Documentation

Retrieves up-to-date documentation and code examples for the resolved library.

```bash
bunx ctx7@latest docs /facebook/react "How to clean up useEffect with async operations"
bunx ctx7@latest docs /vercel/next.js "How to add authentication middleware to app router"
bunx ctx7@latest docs /prisma/prisma "How to define one-to-many relations with cascade delete"
```

### Writing good queries

The query directly affects the quality of results. Be specific and include relevant details. Do not include any sensitive or confidential information such as API keys, passwords, credentials, personal data, or proprietary code in your query.

| Quality | Example |
|---------|---------|
| Good | `"How to set up authentication with JWT in Express.js"` |
| Good | `"React useEffect cleanup function with async operations"` |
| Bad | `"auth"` |
| Bad | `"hooks"` |

Use the user's full question as the query when possible, vague one-word queries return generic results.

The output contains two types of content: **code snippets** (titled, with language-tagged blocks) and **info snippets** (prose explanations with breadcrumb context).

## Authentication

Works without authentication. For higher rate limits:

```bash
# Option A: environment variable
export CONTEXT7_API_KEY=your_key

# Option B: OAuth login
bunx ctx7@latest login
```

## Error Handling

If a command fails with a quota error ("Monthly quota reached" or "quota exceeded"):
1. Inform the user their Context7 quota is exhausted
2. Suggest they authenticate for higher limits: `bunx ctx7@latest login`
3. If they cannot or choose not to authenticate, consult official vendor documentation
4. Use training knowledge only as the final fallback and clearly label it as potentially stale

Do not silently fall back to training data — always tell the user why Context7 was not used.

## Common Mistakes

- Library IDs require a `/` prefix — `/facebook/react` not `facebook/react`
- Always resolve first — `bunx ctx7@latest docs react "hooks"` will fail without a valid ID
- Use descriptive queries, not single words — `"React useEffect cleanup function"` not `"hooks"`
- Do not include sensitive information (API keys, passwords, credentials) in queries
