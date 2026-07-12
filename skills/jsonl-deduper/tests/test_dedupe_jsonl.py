import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "dedupe_jsonl.py"


class JsonlDeduperTests(unittest.TestCase):
    def run_dedupe(self, contents, keep="first", key="id"):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        input_path = root / "input.jsonl"
        output_path = root / "output.jsonl"
        stats_path = root / "stats.json"
        input_path.write_text(contents, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(input_path), str(output_path), "--key", key,
             "--keep", keep, "--stats-json", str(stats_path)],
            capture_output=True, text=True, check=False,
        )
        return result, output_path, stats_path

    def test_keep_first_writes_unique_records_and_stats(self):
        result, output_path, stats_path = self.run_dedupe(
            '{"id":"a","version":1}\n{"id":"b"}\n{"id":"a","version":2}\n'
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual([json.loads(line) for line in output_path.read_text(encoding="utf-8").splitlines()],
                         [{"id": "a", "version": 1}, {"id": "b"}])
        self.assertEqual(json.loads(stats_path.read_text(encoding="utf-8"))["duplicates_removed"], 1)

    def test_keep_last_retains_last_position_order(self):
        result, output_path, _ = self.run_dedupe(
            '{"id":"a","version":1}\n{"id":"b"}\n{"id":"a","version":2}\n', keep="last"
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual([json.loads(line) for line in output_path.read_text(encoding="utf-8").splitlines()],
                         [{"id": "b"}, {"id": "a", "version": 2}])

    def test_malformed_or_missing_key_fails_without_output(self):
        result, output_path, _ = self.run_dedupe('{"id":"a"}\n{"name":"missing"}\n')
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing key id", result.stderr)
        self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
