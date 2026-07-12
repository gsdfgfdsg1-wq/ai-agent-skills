import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "release_note_linter.py"
SPEC = importlib.util.spec_from_file_location("release_note_linter", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReleaseNoteLinterTests(unittest.TestCase):
    def test_released_note_at_version_and_issue_boundaries(self):
        markdown = "## [v1.0] - 2026-07-13\n\n## Added\n\n- Ship #1.\n"
        self.assertEqual([], MODULE.audit(markdown, "released", ["Added"]))

    def test_reports_mode_section_and_bad_issue_styles(self):
        markdown = "## [Unreleased]\n\n## Added\n\n- Fix GH-12, issue 13, #0, and item#14.\n"
        errors = MODULE.audit(markdown, "released", ["Fixed"])
        self.assertEqual({"unreleased_marker", "required_section", "issue_reference_style"},
                         {error["rule"] for error in errors})
        self.assertEqual(4, len([error for error in errors if error["rule"] == "issue_reference_style"]))

    def test_ignores_invalid_issue_style_in_fenced_code(self):
        markdown = "## [Unreleased]\n\n## Added\n\n```text\nGH-12\n```\n"
        self.assertEqual([], MODULE.audit(markdown, "unreleased", ["Added"]))


if __name__ == "__main__":
    unittest.main()
