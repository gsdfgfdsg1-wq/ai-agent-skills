import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_csv.py"


class CsvSchemaAuditTests(unittest.TestCase):
    def run_audit(self, csv_text, schema):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            csv_path = root / "input.csv"
            schema_path = root / "schema.json"
            csv_path.write_text(csv_text, encoding="utf-8")
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(csv_path), str(schema_path), "--json"],
                capture_output=True, text=True, check=False,
            )

    def test_valid_csv_passes(self):
        result = self.run_audit(
            "id,email,nickname\n1,a@example.test,\n2,b@example.test,Bea\n",
            {"required_columns": ["id", "email"], "columns": {"id": {"nullable": False}, "email": {"nullable": False}}},
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["errors"], [])

    def test_duplicate_missing_and_null_are_reported(self):
        result = self.run_audit(
            "id,email,email\n,one@example.test,two@example.test\n",
            {"required_columns": ["id", "name"], "columns": {"id": {"nullable": False}}},
        )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual({item["rule"] for item in payload["errors"]},
                         {"duplicate_header", "required_column", "null_not_allowed"})

    def test_invalid_schema_is_input_error(self):
        result = self.run_audit("id\n1\n", {"columns": {"id": {"nullable": "no"}}})
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["errors"][0]["rule"], "input")


if __name__ == "__main__":
    unittest.main()
