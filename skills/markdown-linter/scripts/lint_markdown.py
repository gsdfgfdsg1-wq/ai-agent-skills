#!/usr/bin/env python3
"""markdown-linter — check Markdown files for style issues.

Usage:
    python lint_markdown.py PATH [PATH ...] [--json] [--severity MIN] [--exit-code] [--max-line N]

Detects: heading style, heading levels jumps, trailing whitespace, long lines,
missing newline at EOF, multiple blank lines, and more.
"""

import argparse
import json
import os
import re
import sys

SEV_RANK = {"info": 0, "warning": 1, "error": 2}
SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__", ".tox", ".mypy_cache"}
MD_EXT = {".md", ".markdown", ".mdx"}
MAX_LINE_DEFAULT = 120


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    if os.path.splitext(fn)[1].lower() in MD_EXT:
                        yield os.path.join(root, fn)


def _check_file(path, max_line):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return []

    findings = []
    prev_heading_level = 0
    in_code_block = False
    consecutive_blank = 0

    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # MD001: Trailing whitespace
        if line != line.rstrip():
            findings.append({"rule": "MD001", "severity": "warning",
                             "line": i, "message": "trailing whitespace",
                             "file": path})

        # MD002: Multiple blank lines
        if stripped == "":
            consecutive_blank += 1
            if consecutive_blank > 1:
                findings.append({"rule": "MD002", "severity": "info",
                                 "line": i, "message": "multiple consecutive blank lines",
                                 "file": path})
        else:
            consecutive_blank = 0

        # Skip further checks on blank lines
        if not stripped:
            continue

        # MD003: Line too long
        if len(line) > max_line:
            # Allow long lines in tables
            if not stripped.startswith("|"):
                findings.append({"rule": "MD003", "severity": "info",
                                 "line": i,
                                 "message": f"line exceeds {max_line} characters ({len(line)})",
                                 "file": path})

        # MD004: Heading style — check for inconsistent ATX style
        heading_match = re.match(r'^(#{1,6})\s+(.+)', stripped)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2)

            # MD005: Heading level jump (skip more than one level)
            if prev_heading_level > 0 and level > prev_heading_level + 1:
                findings.append({"rule": "MD005", "severity": "warning",
                                 "line": i,
                                 "message": f"heading level jump from H{prev_heading_level} to H{level}",
                                 "file": path})

            # MD006: Multiple h1 headings
            if level == 1 and prev_heading_level >= 1:
                # Check if there was a previous h1
                findings.append({"rule": "MD006", "severity": "warning",
                                 "line": i,
                                 "message": "multiple H1 headings found",
                                 "file": path})

            prev_heading_level = level

        # MD007: Setext-style headings (underlines) — just note them
        if re.match(r'^[=\-]{3,}\s*$', stripped):
            if i > 1 and lines[i - 2].strip():
                findings.append({"rule": "MD007", "severity": "info",
                                 "line": i - 1,
                                 "message": "setext-style heading (consider ATX # style)",
                                 "file": path})

        # MD008: Missing space after # in heading
        if re.match(r'^#{1,6}[^#\s]', stripped):
            findings.append({"rule": "MD008", "severity": "error",
                             "line": i,
                             "message": "missing space after # in heading",
                             "file": path})

        # MD009: Inline HTML
        if re.search(r'<(?!https?://|mailto:)[a-zA-Z][a-zA-Z0-9]*[\s>/]', stripped):
            findings.append({"rule": "MD009", "severity": "info",
                             "line": i,
                             "message": "inline HTML detected",
                             "file": path})

    # MD010: Missing newline at EOF
    if lines and not lines[-1].endswith("\n"):
        findings.append({"rule": "MD010", "severity": "warning",
                         "line": len(lines),
                         "message": "missing newline at end of file",
                         "file": path})

    # MD011: First line should be a heading
    if lines:
        first = lines[0].strip()
        if first and not first.startswith("#") and not first.startswith("---"):
            findings.append({"rule": "MD011", "severity": "info",
                             "line": 1,
                             "message": "first line is not a heading",
                             "file": path})

    return findings


def main():
    ap = argparse.ArgumentParser(
        description="Check Markdown files for style issues."
    )
    ap.add_argument("paths", nargs="+", help="Markdown files or directories to check")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--severity", default="info", choices=list(SEV_RANK),
                    help="minimum severity to report (default: info)")
    ap.add_argument("--max-line", type=int, default=MAX_LINE_DEFAULT,
                    help=f"maximum line length (default: {MAX_LINE_DEFAULT})")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit non-zero when findings >= --severity")
    args = ap.parse_args()

    all_findings = []
    for fp in _iter_targets(args.paths):
        all_findings.extend(_check_file(fp, args.max_line))

    min_rank = SEV_RANK[args.severity]
    shown = [f for f in all_findings if SEV_RANK[f["severity"]] >= min_rank]

    if args.json:
        print(json.dumps(shown, indent=2, ensure_ascii=False))
    elif not shown:
        print(f"No issues found (>= {args.severity}).")
    else:
        print(f"Found {len(shown)} issue(s):\n")
        for f in sorted(shown, key=lambda x: (x["file"], x["line"])):
            print(f"[{f['severity'].upper()}] {f['rule']} {f['file']}:{f['line']}")
            print(f"  {f['message']}\n")

    if args.exit_code and shown:
        sys.exit(1)


if __name__ == "__main__":
    main()
