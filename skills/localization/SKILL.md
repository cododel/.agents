---
name: localization
description: Use for any work that adds or changes user-facing localized strings, including copy edits in translation catalogs, UI code, templates, notifications, and validation messages.
---

# Localization

When adding user-facing text or changing its meaning, update the corresponding message for **every language supported by the owning project in the same change**. A fallback is not a substitute for a missing translation.

- Determine the project's supported languages, source and fallback locale, translation structure, and established product voice from its own configuration and nearby strings. Do not assume a fixed language count, key scheme, or currency convention.
- Translate the intended meaning naturally in each language. Preserve the product's terminology and style, as well as placeholders, variables, links, markup, plural forms, and other formatting that the message requires.
- Inspect related variants of the same message, such as short and long labels, errors, notifications, or alternate states, and update those whose meaning also changes.
- Before finishing, check that every supported language has the revised message and that placeholders, formatting, and related variants remain consistent. Use the project's existing localization checks when available; otherwise compare the affected entries directly.

A spelling or punctuation correction that does not change meaning may be limited to the affected language.
