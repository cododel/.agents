import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts/check-skills.py"
SPEC = importlib.util.spec_from_file_location("check_skills", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
check_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_skills)


class ClientNeutralityTest(unittest.TestCase):
    def test_rejects_client_runtime_and_tool_api_markers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills/example/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("Use Claude Code through the Agent tool.\n", encoding="utf-8")

            errors = check_skills.validate_client_neutrality(root, [skill])

        self.assertEqual(2, len(errors))
        self.assertTrue(any("claude code" in error for error in errors))
        self.assertTrue(any("agent tool" in error for error in errors))

    def test_accepts_capability_based_independent_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "skills/example/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(
                "Use isolated read-only reviewers already exposed by the execution environment.\n",
                encoding="utf-8",
            )

            errors = check_skills.validate_client_neutrality(root, [skill])

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
