#!/usr/bin/env python3
"""Serve canonical Markdown drafts through a read-only loopback preview."""

import argparse
import hashlib
import json
import math
import mimetypes
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


ASSETS = Path(__file__).resolve().parents[1] / "assets" / "preview"
MEDIA = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".mp4", ".webm", ".mov", ".ogg"}


class PreviewServer(ThreadingHTTPServer):
    def __init__(self, address, handler, clock=time.monotonic):
        super().__init__(address, handler)
        self.clock = clock
        self.started_at = self.last_poll = clock()

    def record_poll(self):
        self.last_poll = self.clock()


def serve_preview(server, idle_timeout, max_lifetime):
    while True:
        now = server.clock()
        idle_remaining = idle_timeout - (now - server.last_poll)
        lifetime_remaining = max_lifetime - (now - server.started_at)
        if lifetime_remaining <= 0:
            return "maximum lifetime reached"
        if idle_remaining <= 0:
            return "no preview polls within idle timeout"
        server.timeout = min(0.5, idle_remaining, lifetime_remaining)
        server.handle_request()


class Collection:
    def __init__(self, manifest):
        self.manifest = Path(manifest).resolve(strict=True)
        self.root = self.manifest.parent

    def inside(self, relative):
        if not isinstance(relative, str) or Path(relative).is_absolute():
            raise ValueError("Expected a relative path inside the preview folder")
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("Path leaves the preview folder")
        return path

    def reports(self):
        entries = json.loads(self.manifest.read_text(encoding="utf-8"))["reports"]
        if not isinstance(entries, list) or not entries:
            raise ValueError("Manifest requires a nonempty reports array")
        reports, ids = [], set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError("Each report must be an object")
            for field in ("id", "title", "kind", "target", "path"):
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    raise ValueError(f"Report requires a nonempty {field}")
            if entry["id"] in ids or entry["kind"] not in {"issue", "pr"}:
                raise ValueError("Report IDs must be unique; kind must be issue or pr")
            ids.add(entry["id"])
            path = self.inside(entry["path"])
            if path.suffix.lower() != ".md":
                raise ValueError("Report body must be a Markdown file")
            report = {key: entry[key] for key in ("id", "title", "kind", "target", "path")}
            report["path"] = path.relative_to(self.root).as_posix()
            try:
                body = path.read_bytes()
                report.update(markdown=body.decode("utf-8"), revision=hashlib.sha256(body).hexdigest())
            except (OSError, UnicodeError):
                report["error"] = "Markdown source is missing or is not readable UTF-8"
            reports.append(report)
        return reports


def handler_for(collection):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def respond(self, code, body, content_type):
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self'; img-src 'self' https: data:; media-src 'self' https:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def do_HEAD(self):
            self.do_GET()

        def do_GET(self):
            allowed_hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            if self.headers.get("Host") not in allowed_hosts:
                self.respond(403, b"Invalid host", "text/plain")
                return
            route = unquote(urlsplit(self.path).path)
            try:
                if route == "/api/reports":
                    self.server.record_poll()
                    payload = json.dumps({"reports": collection.reports()}, ensure_ascii=False).encode()
                    self.respond(200, payload, "application/json; charset=utf-8")
                    return
                if route.startswith("/files/"):
                    path = collection.inside(route[len("/files/"):])
                    sources = {collection.inside(r["path"]) for r in collection.reports()}
                    if path not in sources and path.suffix.lower() not in MEDIA:
                        raise FileNotFoundError
                    content_type = "text/plain; charset=utf-8" if path in sources else mimetypes.guess_type(path.name)[0]
                else:
                    name = {"/": "index.html", "/preview.css": "preview.css", "/preview.js": "preview.js"}.get(route)
                    if name is None:
                        raise FileNotFoundError
                    path = ASSETS / name
                    content_type = mimetypes.guess_type(name)[0]
                self.respond(200, path.read_bytes(), content_type or "application/octet-stream")
            except FileNotFoundError:
                self.respond(404, b"Not found", "text/plain")
            except (ValueError, KeyError, TypeError, OSError):
                self.respond(422, b"Cannot read collection; check manifest paths and required fields", "text/plain")

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--port", type=int, default=0, help="Loopback port; default chooses a free port")
    parser.add_argument("--idle-timeout", type=positive_seconds, default=300,
                        help="Stop after this many seconds without preview polls (default: 300)")
    parser.add_argument("--max-lifetime", type=positive_seconds, default=14400,
                        help="Stop after this many seconds even with active tabs (default: 14400)")
    args = parser.parse_args()
    collection = Collection(args.manifest)
    collection.reports()
    server = PreviewServer(("127.0.0.1", args.port), handler_for(collection))
    print(f"Preview: http://127.0.0.1:{server.server_port}/", flush=True)
    print(f"PID: {os.getpid()}. Stop with Ctrl+C.", flush=True)
    print(f"Auto-stop: {args.idle_timeout:g}s without preview polls; {args.max_lifetime:g}s maximum lifetime.", flush=True)
    try:
        reason = serve_preview(server, args.idle_timeout, args.max_lifetime)
        print(f"Preview stopped: {reason}.", flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def positive_seconds(value):
    seconds = float(value)
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("Expected a finite positive number of seconds")
    return seconds


if __name__ == "__main__":
    main()
