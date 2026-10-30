import importlib.util
import json
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.client import HTTPConnection
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "report_preview", Path(__file__).resolve().parents[1] / "skills/bug-report/scripts/preview.py"
)
preview = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preview)


class PreviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.body = self.root / "issue.md"
        self.body.write_text("## Observed\nOriginal body\n", encoding="utf-8")
        self.manifest = self.root / "reports.json"
        self.entries = [{"id": "one", "kind": "issue", "title": "First", "target": "example/repo", "path": "issue.md"}]
        self.write_manifest()
        self.collection = preview.Collection(self.manifest)

    def write_manifest(self):
        self.manifest.write_text(json.dumps({"reports": self.entries}), encoding="utf-8")

    def start_server(self):
        server = preview.PreviewServer(("127.0.0.1", 0), preview.handler_for(self.collection))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        def stop():
            server.shutdown()
            server.server_close()
            thread.join()
        self.addCleanup(stop)
        return server

    def request(self, server, path, headers=None, method="GET"):
        connection = HTTPConnection("127.0.0.1", server.server_port)
        try:
            connection.request(method, path, headers=headers or {})
            response = connection.getresponse()
            return response.status, response.read(), response.getheaders()
        finally:
            connection.close()

    def test_http_returns_current_canonical_body_and_recovers_from_missing_source(self):
        server = self.start_server()
        status, body, _ = self.request(server, "/api/reports")
        original = json.loads(body)["reports"][0]
        self.assertEqual(200, status)
        self.assertEqual(self.body.read_text(), original["markdown"])
        self.assertEqual(self.body.read_bytes(), self.request(server, "/files/issue.md")[1])
        self.body.write_text("Changed **body**\n", encoding="utf-8")
        changed = json.loads(self.request(server, "/api/reports")[1])["reports"][0]
        self.assertNotEqual(original["revision"], changed["revision"])
        self.assertEqual(self.body.read_text(), changed["markdown"])
        self.body.unlink()
        missing = json.loads(self.request(server, "/api/reports")[1])["reports"][0]
        self.assertIn("error", missing)
        self.assertNotIn("markdown", missing)
        self.body.write_text("Recovered")
        recovered = json.loads(self.request(server, "/api/reports")[1])["reports"][0]
        self.assertEqual("Recovered", recovered["markdown"])

    def test_distinct_issue_pr_and_manifest_edits(self):
        (self.root / "pr.md").write_text("Before / after evidence")
        self.entries.append({"id": "two", "kind": "pr", "title": "Fix", "target": "example/repo", "path": "pr.md"})
        self.write_manifest()
        reports = self.collection.reports()
        self.assertEqual(["issue", "pr"], [report["kind"] for report in reports])
        self.entries[1]["title"] = "Updated title"
        self.write_manifest()
        self.assertEqual("Updated title", self.collection.reports()[1]["title"])

    def test_paths_symlinks_and_unregistered_files_are_not_exposed(self):
        with tempfile.TemporaryDirectory() as outside:
            secret = Path(outside) / "private.md"
            secret.write_text("private")
            (self.root / "escape.md").symlink_to(secret)
            with self.assertRaises(ValueError):
                self.collection.inside("escape.md")
            with self.assertRaises(ValueError):
                self.collection.inside("../private.md")
            with self.assertRaises(ValueError):
                self.collection.inside(str(secret))
            server = self.start_server()
            (self.root / "unregistered.md").write_text("not selected")
            self.assertEqual(404, self.request(server, "/files/unregistered.md")[0])
            self.assertEqual(422, self.request(server, "/files/%2e%2e/private.md")[0])
            self.assertEqual(422, self.request(server, "/files/escape.md")[0])
            self.assertEqual(403, self.request(server, "/api/reports", {"Host": "example.com"})[0])
            self.assertEqual(501, self.request(server, "/api/reports", method="POST")[0])

    def test_media_and_invalid_manifest(self):
        server = self.start_server()
        (self.root / "image.png").write_bytes(b"synthetic-image")
        self.assertEqual(b"synthetic-image", self.request(server, "/files/image.png")[1])
        self.manifest.write_text("broken json")
        self.assertEqual(422, self.request(server, "/api/reports")[0])
        self.write_manifest()
        self.entries.append(self.entries[0])
        self.write_manifest()
        with self.assertRaises(ValueError):
            self.collection.reports()


    def test_polls_extend_idle_deadline_but_do_not_reset_lifetime(self):
        now = [0.0]
        server = preview.PreviewServer(("127.0.0.1", 0), preview.handler_for(self.collection), clock=lambda: now[0])
        self.addCleanup(server.server_close)
        now[0] = 100.0
        # Exercise the real HTTP handler, not only a direct timer assignment.
        worker = threading.Thread(target=server.handle_request)
        worker.start()
        self.assertEqual(200, self.request(server, "/api/reports")[0])
        worker.join(timeout=2)
        self.assertFalse(worker.is_alive())
        self.assertEqual(100.0, server.last_poll)
        self.assertEqual(0.0, server.started_at)

    def test_process_stops_and_releases_port_after_idle_timeout(self):
        command = [sys.executable, str(Path(preview.__file__)), str(self.manifest),
                   "--idle-timeout", "0.2", "--max-lifetime", "5"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            url = process.stdout.readline().strip().removeprefix("Preview: ")
            output, errors = process.communicate(timeout=5)
        finally:
            if process.poll() is None:
                process.kill()
            process.communicate()
        self.assertEqual(0, process.returncode, errors)
        self.assertIn("no preview polls within idle timeout", output)
        port = int(url.split(":")[-1].rstrip("/"))
        connection = HTTPConnection("127.0.0.1", port, timeout=1)
        try:
            with self.assertRaises(OSError):
                connection.request("GET", "/api/reports")
        finally:
            connection.close()

    def test_maximum_lifetime_wins_despite_continuous_polls(self):
        class ActiveServer:
            started_at = last_poll = 0.0
            now = 0.0
            def clock(self):
                return self.now
            def handle_request(self):
                self.now += self.timeout
                self.last_poll = self.now
        server = ActiveServer()
        self.assertEqual("maximum lifetime reached", preview.serve_preview(server, 1, 4))
        self.assertEqual(4.0, server.now)

    def test_process_expires_while_browser_keeps_polling(self):
        command = [sys.executable, str(Path(preview.__file__)), str(self.manifest),
                   "--idle-timeout", "0.4", "--max-lifetime", "1"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        successful_polls = 0
        try:
            url = process.stdout.readline().strip().removeprefix("Preview: ")
            port = int(url.split(":")[-1].rstrip("/"))
            deadline = time.monotonic() + 5
            while process.poll() is None and time.monotonic() < deadline:
                connection = HTTPConnection("127.0.0.1", port, timeout=1)
                try:
                    connection.request("GET", "/api/reports")
                    response = connection.getresponse()
                    response.read()
                    successful_polls += response.status == 200
                except OSError:
                    pass
                finally:
                    connection.close()
                time.sleep(0.05)
            output, errors = process.communicate(timeout=1)
            self.assertEqual(0, process.returncode, errors)
            self.assertGreater(successful_polls, 1)
            self.assertIn("maximum lifetime reached", output)
        finally:
            if process.poll() is None:
                process.kill()
            process.communicate()

    def test_lifetime_arguments_reject_disabled_or_invalid_limits(self):
        for value in ("0", "-1", "nan", "inf"):
            with self.subTest(value=value), self.assertRaises(preview.argparse.ArgumentTypeError):
                preview.positive_seconds(value)


if __name__ == "__main__":
    unittest.main()
