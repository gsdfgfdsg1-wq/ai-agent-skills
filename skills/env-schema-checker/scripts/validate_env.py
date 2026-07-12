#!/usr/bin/env python3
"""Validate dotenv values against a focused top-level JSON Schema subset."""

import argparse
import json
import re
import sys
from pathlib import Path


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("cannot read JSON file {}: {}".format(path, error))


def parse_dotenv(path):
    values = {}
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ValueError("cannot read dotenv file {}: {}".format(path, error))
    for line_number, raw_line in enumerate(lines, 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        if "=" not in line:
            raise ValueError("invalid dotenv line {}: expected KEY=VALUE".format(line_number))
        key, value = line.split("=", 1)
        key = key.strip()
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise ValueError("invalid key on line {}: {}".format(line_number, key))
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("\"", chr(39)):
            value = value[1:-1]
        values[key] = value
    return values


def matches_type(value, expected_type):
    if expected_type == "string":
        return True
    if expected_type == "boolean":
        return value in ("true", "false")
    if expected_type == "integer":
        return bool(re.fullmatch(r"[+-]?\d+", value))
    if expected_type == "number":
        try:
            float(value)
            return True
        except ValueError:
            return False
    if expected_type in ("array", "object", "null"):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return False
        return ((expected_type == "array" and isinstance(decoded, list)) or
                (expected_type == "object" and isinstance(decoded, dict)) or
                (expected_type == "null" and decoded is None))
    return None


def validate(values, schema):
    if not isinstance(schema, dict):
        raise ValueError("schema root must be a JSON object")
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    if not isinstance(properties, dict) or not isinstance(required, list):
        raise ValueError("schema properties must be an object and required must be an array")
    errors = []
    for key in required:
        if not isinstance(key, str):
            raise ValueError("every required key must be a string")
        if key not in values:
            errors.append({"key": key, "rule": "required", "message": "missing required key"})
    if schema.get("additionalProperties") is False:
        for key in sorted(set(values) - set(properties)):
            errors.append({"key": key, "rule": "allowed", "message": "key is not allowed"})
    for key, value in values.items():
        rule = properties.get(key)
        if not isinstance(rule, dict):
            continue
        expected_type = rule.get("type")
        if expected_type is not None:
            types = expected_type if isinstance(expected_type, list) else [expected_type]
            matches = [matches_type(value, item) for item in types]
            if any(result is None for result in matches):
                raise ValueError("unsupported type for key {}".format(key))
            if not any(matches):
                errors.append({"key": key, "rule": "type", "message": "expected {}".format(expected_type)})
                continue
        if "enum" in rule and value not in [str(item) for item in rule["enum"]]:
            errors.append({"key": key, "rule": "enum", "message": "value is not in enum"})
        if rule.get("type") == "string" and "minLength" in rule and len(value) < rule["minLength"]:
            errors.append({"key": key, "rule": "minLength", "message": "value is too short"})
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dotenv", help="path to dotenv file")
    parser.add_argument("schema", help="path to top-level JSON Schema file")
    parser.add_argument("--json", action="store_true", help="emit a JSON result")
    args = parser.parse_args()
    try:
        errors = validate(parse_dotenv(args.dotenv), load_json(args.schema))
    except ValueError as error:
        if args.json:
            print(json.dumps({"valid": False, "errors": [{"rule": "input", "message": str(error)}]}))
        else:
            print("error: {}".format(error), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    elif errors:
        for error in errors:
            print("{}: {} ({})".format(error["key"], error["message"], error["rule"]))
    else:
        print("valid")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
