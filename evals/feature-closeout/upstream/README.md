# Skill evaluation protocol

These are seven small, original, synthetic fixtures with known behavior. They are intended to test task scoping, semantic understanding, requirement alignment, evidence discipline and false positives. They are not a substitute for evaluations on genuinely large production changes. Case 07 is a small multi-component proxy, not a large-repository benchmark.

Keep the oracle separate from the review agent. Do not let it read this directory or the expected results. Copy the skill without `evals/` into the test agent's normal skill path, and expose only one temporary case repository and its specification. Do not activate this skill's evals during normal reviews.

## Set up a case

From `evals/`, for each case (replace `01-extra-request` as needed):

```bash
CASE="$PWD/fixtures/01-extra-request"
WORK="$(mktemp -d)"
cp "$CASE/spec.md" "$WORK/spec.md"
mkdir "$WORK/repo"
cp -R "$CASE/base/." "$WORK/repo/"
git -C "$WORK/repo" init -q
git -C "$WORK/repo" -c user.name=Eval -c user.email=eval@example.invalid add .
git -C "$WORK/repo" -c user.name=Eval -c user.email=eval@example.invalid commit -qm baseline
BASE="$(git -C "$WORK/repo" rev-parse HEAD)"
# Replace the fixture source tree (NOT a real user project) without leaving files that were removed.
git -C "$WORK/repo" rm -qr .
cp -R "$CASE/candidate/." "$WORK/repo/"
git -C "$WORK/repo" add -A
git -C "$WORK/repo" -c user.name=Eval -c user.email=eval@example.invalid commit -qm candidate
HEAD_SHA="$(git -C "$WORK/repo" rev-parse HEAD)"
printf 'Repo: %s\nSpec: %s\nBase: %s\nTarget: %s\n' "$WORK/repo" "$WORK/spec.md" "$BASE" "$HEAD_SHA"
```

Use a fresh repository/session for each run. Python fixtures need only the standard library; run candidate tests using `python3 -m unittest discover -v` inside the isolated repo (or `PYTHONDONTWRITEBYTECODE=1` to avoid cache files). Case 02 is a JS static-analysis fixture; do not install lodash for it. It has no runtime test, and a skill must not claim execution or a generated lockfile. Other fixtures have ordinary candidate tests, intentionally incomplete in some cases. A reviewer may devise additional safe probes in scratch.

## Compare

Use the same model/version, thinking effort, tool access, baseline and specification. Compare unassisted review, `engineering-review`, and optionally an existing reviewer such as `ce-code-review`. Do not ask a generic bug-finding baseline to produce architecture diagrams without acknowledging the different objective. For a fair direct comparison give every arm the same user-level requested outcome: acceptance report with architecture/behavior changes and evidence. Record actual reviewer settings, any retries, tokens/time if available, and artifacts. Keep the report-only constraint constant.

Example prompt:

> Review the completed task against the attached specification. Use base SHA [BASE] and target SHA [TARGET]. I need to understand all material behavior/architecture changes, avoidable complexity, compliance and risks without reading the code. Check important claims with available evidence, and report unknowns. Do not fix or install anything. Produce a local acceptance report. [For the skill arm only: use engineering-review.]

Run at least three independent samples per arm if practical. Grade without knowing which method produced each report; use `oracle.md` only after the output is frozen. Count observed behavior, not confident language. This is a manual protocol, not an automated LLM evaluator. The supplied tests check fixture behavior, not skill effectiveness.
