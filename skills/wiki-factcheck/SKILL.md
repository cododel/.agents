---
name: wiki-factcheck
description: "Manually fact-check selected pages in Alexander's personal LLM Wiki using authoritative web sources, classify claims as confirmed, contradicted, unverified, or opinion, and write a dated evidence readout only after exact approval. Use when the user asks to verify Wiki facts or prepare a selected page for publication. Never runs scheduled or automated fact-check workflows."
---

# Wiki Factcheck

Use `/Users/cododel/Documents/LLM-Wiki` and its `SCHEMA.md` as the contract. This skill is a manual, bounded workflow; it does not run queues, background jobs, or legacy automated fact-check tooling.

## Investigate without writing

1. Use `$wiki-context` and identify the exact pages or publication scope. Exclude raw sources and do not label hypotheses, subjective judgments, or authorial voice as factual errors.
2. Extract discrete, externally verifiable claims. Ignore ephemeral prices, counters, and similar lookup facts unless the schema identifies their value as tracked knowledge.
3. Search primary sources first: official documentation, releases, APIs, vendor material, standards, or original research. Read enough source material to compare each claim.
4. Classify each claim exactly once:
   - `confirmed` — supported by an authoritative source;
   - `contradicted` — directly conflicts with an authoritative source;
   - `unverified` — no adequate confirmation found, not proof of falsehood;
   - `opinion` — not a factual claim.
5. Report findings and propose the exact dated readout, append-only ignored `.factcheck-log.md`, validation, commit, and push. Do not modify the checked pages.

## Write only after approval

After explicit scope confirmation, append the operational log and create the agreed readout under `readouts/`. Keep `sources: []` unless the readout cites material preserved in `raw/`; refer to checked Wiki pages with resolvable Obsidian wikilinks, never bare Markdown paths.

Run the current lint for the generated readout. If `bad_sources` or `bad_wikilinks` are non-zero, stop before delivery and report the defect. Before Git mutation, verify vault, `main`, `HEAD`, `origin/main`, status, and the exact approved path set. Stage only the readout, create one Conventional Commit, and push it to `origin/main`; keep the ignored operational log out of the commit.
