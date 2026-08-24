# Session History (Layer 3)

Optional client-neutral adapter for locating and mining past agent-session transcripts. Run it only
after explicit user approval and only against a bounded transcript directory supplied by the user or
already exposed by the current execution environment. `scripts/scan_sessions.py` implements all of
this; read this file to understand it and to debug compatible layouts. The guiding principle is
**discover, don't hardcode**: transcript layouts and JSONL schemas drift, so match on stable signals
(`cwd` plus readable message text), not a client-specific path.

---

## Transcript input

- Require `--transcript-dir <directory>`; never guess a client configuration root.
- The directory may contain JSONL files directly or below a `projects/` subtree. Treat that subtree
  as a discovery hint, not a required layout.
- If the environment exposes an exact current transcript path, pass its bounded parent directory
  rather than scanning a broader user-data root.

## Discovery strategy (in order)

1. Glob `<transcript_root>/projects/**/*.jsonl`. If empty, fall back to a bounded
   `<transcript_root>/**/*.jsonl`.
2. For each candidate, determine its `cwd` by scanning the first lines for a `cwd` field.
   Keep it only if `cwd` equals the target root or is a descendant of it. Never include a broad
   ancestor session merely because the target project sits below its cwd.
3. **Fallback match** when no `cwd` is found: require exact equality between the parent
   directory name and sanitized project root (`re.sub(r"[/.]", "-", root)`).
4. If still nothing matches, do not force it — return empty and let the caller proceed with
   Layers 1–2, noting history was unavailable.

## Parsing (defensive)

- JSONL: one JSON object per line. Wrap every `json.loads` in try/except and skip bad lines —
  partial/streamed transcripts and version differences are normal.
- A message entry typically has a `type` (`"user"` / `"assistant"`) or `role`, and a `message`
  object whose `content` is either a string or a list of blocks. For block lists, take blocks
  with `type == "text"` and read their `text`. Ignore tool-use / tool-result / image blocks and
  large outputs.
- Be tolerant of unknown shapes: if you can't find structured content, skip the entry rather
  than crashing.

## What to extract — and what NOT to

- **Extract only design-relevant, human-readable snippets:** discussion of color/palette,
  typography/fonts, spacing/radius/borders, components and their states, layout/grid, motion,
  branding/voice, and aesthetic direction. The script filters by a bilingual (EN/RU) keyword set.
- **Weight user corrections heavily.** When a past session shows the user rejecting a direction
  or correcting the agent ("no, keep it pure black", "radius should be 0"), that is among the
  strongest evidence of the real design intent.
- **Privacy / minimization (required):**
  - Never copy whole transcripts into the output document or into context wholesale.
  - Snippets are short and truncated; tool output and non-design chatter are dropped.
  - Drop lines containing likely secrets, credentials, authorization headers, private keys,
    or password/token assignments. Keyword filtering is not secret redaction by itself.
  - In the final document's provenance footer, state only that session history was *consulted*
    (and roughly how many sessions matched) — do not quote private/unrelated content.
- If transcripts are found but none are design-relevant, treat Layer 3 as empty and say so.
