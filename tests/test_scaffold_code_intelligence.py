import json
import os
import time
from unittest import mock

from scaffold_test_support import (
    OLD_AST_GREP_SCRIPT,
    OLD_MCPLS_SCRIPT,
    ScaffoldTestCase,
    common,
)


class ScaffoldContractTest(ScaffoldTestCase):
    def test_validate_accepts_tracked_contract(self):
        result, stdout, stderr = self.run_main(["validate"])
        self.assertEqual(0, result)
        self.assertIn("are valid", stdout)
        self.assertEqual("", stderr)

    def test_plan_is_read_only_and_reports_codex_delta(self):
        self.add_client("codex")
        self.ready_components()
        self.language_servers()
        unrelated = {"name": "other", "transport": {"type": "http"}}
        self.codex_state.write_text(json.dumps([unrelated]))
        before = self.codex_state.read_bytes()

        result, stdout, stderr = self.run_main(["plan", "--client", "codex", "--json"])

        self.assertEqual(0, result, stderr)
        self.assertEqual(before, self.codex_state.read_bytes())
        plan = json.loads(stdout)
        self.assertEqual([{
            "client": "codex", "kind": "client-delta", "name": "mcpls", "state": "missing",
        }], plan["actions"])
        self.assertEqual([{
            "detected": True, "id": "codex", "mode": "mcp_stdio", "state": "missing",
        }], plan["clients"])

    def test_plan_reports_rust_repair(self):
        self.add_client("codex")
        self.ready_components()
        self.language_servers()
        self.write_executable(self.bin / "rust-analyzer", "#!/usr/bin/env python3\nraise SystemExit(1)\n")
        result, stdout, stderr = self.run_main(["plan", "--client", "codex"])
        self.assertEqual(0, result, stderr)
        self.assertIn("fix: rustup component add rust-analyzer", stdout)

    def test_plan_reports_pinned_php_language_server_repair(self):
        self.add_client("codex")
        self.ready_components()
        self.language_servers()
        (self.bin / "intelephense").unlink()

        result, stdout, stderr = self.run_main(["plan", "--client", "codex"])

        self.assertEqual(0, result, stderr)
        self.assertIn("language server php is missing", stdout)
        self.assertIn("fix: npm install --global intelephense@1.18.5", stdout)

    def test_unsupported_platform_fails_before_external_commands(self):
        self.add_client("codex")
        self.platform.stop()
        self.platform = mock.patch.object(common.sys, "platform", "linux")
        self.platform.start()
        before = self.codex_state.read_bytes()
        result, _, stderr = self.run_main([
            "apply", "--client", "codex", "--install", "--replace",
        ])
        self.assertEqual(2, result)
        self.assertIn("unsupported platform", stderr)
        self.assertEqual(before, self.codex_state.read_bytes())
        self.assertFalse(self.install_log.exists())


