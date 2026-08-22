"""Shared fake clients and isolated HOME fixture for scaffold tests."""

import contextlib
import io
import json
import os
from pathlib import Path
import plistlib
import shutil
import stat
import sys
import tempfile
import textwrap
import unittest
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

from code_intelligence_scaffold import cli, clients, common  # noqa: E402


CODEX_SCRIPT = r"""
#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
path = Path(os.environ["FAKE_CODEX_STATE"])
state = json.loads(path.read_text()) if path.exists() else []
args = sys.argv[1:]
if args[:2] == ["mcp", "list"]:
    print(json.dumps(state))
elif args[:2] == ["mcp", "get"]:
    entry = next((x for x in state if x.get("name") == args[2]), None)
    if entry is None: raise SystemExit(1)
    print(json.dumps(entry))
elif args[:2] == ["mcp", "add"]:
    sep = args.index("--"); name = args[2]
    entry = {
        "name": name, "enabled": True,
        "transport": {"type": "stdio", "command": args[sep+1], "args": args[sep+2:], "env": None, "env_vars": [], "cwd": None},
        "enabled_tools": None, "disabled_tools": None,
        "startup_timeout_sec": None, "tool_timeout_sec": None,
    }
    state = [x for x in state if x.get("name") != name] + [entry]
    path.write_text(json.dumps(state))
elif args[:2] == ["mcp", "remove"]:
    state = [x for x in state if x.get("name") != args[2]]
    path.write_text(json.dumps(state))
else: raise SystemExit(2)
"""


GROK_SCRIPT = r"""
#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
path = Path(os.environ["FAKE_GROK_STATE"])
state = json.loads(path.read_text()) if path.exists() else []
args = sys.argv[1:]
if args[:3] == ["mcp", "list", "--json"]:
    print(json.dumps(state))
elif args[:2] == ["mcp", "add"]:
    sep = args.index("--"); name = args[4]
    entry = {"command": args[sep+1], "args": args[sep+2:], "enabled": True, "name": name, "scope": "user"}
    state = [x for x in state if not (x.get("name") == name and x.get("scope") == "user")] + [entry]
    path.write_text(json.dumps(state))
elif args[:2] == ["mcp", "remove"]:
    name = args[4]
    state = [x for x in state if not (x.get("name") == name and x.get("scope") == "user")]
    path.write_text(json.dumps(state))
elif args[:2] == ["mcp", "doctor"]:
    entry = next((x for x in state if x.get("name") == args[2] and x.get("scope") == "user"), None)
    healthy = bool(entry and Path(entry["command"]).exists())
    print(json.dumps({"servers": [{"name": args[2], "healthy": healthy}]}))
else: raise SystemExit(2)
"""


CLAUDE_SCRIPT = r"""
#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
path = Path(os.environ["HOME"]) / ".claude.json"
value = json.loads(path.read_text()) if path.exists() and path.read_text().strip() else {}
servers = value.setdefault("mcpServers", {})
args = sys.argv[1:]
if args[:2] == ["mcp", "add"]:
    sep = args.index("--"); name = args[4]
    servers[name] = {"type": "stdio", "command": args[sep+1], "args": args[sep+2:], "env": {}}
    path.write_text(json.dumps(value))
elif args[:2] == ["mcp", "remove"]:
    servers.pop(args[4], None); path.write_text(json.dumps(value))
elif args == ["--version"]: print("2.1.221")
else: raise SystemExit(2)
"""


OPENCODE_SCRIPT = r"""
#!/usr/bin/env python3
import os, sys
if sys.argv[1:] == ["--version"]: print(os.environ.get("FAKE_OPENCODE_VERSION", "1.18.4"))
else: raise SystemExit(2)
"""


