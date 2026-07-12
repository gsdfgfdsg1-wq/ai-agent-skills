#!/usr/bin/env python3
"""Recursively redact JSON values by field name or field-name regular expression."""

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


def compile_patterns(patterns):
    try:
        return [re.compile(pattern) for pattern in patterns]
    except re.error as error:
        raise ValueError("invalid field regular expression: {}".format(error))


def redact(value, field_names, patterns, replacement):
    if isinstance(value, dict):
        result = {}
        for key, child in value.items():
            if key.casefold() in field_names or any(pattern.fullmatch(key) for pattern in patterns):
                result[key] = replacement
            else:
                result[key] = redact(child, field_names, patterns, replacement)
        return result
    if isinstance(value, list):
        return [redact(item, field_names, patterns, replacement) for item in value]
    return value


def write_json(path, value):
    try:
        Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as error:
        raise ValueError("cannot write JSON file {}: {}".format(path, error))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="path to the source JSON fixture")
    parser.add_argument("--output", required=True, help="path for the redacted JSON fixture")
    parser.add_argument("--field", action="append", default=[], help="case-insensitive field name to redact; repeatable")
    parser.add_argument("--field-regex", action="append", default=[], help="regular expression matching a complete field name; repeatable")
    parser.add_argument("--replacement", default="[REDACTED]", help="replacement JSON string value")
    args = parser.parse_args()

    if not args.field and not args.field_regex:
        parser.error("provide at least one --field or --field-regex rule")

    try:
        document = load_json(args.input)
        patterns = compile_patterns(args.field_regex)
        redacted = redact(document, {field.casefold() for field in args.field}, patterns, args.replacement)
        write_json(args.output, redacted)
    except ValueError as error:
        print("error: {}".format(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
