#!/usr/bin/env python3
"""Lint XML files for common issues without external dependencies."""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET


def check_encoding_declaration(content):
    """Check if encoding declaration is present and valid."""
    issues = []
    m = re.match(r'<\?xml\s+([^?]*)\?>', content)
    if not m:
        # No XML declaration at all - not required but worth noting
        return issues

    decl = m.group(1)
    enc_m = re.search(r'encoding\s*=\s*["\']([^"\']+)["\']', decl)
    if enc_m:
        enc = enc_m.group(1).lower()
        valid = ["utf-8", "utf-16", "iso-8859-1", "ascii", "us-ascii", "windows-1252"]
        if enc not in valid and not enc.startswith("iso-"):
            issues.append({
                "rule": "encoding-value",
                "severity": "warning",
                "message": f"Uncommon encoding '{enc}' — consider UTF-8",
            })
    else:
        issues.append({
            "rule": "missing-encoding",
            "severity": "info",
            "message": "No encoding declaration in XML header — UTF-8 is assumed",
        })
    return issues


def check_trailing_whitespace(content):
    """Check for trailing whitespace in lines."""
    issues = []
    for i, line in enumerate(content.splitlines(), 1):
        if line != line.rstrip():
            issues.append({
                "rule": "trailing-whitespace",
                "severity": "warning",
                "line": i,
                "message": f"Trailing whitespace on line {i}",
            })
    return issues


def check_tabs(content):
    """Check for tab characters in content."""
    issues = []
    for i, line in enumerate(content.splitlines(), 1):
        if "\t" in line:
            issues.append({
                "rule": "tab-character",
                "severity": "warning",
                "line": i,
                "message": f"Tab character on line {i} — use spaces for indentation",
            })
    return issues


def check_long_lines(content, max_len=200):
    """Check for excessively long lines."""
    issues = []
    for i, line in enumerate(content.splitlines(), 1):
        if len(line) > max_len:
            issues.append({
                "rule": "long-line",
                "severity": "info",
                "line": i,
                "message": f"Line {i} is {len(line)} chars (max {max_len})",
            })
    return issues


def check_duplicate_attributes(content):
    """Check for duplicate attributes in the same element."""
    issues = []
    # Find all opening tags
    for m in re.finditer(r'<([a-zA-Z_][\w:.-]*)((?:\s+[^>]*?)?)\s*/?>', content):
        tag = m.group(1)
        attrs_str = m.group(2)
        attrs = re.findall(r'([a-zA-Z_][\w:.-]*)\s*=\s*["\']', attrs_str)
        seen = set()
        for attr in attrs:
            if attr in seen:
                issues.append({
                    "rule": "duplicate-attribute",
                    "severity": "error",
                    "message": f"Duplicate attribute '{attr}' in <{tag}>",
                })
            seen.add(attr)
    return issues


def check_unclosed_cdata(content):
    """Check for unclosed CDATA sections."""
    issues = []
    count_open = content.count("<![CDATA[")
    count_close = content.count("]]>")
    if count_open != count_close:
        issues.append({
            "rule": "unclosed-cdata",
            "severity": "error",
            "message": f"Unmatched CDATA: {count_open} opening, {count_close} closing",
        })
    return issues


def check_unclosed_comments(content):
    """Check for unclosed comments."""
    issues = []
    count_open = content.count("<!--")
    count_close = content.count("-->")
    if count_open != count_close:
        issues.append({
            "rule": "unclosed-comment",
            "severity": "error",
            "message": f"Unmatched comments: {count_open} opening, {count_close} closing",
        })
    return issues


def check_blank_lines(content):
    """Check for multiple consecutive blank lines."""
    issues = []
    blank_count = 0
    for i, line in enumerate(content.splitlines(), 1):
        if not line.strip():
            blank_count += 1
            if blank_count >= 3:
                issues.append({
                    "rule": "multiple-blank-lines",
                    "severity": "info",
                    "line": i,
                    "message": f"3+ consecutive blank lines at line {i}",
                })
        else:
            blank_count = 0
    return issues


def check_well_formedness(filepath):
    """Check XML well-formedness using ElementTree."""
    issues = []
    try:
        tree = ET.parse(filepath)
        tree.getroot()
    except ET.ParseError as e:
        issues.append({
            "rule": "well-formedness",
            "severity": "error",
            "message": str(e),
        })
    except OSError as e:
        issues.append({
            "rule": "file-read",
            "severity": "error",
            "message": str(e),
        })
    return issues


def cmd_lint(args):
    try:
        with open(args.file, encoding="utf-8", errors="replace") as f:
            content = f.read()
    except OSError as e:
        print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    issues = []
    issues.extend(check_encoding_declaration(content))
    issues.extend(check_trailing_whitespace(content))
    issues.extend(check_tabs(content))
    issues.extend(check_long_lines(content))
    issues.extend(check_duplicate_attributes(content))
    issues.extend(check_unclosed_cdata(content))
    issues.extend(check_unclosed_comments(content))
    issues.extend(check_blank_lines(content))
    issues.extend(check_well_formedness(args.file))

    if args.json:
        print(json.dumps({"file": args.file, "issues": issues, "total": len(issues)}, indent=2))
    else:
        if not issues:
            print(f"OK: {args.file} — no issues found.")
        else:
            errors = sum(1 for i in issues if i.get("severity") == "error")
            warnings = sum(1 for i in issues if i.get("severity") == "warning")
            infos = len(issues) - errors - warnings
            print(f"{args.file}: {len(issues)} issue(s) ({errors} errors, {warnings} warnings, {infos} info)")
            for issue in issues:
                line_info = f" line {issue['line']}" if "line" in issue else ""
                print(f"  [{issue['severity'].upper()}] {issue['rule']}{line_info}: {issue['message']}")

    if any(i.get("severity") == "error" for i in issues):
        sys.exit(1)


def cmd_check_well_formed(args):
    issues = check_well_formedness(args.file)

    if args.json:
        print(json.dumps({"file": args.file, "issues": issues, "well_formed": len(issues) == 0}, indent=2))
    else:
        if not issues:
            print(f"OK: {args.file} is well-formed XML.")
        else:
            for issue in issues:
                print(f"  [{issue['severity'].upper()}] {issue['message']}")

    if any(i.get("severity") == "error" for i in issues):
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Lint XML files for common issues.")
    sub = parser.add_subparsers(dest="command")

    p_lint = sub.add_parser("lint", help="Lint XML file for all issues")
    p_lint.add_argument("--file", required=True, help="XML file to lint")
    p_lint.add_argument("--json", action="store_true", help="JSON output")

    p_wf = sub.add_parser("check-well-formed", help="Check XML well-formedness")
    p_wf.add_argument("--file", required=True, help="XML file to check")
    p_wf.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "lint":
        cmd_lint(args)
    elif args.command == "check-well-formed":
        cmd_check_well_formed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
