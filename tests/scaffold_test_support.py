"""Isolated Git projects and fake binaries for code-intelligence scaffold tests."""

import contextlib
import io
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from code_intelligence_scaffold import cli, common  # noqa: E402


MCPLS_SCRIPT = r"""
#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path
if sys.argv[1:] == ["--version"]:
    print("mcpls 0.3.9"); raise SystemExit(0)
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
if os.environ.get("FAKE_MCPLS_CHILD"):
    Path(os.environ["FAKE_MCPLS_CHILD"]).write_text(str(child.pid))
names = ["get_hover", "get_definition", "get_references", "get_diagnostics", "get_code_actions", "get_document_symbols", "workspace_symbol_search", "rename_symbol", "prepare_call_hierarchy", "get_incoming_calls", "get_outgoing_calls"]
for line in sys.stdin:
    message = json.loads(line); request_id = message.get("id")
    if request_id is None: continue
    method = message.get("method")
    if method == "initialize": result = {"protocolVersion": "2025-06-18", "capabilities": {}}
    elif method == "tools/list": result = {"tools": [{"name": name} for name in names]}
    elif method == "tools/call": result = {"content": [{"type": "text", "text": "ok"}], "isError": False}
    else: result = {}
    print(json.dumps({"jsonrpc": "2.0", "id": request_id, "result": result}), flush=True)
"""


CODEX_SCRIPT = r"""
#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
state_path = Path(os.environ["FAKE_CODEX_STATE"])
state = json.loads(state_path.read_text()) if state_path.exists() else []
args = sys.argv[1:]
if args[:3] == ["mcp", "get", "mcpls"]:
    entry = next((item for item in state if item.get("name") == "mcpls"), None)
    if entry is None: raise SystemExit(1)
    print(json.dumps(entry))
elif args[:2] == ["mcp", "list"]:
    print(json.dumps(state))
elif args[:3] == ["mcp", "remove", "mcpls"]:
    state_path.write_text(json.dumps([item for item in state if item.get("name") != "mcpls"]))
else: raise SystemExit(2)
"""


class ScaffoldTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agents-project-mcpls-test-")
        self.root = Path(self.temp.name)
        self.home = self.root / "home"
        self.bin = self.root / "bin"
        self.home.mkdir()
        self.bin.mkdir()
        for name in ("git", "python3"):
            resolved = shutil.which(name)
            if resolved:
                (self.bin / name).symlink_to(resolved)
        self.child_path = self.root / "mcpls-child.pid"
        self.environ = mock.patch.dict(os.environ, {
            "HOME": str(self.home),
            "PATH": str(self.bin),
            "FAKE_MCPLS_CHILD": str(self.child_path),
            "FAKE_CODEX_STATE": str(self.root / "codex-state.json"),
        }, clear=False)
        self.environ.start()
        self.platform = mock.patch.object(common.sys, "platform", "darwin")
        self.platform.start()
        self.ready_mcpls()

    def tearDown(self):
        self.platform.stop()
        self.environ.stop()
        self.temp.cleanup()

    def write_executable(self, path, source):
        path.write_text(textwrap.dedent(source).lstrip(), encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def ready_mcpls(self):
        self.write_executable(self.bin / "mcpls", MCPLS_SCRIPT)

    def ready_language_servers(self):
        version = "#!/bin/sh\nexit 0\n"
        for name in (
            "basedpyright", "basedpyright-langserver", "typescript-language-server", "npm",
            "intelephense", "rust-analyzer", "clangd", "sourcekit-lsp",
        ):
            self.write_executable(self.bin / name, version)

    def git_project(self, name="project"):
        project = self.root / name
        project.mkdir()
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        return project

    def add_stack(self, project, stack):
        values = {
            "python": ("pyproject.toml", "src/main.py"),
            "typescript": ("package.json", "src/main.ts"),
            "php": ("composer.json", "src/main.php"),
            "rust": ("Cargo.toml", "src/main.rs"),
            "cpp": ("CMakeLists.txt", "src/main.cpp"),
            "swift": ("Package.swift", "Sources/main.swift"),
        }
        marker, source = values[stack]
        (project / marker).write_text("{}\n", encoding="utf-8")
        source_path = project / source
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_text("# source\n", encoding="utf-8")

    def add_harness(self, project, harness):
        if harness == "json":
            (project / "mcp.json").write_text('{\n  "mcpServers": {}\n}\n', encoding="utf-8")
        else:
            path = project / ".codex/config.toml"
            path.parent.mkdir(parents=True)
            path.write_text('model = "gpt-test"\n', encoding="utf-8")

    def run_main(self, argv):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = cli.main(argv)
        return result, stdout.getvalue(), stderr.getvalue()
