import unittest

from scaffold_test_support import ScaffoldTestCase
from code_intelligence_scaffold.jsonc import delete_path, get_path, set_path


class JsoncPatcherTest(ScaffoldTestCase):
    def test_set_and_delete_preserve_comments_trailing_commas_and_unrelated_text(self):
        source = '{\n  // keep this comment\n  "model": "x",\n}\n'
        entry = {"command": "/x", "args": ["--config", ".agents/mcpls.toml"]}
        updated = set_path(source, ["mcpServers", "mcpls"], entry)
        self.assertIn('// keep this comment\n  "model": "x",', updated)
        self.assertEqual((True, entry), get_path(updated, ["mcpServers", "mcpls"]))
        removed, changed = delete_path(updated, ["mcpServers", "mcpls"])
        self.assertTrue(changed)
        self.assertIn('// keep this comment\n  "model": "x",', removed)
        self.assertEqual((False, None), get_path(removed, ["mcpServers", "mcpls"]))

    def test_replacement_changes_only_target_value_span(self):
        source = '{\n  "mcpServers": {\n    "mcpls": {"command": "/old/mcpls"},\n    // sibling\n    "other": {"url": "https://example.invalid"},\n  },\n}\n'
        replacement = {"command": "/new/mcpls"}
        updated = set_path(source, ["mcpServers", "mcpls"], replacement)
        self.assertEqual((True, replacement), get_path(updated, ["mcpServers", "mcpls"]))
        self.assertIn('// sibling\n    "other"', updated)


if __name__ == "__main__":
    unittest.main()
