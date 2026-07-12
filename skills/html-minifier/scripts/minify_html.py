#!/usr/bin/env python3
"""html-minifier — minify HTML by removing comments, whitespace, and optional tags.

Usage:
    python minify_html.py FILE [-o OUTPUT] [--stats] [--keep-conditional-comments]

Reads an HTML file and outputs a minified version.
"""

import argparse
import os
import re
import sys

# Optional closing tags per HTML5 spec
OPTIONAL_CLOSE = {"p", "li", "dt", "dd", "tr", "td", "th", "thead", "tbody", "tfoot",
                  "colgroup", "option", "optgroup", "rt", "rp", "summary", "figcaption"}

# Void elements (self-closing)
VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                 "link", "meta", "param", "source", "track", "wbr"}


def _remove_comments(html, keep_conditional=False):
    """Remove HTML comments."""
    if keep_conditional:
        # Keep <!--[if ...]>...<![endif]-->
        return re.sub(r"<!--(?!\[if).*?-->", "", html, flags=re.S)
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def _collapse_whitespace(html):
    """Collapse whitespace between tags but preserve inside <pre>, <script>, <style>."""
    # Split into protected blocks (pre, script, style) and normal HTML
    parts = []
    last = 0
    for m in re.finditer(r"<(pre|script|style)[^>]*>.*?</\1>", html, re.S | re.I):
        # Process normal HTML before this block
        normal = html[last:m.start()]
        parts.append(re.sub(r"\s+", " ", normal))
        # Keep protected block as-is (except leading/trailing whitespace between tags)
        parts.append(m.group(0))
        last = m.end()
    # Process remaining normal HTML
    normal = html[last:]
    parts.append(re.sub(r"\s+", " ", normal))
    return "".join(parts)


def _strip_optional_close_tags(html):
    """Remove optional closing tags."""
    for tag in OPTIONAL_CLOSE:
        html = re.sub(rf"</{tag}\s*>", "", html, flags=re.I)
    return html


def _remove_empty_attrs(html):
    """Remove empty attribute values like style="" or class=""."""
    html = re.sub(r'\s+(class|style|id|lang|dir)\s*=\s*["\']\s*["\']', "", html, flags=re.I)
    return html


def _remove_attr_quotes(html):
    """Remove quotes from simple attribute values (alphanumeric, dash, underscore, dot)."""
    def _unquote(m):
        attr = m.group(1)
        val = m.group(2)
        if re.match(r"^[a-zA-Z0-9_\-:.]+$", val):
            return f"{attr}={val}"
        return m.group(0)
    return re.sub(r'(\w+)\s*=\s*"([^"]*)"', _unquote, html)


def _trim_between_tags(html):
    """Remove whitespace immediately between tags."""
    html = re.sub(r">\s+<", "><", html)
    return html


def minify_html(html, keep_conditional=False):
    """Apply all minification steps."""
    html = _remove_comments(html, keep_conditional)
    html = _collapse_whitespace(html)
    html = _strip_optional_close_tags(html)
    html = _remove_empty_attrs(html)
    html = _remove_attr_quotes(html)
    html = _trim_between_tags(html)
    html = html.strip()
    return html


def main():
    ap = argparse.ArgumentParser(
        description="Minify HTML by removing comments, whitespace, and optional tags."
    )
    ap.add_argument("file", help="HTML file to minify, or '-' for stdin")
    ap.add_argument("-o", "--output", help="output file (default: stdout)")
    ap.add_argument("--stats", action="store_true", help="show size reduction stats")
    ap.add_argument("--keep-conditional-comments", action="store_true",
                    help="keep IE conditional comments")
    args = ap.parse_args()

    if args.file == "-":
        html = sys.stdin.read()
    else:
        if not os.path.isfile(args.file):
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(2)
        with open(args.file, "r", encoding="utf-8") as f:
            html = f.read()

    original_size = len(html.encode("utf-8"))
    result = minify_html(html, args.keep_conditional_comments)
    result_size = len(result.encode("utf-8"))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        if args.stats:
            saved = original_size - result_size
            pct = (saved / original_size * 100) if original_size > 0 else 0
            print(f"Original: {original_size} bytes")
            print(f"Minified: {result_size} bytes")
            print(f"Saved:    {saved} bytes ({pct:.1f}%)")
    else:
        print(result, end="")
        if args.stats:
            saved = original_size - result_size
            pct = (saved / original_size * 100) if original_size > 0 else 0
            print(f"\n\n--- Stats ---", file=sys.stderr)
            print(f"Original: {original_size} bytes", file=sys.stderr)
            print(f"Minified: {result_size} bytes", file=sys.stderr)
            print(f"Saved:    {saved} bytes ({pct:.1f}%)", file=sys.stderr)


if __name__ == "__main__":
    main()
