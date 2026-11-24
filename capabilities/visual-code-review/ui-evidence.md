# Compare a frontend with ui-evidence

## Install

Start in the **root of a copy of this repository**. Use a POSIX shell on macOS or a Playwright-supported Linux system, with a current [Node.js LTS and npm](https://nodejs.org/en/download) on `PATH`. Installation needs network access to GitHub, the npm registry and Playwright's browser downloads. The [tool lockfile](ui-evidence/package-lock.json) pins ui-evidence 0.1.0 at revision `3549b271`, Playwright 1.65.1 and the native Sharp image dependencies.

Run these commands in the same shell. The default gives the CLI, npm packages and browser their own user directory. To use another location, set `UI_EVIDENCE_TOOLS_DIR` to an absolute path dedicated to this tool before running them. `npm ci` replaces any existing `node_modules` in that directory.

```sh
ui_kit="$PWD/capabilities/visual-code-review/ui-evidence"
ui_tools="${UI_EVIDENCE_TOOLS_DIR:-$HOME/.local/share/ui-evidence}"
mkdir -p "$ui_tools"
cp "$ui_kit/package.json" "$ui_kit/package-lock.json" "$ui_tools/"
npm ci --prefix "$ui_tools" --include=optional --ignore-scripts --no-audit --no-fund
PLAYWRIGHT_BROWSERS_PATH="$ui_tools/browsers" "$ui_tools/node_modules/.bin/playwright" install --only-shell chromium
install -m 755 "$ui_kit/launcher.sh" "$ui_tools/ui-evidence"
install -m 644 "$ui_kit/config.yaml" "$ui_tools/config.example.yaml"
"$ui_tools/ui-evidence" help
```

The last command should list `capture`, `run` and `snapshot`. On a minimal Linux image, Chromium may also need OS libraries. The installed `"$ui_tools/node_modules/.bin/playwright" install-deps chromium` command installs those on supported distributions and can require administrator access. [Playwright browser dependencies](https://playwright.dev/docs/browsers#install-system-dependencies)

## Verify a first comparison

From any directory in a **second terminal**, start this example. It serves an original and a changed status label on two loopback ports using only Node.js. Leave it running during the capture.

```sh
node -e '
const http = require("node:http");
for (const [port, label] of [[4173, "Draft"], [4174, "Approved"]]) {
  http.createServer((_req, res) => {
    res.writeHead(200, {"Content-Type": "text/html; charset=utf-8"});
    res.end(`<!doctype html><main data-testid="screen-home"><h1>Release status</h1><p>${label}</p></main>`);
  }).listen(port, "127.0.0.1");
}'
```

In the **installation terminal**, create a temporary review and capture both builds. All generated files live under `review_dir`. In a new shell, set `ui_tools` again as in the install step.

```sh
review_dir=$(mktemp -d "${TMPDIR:-/tmp}/ui-review.XXXXXXXX")
ui_config="$review_dir/ui-evidence/config.yaml"
mkdir -p "$review_dir/ui-evidence"
cp "$ui_tools/config.example.yaml" "$ui_config"
"$ui_tools/ui-evidence" doctor --config "$ui_config" --ready
"$ui_tools/ui-evidence" run --config "$ui_config" --stage primary-flow
printf '%s\n' "$review_dir/.tmp/ui-evidence/screenshots/primary-flow/review/index.html"
```

Open the printed file in a browser. Expect two side-by-side pairs, at 1280×800 and 390×844, showing **Draft** on the left and **Approved** on the right. `manifest.json` next to the `review` directory should show two complete captures and zero failures. Stop the example servers with Ctrl+C in their terminal.

## Use a frontend preview

For a one-off review, create another temporary directory and config as above. For repeated reviews, keep the screen definitions in the frontend project under `ui-evidence/config.yaml` and set `ui_config` to its absolute path. Reuse an existing config when available. The [template](ui-evidence/config.yaml) resolves `project.rootDir: ..` relative to the config directory.

- **Compare two builds.** Start both local previews. Set `servers.before.baseUrl` and `servers.after.baseUrl` to their addresses. Set each screen's `path` to a route present in both builds. For readiness, use `waitFor.testId` or `waitFor.selector` for an element visible after the screen finishes loading. Run the same `doctor` and `run` commands above.
- **Compare one preview before and after editing.** Capture the baseline before updating the running app. Keep the config, fixtures and stage identical for both commands.

```sh
"$ui_tools/ui-evidence" capture --config "$ui_config" --phase before --stage primary-flow --base-url http://127.0.0.1:4173
# Run the next command after this preview serves the candidate.
"$ui_tools/ui-evidence" run --config "$ui_config" --skip-before --after-attach http://127.0.0.1:4173 --stage primary-flow
```

- **Capture only the current UI.** Set `servers.after.baseUrl` to the active local preview. Run `"$ui_tools/ui-evidence" snapshot --config "$ui_config" --stage primary-flow` and open the printed review path.

## Outputs and limits

The HTML report links the original screenshots and comparison PNGs. A stage also includes an overview PNG, a Markdown report and a manifest. Save the whole stage directory before reusing its output paths. Use `--resume` only for an interrupted capture of the same builds. Reviewers decide whether a visual change is acceptable.

The template uses Chromium, including for the narrow viewport. Keep fixture data, fonts and locale identical across previews. Screenshots and reports include whatever the page displays. Keep `.tmp/ui-evidence/` out of version control and use local assets and services for private offline reviews. The browser follows the page's own network requests.

This setup uses the CLI directly. The separate upstream `ui-evidence install` bootstrap writes agent-specific files. [Upstream README](https://github.com/0xBrewing/ui-evidence/blob/3549b2710b7a062b547f1582df7e7947807e5391/README.md) · [Configuration schema](https://github.com/0xBrewing/ui-evidence/blob/3549b2710b7a062b547f1582df7e7947807e5391/schemas/ui-evidence.schema.json)
