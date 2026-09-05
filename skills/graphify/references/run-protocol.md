# Graphify run and publication contract

This reference owns local run identity, input freshness, chunk transport and publication. It applies
to full builds, updates and cluster-only operations. Graphify's extraction and exported graph formats
remain unchanged. The helper uses only the Python standard library; Graphify is needed by the build
steps, not to validate a run or read existing JSON.

## Resolve and begin

Resolve the original corpus root (INPUT_PATH), published output directory, installed interpreter and
this skill's helper to absolute paths before changing directory. Check the installed package version
against `.graphify_version`; for a mismatch, verify the relevant APIs before executing the runbook.
Do not install, upgrade, search for credentials, or invoke an external synthesis service. A setup
request may authorize a separate isolated installation, but a query never does.

```bash
python3 /absolute/skill/scripts/run_state.py begin --output /absolute/project/graphify-out
```

The command returns RUN_DIR under the output's `.runs` directory. Record it in task context.
Run all subsequent Graphify Python blocks and CLI exports with working directory RUN_DIR/work.
`graphify-out` now means staged output. Write the verified interpreter to the staged `.graphify_python`
and INPUT_PATH to `.graphify_root`. Do not execute an unchecked path inherited from an old run.
For every Graphify child command, set GRAPHIFY_OUT to the absolute RUN_DIR/work/graphify-out.
This also redirects caches, conversion sidecars and incremental detection writes that otherwise
resolve against the original corpus root. Scope the environment override to this run only.

The helper snapshots the published files and seeds graph, manifest, cost and a private cache copy for incremental detection
and shrink protection. Detection must exclude the absolute published output directory (including
`.runs`) if it is inside the corpus. Do not scan generated output as input. Generated transcripts
must also stay in the run, with originals included in the input fingerprint.

## Prepare once

After detection and cache lookup, before extraction, write RUN_DIR/plan.json:

```json
{
  "sources": ["/absolute/corpus/file.py", "/absolute/corpus/doc.md", "/absolute/skill/references/extraction-spec.md", "/absolute/skill/.graphify_version"],
  "parameters": {"mode":"standard", "directed":false, "operation":"build", "tool_version":"<verified installed version>"},
  "read_paths": {},
  "chunks": [["/absolute/corpus/doc.md"]]
}
```

Include the full detected original corpus, every derived reading path, the extraction specification
and version marker. Supply read_paths as original-to-derived absolute path pairs from detection and
transcription. Chunk source identities are originals; temporary paths are reading material only. For updates use
`all_files` plus newly generated transcripts and original media; include effective extraction options
in parameters. Chunk lists contain only uncached semantic files, assigned exactly once. Use an empty
list for code-only, cached-only, deletion-only and cluster-only work.

```bash
python3 /absolute/skill/scripts/run_state.py prepare --run RUN_DIR --plan RUN_DIR/plan.json
```

The returned fingerprint binds input bytes, parameters and expected chunks. Preparation is immutable;
a requirement/parameter/source change starts a fresh run. Do not reuse old envelopes in a new run.
Prepare before Part A even when no semantic work is required.

Each chunk uses the envelope in [build.md](build.md). Missing or invalid chunks get one focused retry;
remaining failures stop the run as incomplete. Existing files alone are not completion evidence.

```bash
python3 /absolute/skill/scripts/run_state.py merge --run RUN_DIR
```

An empty expected list produces an empty fresh extraction. Unknown chunk files are ignored; expected
files with foreign run IDs, fingerprints or source attribution fail. Only a fully validated merge
can proceed to caching and output generation. Check the complete detected file inventory again before
publication: additions, deletions, exclusions or renamed inputs require a fresh run. The helper also
rechecks recorded input bytes and chunk receipts.

## Publish and recover

Finish extraction, graph, report, requested HTML and manifest inside staging. Run diagnostics before
publication. All required outputs must be generated successfully; never publish after a failed command.

```bash
python3 /absolute/skill/scripts/run_state.py publish --run RUN_DIR
```

Publication checks current sources, unchanged chunk receipts, graph structure, a nonempty report and
JSON state files. It rejects drift in the published output since begin. Only the explicit supported
artifact list (including the private cache copy) is replaced; graph.json is last and replaced atomically. File replacements are not a single
transaction across the entire bundle. A normal I/O failure restores the previous files; an abrupt
process termination may leave mixed sidecars and a `.publish-lock`. Stop on that lock, inspect the
run state and backups, and reconcile the listed files before removing it. Do not automatically steal
a lock or report completion from an interrupted run.

Keep the exact run directory and backup on failure. A new interrupted-extraction attempt gets a new
run directory, so old chunks cannot enter it. After successful publication, an optional cleanup may
remove only that exact task-owned run after resolving its path and state; never glob-delete runs.
Exporting to another vault, pushing to a database, hooks and watchers remain separately scoped
operations, not side effects of preparing a graph. The staged interpreter/root/labels persist for
subsequent authorized exports.
