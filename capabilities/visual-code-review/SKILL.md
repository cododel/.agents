---
name: visual-code-review
description: Capture frontend screens with Playwright and prepare a local HTML report for before/after visual review.
---

# Visual code review

On a new machine, follow the [ui-evidence installation](ui-evidence.md#install) from the root of the tooling checkout. The commands run from a shell, and this directory can also be supplied as a portable agent skill.

To [compare a frontend preview](ui-evidence.md#use-a-frontend-preview), use two local builds or capture the baseline before editing. Reuse a project's screen definitions if available. For a one-off request, keep the configuration and report outside the app. Keep private source, screenshots and reports local unless the operator authorizes a specific destination.

For visual acceptance, derive the screens, states and viewport sizes from the requested change. Set up and run the capture on the reviewer's behalf. Return the local HTML report, identify the baseline and candidate used, and name any requested state that was missed. If only the current UI is available, describe the evidence as a snapshot.