class NativeClientTest(ScaffoldTestCase):
    def test_codex_install_preserves_other_mcp_and_is_idempotent(self):
        self.add_client("codex")
        unrelated = {"name": "other", "transport": {"type": "http"}}
        self.codex_state.write_text(json.dumps([unrelated]))

        result, _, stderr = self.run_main(["apply", "--client", "codex", "--install"])
        self.assertEqual(0, result, stderr)
        self.assertEqual([
            "cargo install mcpls --version 0.3.9 --locked",
            "brew install ast-grep",
        ], self.install_log.read_text().splitlines())
        entries = json.loads(self.codex_state.read_text())
        self.assertEqual(unrelated, entries[0])
        self.assertEqual(self.desired("codex"), entries[1])

        before_state = self.codex_state.read_bytes()
        before_log = self.install_log.read_bytes()
        result, stdout, stderr = self.run_main(["apply", "--client", "codex"])
        self.assertEqual(0, result, stderr)
        self.assertIn("already configured", stdout)
        self.assertEqual(before_state, self.codex_state.read_bytes())
        self.assertEqual(before_log, self.install_log.read_bytes())

    def test_native_clients_conflict_replace_and_unconfigure_are_scoped(self):
        self.ready_components()
        for client_id, state_path in (("codex", self.codex_state), ("grok", self.grok_state)):
            self.add_client(client_id)
            if client_id == "codex":
                foreign = {"name": "mcpls", "enabled": True, "transport": {"type": "stdio", "command": "/foreign/mcpls", "args": []}}
                unrelated = {"name": "other", "transport": {"type": "http"}}
            else:
                foreign = {"name": "mcpls", "command": "/foreign/mcpls", "args": [], "enabled": True, "scope": "user"}
                unrelated = {"name": "other", "command": "/other", "args": [], "enabled": True, "scope": "user"}
            state_path.write_text(json.dumps([unrelated, foreign]))
            before = state_path.read_bytes()
            result, _, stderr = self.run_main(["apply", "--client", client_id])
            self.assertEqual(2, result)
            self.assertIn("--replace", stderr)
            self.assertEqual(before, state_path.read_bytes())
            result, _, stderr = self.run_main(["apply", "--client", client_id, "--replace"])
            self.assertEqual(0, result, stderr)
            self.assertEqual(unrelated, json.loads(state_path.read_text())[0])
            result, _, stderr = self.run_main(["unconfigure", "--client", client_id])
            self.assertEqual(0, result, stderr)
            self.assertEqual([unrelated], json.loads(state_path.read_text()))

    def test_claude_uses_native_cli_and_preserves_user_config(self):
        self.add_client("claude-code")
        self.ready_components()
        config = self.home / ".claude.json"
        self.write_json(config, {"theme": "dark", "mcpServers": {"other": {"type": "http", "url": "https://example.invalid"}}})
        result, _, stderr = self.run_main(["apply", "--client", "claude-code"])
        self.assertEqual(0, result, stderr)
        value = json.loads(config.read_text())
        self.assertEqual("dark", value["theme"])
        self.assertEqual(self.desired("claude-code"), value["mcpServers"]["mcpls"])
        result, _, stderr = self.run_main(["unconfigure", "--client", "claude-code"])
        self.assertEqual(0, result, stderr)
        value = json.loads(config.read_text())
        self.assertIn("other", value["mcpServers"])
        self.assertNotIn("mcpls", value["mcpServers"])

    def test_refuses_component_install_without_flag(self):
        self.add_client("codex")
        before = self.codex_state.read_bytes()
        result, _, stderr = self.run_main(["apply", "--client", "codex"])
        self.assertEqual(2, result)
        self.assertIn("--install", stderr)
        self.assertEqual(before, self.codex_state.read_bytes())

    def test_updates_incompatible_component_versions(self):
        self.add_client("codex")
        self.write_executable(self.bin / "mcpls", OLD_MCPLS_SCRIPT)
        self.write_executable(self.bin / "ast-grep", OLD_AST_GREP_SCRIPT)
        result, _, stderr = self.run_main(["apply", "--client", "codex", "--install"])
        self.assertEqual(0, result, stderr)
        self.assertEqual([
            "cargo install mcpls --version 0.3.9 --locked",
            "brew upgrade ast-grep",
        ], self.install_log.read_text().splitlines())


class JsonClientTest(ScaffoldTestCase):
    def test_antigravity_empty_config_is_merged_and_unconfigured(self):
        self.add_client("antigravity")
        self.ready_components()
        path = self.home / ".gemini" / "config" / "mcp_config.json"
        path.parent.mkdir(parents=True)
        path.write_text("")
        result, _, stderr = self.run_main(["apply", "--client", "antigravity"])
        self.assertEqual(0, result, stderr)
        self.assertEqual(self.desired("antigravity"), json.loads(path.read_text())["mcpServers"]["mcpls"])
        result, _, stderr = self.run_main(["unconfigure", "--client", "antigravity"])
        self.assertEqual(0, result, stderr)
        self.assertNotIn("mcpls", json.loads(path.read_text())["mcpServers"])

    def test_kimi_honors_kimi_code_home_and_preserves_other_servers(self):
        self.add_client("kimi-code")
        self.ready_components()
        path = self.kimi_home / "mcp.json"
        other = {"command": "/other", "args": []}
        self.write_json(path, {"mcpServers": {"other": other}, "metadata": {"keep": True}})
        result, _, stderr = self.run_main(["apply", "--client", "kimi-code"])
        self.assertEqual(0, result, stderr)
        value = json.loads(path.read_text())
        self.assertEqual(other, value["mcpServers"]["other"])
        self.assertTrue(value["metadata"]["keep"])
        self.assertEqual(self.desired("kimi-code"), value["mcpServers"]["mcpls"])

    def test_plain_json_conflict_and_parse_error_fail_closed(self):
        self.add_client("kimi-code")
        self.ready_components()
        path = self.kimi_home / "mcp.json"
        self.write_json(path, {"mcpServers": {"mcpls": {"command": "/foreign/mcpls", "args": []}}})
        before = path.read_bytes()
        result, _, stderr = self.run_main(["apply", "--client", "kimi-code"])
        self.assertEqual(2, result)
        self.assertIn("--replace", stderr)
        self.assertEqual(before, path.read_bytes())
        path.write_text("{broken")
        before = path.read_bytes()
        result, _, stderr = self.run_main(["apply", "--client", "kimi-code", "--replace"])
        self.assertEqual(2, result)
        self.assertIn("cannot inspect", stderr)
        self.assertEqual(before, path.read_bytes())

    def test_unconfigure_foreign_entry_requires_force(self):
        self.add_client("kimi-code")
        path = self.kimi_home / "mcp.json"
        other = {"command": "/other", "args": []}
        self.write_json(path, {"mcpServers": {
            "other": other,
            "mcpls": {"command": "/foreign/mcpls", "args": []},
        }})
        before = path.read_bytes()
        result, _, stderr = self.run_main(["unconfigure", "--client", "kimi-code"])
        self.assertEqual(2, result)
        self.assertIn("--force", stderr)
        self.assertEqual(before, path.read_bytes())
        result, _, stderr = self.run_main([
            "unconfigure", "--client", "kimi-code", "--force",
        ])
        self.assertEqual(0, result, stderr)
        value = json.loads(path.read_text())
        self.assertEqual(other, value["mcpServers"]["other"])
        self.assertNotIn("mcpls", value["mcpServers"])


