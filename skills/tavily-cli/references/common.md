# Tavily CLI runtime contract

Apply this contract from every Tavily CLI skill.

## Selection

Tavily supplies web evidence; the agent owns source selection and final conclusions. Follow the
global web-tool policy in `../../../AGENTS.md`. Select Search for an explicit request, unavailable
suitable native search, a specific evidence gap, additional source discovery, or needed Tavily
filters. Prefer suitable native reading for an ordinary known page; choose Extract directly for
batch Markdown/text or difficult extraction, Map for site URL discovery, and Crawl for a bounded
site corpus. Do not require a failed native call when the task already establishes the need.

Research requires an explicit user request to delegate synthesis to Tavily. Generic research,
comparison, a missing native tool, or a request merely to search through Tavily is insufficient.
Search failure never authorizes escalation to Research.

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

Classify a non-zero exit using the global tool-failure policy. Correct invalid input against the
installed schema; bound retries for transient reads and honor rate-limit guidance. Retain successful
URLs on partial failures and report the missing coverage. After an uncertain write, reconcile its
state or use documented idempotency before repeating it.

When Tavily was optional, an unavailable CLI, authentication prerequisite, or service failure may
justify an already authorized retrieval alternative; do not require a new key solely to continue.
Disclose material coverage differences. An explicit Tavily request remains a provider constraint:
report the limitation rather than silently switching. Never bypass access restrictions, and never
escalate to Research without its explicit delegation gate.
