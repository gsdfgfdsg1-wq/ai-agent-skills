#!/usr/bin/env python3
"""Lint nginx configuration files for common issues and best practices."""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_nginx_conf(filepath):
    """Parse nginx config into a list of (line_no, line_text) tuples."""
    try:
        text = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except (OSError, IOError) as e:
        print(f"Error: cannot read {filepath}: {e}", file=sys.stderr)
        sys.exit(1)
    lines = []
    for i, line in enumerate(text.splitlines(), 1):
        lines.append((i, line))
    return lines


def check_missing_server_name(lines):
    """Check if server block is missing server_name."""
    issues = []
    in_server = 0
    has_server_name = False
    server_start = 0
    for i, line in lines:
        stripped = line.strip()
        if re.match(r"server\s*\{", stripped):
            in_server = 1
            has_server_name = False
            server_start = i
        elif in_server > 0:
            if stripped.startswith("server_name"):
                has_server_name = True
            if stripped == "}":
                in_server -= 1
                if in_server == 0 and not has_server_name:
                    issues.append({
                        "line": server_start,
                        "severity": "warning",
                        "rule": "missing-server-name",
                        "message": "server block missing server_name directive",
                    })
    return issues


def check_autoindex(lines):
    """Check if autoindex is enabled."""
    issues = []
    for i, line in lines:
        stripped = line.strip()
        if re.match(r"autoindex\s+on\s*;", stripped):
            issues.append({
                "line": i,
                "severity": "warning",
                "rule": "autoindex-on",
                "message": "autoindex is enabled — may expose directory listings",
            })
    return issues


def check_hardcoded_secrets(lines):
    """Check for hardcoded passwords, API keys, tokens."""
    issues = []
    patterns = [
        (r"(?:password|passwd|secret|api_key|token)\s+\S+;", "hardcoded-secret"),
    ]
    for i, line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for pattern, rule in patterns:
            if re.search(pattern, stripped, re.IGNORECASE):
                issues.append({
                    "line": i,
                    "severity": "error",
                    "rule": rule,
                    "message": f"possible hardcoded secret found: {stripped[:60]}",
                })
    return issues


def check_ssl_on_443(lines):
    """Check if port 443 block has SSL directives."""
    issues = []
    in_server = 0
    has_ssl = False
    has_443 = False
    server_start = 0
    for i, line in lines:
        stripped = line.strip()
        if re.match(r"server\s*\{", stripped):
            in_server = 1
            has_ssl = False
            has_443 = bool(re.search(r":?443\b", stripped))
            server_start = i
        elif in_server > 0:
            if re.match(r"listen\s+.*443", stripped):
                has_443 = True
            if stripped.startswith("ssl_certificate"):
                has_ssl = True
            if stripped == "}":
                in_server -= 1
                if in_server == 0 and has_443 and not has_ssl:
                    issues.append({
                        "line": server_start,
                        "severity": "error",
                        "rule": "missing-ssl-cert",
                        "message": "server block on port 443 missing ssl_certificate",
                    })
    return issues


def check_missing_access_log(lines):
    """Check if server block is missing access_log."""
    issues = []
    in_server = 0
    has_access_log = False
    server_start = 0
    for i, line in lines:
        stripped = line.strip()
        if re.match(r"server\s*\{", stripped):
            in_server = 1
            has_access_log = False
            server_start = i
        elif in_server > 0:
            if stripped.startswith("access_log"):
                has_access_log = True
            if stripped == "}":
                in_server -= 1
                if in_server == 0 and not has_access_log:
                    issues.append({
                        "line": server_start,
                        "severity": "info",
                        "rule": "missing-access-log",
                        "message": "server block missing access_log directive",
                    })
    return issues


def check_root_in_location(lines):
    """Check if root is inside a location block (usually wrong)."""
    issues = []
    in_location = 0
    for i, line in lines:
        stripped = line.strip()
        if re.match(r"location\s+.*\{", stripped):
            in_location += 1
        elif in_location > 0:
            if stripped.startswith("root"):
                issues.append({
                    "line": i,
                    "severity": "warning",
                    "rule": "root-in-location",
                    "message": "root directive inside location block — consider moving to server block",
                })
            if stripped == "}":
                in_location -= 1
    return issues


def check_duplicate_directives(lines):
    """Check for duplicate directives in the same block scope."""
    issues = []
    scope_stack = [set()]
    for i, line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.endswith("{"):
            scope_stack.append(set())
        elif stripped == "}":
            if len(scope_stack) > 1:
                scope_stack.pop()
        else:
            m = re.match(r"(\w+)\s+", stripped)
            if m:
                directive = m.group(1)
                # Allow duplicate for some directives
                if directive in ("location", "server", "if", "map", "upstream", "types"):
                    return issues
                if directive in scope_stack[-1]:
                    issues.append({
                        "line": i,
                        "severity": "warning",
                        "rule": "duplicate-directive",
                        "message": f"duplicate directive '{directive}' in same block",
                    })
                scope_stack[-1].add(directive)
    return issues


ALL_CHECKS = [
    check_missing_server_name,
    check_autoindex,
    check_hardcoded_secrets,
    check_ssl_on_443,
    check_missing_access_log,
    check_root_in_location,
    check_duplicate_directives,
]


def cmd_lint(args):
    lines = parse_nginx_conf(args.file)
    all_issues = []
    for check in ALL_CHECKS:
        all_issues.extend(check(lines))

    if args.severity:
        all_issues = [i for i in all_issues if i["severity"] == args.severity]

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
                print(f"  {sym} L{issue['line']}: [{issue['severity']}] {issue['rule']}: {issue['message']}")
            print(f"\nTotal: {len(all_issues)} issue(s)")

    if any(i["severity"] == "error" for i in all_issues):
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Lint nginx configuration files.")
    sub = parser.add_subparsers(dest="command")

    p_lint = sub.add_parser("lint", help="Lint an nginx config file")
    p_lint.add_argument("--file", required=True, help="Nginx config file to lint")
    p_lint.add_argument("--json", action="store_true", help="JSON output")
    p_lint.add_argument("--severity", choices=["info", "warning", "error"], help="Filter by severity")

    args = parser.parse_args()
    if args.command == "lint":
        cmd_lint(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
