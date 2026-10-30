# Markdown review preview

Use this optional wrapper when the operator requests a rendered review. It supports a collection
of Issue and fix-PR bodies with sidebar navigation, GitHub-like Markdown styling, media, source
links and automatic refresh. It is local-only and read-only; it has no publishing or editing API.
This is the single review renderer specified by the skill entrypoint. The publication Markdown
and evidence remain the deliverables; a requested archive can retain those sources without a second
HTML representation.

## Canonical drafts

Create one collection folder in the task's ignored scratch directory, or use the operator's chosen
draft folder. Keep each actual publication body in its own UTF-8 `.md` file. Create `reports.json`:

```json
{
  "reports": [
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

IDs are stable and unique; `kind` is `issue` or `pr`. Titles in the manifest are the actual proposed
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
python3 <skill-directory>/scripts/preview.py <collection-directory>/reports.json
```

Resolve placeholders to actual paths. Python's standard library is sufficient; no package install
or build is needed. The server chooses a free loopback port and prints its URL. `--port` selects a
specific port if needed. Verify a successful response, then open that URL in an available embedded
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
value of an attachment or the correctness of a fix; apply the report's evidence standard separately.

Use the host's own annotation feature when available; no custom comment system is included. Treat
feedback as referring to the selected report and displayed source revision. Apply it to that report's
Markdown, check the refreshed render, and keep unresolved comments explicit. Host annotations may
need to be revisited after a source update; do not promise persistence or remapping that the host
does not establish. Viewing or commenting on a preview does not itself approve publication.

## Rendering limits

The body is parsed directly from the publication Markdown, not reconstructed from a second data
model. Marked's GFM tables, lists, task checkboxes and fenced code are supported, with line breaks
matching GitHub comments. This is a review approximation, not GitHub's own renderer: platform-specific
mentions, autolinks, diagrams and attachment processing may differ. Inspect material differences
before claiming the published result will be identical. The wrapper does not verify that a proposed
fix works; use the fix-report evidence requirements in the skill entrypoint.
