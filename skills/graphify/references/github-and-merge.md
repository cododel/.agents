# graphify reference: GitHub clone and cross-repo merge

Load this when the user passed one or more `https://github.com/...` URLs, or named several local subfolders to merge into one graph.

### Step 0 - Clone GitHub repo(s) (only if a GitHub URL was given)

**Single repo:**
```bash
LOCAL_PATH=$(graphify clone <github-url> [--branch <branch>])
# Use LOCAL_PATH as the target for all subsequent steps
```

**Multiple repos (cross-repo graph):**
```bash
# Clone each repo, run the full pipeline on each, then merge
graphify clone <url1>   # → ~/.graphify/repos/<owner1>/<repo1>
graphify clone <url2>   # → ~/.graphify/repos/<owner2>/<repo2>
# Run /graphify on each local path to produce their graph.json files
# Then merge:
graphify merge-graphs \
  ~/.graphify/repos/<owner1>/<repo1>/graphify-out/graph.json \
  ~/.graphify/repos/<owner2>/<repo2>/graphify-out/graph.json \
  --out graphify-out/cross-repo-graph.json
```

Graphify clones into `~/.graphify/repos/<owner>/<repo>` and reuses existing clones on repeat runs. Each node in the merged graph carries a `repo` attribute so you can filter by origin.

**Multiple local subfolders (monorepo or multi-service layout):**

Run the staged build protocol separately for each original subfolder, choosing a distinct published
output directory for each. Preserve each original scan root; never run direct CLI extraction that
may select a synthesis backend or overwrite shared output.

For an explicitly requested cross-graph merge, prepare a new staged run with the constituent graph
files as sources and an empty semantic chunk list. Run helper merge, then use the installed
`merge-graphs` command with its output explicitly inside the new staging directory. Reconstruct the
extraction from that graph's nodes/links/hyperedges, generate its report using the local output
pipeline, and publish through [run-protocol.md](run-protocol.md). Do not write a merged graph directly
over published output. Verify relevant CLI flags against the installed version before execution.