MCPLS_SCRIPT = r"""
#!/usr/bin/env python3
import json, os, subprocess, sys
from pathlib import Path
if sys.argv[1:] == ["--version"]:
    print("mcpls 0.3.9"); raise SystemExit(0)
child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
if os.environ.get("FAKE_MCPLS_CHILD"): Path(os.environ["FAKE_MCPLS_CHILD"]).write_text(str(child.pid))
names = ["get_hover", "get_definition", "get_references", "get_diagnostics", "get_code_actions", "get_document_symbols", "workspace_symbol_search", "rename_symbol", "prepare_call_hierarchy", "get_incoming_calls", "get_outgoing_calls"]
tool_calls = 0
for line in sys.stdin:
    message = json.loads(line); request_id = message.get("id")
    if request_id is None: continue
    if message["method"] == "initialize": result = {"protocolVersion": "2025-06-18", "capabilities": {}}
    elif message["method"] == "tools/list": result = {"tools": [{"name": x, "inputSchema": {"type": "object"}} for x in names]}
    elif message["method"] == "tools/call":
        tool_calls += 1
        if os.environ.get("FAKE_MCPLS_INITIALIZING_ONCE") and tool_calls == 1:
            print(json.dumps({"jsonrpc": "2.0", "id": request_id, "error": {"code": -32603, "message": "LSP server 'python' is still initializing"}}), flush=True)
            continue
        result = {"content": [{"type": "text", "text": "answer"}], "isError": False}
    else: result = {}
    print(json.dumps({"jsonrpc": "2.0", "id": request_id, "result": result}), flush=True)
"""


AST_GREP_SCRIPT = """
#!/usr/bin/env python3
import sys
if sys.argv[1:] == ["--version"]: print("ast-grep 0.45.0")
"""


OLD_MCPLS_SCRIPT = MCPLS_SCRIPT.replace("mcpls 0.3.9", "mcpls 0.3.8")
OLD_AST_GREP_SCRIPT = AST_GREP_SCRIPT.replace("0.45.0", "0.44.0")


MANAGER_SCRIPT = r"""
#!/usr/bin/env python3
import os, shutil, sys
from pathlib import Path
manager = Path(sys.argv[0]).name
with Path(os.environ["FAKE_INSTALL_LOG"]).open("a") as stream: stream.write(manager + " " + " ".join(sys.argv[1:]) + "\n")
if manager == "cargo": source, target = Path(os.environ["FAKE_MCPLS_TEMPLATE"]), Path(os.environ["FAKE_BIN"]) / "mcpls"
else: source, target = Path(os.environ["FAKE_AST_TEMPLATE"]), Path(os.environ["FAKE_BIN"]) / "ast-grep"
shutil.copyfile(str(source), str(target)); target.chmod(0o755)
"""


VERSION_SCRIPT = """
#!/usr/bin/env python3
print("fake language server 1.0.0")
"""


NOOP_SCRIPT = """
#!/usr/bin/env python3
import sys
if sys.argv[1:] == ["--version"]: print("0.1.0")
"""


class ScaffoldTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agents-code-intelligence-test-")
        self.root = Path(self.temp.name)
        self.home = self.root / "home"
        self.bin = self.root / "bin"
        self.xdg = self.root / "xdg"
        self.kimi_home = self.root / "kimi-home"
        self.tmp = self.root / "tmp"
        for path in (self.home, self.bin, self.xdg, self.kimi_home, self.tmp): path.mkdir()
        self.codex_state = self.root / "codex-state.json"
        self.grok_state = self.root / "grok-state.json"
        self.install_log = self.root / "install.log"
        self.child_path = self.root / "mcpls-child.pid"
        self.mcpls_template = self.root / "mcpls-template"
        self.ast_template = self.root / "ast-template"
        self.write_executable(self.mcpls_template, MCPLS_SCRIPT)
        self.write_executable(self.ast_template, AST_GREP_SCRIPT)
        self.write_executable(self.bin / "cargo", MANAGER_SCRIPT)
        self.write_executable(self.bin / "brew", MANAGER_SCRIPT)
        self.codex_state.write_text("[]")
        self.grok_state.write_text("[]")
        self.environment = mock.patch.dict(os.environ, {
            "HOME": str(self.home),
            "PATH": str(self.bin) + os.pathsep + "/usr/bin:/bin",
            "XDG_CONFIG_HOME": str(self.xdg),
            "KIMI_CODE_HOME": str(self.kimi_home),
            "TMPDIR": str(self.tmp),
            "FAKE_BIN": str(self.bin),
            "FAKE_CODEX_STATE": str(self.codex_state),
            "FAKE_GROK_STATE": str(self.grok_state),
            "FAKE_INSTALL_LOG": str(self.install_log),
            "FAKE_MCPLS_TEMPLATE": str(self.mcpls_template),
            "FAKE_AST_TEMPLATE": str(self.ast_template),
            "FAKE_MCPLS_CHILD": str(self.child_path),
            "FAKE_OPENCODE_VERSION": "1.18.4",
        }, clear=True)
        self.environment.start()
        self.platform = mock.patch.object(common.sys, "platform", "darwin")
        self.platform.start()
        self.real_detect_client = clients.detect_client
        self.client_detection = mock.patch.object(
            clients, "detect_client", side_effect=self.detect_client
        )
        self.client_detection.start()

    def tearDown(self):
        self.client_detection.stop()
        self.platform.stop()
        self.environment.stop()
        self.temp.cleanup()

    @staticmethod
    def write_executable(path, source):
        path.write_text(textwrap.dedent(source).lstrip(), encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def add_client(self, client_id):
        scripts = {
            "codex": CODEX_SCRIPT, "grok": GROK_SCRIPT, "claude-code": CLAUDE_SCRIPT,
            "kimi-code": NOOP_SCRIPT, "opencode": OPENCODE_SCRIPT, "pi": NOOP_SCRIPT,
        }
        binaries = {
            "codex": "codex", "grok": "grok", "claude-code": "claude",
            "kimi-code": "kimi", "opencode": "opencode", "pi": "pi",
        }
        if client_id == "antigravity":
            app = self.home / "Applications" / "Antigravity.app" / "Contents"
            app.mkdir(parents=True)
            with (app / "Info.plist").open("wb") as stream:
                plistlib.dump({"CFBundleIdentifier": "com.google.antigravity"}, stream)
            return
        self.write_executable(self.bin / binaries[client_id], scripts[client_id])

    def detect_client(self, delta):
        detection = delta["detection"]
        if detection["kind"] != "darwin_bundle":
            return self.real_detect_client(delta)
        application = self.home / "Applications" / "Antigravity.app"
        info_path = application / "Contents" / "Info.plist"
        if not info_path.is_file():
            return False, None
        with info_path.open("rb") as stream:
            info = plistlib.load(stream)
        if info.get("CFBundleIdentifier") != detection["bundle_id"]:
            return False, None
        return True, str(application)

    def ready_components(self, mcpls=True, ast=True):
        if mcpls:
            shutil.copyfile(str(self.mcpls_template), str(self.bin / "mcpls")); (self.bin / "mcpls").chmod(0o755)
        if ast:
            shutil.copyfile(str(self.ast_template), str(self.bin / "ast-grep")); (self.bin / "ast-grep").chmod(0o755)

    def language_servers(self):
        for name in [
            "basedpyright-langserver", "basedpyright", "typescript-language-server",
            "intelephense", "npm", "rust-analyzer", "clangd", "sourcekit-lsp",
        ]:
            self.write_executable(self.bin / name, VERSION_SCRIPT)

    def run_main(self, argv):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = cli.main(argv)
        return result, stdout.getvalue(), stderr.getvalue()

    def manifest(self):
        return common.read_manifest()

    def desired(self, client_id, major=None):
        return clients.desired_entry(self.manifest(), client_id, str((self.bin / "mcpls").resolve()), major)

    def write_json(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
