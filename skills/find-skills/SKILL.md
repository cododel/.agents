---
name: find-skills
description: "Discover agent skills when the user requests an extension or a concrete capability gap prevents the task, including a demonstrated gap during implementation. A how-to question, review, changelog, or implementation request alone does not trigger discovery."
---

# Find Skills

Use existing capabilities to complete the task first. Search for an extension when explicitly asked,
or when repository and available-tool evidence establish a capability gap that an extension could
resolve. A specialized topic alone is not a gap.

## Discovery

1. Identify the requested capability and constraints. Do not replace the original task with a search
   merely because a matching skill might exist.
2. Use an available skill catalog or an already installed discovery tool. Search narrowly; no
   mandatory leaderboard visit, installation, or new package runner is needed for discovery.
3. Before recommending a candidate, inspect its actual instructions, provenance, maintenance,
   required tools, permissions, data handling, and compatibility with the current environment.
   Popularity can aid discovery but cannot establish quality or authorization.
4. Present the relevant candidate, what gap it closes, and material setup requirements. Installation
   needs the operator's authorization and the environment's established installation mechanism;
   permission to discover or recommend candidates is not permission to install them.
5. No suitable candidate is a valid result. Report the specific gap and continue the parts possible
   with existing tools; do not force a recommendation or expand the search to justify installation.

Examples: “find a skill for diagram editing” triggers discovery; “create a changelog” or “review this
PR” uses current capabilities unless a concrete missing capability is demonstrated.

This skill is locally maintained; upstream provenance is recorded in the repository README.
