import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "check_markdown_links.py"


class MarkdownLinkTests(unittest.TestCase):
    def run_check(self, path):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(path), "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_relative_file_and_anchor_links_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.md").write_text("# Quick Start\n\nReady.\n", encoding="utf-8")
            (root / "README.md").write_text("[Guide](guide.md#quick-start)\n[Local](#overview)\n\n# Overview\n", encoding="utf-8")
            result = self.run_check(root)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["errors"], [])

    def test_links_in_fenced_code_are_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("```markdown\n[Example](missing.md#absent)\n```\n", encoding="utf-8")
            result = self.run_check(root)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["errors"], [])

    def test_missing_file_and_anchor_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "guide.md").write_text("# Existing\n", encoding="utf-8")
            (root / "README.md").write_text("[Missing](missing.md)\n[Anchor](guide.md#absent)\n", encoding="utf-8")
            result = self.run_check(root)

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual({item["reason"] for item in payload["errors"]}, {"target file not found", "target anchor not found"})

    def test_missing_input_is_error(self):
        result = self.run_check(Path("not-a-real-markdown-path"))

        self.assertEqual(result.returncode, 2)
        self.assertIn("path is not a Markdown file or directory", json.loads(result.stdout)["errors"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
