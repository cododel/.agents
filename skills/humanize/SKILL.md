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

Apply only when the request includes humanization, matching a supplied voice, or reviewing synthetic
phrasing. Producing user-facing text, proofreading, translation, summarization, or fresh copy alone
does not activate this skill.

Choose the mode from the request:

- **Rewrite:** return a revised version of inline text.
- **File edit:** edit only the named file or section when the request authorizes the change.
- **Audit:** identify material synthetic patterns without rewriting unless asked.
- **Voice match:** calibrate from writing that the operator identifies as the target voice.

Do not require a voice sample. When none is supplied, preserve the source's apparent register and
make the smallest rewrite that solves the stated problem.

## Invariants

Preserve:

- factual claims and their scope, names, numbers, quotations, attribution, citations, and confidence
  levels;
- causal relationships, chronology, conditions, caveats, and technical meaning;
- the intended audience, genre, tone, length constraints, and required structure;
- deliberate terminology, brand language, legal wording, and repository conventions unless the
  operator explicitly asks to change them.

Never invent anecdotes, sources, measurements, opinions, emotions, first-person experience, or
concrete scene details to make prose feel human. Do not strengthen certainty, turn correlation into
causation, narrow an assertion, remove attribution, or drop a necessary disclaimer merely to improve
style. Changing meaning requires an explicit semantic-edit request; humanization alone is not that
authority. If a natural rewrite requires information the source does not contain, preserve the
uncertainty or ask one narrow question.

Use the source's or supplied sample's voice. Do not manufacture a persona through slang,
messiness, or punctuation; structured and restrained prose may fit the genre.

## Workflow

Identify the claims, evidence, confidence, requested action, and fixed wording before rewriting.
For a file, inspect nearby prose and project language. Calibrate recurring vocabulary, rhythm,
punctuation, directness, and humor from any supplied voice sample without copying distinctive
phrases or exaggerating quirks; a sample does not authorize impersonation or invented experience.

Diagnose phrasing in context rather than banning words. These are editorial heuristics, not proof
of AI authorship: describe the wording and its effect, without inferring who or what wrote it.
Read only the relevant sections of [references/patterns.md](references/patterns.md) for a broad audit,
a stubborn passage, or an explanation of specific patterns. Ordinary rewrites need no catalog.

Rewrite at the smallest useful radius, preserving navigation, genre conventions, and connected
titles or captions outside the authorized scope. Use existing specifics only when meaning and scope
survive. If specifics are missing, retain the assertion and attribution; flag an evidence gap
separately when useful. For ungrounded verdicts, the reference's
[material-grounding test](references/patterns.md#material-grounding-test) helps recover source-backed
actions and observations without filling gaps.

Compare the revision with the source: every factual detail and qualification must survive, no new
claim may appear, and the voice must fit its audience. Read it aloud when useful. Do not expose
private chain-of-thought or manufacture an internal critique transcript.

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
