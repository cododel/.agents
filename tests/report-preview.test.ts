import {afterEach, beforeEach, expect, test} from "bun:test";
import {mkdtempSync, writeFileSync, readFileSync, rmSync, symlinkSync, unlinkSync} from "node:fs";
import {tmpdir} from "node:os";
import {join, resolve} from "node:path";
import {ASSETS, Collection, positiveSeconds, startPreview} from "../skills/markdown-preview/scripts/preview";

let root: string;
let manifest: string;
let entries: {id: string; kind: string; title: string; target?: string; path: string}[];
const stops: (() => void)[] = [];
function writeManifest() { writeFileSync(manifest, JSON.stringify({reports: entries})); }
function start(input = manifest) {
  const preview = startPreview(new Collection(input));
  stops.push(preview.stop);
  return preview.server.url.href;
}
beforeEach(() => {
  root = mkdtempSync(join(tmpdir(), "markdown-preview-"));
  manifest = join(root, "reports.json");
  entries = [{id: "one", kind: "issue", title: "First", target: "example/repo", path: "issue.md"}];
  writeFileSync(join(root, "issue.md"), "## Observed\nOriginal body\n");
  writeManifest();
});
afterEach(() => {
  for (const stop of stops.splice(0)) stop();
  rmSync(root, {recursive: true, force: true});
});
async function reports(url: string) {
  return (await (await fetch(url + "api/reports")).json()).reports;
}

test("HTTP serves canonical bytes and refreshes changed, missing and recovered Markdown", async () => {
  const url = start();
  const original = (await reports(url))[0];
  expect(original.markdown).toBe("## Observed\nOriginal body\n");
  expect(await (await fetch(url + "files/issue.md")).text()).toBe(original.markdown);
  writeFileSync(join(root, "issue.md"), "Changed **body**\n");
  const changed = (await reports(url))[0];
  expect(changed.markdown).toBe("Changed **body**\n");
  expect(changed.revision).not.toBe(original.revision);
  unlinkSync(join(root, "issue.md"));
  expect((await reports(url))[0]).toHaveProperty("error");
  expect((await reports(url))[0]).not.toHaveProperty("markdown");
  writeFileSync(join(root, "issue.md"), "Recovered");
  expect((await reports(url))[0].markdown).toBe("Recovered");
  writeFileSync(join(root, "issue.md"), new Uint8Array([0xff]));
  expect((await reports(url))[0]).toHaveProperty("error");
});

test("Issue and PR metadata updates are read from the manifest", async () => {
  writeFileSync(join(root, "pr.md"), "After evidence");
  writeFileSync(join(root, "README.md"), "# Project");
  entries.push({id: "two", kind: "pr", title: "Fix", target: "example/repo", path: "pr.md"});
  entries.push({id: "docs", kind: "markdown", title: "README", path: "README.md"});
  writeManifest();
  const url = start();
  expect((await reports(url)).map((r: {kind: string}) => r.kind)).toEqual(["issue", "pr", "markdown"]);
  entries[1].title = "Updated title";
  writeManifest();
  expect((await reports(url))[1].title).toBe("Updated title");
});

test("a Markdown file opens directly and refreshes its original source", async () => {
  const path = join(root, "Project README.MD");
  const original = '<div align="center"><img src="cover.png" alt="Cover"></div>\n';
  writeFileSync(path, original);
  writeFileSync(join(root, "cover.png"), "synthetic-cover");
  const url = start(path);
  expect((await reports(url))[0]).toMatchObject({
    kind: "markdown", title: "Project README.MD", path: "Project README.MD", markdown: original,
  });
  expect(await (await fetch(url + "files/Project%20README.MD")).text()).toBe(original);
  expect(await (await fetch(url + "files/cover.png")).text()).toBe("synthetic-cover");
  expect((await fetch(url + "files/issue.md")).status).toBe(404);
  writeFileSync(path, "# Updated");
  expect((await reports(url))[0].markdown).toBe("# Updated");
});

test("containment blocks traversal, symlinks, missing paths through symlinks and private files", async () => {
  const outside = mkdtempSync(join(tmpdir(), "preview-private-"));
  try {
    writeFileSync(join(outside, "private.md"), "private");
    symlinkSync(outside, join(root, "escape"));
    symlinkSync(join(outside, "absent.md"), join(root, "dangling.md"));
    const collection = new Collection(manifest);
    for (const path of ["../private.md", outside, "escape/private.md", "escape/absent.md", "dangling.md"]) {
      expect(() => collection.inside(path)).toThrow();
    }
    const url = start();
    writeFileSync(join(root, "unregistered.md"), "not selected");
    for (const path of ["files/unregistered.md", "files/escape/private.md", "files/..%2fprivate.md"]) {
      expect((await fetch(url + path)).status).toBeGreaterThanOrEqual(400);
    }
    expect((await fetch(url + "api/reports", {headers: {Host: "example.com"}})).status).toBe(403);
    expect((await fetch(url + "api/reports", {method: "POST"})).status).toBe(405);
  } finally { rmSync(outside, {recursive: true, force: true}); }
});

