# Tavily CLI runtime contract

Apply this contract from every Tavily CLI skill.

## Readiness

1. Run `command -v tvly` and `tvly --status`.
2. If the CLI is missing, report the prerequisite and ask before installing. Supported upstream
   paths include the official installer and `uv tool install tavily-cli`; never pipe a remote
   installer into a shell without operator authorization.
3. `search` and `extract` can run without a key subject to the CLI's current rate cap. `map`,
   `crawl`, and `research` require `TAVILY_API_KEY` or `tvly login`. Do not print, inspect, or store
   keys in output.

## Current command contract

Run `tvly <command> --help` immediately before composing a non-trivial invocation. Help from the
installed CLI is authoritative for flags, ranges, defaults, and auth requirements; do not rely on
a copied option table. Quote queries and URLs.

## Output and isolation

- Prefer `--json` for programmatic work and parse only the fields needed by the task.
- Use `-o` or `--output-dir` only when the operator requested a file or bulk download; resolve the
  exact destination and normal mutation gates first.
- Bound result/page counts and printed excerpts. Raw JSON, raw page bodies, and crawl corpora stay
  out of the main context unless the user explicitly needs them.

## Errors

Treat a non-zero exit as a failed operation. Report the command category and actionable error
without secrets. Do not silently switch tools after auth, rate-limit, invalid-input, timeout, or
API failures. For rate limits, honor server/CLI retry guidance; for auth, ask the operator to log in
or provide the key through the established environment; for partial extract/crawl failures, retain
successful URLs and list failed URLs separately.
