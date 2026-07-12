import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "readme_section_audit.py"
SPEC = importlib.util.spec_from_file_location("readme_section_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReadmeSectionAuditTests(unittest.TestCase):
    def test_valid_readme_at_summary_boundary(self):
        markdown = "## Summary\n\nExactly ten\n\n## Usage\n\nRun it.\n"
        self.assertEqual([], MODULE.audit(markdown, ["Summary", "Usage"], "Summary", 11, 11))

    def test_reports_duplicate_missing_and_long_summary(self):
        markdown = "## Summary\n\nThis summary is much too long.\n\n## Usage\n\nRun.\n\n## Usage\n\nAgain.\n"
        errors = MODULE.audit(markdown, ["Summary", "Install"], "Summary", None, 10)
        self.assertEqual({"duplicate_heading", "required_section", "summary_too_long"},
                         {error["rule"] for error in errors})

    def test_reports_missing_summary_paragraph(self):
        errors = MODULE.audit("## Summary\n\n## Usage\n", [], "Summary", 0, None)
        self.assertEqual("summary_missing", errors[0]["rule"])


if __name__ == "__main__":
    unittest.main()