test("media, HEAD and bundled HTML/CSS/JS work with restrictive headers", async () => {
  const url = start();
  writeFileSync(join(root, "image.png"), "synthetic-image");
  expect(await (await fetch(url + "files/image.png")).text()).toBe("synthetic-image");
  for (const [route, file] of [["", "index.html"], ["preview.css", "preview.css"], ["preview.js", "preview.js"]]) {
    const response = await fetch(url + route);
    expect(response.status).toBe(200);
    expect(await response.text()).toBe(readFileSync(join(ASSETS, file), "utf8"));
    expect(response.headers.get("Cache-Control")).toBe("no-store");
    expect(response.headers.get("Content-Security-Policy")).toContain("frame-ancestors 'none'");
    expect(response.headers.has("Access-Control-Allow-Origin")).toBe(false);
  }
  const head = await fetch(url, {method: "HEAD"});
  expect(head.status).toBe(200);
  expect(await head.text()).toBe("");
});

test("malformed manifest fails visibly and recovers", async () => {
  const url = start();
  writeFileSync(manifest, "broken json");
  expect((await fetch(url + "api/reports")).status).toBe(422);
  writeManifest();
  expect((await fetch(url + "api/reports")).status).toBe(200);
  entries.push(entries[0]);
  writeManifest();
  expect((await fetch(url + "api/reports")).status).toBe(422);
});

async function processPreview(args: string[], poll: boolean, signal?: NodeJS.Signals) {
  const proc = Bun.spawn([process.execPath, resolve(import.meta.dir, "../skills/markdown-preview/scripts/preview.ts"),
    manifest, ...args], {stdout: "pipe", stderr: "pipe"});
  const output: string[] = [];
  let url = "";
  let polling: ReturnType<typeof setInterval> | undefined;
  let polls = 0;
  const timeout = setTimeout(() => proc.kill(), 5000);
  try {
    for await (const chunk of proc.stdout) {
      output.push(new TextDecoder().decode(chunk));
      if (!url) {
        const match = output.join("").match(/Preview: (http:\/\/127\.0\.0\.1:\d+\/)/);
        if (match) {
          url = match[1];
          if (signal) proc.kill(signal);
          else if (poll) polling = setInterval(() => {
            fetch(url + "api/reports").then(r => { if (r.ok) polls++; }).catch(() => {});
          }, 30);
        }
      }
    }
    expect(await proc.exited).toBe(0);
    expect(await new Response(proc.stderr).text()).toBe("");
    expect(url).not.toBe("");
    await expect(fetch(url)).rejects.toThrow();
    return {output: output.join(""), polls};
  } finally {
    clearTimeout(timeout);
    clearInterval(polling);
    proc.kill();
    await proc.exited;
  }
}

test("CLI exits and releases its port after idle expiry", async () => {
  const result = await processPreview(["--idle-timeout", "0.2", "--max-lifetime", "5"], false);
  expect(result.output).toContain("no preview polls within idle timeout");
});
test("polls extend idle deadline but cannot extend absolute lifetime", async () => {
  const result = await processPreview(["--idle-timeout", "0.2", "--max-lifetime", "0.8"], true);
  expect(result.polls).toBeGreaterThan(3);
  expect(result.output).toContain("maximum lifetime reached");
});
test("SIGTERM closes the listener and exits cleanly", async () => {
  await processPreview([], false, "SIGTERM");
});
test("disabled and nonfinite time limits are rejected", async () => {
  for (const value of ["0", "-1", "NaN", "Infinity", ""]) expect(() => positiveSeconds(value)).toThrow();
  for (const flag of ["--idle-timeout", "--max-lifetime"]) {
    const proc = Bun.spawn([process.execPath, resolve(import.meta.dir, "../skills/markdown-preview/scripts/preview.ts"),
      manifest, flag, "0"], {stdout: "pipe", stderr: "pipe"});
    expect(await proc.exited).toBe(1);
    expect(await new Response(proc.stderr).text()).toContain("finite positive");
  }
});
