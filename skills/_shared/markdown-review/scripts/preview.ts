#!/usr/bin/env bun
/** Serve canonical Markdown drafts through a read-only loopback preview. */
import { readFileSync, realpathSync, lstatSync, readlinkSync } from "node:fs";
import { basename, dirname, extname, isAbsolute, relative, resolve } from "node:path";
import { parseArgs } from "node:util";

export const ASSETS = resolve(import.meta.dir, "../assets/preview");
const MEDIA = new Set([".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".mp4", ".webm", ".mov", ".ogg"]);
const HEADERS = {
  "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer",
  "Content-Security-Policy": "default-src 'none'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self'; img-src 'self' https: data:; media-src 'self' https:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'",
};

// Resolve existing ancestors too: a missing draft below a symlink must stay contained.
function canonical(path: string): string {
  try { return realpathSync(path); }
  catch (error) {
    if (!(error instanceof Error) || !("code" in error) || error.code !== "ENOENT") throw error;
    try {
      if (lstatSync(path).isSymbolicLink()) return canonical(resolve(dirname(path), readlinkSync(path)));
    } catch (missing) {
      if (!(missing instanceof Error) || !("code" in missing) || missing.code !== "ENOENT") throw missing;
    }
    return resolve(canonical(dirname(path)), basename(path));
  }
}

type Report = { id: string; title: string; kind: "issue" | "pr"; target: string; path: string;
  markdown?: string; revision?: string; error?: string };

export class Collection {
  readonly manifest: string;
  readonly root: string;
  constructor(manifest: string) {
    this.manifest = realpathSync(manifest);
    this.root = dirname(this.manifest);
  }
  inside(input: string): string {
    if (typeof input !== "string" || isAbsolute(input)) throw new Error("Expected a relative path");
    const path = canonical(resolve(this.root, input));
    const rel = relative(this.root, path);
    if (rel === ".." || rel.startsWith("../") || rel.startsWith("..\\") || isAbsolute(rel)) {
      throw new Error("Path leaves the preview folder");
    }
    return path;
  }
  reports(): Report[] {
    const entries: unknown = JSON.parse(readFileSync(this.manifest, "utf8")).reports;
    if (!Array.isArray(entries) || !entries.length) throw new Error("Manifest requires a nonempty reports array");
    const ids = new Set<string>();
    return entries.map((entry) => {
      if (!entry || typeof entry !== "object") throw new Error("Each report must be an object");
      for (const field of ["id", "title", "kind", "target", "path"]) {
        if (typeof entry[field] !== "string" || !entry[field].trim()) throw new Error(`Report requires ${field}`);
      }
      if (ids.has(entry.id) || !["issue", "pr"].includes(entry.kind)) throw new Error("Invalid ID or kind");
      ids.add(entry.id);
      const path = this.inside(entry.path);
      if (extname(path).toLowerCase() !== ".md") throw new Error("Body must be Markdown");
      const report: Report = {id: entry.id, title: entry.title, kind: entry.kind, target: entry.target,
        path: relative(this.root, path).split("\\").join("/")};
      try {
        const body = readFileSync(path);
        report.markdown = new TextDecoder("utf-8", {fatal: true, ignoreBOM: true}).decode(body);
        report.revision = new Bun.CryptoHasher("sha256").update(body).digest("hex");
      } catch {
        report.error = "Markdown source is missing or is not readable UTF-8";
      }
      return report;
    });
  }
}

export function positiveSeconds(value: string): number {
  const number = Number(value);
  if (!value.trim() || !Number.isFinite(number) || number <= 0) throw new Error("Expected finite positive seconds");
  return number;
}

export function startPreview(collection: Collection, {port = 0, idleTimeout = 300, maxLifetime = 14400,
  onStop = (_reason: string) => {}} = {}) {
  positiveSeconds(String(idleTimeout));
  positiveSeconds(String(maxLifetime));
  collection.reports();
  const started = performance.now();
  let lastPoll = started;
  let timer: ReturnType<typeof setTimeout>;
  let stopped = false;
  const server = Bun.serve({
    hostname: "127.0.0.1", port,
    fetch(request, server) {
      const respond = (status: number, body: BodyInit, type = "text/plain; charset=utf-8") =>
        new Response(request.method === "HEAD" ? null : body, {status, headers: {...HEADERS, "Content-Type": type}});
      if (![ `127.0.0.1:${server.port}`, `localhost:${server.port}` ].includes(request.headers.get("host") || "")) {
        return respond(403, "Invalid host");
      }
      if (!["GET", "HEAD"].includes(request.method)) return respond(405, "Method not allowed");
      try {
        const route = decodeURIComponent(new URL(request.url).pathname);
        if (route === "/api/reports") {
          lastPoll = performance.now();
          return respond(200, JSON.stringify({reports: collection.reports()}), "application/json; charset=utf-8");
        }
        let path: string;
        let type: string;
        if (route.startsWith("/files/")) {
          path = collection.inside(route.slice(7));
          const source = collection.reports().some(r => collection.inside(r.path) === path);
          if (!source && !MEDIA.has(extname(path).toLowerCase())) return respond(404, "Not found");
          type = source ? "text/plain; charset=utf-8" : Bun.file(path).type;
        } else {
          const name = new Map([["/", "index.html"], ["/preview.css", "preview.css"], ["/preview.js", "preview.js"]]).get(route);
          if (!name) return respond(404, "Not found");
          path = resolve(ASSETS, name);
          type = Bun.file(path).type;
        }
        return respond(200, readFileSync(path), type);
      } catch (error) {
        const missing = error instanceof Error && "code" in error && error.code === "ENOENT";
        return respond(missing ? 404 : 422, missing ? "Not found" : "Cannot read collection; check manifest paths and required fields");
      }
    },
  });
  function stop() {
    stopped = true;
    clearTimeout(timer);
    server.stop(true);
  }
  function checkDeadline() {
    if (stopped) return;
    const now = performance.now();
    const remaining = Math.min(idleTimeout * 1000 - (now - lastPoll), maxLifetime * 1000 - (now - started));
    if (remaining <= 0) {
      const reason = now - started >= maxLifetime * 1000 ? "maximum lifetime reached" : "no preview polls within idle timeout";
      stop();
      onStop(reason);
    } else timer = setTimeout(checkDeadline, Math.min(500, remaining));
  }
  checkDeadline();
  return {server, stop};
}

if (import.meta.main) {
  try {
    const {values, positionals} = parseArgs({args: Bun.argv.slice(2), allowPositionals: true, options: {
      port: {type: "string", default: "0"}, "idle-timeout": {type: "string", default: "300"},
      "max-lifetime": {type: "string", default: "14400"}, help: {type: "boolean"},
    }});
    if (values.help) {
      console.log("Usage: bun preview.ts <reports.json> [--port N] [--idle-timeout 300] [--max-lifetime 14400]");
    } else {
      if (positionals.length !== 1) throw new Error("Expected one reports.json path; use --help");
      const port = Number(values.port);
      if (!Number.isInteger(port) || port < 0 || port > 65535) throw new Error("Invalid port");
      const idleTimeout = positiveSeconds(values["idle-timeout"]!);
      const maxLifetime = positiveSeconds(values["max-lifetime"]!);
      const preview = startPreview(new Collection(positionals[0]), {port, idleTimeout, maxLifetime,
        onStop: reason => console.log(`Preview stopped: ${reason}.`)});
      console.log(`Preview: ${preview.server.url}`);
      console.log(`PID: ${process.pid}. Stop with Ctrl+C.`);
      console.log(`Auto-stop: ${idleTimeout}s without preview polls; ${maxLifetime}s maximum lifetime.`);
      for (const signal of ["SIGINT", "SIGTERM"] as const) {
        process.once(signal, () => { preview.stop(); process.exit(0); });
      }
    }
  } catch (error) {
    console.error(error instanceof Error ? error.message : "Cannot start preview");
    process.exitCode = 1;
  }
}
