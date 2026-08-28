import json
import os
from pathlib import Path
import subprocess
import time

from scaffold_test_support import CODEX_SCRIPT, ScaffoldTestCase


class ManifestAndSurfaceTest(ScaffoldTestCase):
    def test_validate_and_public_commands(self):
        result, stdout, stderr = self.run_main(["validate"])
        self.assertEqual(0, result, stderr)
        self.assertIn("project-scoped", stdout)
        parser = __import__("code_intelligence_scaffold.cli", fromlist=["parser"]).parser()
        choices = parser._subparsers._group_actions[0].choices
        self.assertEqual(
            {"validate", "inspect-project", "setup-project", "verify-project", "unconfigure-global"},
            set(choices),
        )

    def test_non_git_and_home_roots_are_rejected(self):
        result, _, stderr = self.run_main(["inspect-project", "--root", str(self.root)])
        self.assertEqual(2, result)
        self.assertIn("not inside a Git checkout", stderr)
        subprocess.run(["git", "init", "-q", str(self.home)], check=True)
        result, _, stderr = self.run_main(["inspect-project", "--root", str(self.home)])
        self.assertEqual(2, result)
        self.assertIn("unsafe Git root", stderr)


class DetectionTest(ScaffoldTestCase):
    def test_each_supported_stack_requires_marker_and_source(self):
        self.ready_language_servers()
        for stack in ("python", "typescript", "php", "rust", "cpp", "swift"):
            project = self.git_project(stack)
            self.add_stack(project, stack)
            result, stdout, stderr = self.run_main([
                "inspect-project", "--root", str(project), "--json",
            ])
            self.assertEqual(0, result, stderr)
            self.assertEqual([stack], json.loads(stdout)["languages"])

    def test_mixed_monorepo_and_ignored_dependencies(self):
        self.ready_language_servers()
        project = self.git_project()
        self.add_stack(project, "python")
        self.add_stack(project, "rust")
        dependency = project / "node_modules/package"
        dependency.mkdir(parents=True)
        (dependency / "package.json").write_text("{}")
        (dependency / "index.ts").write_text("export {}")
        result, stdout, stderr = self.run_main([
            "inspect-project", "--root", str(project), "--json",
        ])
        self.assertEqual(0, result, stderr)
        self.assertEqual(["python", "rust"], json.loads(stdout)["languages"])


