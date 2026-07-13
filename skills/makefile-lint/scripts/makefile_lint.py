#!/usr/bin/env python3
"""Lint Makefiles for common issues and best practices."""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_makefile(filepath):
    """Read a Makefile and return lines."""
    try:
        text = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except (OSError, IOError) as e:
        print(f"Error: cannot read {filepath}: {e}", file=sys.stderr)
        sys.exit(1)
    return text.splitlines()


def check_phony(lines):
    """Check if targets that should be .PHONY are declared."""
    issues = []
    phony_targets = set()
    all_targets = set()

    for line in lines:
        stripped = line.strip()
        # Collect .PHONY declarations
        m = re.match(r"\.PHONY\s*:\s*(.*)", stripped)
        if m:
            for t in m.group(1).split():
                phony_targets.add(t)
        # Collect rule targets
        m = re.match(r"^([a-zA-Z_][\w.-]*)\s*:", stripped)
        if m:
            all_targets.add(m.group(1))

    # Common phony targets
    likely_phony = {"all", "clean", "install", "uninstall", "test", "check",
                    "dist", "distclean", "help", "build", "run", "start",
                    "stop", "restart", "lint", "format", "fmt"}
    for t in all_targets:
        if t in likely_phony and t not in phony_targets:
            issues.append({
                "severity": "warning",
                "rule": "missing-phony",
                "message": f"target '{t}' should be declared .PHONY",
            })

    return issues


def check_space_indent(lines):
    """Check for space indentation instead of tabs in recipe lines."""
    issues = []
    in_recipe = False
    target_line = 0
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if re.match(r"^[\w.%-]+\s*:", stripped) and not stripped.startswith("#"):
            in_recipe = True
            target_line = i
        elif in_recipe:
            if line and not line[0].isspace() and stripped and not stripped.startswith("#"):
                in_recipe = bool(re.match(r"^[\w.%-]+\s*:", stripped))
            elif line.startswith("    ") and stripped and not stripped.startswith("#"):
                # 4 spaces instead of tab
                issues.append({
                    "severity": "error",
                    "rule": "space-indent",
                    "line": i,
                    "message": f"recipe line {i} uses spaces instead of tab",
                })
            elif line.startswith("\t") and stripped:
                pass  # Correct tab indentation
    return issues


def check_recursive_make(lines):
    """Check for recursive make calls not using $(MAKE)."""
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if re.search(r"\bmake\b", stripped) and not re.search(r"\$\(MAKE\)", stripped):
            # Skip comments and variable definitions with 'make' in string
            if stripped.startswith("#") or "=" in stripped and "make" in stripped.split("=", 1)[1]:
                continue
            if re.match(r"^\t", line):  # In recipe
                issues.append({
                    "severity": "warning",
                    "rule": "recursive-make",
                    "line": i,
                    "message": f"line {i}: use $(MAKE) instead of 'make' for recursive calls",
                })
    return issues


def check_missing_default(lines):
    """Check if the first target is 'all' or a sensible default."""
    issues = []
    first_target = None
    for line in lines:
        stripped = line.strip()
        m = re.match(r"^([a-zA-Z_][\w.-]*)\s*:", stripped)
        if m and not stripped.startswith("."):
            first_target = m.group(1)
            break
    if first_target and first_target != "all":
        issues.append({
            "severity": "info",
            "rule": "non-default-first-target",
            "message": f"first target is '{first_target}' — convention is 'all'",
        })
    return issues


def check_empty_recipe(lines):
    """Check for targets with no recipe."""
    issues = []
    prev_target = None
    prev_target_line = 0
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        m = re.match(r"^([a-zA-Z_][\w.-]*)\s*:", stripped)
        if m and not stripped.startswith("."):
            if prev_target and prev_target_line == i - 1:
                # Two consecutive target lines means first has no recipe
                pass
            prev_target = m.group(1)
            prev_target_line = i
    return issues


def check_double_colon(lines):
    """Check for double-colon rules (rarely needed, often a mistake)."""
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if re.match(r"^[\w.%-]+\s*::", stripped):
            issues.append({
                "severity": "warning",
                "rule": "double-colon",
                "line": i,
                "message": f"line {i}: double-colon rule — ensure this is intentional",
            })
    return issues


ALL_CHECKS = [
    check_phony,
    check_space_indent,
    check_recursive_make,
    check_missing_default,
    check_empty_recipe,
    check_double_colon,
]


def cmd_lint(args):
    lines = parse_makefile(args.file)
    all_issues = []
    for check in ALL_CHECKS:
        all_issues.extend(check(lines))

    all_issues.sort(key=lambda x: x.get("line", 0))

    if args.json:
        print(json.dumps({"file": str(args.file), "issues": all_issues}, indent=2, ensure_ascii=False))
    else:
        if not all_issues:
            print(f"✓ No issues found in {args.file}")
        else:
            print(f"Issues in {args.file}:")
            for issue in all_issues:
                sym = {"error": "✗", "warning": "⚠", "info": "ℹ"}[issue["severity"]]
                ln = f" L{issue['line']}" if "line" in issue else ""
                print(f"  {sym}{ln} [{issue['severity']}] {issue['rule']}: {issue['message']}")
            print(f"\nTotal: {len(all_issues)} issue(s)")

    if any(i["severity"] == "error" for i in all_issues):
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Lint Makefiles for common issues.")
    sub = parser.add_subparsers(dest="command")

    p_lint = sub.add_parser("lint", help="Lint a Makefile")
    p_lint.add_argument("--file", required=True, help="Makefile to lint")
    p_lint.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "lint":
        cmd_lint(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
