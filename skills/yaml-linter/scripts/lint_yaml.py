#!/usr/bin/env python3
"""yaml-linter — check YAML files for common issues without a full parser.

Usage:
    python lint_yaml.py PATH [PATH ...] [--json] [--severity MIN] [--exit-code]

Detects: tabs in indentation, trailing whitespace, inconsistent indent,
duplicate keys, missing document start marker, long lines, and more.
"""

import argparse
import json
import os
import re
import sys

SEV_RANK = {"info": 0, "warning": 1, "error": 2}

SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__", ".tox", ".mypy_cache"}
YAML_EXT = {".yaml", ".yml"}
MAX_LINE = 120


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    if os.path.splitext(fn)[1].lower() in YAML_EXT:
                        yield os.path.join(root, fn)


def _check_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return []

    findings = []
    indent_stack = [0]  # stack of expected indent levels
    seen_keys_at_level = {}  # (indent_level, key) for duplicate detection

    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # Y001: Tab in indentation
        leading = line[:indent]
        if "\t" in leading:
            findings.append({"rule": "Y001", "severity": "error",
                             "line": i, "message": "tab character in indentation (use spaces)",
                             "file": path})

        # Y002: Trailing whitespace
        if raw.rstrip("\n") != raw.rstrip("\n").rstrip():
            findings.append({"rule": "Y002", "severity": "warning",
                             "line": i, "message": "trailing whitespace",
                             "file": path})

        # Y003: Line too long
        if len(stripped) > MAX_LINE:
            findings.append({"rule": "Y003", "severity": "info",
                             "line": i,
                             "message": f"line exceeds {MAX_LINE} characters ({len(stripped)})",
                             "file": path})

        # Skip comments and empty lines for structural checks
        if not stripped or stripped.startswith("#"):
            continue

        # Y004: Inconsistent indentation (not a multiple of 2)
        if indent > 0 and indent % 2 != 0 and "\t" not in leading:
            findings.append({"rule": "Y004", "severity": "warning",
                             "line": i,
                             "message": f"indentation is {indent} spaces (not a multiple of 2)",
                             "file": path})

        # Y005: Duplicate key detection at same indent level
        key_match = re.match(r'^(\s*)([A-Za-z_][A-Za-z0-9_\-]*)\s*:', line)
        if key_match:
            key = key_match.group(2)
            level_key = (indent, key)
            if level_key in seen_keys_at_level:
                findings.append({"rule": "Y005", "severity": "error",
                                 "line": i,
                                 "message": f"duplicate key '{key}' (first at line {seen_keys_at_level[level_key]})",
                                 "file": path})
            else:
                seen_keys_at_level[level_key] = i

        # Y006: Missing space after colon in mapping
        colon_match = re.search(r':[^\s:!]', stripped)
        if colon_match and not stripped.startswith("-"):
            # Exclude URLs and flow-style values
            before = stripped[:colon_match.start()]
            if ":" not in before.split()[-1:] and not re.match(r'^\s*\{', stripped):
                findings.append({"rule": "Y006", "severity": "info",
                                 "line": i,
                                 "message": "missing space after colon in mapping",
                                 "file": path})

    # Y007: Missing document start marker (---) for multi-doc or non-trivial files
    if len(lines) > 5 and not lines[0].strip().startswith("---"):
        findings.append({"rule": "Y007", "severity": "info",
                         "line": 1,
                         "message": "missing document start marker (---)",
                         "file": path})

    return findings


def main():
    ap = argparse.ArgumentParser(
        description="Check YAML files for common issues."
    )
    ap.add_argument("paths", nargs="+", help="YAML files or directories to check")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--severity", default="info", choices=list(SEV_RANK),
                    help="minimum severity to report (default: info)")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit non-zero when findings >= --severity")
    args = ap.parse_args()

    all_findings = []
    for fp in _iter_targets(args.paths):
        all_findings.extend(_check_file(fp))

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
