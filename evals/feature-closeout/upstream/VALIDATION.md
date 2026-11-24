# Packaging and fixture verification — v0.1.0

Checks actually performed when preparing this version:

- Parsed Agent Skills YAML metadata, checked directory/name match, description length and all local reference links from `SKILL.md`.
- Created temporary Git repositories with baseline and candidate commits for all seven fixtures; verified nonempty changes and clean candidate trees.
- Ran all eight supplied Python candidate tests across six fixtures; all passed, including the intentionally incomplete tests in the negative controls. The JavaScript fixture's package manifests were parsed; its dependency was not installed or executed.
- Ran targeted synthetic probes confirming the extra mock transport call (0 → 1 for an equal subtotal), missing CSV currency header, order mutation at 30 minutes, and duplicate-event balance regression (250 → 500 cents).
- Parsed HTML template anchors and checked the lack of scripts and external resources. Previewed the template in Chromium at 390px and 1280px using in-memory HTML because the environment blocked file-URL navigation; checked horizontal overflow, section anchors and disclosure control. No external requests occurred.

These are structural, fixture and template checks only. **No coding-agent evaluation runs or real-project trials have been performed.** Use the protocol in README.md and the separate evaluator oracle to measure skill behavior.
