#!/usr/bin/env python3
"""Audit CSV headers and nullability against a small JSON column schema."""

import argparse
import csv
import json
import sys
from pathlib import Path


def load_schema(path):
    try:
        schema = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("cannot read schema file {}: {}".format(path, error))
    if not isinstance(schema, dict):
        raise ValueError("schema root must be a JSON object")

    required = schema.get("required_columns", [])
    columns = schema.get("columns", {})
    if not isinstance(required, list) or any(not isinstance(name, str) or not name for name in required):
        raise ValueError("required_columns must be an array of non-empty strings")
    if len(set(required)) != len(required):
        raise ValueError("required_columns must not contain duplicates")
    if not isinstance(columns, dict):
        raise ValueError("columns must be an object")
    for name, rule in columns.items():
        if not isinstance(name, str) or not name:
            raise ValueError("columns keys must be non-empty strings")
        if not isinstance(rule, dict):
            raise ValueError("column rule for {} must be an object".format(name))
        if "nullable" in rule and not isinstance(rule["nullable"], bool):
            raise ValueError("nullable for {} must be a boolean".format(name))
    return required, columns


def audit(csv_path, required, columns):
    errors = []
    try:
        stream = Path(csv_path).open("r", encoding="utf-8-sig", newline="")
    except OSError as error:
        raise ValueError("cannot read CSV file {}: {}".format(csv_path, error))

    try:
        reader = csv.reader(stream)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("CSV file is empty")

        indexes = {}
        for index, name in enumerate(header):
            indexes.setdefault(name, []).append(index)
        for name, occurrences in indexes.items():
            if len(occurrences) > 1:
                errors.append({"rule": "duplicate_header", "header": name,
                               "columns": [index + 1 for index in occurrences],
                               "message": "header appears more than once"})
        for name in required:
            if name not in indexes:
                errors.append({"rule": "required_column", "header": name,
                               "message": "required column is missing"})

        non_nullable = {name for name, rule in columns.items() if rule.get("nullable") is False}
        for line_number, row in enumerate(reader, 2):
            for name in sorted(non_nullable):
                positions = indexes.get(name, [])
                if not positions:
                    continue
                for index in positions:
                    value = row[index] if index < len(row) else ""
                    if not value.strip():
                        errors.append({"rule": "null_not_allowed", "header": name,
                                       "row": line_number, "column": index + 1,
                                       "message": "null value is not allowed"})
    except csv.Error as error:
        raise ValueError("malformed CSV: {}".format(error))
    finally:
        stream.close()
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", help="path to the CSV file")
    parser.add_argument("schema", help="path to the small JSON schema file")
    parser.add_argument("--json", action="store_true", help="emit a JSON result")
    args = parser.parse_args()
    try:
        required, columns = load_schema(args.schema)
        errors = audit(args.csv_file, required, columns)
    except ValueError as error:
        result = {"valid": False, "error_count": 1,
                  "errors": [{"rule": "input", "message": str(error)}]}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("error: {}".format(error), file=sys.stderr)
        return 2

    result = {"valid": not errors, "error_count": len(errors), "errors": errors}
    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        for error in errors:
            location = "row {}".format(error["row"]) if "row" in error else "header"
            print("{}: {} ({})".format(location, error["message"], error["rule"]))
    else:
        print("valid")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
