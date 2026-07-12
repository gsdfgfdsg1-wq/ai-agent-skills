#!/usr/bin/env python3
"""Check Markdown README H2 sections, duplicate headings, and summary length."""

import argparse
import json
import re
import sys
from pathlib import Path

H2_PATTERN = re.compile(r"^ {0,3}##[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$")


def normalize_heading(value):
    return " ".join(value.strip().split()).casefold()


def read_markdown(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError("cannot read Markdown file {}: {}".format(path, error))


def h2_headings(lines):
    headings = []
    for line_number, line in enumerate(lines, 1):
        match = H2_PATTERN.match(line)
        if match:
            title = " ".join(match.group(1).strip().split())
            headings.append((line_number, title, normalize_heading(title)))
    return headings


def summary_after(lines, heading_index):
    paragraph = []
    for line in lines[heading_index + 1:]:
        if H2_PATTERN.match(line):
            break
        stripped = line.strip()
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith("#"):
            if paragraph:
                break
            continue
        paragraph.append(stripped)
    return " ".join(" ".join(paragraph).split())


def audit(markdown, required_sections, summary_section, min_length, max_length):
    lines = markdown.splitlines()
    headings = h2_headings(lines)
    errors = []
    locations = {}
    for line_number, title, normalized in headings:
        locations.setdefault(normalized, []).append(line_number)

    for normalized, line_numbers in locations.items():
        if len(line_numbers) > 1:
            errors.append({"rule": "duplicate_heading", "heading": headings_by_key(headings, normalized),
                           "lines": line_numbers, "message": "H2 heading appears more than once"})

    for title in required_sections:
        if normalize_heading(title) not in locations:
            errors.append({"rule": "required_section", "heading": title,
                           "message": "required H2 section is missing"})

    if min_length is not None or max_length is not None:
        target = normalize_heading(summary_section)
        matches = [(index, item) for index, item in enumerate(headings) if item[2] == target]
        if not matches:
            errors.append({"rule": "summary_section", "heading": summary_section,
                           "message": "summary H2 section is missing"})
        else:
            line_number = matches[0][1][0]
            summary = summary_after(lines, line_number - 1)
            if not summary:
                errors.append({"rule": "summary_missing", "heading": summary_section,
                               "line": line_number, "message": "summary paragraph is missing"})
            else:
                length = len(summary)
                if min_length is not None and length < min_length:
                    errors.append({"rule": "summary_too_short", "heading": summary_section,
                                   "line": line_number, "length": length, "minimum": min_length,
                                   "message": "summary is shorter than the minimum length"})
                if max_length is not None and length > max_length:
                    errors.append({"rule": "summary_too_long", "heading": summary_section,
                                   "line": line_number, "length": length, "maximum": max_length,
                                   "message": "summary exceeds the maximum length"})
    return errors


def headings_by_key(headings, normalized):
    for _, title, key in headings:
        if key == normalized:
            return title
    return normalized


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown_file", help="path to the README Markdown file")
    parser.add_argument("--required-section", action="append", default=[], metavar="HEADING",
                        help="required H2 heading; may be repeated")
    parser.add_argument("--summary-section", default="Summary", metavar="HEADING",
                        help="H2 heading containing the summary paragraph (default: Summary)")
    parser.add_argument("--min-summary-length", type=int, metavar="N",
                        help="minimum normalized summary length in characters")
    parser.add_argument("--max-summary-length", type=int, metavar="N",
                        help="maximum normalized summary length in characters")
    parser.add_argument("--json", action="store_true", help="emit a JSON result")
    args = parser.parse_args()

    if args.min_summary_length is not None and args.min_summary_length < 0:
        parser.error("--min-summary-length must be zero or greater")
    if args.max_summary_length is not None and args.max_summary_length < 0:
        parser.error("--max-summary-length must be zero or greater")
    if (args.min_summary_length is not None and args.max_summary_length is not None
            and args.min_summary_length > args.max_summary_length):
        parser.error("--min-summary-length cannot exceed --max-summary-length")

    try:
        errors = audit(read_markdown(args.markdown_file), args.required_section,
                       args.summary_section, args.min_summary_length, args.max_summary_length)
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
