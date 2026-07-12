import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "gitignore_audit.py"


class GitignoreAuditTests(unittest.TestCase):
    def run_audit(self, root):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root), "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

    def initialize_repository(self, root):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.test"], check=True)
        subprocess.run(["git", "-C", str(root), "config", "user.name", "Test User"], check=True)

    def test_clean_repository_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize_repository(root)
            (root / "kept.txt").write_text("kept\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "kept.txt"], check=True)
            result = self.run_audit(root)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["findings"], [])

    def test_tracked_ignored_file_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize_repository(root)
            (root / ".gitignore").write_text("*.log\n", encoding="utf-8")
            (root / "debug.log").write_text("tracked\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "-f", ".gitignore", "debug.log"], check=True)
            result = self.run_audit(root)

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["findings"][0]["path"], "debug.log")
        self.assertEqual(payload["findings"][0]["pattern"], "*.log")

    def test_non_repository_is_input_error(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_audit(Path(directory))

        self.assertEqual(result.returncode, 2)
        self.assertIn("not a Git worktree", json.loads(result.stdout)["error"])


if __name__ == "__main__":
    unittest.main()
