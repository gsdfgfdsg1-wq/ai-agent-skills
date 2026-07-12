#!/usr/bin/env python3
"""css-unused-finder — find CSS selectors not referenced in HTML files.

Usage:
    python find_unused.py CSS_FILE [CSS_FILE ...] --html HTML_PATH [HTML_PATH ...] [--json] [--exit-code]

Parses CSS selectors and checks them against HTML class/id/tag usage.
"""

import argparse
import json
import os
import re
import sys


def _extract_css_selectors(css_text):
    """Extract selectors from CSS text, returning a list of selector strings."""
    # Remove comments
    css_text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.S)
    # Remove @media and other at-rules content for simplicity
    # Split by } to get rule blocks, then extract selector part (before {)
    selectors = []
    for block in re.split(r"\}", css_text):
        if "{" not in block:
            continue
        selector_part = block.split("{")[0].strip()
        if not selector_part:
            continue
        # Split comma-separated selectors
        for sel in selector_part.split(","):
            sel = sel.strip()
            if sel and not sel.startswith("@"):
                selectors.append(sel)
    return selectors


def _parse_selectors(selectors):
    """Parse selectors into categorized lists of class, id, and tag names."""
    classes = set()
    ids = set()
    tags = set()

    for sel in selectors:
        # Remove pseudo-elements and pseudo-classes for matching
        clean = re.sub(r"::?[a-zA-Z-]+(\([^)]*\))?", "", sel)
        # Extract classes
        for m in re.finditer(r"\.([a-zA-Z_][\w-]*)", clean):
            classes.add(m.group(1))
        # Extract IDs
        for m in re.finditer(r"#([a-zA-Z_][\w-]*)", clean):
            ids.add(m.group(1))
        # Extract tag names (word at start or after combinator, not preceded by . or #)
        for m in re.finditer(r"(?:^|[\s>+~])([a-zA-Z][\w-]*)", clean):
            tag = m.group(1)
            if tag not in ("none", "auto", "inherit", "initial", "unset", "normal"):
                tags.add(tag.lower())

    return classes, ids, tags


def _extract_html_usage(html_text):
    """Extract classes, IDs, and tags used in HTML."""
    classes = set()
    ids = set()
    tags = set()

    # Classes
    for m in re.finditer(r'class\s*=\s*["\']([^"\']*)["\']', html_text, re.I):
        for cls in m.group(1).split():
            classes.add(cls)

    # IDs
    for m in re.finditer(r'id\s*=\s*["\']([^"\']*)["\']', html_text, re.I):
        ids.add(m.group(1))

    # Tags
    for m in re.finditer(r"<([a-zA-Z][\w-]*)", html_text):
        tags.add(m.group(1).lower())

    return classes, ids, tags


def _iter_files(paths, ext):
    """Yield file paths matching extension from given paths."""
    for p in paths:
        if os.path.isfile(p):
            yield p
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
                for fn in files:
                    if fn.lower().endswith(ext):
                        yield os.path.join(root, fn)


def main():
    ap = argparse.ArgumentParser(
        description="Find CSS selectors not referenced in HTML files."
    )
    ap.add_argument("css", nargs="+", help="CSS file(s) to analyze")
    ap.add_argument("--html", nargs="+", required=True,
                    help="HTML file(s) or directory(ies) to check against")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit 1 if unused selectors found")
    args = ap.parse_args()

    # Parse CSS
    all_selectors = []
    for css_file in args.css:
        if not os.path.isfile(css_file):
            print(f"Warning: CSS file not found: {css_file}", file=sys.stderr)
            continue
        with open(css_file, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        all_selectors.extend(_extract_css_selectors(text))

    css_classes, css_ids, css_tags = _parse_selectors(all_selectors)

    # Parse HTML
    html_classes = set()
    html_ids = set()
    html_tags = set()
    for html_file in _iter_files(args.html, ".html"):
        with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        hc, hi, ht = _extract_html_usage(text)
        html_classes |= hc
        html_ids |= hi
        html_tags |= ht

    # Also add htm files
    for html_file in _iter_files(args.html, ".htm"):
        with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        hc, hi, ht = _extract_html_usage(text)
        html_classes |= hc
        html_ids |= hi
        html_tags |= ht

    # Find unused
    unused_classes = sorted(css_classes - html_classes)
    unused_ids = sorted(css_ids - html_ids)
    unused_tags = sorted(css_tags - html_tags)

    total_unused = len(unused_classes) + len(unused_ids) + len(unused_tags)

    if args.json:
        result = {
            "total_selectors": len(all_selectors),
            "unused": {
                "classes": unused_classes,
                "ids": unused_ids,
                "tags": unused_tags,
            },
            "total_unused": total_unused,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"CSS Unused Selector Report\n")
        print(f"  Total selectors parsed: {len(all_selectors)}")
        print(f"  Unused items: {total_unused}\n")

        if unused_classes:
            print(f"  Unused classes ({len(unused_classes)}):")
            for c in unused_classes[:20]:
                print(f"    .{c}")
            if len(unused_classes) > 20:
                print(f"    ... and {len(unused_classes) - 20} more")

        if unused_ids:
            print(f"\n  Unused IDs ({len(unused_ids)}):")
            for i in unused_ids[:20]:
                print(f"    #{i}")

        if unused_tags:
            print(f"\n  Unused tags ({len(unused_tags)}):")
            for t in unused_tags[:20]:
                print(f"    {t}")

        if not total_unused:
            print("  All CSS selectors are referenced in HTML.")

    if args.exit_code and total_unused > 0:
        print(f"\nCI FAILED: {total_unused} unused CSS selectors found.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