class MultiClientTest(ScaffoldTestCase):
    def test_all_skips_missing_clients_and_reports_pi_limitation(self):
        self.add_client("codex")
        self.add_client("pi")
        self.ready_components()
        self.language_servers()
        result, stdout, stderr = self.run_main(["plan", "--client", "all", "--json"])
        self.assertEqual(0, result, stderr)
        plan = json.loads(stdout)
        states = {item["id"]: item for item in plan["clients"]}
        self.assertEqual("missing", states["codex"]["state"])
        self.assertEqual("lsp_unsupported", states["pi"]["state"])
        self.assertEqual("skipped", states["grok"]["state"])

    def test_all_preflight_prevents_partial_client_writes(self):
        self.add_client("codex")
        self.add_client("kimi-code")
        self.ready_components()
        path = self.kimi_home / "mcp.json"
        self.write_json(path, {"mcpServers": {"mcpls": {"command": "/foreign/mcpls", "args": []}}})
        codex_before = self.codex_state.read_bytes()
        kimi_before = path.read_bytes()
        result, _, stderr = self.run_main(["apply", "--client", "all"])
        self.assertEqual(2, result)
        self.assertIn("--replace", stderr)
        self.assertEqual(codex_before, self.codex_state.read_bytes())
        self.assertEqual(kimi_before, path.read_bytes())

    def test_all_installs_components_once_and_configures_detected_clients(self):
        self.add_client("codex")
        self.add_client("pi")
        result, stdout, stderr = self.run_main(["apply", "--client", "all", "--install"])
        self.assertEqual(0, result, stderr)
        self.assertIn("Pi uses shared rules", stdout)
        self.assertEqual([
            "cargo install mcpls --version 0.3.9 --locked",
            "brew install ast-grep",
        ], self.install_log.read_text().splitlines())
        self.assertEqual(self.desired("codex"), json.loads(self.codex_state.read_text())[0])

    def test_pi_only_installs_ast_grep_without_mcpls_or_extension(self):
        self.add_client("pi")
        result, stdout, stderr = self.run_main(["apply", "--client", "pi", "--install"])
        self.assertEqual(0, result, stderr)
        self.assertIn("no MCP entry", stdout)
        self.assertEqual(["brew install ast-grep"], self.install_log.read_text().splitlines())
        self.assertFalse((self.bin / "mcpls").exists())
        self.assertFalse((self.home / ".pi" / "agent" / "mcp.json").exists())


class VerifyTest(ScaffoldTestCase):
    def test_verify_retries_while_language_server_initializes(self):
        self.add_client("codex")
        self.ready_components()
        self.language_servers()
        self.codex_state.write_text(json.dumps([self.desired("codex")]))
        os.environ["FAKE_MCPLS_INITIALIZING_ONCE"] = "1"

        result, stdout, stderr = self.run_main(["verify", "--client", "codex"])

        self.assertEqual(0, result, stderr)
        self.assertIn("Python semantic smoke", stdout)

    def test_verify_checks_exact_registry_and_cleans_process_group(self):
        self.add_client("codex")
        self.ready_components()
        self.language_servers()
        self.codex_state.write_text(json.dumps([self.desired("codex")]))
        result, stdout, stderr = self.run_main(["verify", "--client", "codex"])
        self.assertEqual(0, result, stderr)
        self.assertIn("Python semantic smoke", stdout)
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

    def test_verify_pi_is_honest_about_unsupported_lsp(self):
        self.add_client("pi")
        self.ready_components(mcpls=False)
        result, stdout, stderr = self.run_main(["verify", "--client", "pi"])
        self.assertEqual(0, result, stderr)
        self.assertIn("LSP remains unsupported", stdout)

    def test_verify_all_runs_shared_probe_once(self):
        for client_id in ("codex", "grok", "pi"):
            self.add_client(client_id)
        self.ready_components()
        self.language_servers()
        self.codex_state.write_text(json.dumps([self.desired("codex")]))
        self.grok_state.write_text(json.dumps([self.desired("grok")]))
        with mock.patch("code_intelligence_scaffold.cli.mcp_probe") as probe, mock.patch(
            "code_intelligence_scaffold.cli.verify_grok_doctor"
        ) as doctor:
            result, _, stderr = self.run_main(["verify", "--client", "all"])
        self.assertEqual(0, result, stderr)
        probe.assert_called_once()
        doctor.assert_called_once()


if __name__ == "__main__":
    import unittest
    unittest.main()
