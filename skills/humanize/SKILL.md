---
name: humanize
description: "Rewrite supplied prose to remove formulaic AI patterns while preserving facts, intent, tone, evidence, and required structure. Use for explicit humanize, de-AI, voice-matching, or synthetic-writing review requests; not for proofreading, translation, summarization, or inventing a new persona."
metadata:
  version: "2.6.0-adapted"
  source: "https://github.com/blader/humanizer"
  license: "MIT"
---

# Humanize

Make supplied writing sound like a specific person addressing its real audience. Remove synthetic
patterns without changing what the text claims or manufacturing personality that the source does not
support.

## Trigger and mode

Use this skill when the operator explicitly asks to humanize, de-AI, de-slop, remove LLM tells,
match a supplied voice, or review prose for synthetic phrasing. Do not invoke it merely because a
task produces user-facing text. Ordinary proofreading, translation, summarization, and fresh copy
creation remain separate tasks unless the request also includes this intent.

Choose the mode from the request:

- **Rewrite:** return a revised version of inline text.
- **File edit:** edit only the named file or section when the request authorizes the change.
- **Audit:** identify material synthetic patterns without rewriting unless asked.
- **Voice match:** calibrate from writing that the operator identifies as the target voice.

Do not require a voice sample. When none is supplied, preserve the source's apparent register and
make the smallest rewrite that solves the stated problem.

## Invariants

Preserve:

- factual claims, names, numbers, quotations, citations, and confidence levels;
- causal relationships, chronology, conditions, caveats, and technical meaning;
- the intended audience, genre, tone, length constraints, and required structure;
- deliberate terminology, brand language, legal wording, and repository conventions unless the
  operator explicitly asks to change them.

Never invent anecdotes, sources, measurements, opinions, emotions, first-person experience, or
concrete scene details to make prose feel human. Do not strengthen certainty, turn correlation into
causation, or remove a necessary disclaimer. If a natural rewrite requires information the source
does not contain, preserve the uncertainty or ask one narrow question.

Human writing is not defined by slang, messiness, contractions, short sentences, or arbitrary
punctuation preferences. Use those only when they fit the established voice and context. Technical,
legal, academic, and operational prose may appropriately remain structured and restrained.

## Workflow

### 1. Freeze the semantic invariant

Identify what must remain true after the rewrite: the claim, evidence, confidence, requested action,
and any fixed wording or formatting. For a file, inspect nearby prose and project language before
editing so the section remains locally consistent.

### 2. Calibrate voice when evidence exists

From a supplied sample, observe sentence rhythm, vocabulary, paragraph openings, punctuation,
directness, humor, use of first person, and transition style. Match recurring tendencies without
copying distinctive phrases or exaggerating quirks. Treat the sample as evidence, not permission to
impersonate a different author or fabricate their experiences.

### 3. Diagnose before rewriting

Look for clusters rather than banning individual words. Common signals include inflated significance,
promotional adjectives, vague attribution, empty conclusions, repetitive rhetorical symmetry,
formulaic transitions, excessive sectioning, and chatbot correspondence accidentally left in the
text.

Read [references/patterns.md](references/patterns.md) for a broad audit, a stubborn passage, or an
explanation of which patterns changed. Ordinary rewrites do not need the full catalog.

### 4. Restore material grounding

When a sentence is a polished verdict without an inspectable situation, recover only the
source-backed chain:

```text
actor -> action -> object or material -> result -> discrepancy -> evidence
```

Lead with the action, observation, or concrete state when that makes the claim easier to verify.
Do not fabricate missing fields. A short hook or title may remain compressed, but it should compress
an understood fact rather than replace it with a slogan.

### 5. Rewrite at the right radius

- Remove padding and chatbot artifacts before changing vocabulary.
- Replace vague claims with existing specifics; if none exist, narrow the claim.
- Prefer direct subjects and verbs when they make ownership clearer.
- Vary rhythm naturally, but do not force sentence-length randomness.
- Collapse repetitive headings, lists, or parallel clauses only when they add no navigation value.
- Retain useful repetition, domain terms, formatting, and genre conventions.
- Apply the same voice to connected titles, captions, calls to action, and conclusions only when they
  are in scope.

Do not perform a synonym sweep. A rare word, em dash, bold label, passive construction, or group of
three is evidence only in context; it is not automatically an AI tell.

### 6. Run a final evidence and voice pass

Compare the rewrite with the source. Check that every factual detail and qualification survived, no
new claim appeared, and the result reads naturally aloud for its audience. Remove remaining canned
transitions or suspiciously polished verdicts. Do not expose private chain-of-thought or manufacture
an internal critique transcript.

## Output

Default to the final rewrite only. Add a short change summary when it helps review or when the user
asks what changed. For an audit, report the few highest-impact patterns with precise excerpts or
locations. For file edits, preserve unrelated content and summarize the affected sections; show a
full before/after only when requested or short enough to be useful.

If the source contains unsupported claims, distinguish them from style problems. Humanization must
not launder weak evidence into more convincing prose.

## Attribution

Adapted from [blader/humanizer](https://github.com/blader/humanizer), originally by Siqi Chen and
distributed under the included [MIT license](LICENSE). This portable adaptation retains the useful
pattern taxonomy while removing client-specific tool instructions and any guidance that could
encourage invented facts or experiences.
