import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills/design-system-extractor/scripts/scan_sessions.py"
)
SPEC = importlib.util.spec_from_file_location("scan_sessions", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
scan_sessions = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scan_sessions)


class SessionScannerTest(unittest.TestCase):
    def write_session(self, path, cwd, text, prefix=""):
        path.write_text(
            prefix
            + json.dumps({"cwd": str(cwd)})
            + "\n"
            + json.dumps({"type": "user", "content": text})
            + "\n",
            encoding="utf-8",
        )

    def test_non_object_json_does_not_hide_later_project_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            transcripts = root / "transcripts"
            transcripts.mkdir()
            session = transcripts / "session.jsonl"
            self.write_session(
                session, root, "Use blue buttons", '[]\nnull\n42\n"text"\ninvalid json\n'
            )

            result = scan_sessions.scan(root, transcripts, 20)

            self.assertEqual(1, result["matched_sessions"])
            self.assertEqual(["Use blue buttons"], [s["text"] for s in result["snippets"]])

    @unittest.skipUnless(shutil.which("git"), "Git required for repository-boundary fixture")
    def test_explicit_subdirectory_excludes_parent_and_sibling_sessions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            repo = root / "repo"
            selected = repo / "selected"
            sibling = repo / "sibling"
            selected.mkdir(parents=True)
            sibling.mkdir()
            env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
            subprocess.run(["git", "init", "--quiet", str(repo)], check=True, env=env)
            transcripts = root / "transcripts"
            transcripts.mkdir()
            self.write_session(transcripts / "selected.jsonl", selected, "Selected blue buttons")
            self.write_session(transcripts / "sibling.jsonl", sibling, "Sibling red buttons")
            self.write_session(transcripts / "parent.jsonl", repo, "Parent green buttons")

            boundary = scan_sessions.project_root(str(selected))
            result = scan_sessions.scan(boundary, transcripts, 20)

            self.assertEqual(selected.resolve(), boundary)
            self.assertEqual(1, result["matched_sessions"])
            self.assertEqual(["Selected blue buttons"], [s["text"] for s in result["snippets"]])

    def test_sensitive_assignments_are_excluded_but_named_design_tokens_remain(self):
        for assignment in (
            'token = "SYNTHETIC_SENTINEL"',
            '"token": "SYNTHETIC_SENTINEL"',
            '"access_token": "SYNTHETIC_SENTINEL"',
            "'auth-token' = 'SYNTHETIC_SENTINEL'",
        ):
            with self.subTest(assignment=assignment):
                text = assignment + " # theme design\nTheme uses color_token = #ffffff"
                self.assertEqual(
                    ["Theme uses color_token = #ffffff"], scan_sessions.design_lines(text)
                )


if __name__ == "__main__":
    unittest.main()