class ProjectSetupTest(ScaffoldTestCase):
    def setUp(self):
        super().setUp()
        self.ready_language_servers()
        self.project = self.git_project()
        self.add_stack(self.project, "python")

    def test_no_harness_creates_nothing_and_reports_action(self):
        result, stdout, stderr = self.run_main(["setup-project", "--root", str(self.project)])
        self.assertEqual(0, result, stderr)
        self.assertIn("create mcp.json and/or .codex/config.toml", stdout)
        self.assertFalse((self.project / ".agents").exists())

    def test_json_only_preserves_comments_siblings_and_env(self):
        path = self.project / "mcp.json"
        source = '''{
  // keep project comment
  "mcpServers": {
    "other": {"url": "https://example.invalid"},
    "mcpls": {"command": "/old/mcpls", "args": [], "env": {"KEEP": "yes"}}
  },
  "theme": "dark"
}
'''
        path.write_text(source)
        result, _, stderr = self.run_main(["setup-project", "--root", str(self.project)])
        self.assertEqual(0, result, stderr)
        updated = path.read_text()
        self.assertIn("// keep project comment", updated)
        self.assertIn('"other": {"url": "https://example.invalid"}', updated)
        self.assertIn('"KEEP": "yes"', updated)
        self.assertIn(
            'roots = [{}]'.format(json.dumps(str(self.project.resolve()))),
            (self.project / ".agents/mcpls.toml").read_text(),
        )
        self.assertNotIn("typescript-language-server", (self.project / ".agents/mcpls.toml").read_text())

    def test_codex_only_preserves_comments_siblings_env_and_sets_cwd(self):
        path = self.project / ".codex/config.toml"
        path.parent.mkdir(parents=True)
        path.write_text('''# keep top
model = "gpt-test"

[mcp_servers.other]
url = "https://example.invalid"

[mcp_servers.mcpls]
command = "/old/mcpls" # keep inline
args = []

[mcp_servers.mcpls.env]
KEEP = "yes"
''')
        result, _, stderr = self.run_main(["setup-project", "--root", str(self.project)])
        self.assertEqual(0, result, stderr)
        updated = path.read_text()
        self.assertIn("# keep top", updated)
        self.assertIn("# keep inline", updated)
        self.assertIn("[mcp_servers.other]", updated)
        self.assertIn('[mcp_servers.mcpls.env]\nKEEP = "yes"', updated)
        self.assertIn('cwd = ".."', updated)
        self.assertIn('args = ["--config", ".agents/mcpls.toml"]', updated)

    def test_both_harnesses_and_second_run_are_byte_idempotent(self):
        self.add_harness(self.project, "json")
        self.add_harness(self.project, "codex")
        result, _, stderr = self.run_main(["setup-project", "--root", str(self.project)])
        self.assertEqual(0, result, stderr)
        paths = [
            self.project / "mcp.json",
            self.project / ".codex/config.toml",
            self.project / ".agents/mcpls.toml",
        ]
        before = {path: path.read_bytes() for path in paths}
        result, stdout, stderr = self.run_main(["setup-project", "--root", str(self.project)])
        self.assertEqual(0, result, stderr)
        self.assertIn("already configured", stdout)
        self.assertEqual(before, {path: path.read_bytes() for path in paths})

    def test_missing_lsp_is_configured_and_exact_repair_is_reported(self):
        (self.bin / "basedpyright-langserver").unlink()
        self.add_harness(self.project, "json")
        result, stdout, stderr = self.run_main(["setup-project", "--root", str(self.project)])
        self.assertEqual(0, result, stderr)
        self.assertIn("pipx install basedpyright", stdout)
        self.assertIn("basedpyright-langserver", (self.project / ".agents/mcpls.toml").read_text())

    def test_missing_mcpls_fails_before_writes(self):
        (self.bin / "mcpls").unlink()
        self.add_harness(self.project, "json")
        before = (self.project / "mcp.json").read_bytes()
        result, _, stderr = self.run_main(["setup-project", "--root", str(self.project)])
        self.assertEqual(2, result)
        self.assertIn("cargo install mcpls --version 0.3.9 --locked", stderr)
        self.assertEqual(before, (self.project / "mcp.json").read_bytes())
        self.assertFalse((self.project / ".agents").exists())

    def test_foreign_entry_and_foreign_generated_file_fail_closed(self):
        path = self.project / "mcp.json"
        path.write_text('{"mcpServers":{"mcpls":{"command":"/foreign/server"}}}\n')
        before = path.read_bytes()
        result, _, stderr = self.run_main(["setup-project", "--root", str(self.project)])
        self.assertEqual(2, result)
        self.assertIn("foreign", stderr)
        self.assertEqual(before, path.read_bytes())
        self.assertFalse((self.project / ".agents").exists())
        path.write_text('{"mcpServers":{}}\n')
        generated = self.project / ".agents/mcpls.toml"
        generated.parent.mkdir()
        generated.write_text('[workspace]\nroots = ["."]\n')
        result, _, stderr = self.run_main(["setup-project", "--root", str(self.project)])
        self.assertEqual(2, result)
        self.assertIn("not owned", stderr)

    def test_linked_worktree_resolves_its_own_root(self):
        self.add_harness(self.project, "json")
        subprocess.run(["git", "-C", str(self.project), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.project), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.project), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.project), "commit", "-qm", "init"], check=True)
        linked = self.root / "linked"
        subprocess.run(["git", "-C", str(self.project), "worktree", "add", "-qb", "test-linked", str(linked)], check=True)
        result, stdout, stderr = self.run_main([
            "inspect-project", "--root", str(linked / "src"), "--json",
        ])
        self.assertEqual(0, result, stderr)
        self.assertEqual(str(linked.resolve()), json.loads(stdout)["root"])


class VerificationAndLegacyTest(ScaffoldTestCase):
    def test_verify_runs_handshake_semantic_request_and_cleans_child(self):
        self.ready_language_servers()
        project = self.git_project()
        self.add_stack(project, "python")
        self.add_harness(project, "json")
        self.assertEqual(0, self.run_main(["setup-project", "--root", str(project)])[0])
        result, stdout, stderr = self.run_main(["verify-project", "--root", str(project)])
        self.assertEqual(0, result, stderr)
        self.assertIn("verified: exact project config", stdout)
        child_pid = int(self.child_path.read_text())
        deadline = time.monotonic() + 3
        while time.monotonic() < deadline:
            try:
                os.kill(child_pid, 0)
            except ProcessLookupError:
                break
            time.sleep(0.05)
        else:
            self.fail("fake child language server survived the MCP probe")

    def test_unconfigure_global_codex_preserves_sibling(self):
        self.write_executable(self.bin / "codex", CODEX_SCRIPT)
        state_path = Path(os.environ["FAKE_CODEX_STATE"])
        sibling = {"name": "other", "transport": {"type": "http"}}
        mcpls = {
            "name": "mcpls",
            "transport": {"type": "stdio", "command": "/usr/local/bin/mcpls", "args": []},
        }
        state_path.write_text(json.dumps([sibling, mcpls]))
        result, _, stderr = self.run_main(["unconfigure-global", "--client", "codex"])
        self.assertEqual(0, result, stderr)
        self.assertEqual([sibling], json.loads(state_path.read_text()))
