#!/usr/bin/env python3
"""Lint and validate TOML configuration files."""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


def parse_toml_stdlib(filepath):
    """Try to parse TOML using Python 3.11+ tomllib or tomli."""
    if tomllib is None:
        return None, "No TOML parser available (needs Python 3.11+ or tomli package)"
    try:
        with open(filepath, "rb") as f:
            data = tomllib.load(f)
        return data, None
    except Exception as e:
        return None, str(e)


def lint_basic(filepath):
    """Basic linting that doesn't require a TOML parser."""
    try:
        text = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except (OSError, IOError) as e:
        return [{"severity": "error", "rule": "cannot-read", "message": str(e)}]

    issues = []
    lines = text.splitlines()
    seen_keys = {}  # (section, key) -> line number
    current_section = ""

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip empty and comment lines
        if not stripped or stripped.startswith("#"):
            continue

        # Track sections
        m = re.match(r"^\[([^\[\]]+)\]\s*$", stripped)
        if m:
            current_section = m.group(1).strip()
            # Check for extra whitespace in section name
            if m.group(1) != m.group(1).strip():
                issues.append({
                    "severity": "warning",
                    "rule": "section-whitespace",
                    "line": i,
                    "message": f"section name has extra whitespace: [{m.group(1)}]",
                })
            continue

        # Check for dotted section headers
        m = re.match(r"^\[\[([^\[\]]+)\]\]\s*$", stripped)
        if m:
            current_section = m.group(1).strip()
            continue

        # Check key = value lines
        m = re.match(r"^([\w.-]+)\s*=\s*", stripped)
        if m:
            key = m.group(1)
            full_key = (current_section, key)

            # Check for duplicate keys
            if full_key in seen_keys:
                issues.append({
                    "severity": "error",
                    "rule": "duplicate-key",
                    "line": i,
                    "message": f"duplicate key '{key}' in [{current_section}] (first defined at line {seen_keys[full_key]})",
                })
            seen_keys[full_key] = i

            # Check for values with mixed quotes
            value_part = stripped[m.end():]
            if value_part.count('"') % 2 != 0 and value_part.count("'") % 2 != 0:
                # Could be mismatched quotes
                pass

            # Check for trailing whitespace
            if line != line.rstrip():
                issues.append({
                    "severity": "info",
                    "rule": "trailing-whitespace",
                    "line": i,
                    "message": f"line {i} has trailing whitespace",
                })

        # Check for tabs (TOML uses spaces)
        if "\t" in line:
            issues.append({
                "severity": "warning",
                "rule": "tab-character",
                "line": i,
                "message": f"line {i} contains tab character — TOML uses spaces for indentation",
            })

    return issues


def lint_pyproject(data):
    """Additional checks for pyproject.toml format."""
    issues = []
    if "project" not in data:
        issues.append({
            "severity": "warning",
            "rule": "missing-project-section",
            "message": "pyproject.toml missing [project] section",
        })
    else:
        proj = data["project"]
        if "name" not in proj:
            issues.append({
                "severity": "error",
                "rule": "missing-project-name",
                "message": "[project] missing required 'name' field",
            })
        if "version" not in proj:
            issues.append({
                "severity": "warning",
                "rule": "missing-project-version",
                "message": "[project] missing 'version' field",
            })
    if "build-system" not in data:
        issues.append({
            "severity": "info",
            "rule": "missing-build-system",
            "message": "pyproject.toml missing [build-system] section",
        })
    return issues


def cmd_lint(args):
    issues = lint_basic(args.file)

    # Try full TOML parse for syntax validation
    data, parse_error = parse_toml_stdlib(args.file)
    if parse_error:
        issues.append({
            "severity": "error",
            "rule": "parse-error",
            "message": f"TOML parse error: {parse_error}",
        })

    # Format-specific checks
    if data and args.type == "pyproject":
        issues.extend(lint_pyproject(data))

    issues.sort(key=lambda x: x.get("line", 0))

    if args.json:
        print(json.dumps({"file": str(args.file), "issues": issues}, indent=2, ensure_ascii=False))
    else:
        if not issues:
            print(f"✓ No issues found in {args.file}")
        else:
            print(f"Issues in {args.file}:")
            for issue in issues:
                sym = {"error": "✗", "warning": "⚠", "info": "ℹ"}[issue["severity"]]
                ln = f" L{issue['line']}" if "line" in issue else ""
                print(f"  {sym}{ln} [{issue['severity']}] {issue['rule']}: {issue['message']}")
            print(f"\nTotal: {len(issues)} issue(s)")

    if any(i["severity"] == "error" for i in issues):
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Lint and validate TOML files.")
    sub = parser.add_subparsers(dest="command")

    p_lint = sub.add_parser("lint", help="Lint a TOML file")
    p_lint.add_argument("--file", required=True, help="TOML file to lint")
    p_lint.add_argument("--type", choices=["pyproject", "cargo", "generic"], default="generic", help="Config type")
    p_lint.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "lint":
        cmd_lint(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
