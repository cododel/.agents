import json
import os

from scaffold_test_support import ScaffoldTestCase
from code_intelligence_scaffold.jsonc import delete_path, get_path, set_path


class JsoncPatcherTest(ScaffoldTestCase):
    def test_set_and_delete_preserve_comments_trailing_commas_and_unrelated_text(self):
        source = '{\n  // keep this comment\n  "model": "x",\n}\n'
        entry = {"type": "local", "command": ["/x", "--config", "/c"]}
        updated = set_path(source, ["mcp", "mcpls"], entry)
        self.assertIn('// keep this comment\n  "model": "x",', updated)
        self.assertEqual((True, entry), get_path(updated, ["mcp", "mcpls"]))
        removed, changed = delete_path(updated, ["mcp", "mcpls"])
        self.assertTrue(changed)
        self.assertIn('// keep this comment\n  "model": "x",', removed)
        self.assertEqual((False, None), get_path(removed, ["mcp", "mcpls"]))

    def test_replacement_changes_only_target_value_span(self):
        source = '{\n  "mcp": {\n    "mcpls": {"command": ["/old"]},\n    // sibling\n    "other": {"url": "https://example.invalid"},\n  },\n  "theme": "dark",\n}\n'
        before_prefix = source.split('"mcpls"', 1)[0]
        before_suffix = source.split('// sibling', 1)[1]
        replacement = {"type": "local", "command": ["/new"]}
        updated = set_path(source, ["mcp", "mcpls"], replacement)
        self.assertTrue(updated.startswith(before_prefix))
        self.assertEqual(before_suffix, updated.split('// sibling', 1)[1])
        self.assertEqual((True, replacement), get_path(updated, ["mcp", "mcpls"]))

    def test_insertion_handles_inline_object_at_same_comma_offset(self):
        source = '{"mcp": {"servers": {"other": {"type": "remote"}}}}\n'
        entry = {"type": "local", "command": ["/x"]}
        updated = set_path(source, ["mcp", "servers", "mcpls"], entry)
        self.assertEqual((True, entry), get_path(updated, ["mcp", "servers", "mcpls"]))


class OpenCodeAdapterTest(ScaffoldTestCase):
    def test_v1_jsonc_apply_noop_and_unconfigure_preserve_unrelated_source(self):
        self.add_client("opencode")
        self.ready_components()
        path = self.xdg / "opencode" / "opencode.jsonc"
        path.parent.mkdir(parents=True)
        source = '{\n  // user preference\n  "model": "provider/model",\n}\n'
        path.write_text(source)

        result, _, stderr = self.run_main(["apply", "--client", "opencode"])
        self.assertEqual(0, result, stderr)
        updated = path.read_text()
        self.assertIn('// user preference\n  "model": "provider/model",', updated)
        self.assertEqual((True, self.desired("opencode", 1)), get_path(updated, ["mcp", "mcpls"]))

        before = path.read_bytes()
        result, stdout, stderr = self.run_main(["apply", "--client", "opencode"])
        self.assertEqual(0, result, stderr)
        self.assertIn("already configured", stdout)
        self.assertEqual(before, path.read_bytes())

        result, _, stderr = self.run_main(["unconfigure", "--client", "opencode"])
        self.assertEqual(0, result, stderr)
        removed = path.read_text()
        self.assertIn('// user preference\n  "model": "provider/model",', removed)
        self.assertEqual((False, None), get_path(removed, ["mcp", "mcpls"]))

    def test_v2_uses_nested_servers_shape(self):
        self.add_client("opencode")
        self.ready_components()
        os.environ["FAKE_OPENCODE_VERSION"] = "2.0.0"
        path = self.xdg / "opencode" / "opencode.json"
        path.parent.mkdir(parents=True)
        path.write_text('{"mcp": {"servers": {"other": {"type": "remote", "url": "https://example.invalid"}}}}\n')
        result, _, stderr = self.run_main(["apply", "--client", "opencode"])
        self.assertEqual(0, result, stderr)
        value = json.loads(path.read_text())
        self.assertEqual(self.desired("opencode", 2), value["mcp"]["servers"]["mcpls"])
        self.assertNotIn("mcpls", {key: value for key, value in value["mcp"].items() if key != "servers"})

    def test_mixed_v1_v2_mcpls_paths_fail_closed(self):
        self.add_client("opencode")
        self.ready_components()
        path = self.xdg / "opencode" / "opencode.jsonc"
        path.parent.mkdir(parents=True)
        path.write_text('{"mcp": {"mcpls": {"type": "local", "command": ["/one"]}, "servers": {"mcpls": {"type": "local", "command": ["/two"]}}}}\n')
        before = path.read_bytes()
        result, _, stderr = self.run_main(["apply", "--client", "opencode", "--replace"])
        self.assertEqual(2, result)
        self.assertIn("cannot inspect", stderr)
        self.assertEqual(before, path.read_bytes())

    def test_config_candidate_priority_prefers_jsonc(self):
        self.add_client("opencode")
        self.ready_components()
        directory = self.xdg / "opencode"
        directory.mkdir(parents=True)
        json_path = directory / "opencode.json"
        jsonc_path = directory / "opencode.jsonc"
        json_path.write_text('{"theme": "json"}\n')
        jsonc_path.write_text('{\n  // preferred\n  "theme": "jsonc",\n}\n')
        json_before = json_path.read_bytes()
        result, _, stderr = self.run_main(["apply", "--client", "opencode"])
        self.assertEqual(0, result, stderr)
        self.assertEqual(json_before, json_path.read_bytes())
        self.assertTrue(get_path(jsonc_path.read_text(), ["mcp", "mcpls"])[0])


if __name__ == "__main__":
    import unittest
    unittest.main()
