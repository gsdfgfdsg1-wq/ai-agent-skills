#!/usr/bin/env python3
"""Generate a table of contents from Markdown headings without external dependencies."""

import argparse
import json
import re
import sys


def extract_headings(text):
    """Extract headings from Markdown text. Returns list of (level, text, line_number)."""
    headings = []
    for i, line in enumerate(text.splitlines(), 1):
        # ATX-style headings (# Heading)
        m = re.match(r'^(#{1,6})\s+(.+?)(?:\s+#+)?\s*$', line)
        if m:
            level = len(m.group(1))
            text_val = m.group(2).strip()
            headings.append((level, text_val, i))
            continue
        # Setext-style headings (underlined with === or ---)
        # Checked on next iteration
    # Handle setext style in a second pass
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if i == 0:
            continue
        m = re.match(r'^(\={3,}|\-{3,})\s*$', line)
        if m:
            prev = lines[i - 1].strip()
            if prev and not prev.startswith('#'):
                level = 1 if m.group(1).startswith('=') else 2
                # Check if already captured as ATX
                already = any(h[2] == i and h[0] == level for h in headings)
                if not already:
                    headings.append((level, prev, i))
    headings.sort(key=lambda h: h[2])
    return headings


def heading_to_anchor(text):
    """Convert heading text to a GitHub-compatible anchor slug."""
    slug = text.lower().strip()
    # Remove punctuation except hyphens and spaces
    slug = re.sub(r'[^\w\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug


def cmd_generate(args):
    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    headings = extract_headings(text)
    if args.max_depth:
        headings = [(l, t, n) for l, t, n in headings if l <= args.max_depth]

    if args.json:
        print(json.dumps([{"level": l, "text": t, "line": n, "anchor": heading_to_anchor(t)} for l, t, n in headings], indent=2))
        return

    if not headings:
        print("No headings found.")
        return

    for level, text_val, line_num in headings:
        indent = "  " * (level - 1)
        if args.no_links:
            print(f"{indent}- {text_val}")
        else:
            anchor = heading_to_anchor(text_val)
            print(f"{indent}- [{text_val}](#{anchor})")


def cmd_check(args):
    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    headings = extract_headings(text)
    issues = []
    prev_level = 0
    for level, text_val, line_num in headings:
        if prev_level > 0 and level > prev_level + 1:
            issues.append({
                "line": line_num,
                "heading": text_val,
                "level": level,
                "issue": f"jumped from H{prev_level} to H{level} (should be H{prev_level + 1} or less)",
            })
        prev_level = level

    if args.json:
        print(json.dumps({"headings": len(headings), "issues": issues}, indent=2))
    else:
        if not issues:
            print(f"OK: {len(headings)} headings, no hierarchy issues.")
        else:
            print(f"Found {len(issues)} issue(s):")
            for issue in issues:
                print(f"  Line {issue['line']}: \"{issue['heading']}\" — {issue['issue']}")


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown table of contents.")
    sub = parser.add_subparsers(dest="command")

    p_gen = sub.add_parser("generate", help="Generate TOC from headings")
    p_gen.add_argument("--file", required=True, help="Markdown file")
    p_gen.add_argument("--max-depth", type=int, help="Max heading depth (1-6)")
    p_gen.add_argument("--no-links", action="store_true", help="Plain text without links")
    p_gen.add_argument("--json", action="store_true", help="JSON output")

    p_check = sub.add_parser("check", help="Validate heading hierarchy")
    p_check.add_argument("--file", required=True, help="Markdown file")
    p_check.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "check":
        cmd_check(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
