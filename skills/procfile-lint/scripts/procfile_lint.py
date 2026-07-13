#!/usr/bin/env python3
"""Lint Procfile process declarations using only the Python standard library."""

import argparse
import json
import re
import sys
from pathlib import Path

PROCESS_TYPE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


def issue(line, rule, message):
    return {"line": line, "rule": rule, "message": message}


def lint_procfile(text):
    """Return Procfile declaration issues found in text."""
    issues = []
    seen_types = {}

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if ":" not in raw_line:
            issues.append(issue(
                line_number,
                "missing-colon",
                "process declaration must contain ':' between type and command",
            ))
            continue

        process_type, command = raw_line.split(":", 1)
        process_type = process_type.strip()
        command = command.strip()

        if not process_type:
            issues.append(issue(line_number, "empty-process-type", "process type must not be empty"))
        elif not PROCESS_TYPE_RE.fullmatch(process_type):
            issues.append(issue(
                line_number,
                "invalid-process-type",
                "process type must start with a letter and contain only letters, digits, '_' or '-'",
            ))
        elif process_type in seen_types:
            issues.append(issue(
                line_number,
                "duplicate-process-type",
                "process type '{}' was already declared on line {}".format(
                    process_type, seen_types[process_type]
                ),
            ))
        else:
            seen_types[process_type] = line_number

        if not command:
            issues.append(issue(line_number, "empty-command", "process command must not be empty"))

    return issues


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError("cannot read {}: {}".format(path, error)) from error


def main():
    parser = argparse.ArgumentParser(description="Lint a Procfile.")
    parser.add_argument("file", help="path to the Procfile")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    try:
        issues = lint_procfile(read_text(args.file))
    except ValueError as error:
        if args.json:
            print(json.dumps({"file": args.file, "error": str(error), "issues": []}))
        else:
            print("Error: {}".format(error), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"file": args.file, "issues": issues}, indent=2))
    elif issues:
        print("Issues in {}:".format(args.file))
        for item in issues:
            print("  line {line}: [{rule}] {message}".format(**item))
        print("Total: {} issue(s)".format(len(issues)))
    else:
        print("No issues found in {}".format(args.file))

    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
