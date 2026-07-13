#!/usr/bin/env python3
"""Lint GraphQL SDL files with text checks and no external dependencies."""

import argparse
import json
import re
import sys
from pathlib import Path

TYPE_DEFINITION_RE = re.compile(
    r"^\s*(?:extend\s+)?(?:type|interface|input|enum|union|scalar)\s+([_A-Za-z][_0-9A-Za-z]*)\b"
)
BLOCK_DEFINITION_RE = re.compile(r"^\s*(?:extend\s+)?(?:type|interface|input|enum)\b")
FIELD_RE = re.compile(r"^\s*([_A-Za-z][_0-9A-Za-z]*)\s*(?:\([^)]*\))?\s*:")
PASCAL_CASE_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")
LOWER_CAMEL_CASE_RE = re.compile(r"^[a-z][A-Za-z0-9]*$")


def issue(line, rule, message):
    return {"line": line, "rule": rule, "message": message}


def strip_comments_and_strings(line, in_block_string):
    """Remove comments and string contents while preserving braces outside strings."""
    result = []
    index = 0
    while index < len(line):
        if line.startswith('"""', index):
            in_block_string = not in_block_string
            index += 3
            continue
        if in_block_string:
            index += 1
            continue
        character = line[index]
        if character == '#':
            break
        if character == '"':
            index += 1
            while index < len(line):
                if line[index] == '\\':
                    index += 2
                elif line[index] == '"':
                    index += 1
                    break
                else:
                    index += 1
            continue
        result.append(character)
        index += 1
    return ''.join(result), in_block_string


def lint_schema(text, max_line_length=None):
    """Return practical GraphQL SDL issues found in text."""
    issues = []
    type_definitions = {}
    brace_stack = []
    in_block_string = False
    pending_block = False

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if max_line_length is not None and len(raw_line) > max_line_length:
            issues.append(issue(
                line_number,
                "max-line-length",
                "line has {} characters; limit is {}".format(len(raw_line), max_line_length),
            ))

        code, in_block_string = strip_comments_and_strings(raw_line, in_block_string)
        declaration = TYPE_DEFINITION_RE.match(code)
        if declaration:
            name = declaration.group(1)
            if not PASCAL_CASE_RE.fullmatch(name):
                issues.append(issue(
                    line_number,
                    "type-name",
                    "type name '{}' must use PascalCase".format(name),
                ))
            if name in type_definitions:
                issues.append(issue(
                    line_number,
                    "duplicate-type-definition",
                    "type '{}' was already defined on line {}".format(name, type_definitions[name]),
                ))
            else:
                type_definitions[name] = line_number

        if BLOCK_DEFINITION_RE.match(code):
            pending_block = True

        for character in code:
            if character == '{':
                brace_stack.append(line_number)
                pending_block = False
            elif character == '}':
                if brace_stack:
                    brace_stack.pop()
                else:
                    issues.append(issue(line_number, "unmatched-closing-brace", "closing brace has no matching opening brace"))

        if brace_stack and not pending_block and '{' not in code:
            field = FIELD_RE.match(code)
            if field:
                name = field.group(1)
                if name != "_" and not LOWER_CAMEL_CASE_RE.fullmatch(name):
                    issues.append(issue(
                        line_number,
                        "field-name",
                        "field name '{}' must use lowerCamelCase".format(name),
                    ))

    for opening_line in brace_stack:
        issues.append(issue(opening_line, "unclosed-opening-brace", "opening brace is not closed"))

    return issues


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError("cannot read {}: {}".format(path, error)) from error


def main():
    parser = argparse.ArgumentParser(description="Lint a GraphQL SDL schema file.")
    parser.add_argument("file", help="path to the GraphQL SDL file")
    parser.add_argument("--max-line-length", type=int, help="maximum permitted line length")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    if args.max_line_length is not None and args.max_line_length < 1:
        parser.error("--max-line-length must be greater than zero")

    try:
        issues = lint_schema(read_text(args.file), args.max_line_length)
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
