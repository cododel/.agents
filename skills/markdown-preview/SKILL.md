---
name: markdown-preview
description: Render local Markdown previews of README files, documentation, notes, and Issue or pull request drafts. Use to open or inspect rendered Markdown, including safe inline HTML, media, and collections of documents.
---

# Markdown preview

Render one or more Markdown files using the bundled local viewer. The viewer provides
sidebar navigation, GitHub-like Markdown styling, media, source links and automatic refresh. Review
is read-only and local. For a requested archive, retain the source Markdown, manifest and evidence.

## Single file

Pass the original file directly. Edits to the source appear in the open preview.

```sh
bun <skill-directory>/scripts/preview.ts /path/to/README.md
```

The file's directory is the serving boundary for relative media. If documentation uses media
from a parent directory, put a temporary manifest in a common ancestor inside the project and
reference the original Markdown by its relative path. The manifest directory is then the serving
boundary. Keep temporary manifests out of Git.

## Collections and draft metadata

For several files or for Issue and PR metadata, create a `reports.json` manifest. Keep each actual
publication body in its own UTF-8 `.md` file. Use the task's ignored scratch directory for generated
drafts or the operator's chosen draft folder.

```json
{
  "reports": [
    {
      "id": "readme",
      "kind": "markdown",
      "title": "README",
      "path": "README.md"
    },
    {
      "id": "browser-focus",
      "kind": "issue",
      "title": "Browser address bar loses focus on first click",
      "target": "owner/repository",
      "path": "issue-focus.md"
    },
    {
      "id": "fix-browser-focus",
      "kind": "pr",
      "title": "fix(browser): preserve address field focus",
      "target": "owner/repository → main",
      "path": "pr-focus.md"
    }
  ]
}
```

IDs are stable and unique. Use `kind: markdown` for a document, with optional `target`, and
`kind: issue` or `kind: pr` for a draft, with a target. Draft titles are the actual proposed
publication titles; `path` points to the exact body to submit, without preview-only frontmatter or
text stripped during publication. Edit titles in the manifest and body content in Markdown. Display
an unknown target honestly rather than inventing a repository. Keep operator notes outside the body.

Paths are relative to the manifest folder and must stay inside it, including through symlinks.
Use a dedicated folder: registered Markdown and supported image/video files inside that folder can
be served. Store local evidence below it, link relative to the Markdown file, and use new filenames
when replacing evidence so existing media and annotations do not silently change meaning.
PNG/JPEG/GIF/WebP/AVIF and MP4/WebM/MOV/OGG attachments are supported; playback depends on the browser's
codecs. A Markdown link to MP4/WebM/MOV also displays a video player. Missing attachments must be
resolved or disclosed before calling the report ready.

Local media URLs are preview locators, not GitHub uploads. Before an authorized publication, resolve
the destination's attachment URLs in the same Markdown and recheck that render. Do not upload from
preview preparation alone or claim local paths will work for GitHub readers.

## Launch and review

From the selected checkout, run in a retained terminal session:

```sh
bun <skill-directory>/scripts/preview.ts <collection-directory>/reports.json
```

Use the directory containing this SKILL.md for `<skill-directory>` and resolve both paths before
launching. The viewer requires Bun.
The server uses built-in Bun/Node APIs, so no package install or build is needed. It chooses a free
loopback port and prints its URL. `--port` selects a specific port if needed. Verify a successful response, then open that URL in an available embedded
browser; use another already authorized local browser only if necessary. Do not publish the server
or expose it on a non-loopback interface. Follow task process ownership rules and report how to stop any
server intentionally kept running for the operator's review; otherwise stop it before handoff.

The process prints its PID and enforces two independent limits: five minutes without requests to
the draft-poll endpoint, and four hours from startup even when a forgotten tab keeps polling.
It closes its listening socket and exits when either limit is reached. `--idle-timeout` and
`--max-lifetime` accept finite positive seconds; their defaults are `300` and `14400`. Keep the
bounded defaults unless the task calls for different limits; do not disable lifecycle protection.
Record the retained terminal session/PID, collection and URL in existing task state or the handoff,
and reuse that process during edits rather than launching another copy. If the preview expires,
verify the previous process has stopped before restarting and reloading the existing tab. The
rendered text remains in the tab, but its disconnected state is not a synchronized preview.

The browser loads pinned Marked 18.1.2 and DOMPurify 3.4.17 from jsDelivr. These are the wrapper's
approved runtime dependencies; there is no telemetry or draft-upload endpoint. CDN access is needed
for initial rendering. If either library cannot load, the page shows an error rather than rendering
unfiltered HTML. CSS is bundled locally; arbitrary Markdown scripts, forms and styles are excluded.

The page polls the collection every 1.2 seconds. Switching reports preserves stable identity through
the `report` URL parameter. Unchanged bodies are not replaced during polling. Changed Markdown or
metadata is re-rendered; missing sources clear the selected body with an error, and collection or
connection failures visibly mark the previous preview as potentially stale.
Source revision checks, loaded media and layout checks validate the preview, not the evidentiary
value of an attachment or the correctness of a fix; apply the owning authoring workflow's evidence standard separately.

Use the host's own annotation feature when available; no custom comment system is included. Treat
feedback as referring to the selected report and displayed source revision. Apply it to that report's
Markdown, check the refreshed render, and keep unresolved comments explicit. Host annotations may
need to be revisited after a source update; do not promise persistence or remapping that the host
does not establish. Viewing or commenting on a preview does not itself approve publication.

If the viewer cannot display required content, return the canonical draft and report the concrete
limitation. Use the bundled viewer for review and keep feedback and corrections tied to the Markdown
source. A ready requested preview may be opened in the embedded browser under the existing request.

## Rendering limits

The body is parsed directly from the publication Markdown, not reconstructed from a second data
model. Marked's GFM tables, lists, task checkboxes and fenced code are supported, with line breaks
matching GitHub comments for Issue and PR drafts. Documents use normal Markdown line breaks.
Safe HTML blocks such as `<div align="center">` and `<details>` are supported. Inline CSS and scripts
are removed. Leave blank lines around Markdown nested in HTML blocks when it should render as
Markdown. This is a review approximation, not GitHub's own renderer: platform-specific
mentions, autolinks, diagrams and attachment processing may differ. Inspect material differences
before claiming the published result will be identical.
