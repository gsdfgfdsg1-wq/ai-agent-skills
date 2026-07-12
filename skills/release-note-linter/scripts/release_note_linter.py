#!/usr/bin/env python3
"""Lint Markdown release notes for headings, sections, markers, and issue references."""

import argparse
import json
import re
import sys
from pathlib import Path

H2_PATTERN = re.compile(r"^ {0,3}##[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$")
RELEASE_PATTERN = re.compile(r"^\[v\d+(?:\.\d+)+\] - \d{4}-\d{2}-\d{2}$")
UNRELEASED_PATTERN = re.compile(r"^\[unreleased\]$", re.IGNORECASE)
INVALID_ISSUE_PATTERN = re.compile(r"(?i)(?:\bgh-|\bissue\s+)\d+|(?<![\w#])#0\b|\w#\d+")


def normalize(value):
    return " ".join(value.strip().split()).casefold()


def read_markdown(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError("cannot read Markdown file {}: {}".format(path, error))


def headings(lines):
    result = []
    for line_number, line in enumerate(lines, 1):
        match = H2_PATTERN.match(line)
        if match:
            title = " ".join(match.group(1).strip().split())
            result.append((line_number, title, normalize(title)))
    return result


def audit(markdown, mode, required_sections):
    lines = markdown.splitlines()
    found_headings = headings(lines)
    errors = []
    title_headings = [(line, title) for line, title, _ in found_headings
                      if RELEASE_PATTERN.fullmatch(title) or UNRELEASED_PATTERN.fullmatch(title)]

    if len(title_headings) != 1:
        errors.append({"rule": "release_heading", "count": len(title_headings),
                       "message": "exactly one release version/date or Unreleased H2 heading is required"})
    else:
        line_number, title = title_headings[0]
        is_released = bool(RELEASE_PATTERN.fullmatch(title))
        if mode == "released" and not is_released:
            errors.append({"rule": "unreleased_marker", "line": line_number,
                           "message": "[Unreleased] is not allowed in released mode"})
        if mode == "unreleased" and is_released:
            errors.append({"rule": "release_heading", "line": line_number,
                           "message": "version/date heading is not allowed in unreleased mode"})

    available = {key for _, _, key in found_headings}
    for section in required_sections:
        if normalize(section) not in available:
            errors.append({"rule": "required_section", "heading": section,
                           "message": "required H2 section is missing"})

    in_fence = False
    for line_number, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or H2_PATTERN.match(line):
            continue
        for match in INVALID_ISSUE_PATTERN.finditer(line):
            errors.append({"rule": "issue_reference_style", "line": line_number,
                           "reference": match.group(0),
                           "message": "use #123 with a positive issue number"})
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown_file", help="path to the release notes Markdown file")
    parser.add_argument("--mode", choices=("released", "unreleased"), required=True,
                        help="whether the document is published or pending")
    parser.add_argument("--required-section", action="append", default=[], metavar="HEADING",
                        help="required H2 heading; may be repeated")
    parser.add_argument("--json", action="store_true", help="emit a JSON result")
    args = parser.parse_args()

    try:
        errors = audit(read_markdown(args.markdown_file), args.mode, args.required_section)
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
            print("{}: {}".format(error["rule"], error["message"]))
    else:
        print("valid")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
