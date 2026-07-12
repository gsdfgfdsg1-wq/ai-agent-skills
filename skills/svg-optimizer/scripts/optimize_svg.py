#!/usr/bin/env python3
"""svg-optimizer — remove bloat from SVG files.

Usage:
    python optimize_svg.py PATH [PATH ...] [--output DIR] [--in-place] [--json] [--aggressive]

Removes comments, metadata, editor data, default attributes, whitespace, and
unused namespace declarations to produce a smaller SVG.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__"}
SVG_EXT = {".svg"}

# XML namespaces commonly added by editors but unnecessary for rendering
EDITOR_NS_PATTERNS = [
    re.compile(r'\s+xmlns:inkscape="[^"]*"'),
    re.compile(r'\s+xmlns:sodipodi="[^"]*"'),
    re.compile(r'\s+xmlns:dc="[^"]*"'),
    re.compile(r'\s+xmlns:cc="[^"]*"'),
    re.compile(r'\s+xmlns:rdf="[^"]*"'),
    re.compile(r'\s+xmlns:svg="[^"]*"'),
    re.compile(r'\s+xmlns:serif="[^"]*"'),
    re.compile(r'\s+xmlns:xlink="[^"]*"'),
]

# Editor-specific elements to remove
EDITOR_ELEMENTS = [
    re.compile(r'<sodipodi:namedview[^/]*/>', re.S),
    re.compile(r'<sodipodi:namedview[^>]*>.*?</sodipodi:namedview>', re.S),
    re.compile(r'<metadata[^>]*>.*?</metadata>', re.S),
    re.compile(r'<rdf:RDF[^>]*>.*?</rdf:RDF>', re.S),
]

# Default attribute values that can be safely removed
DEFAULT_ATTRS = [
    ('fill="none"', ''),
    ('stroke="none"', ''),
    ('fill-opacity="1"', ''),
    ('stroke-opacity="1"', ''),
    ('opacity="1"', ''),
    ('display="inline"', ''),
    ('visibility="visible"', ''),
    ('overflow="visible"', ''),
    ('fill-rule="nonzero"', ''),
    ('clip-rule="nonzero"', ''),
]


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    if os.path.splitext(fn)[1].lower() in SVG_EXT:
                        yield os.path.join(root, fn)


def optimize_svg(content, aggressive=False):
    """Optimize SVG content string, returning (optimized_content, stats)."""
    original_size = len(content.encode("utf-8"))
    svg = content

    # 1. Remove XML comments
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)

    # 2. Remove editor metadata elements
    for pat in EDITOR_ELEMENTS:
        svg = pat.sub('', svg)

    # 3. Remove editor namespace declarations
    for pat in EDITOR_NS_PATTERNS:
        svg = pat.sub('', svg)

    # 4. Remove inkscape/sodipodi/serif prefixed attributes
    svg = re.sub(r'\s+(inkscape|sodipodi|serif):[a-zA-Z-]+="[^"]*"', '', svg)

    # 5. Remove default attribute values
    for attr, _ in DEFAULT_ATTRS:
        svg = svg.replace(' ' + attr, '')

    # 6. Remove XML declaration (not needed for SVG in HTML)
    svg = re.sub(r'<\?xml[^?]*\?>\s*', '', svg)

    # 7. Remove DOCTYPE
    svg = re.sub(r'<!DOCTYPE[^>]*>\s*', '', svg)

    # 8. Collapse whitespace
    svg = re.sub(r'\n\s*\n', '\n', svg)
    svg = re.sub(r'[ \t]+', ' ', svg)
    svg = re.sub(r'>\s+<', '><', svg)

    if aggressive:
        # 9. Remove empty groups
        svg = re.sub(r'<g[^>]*>\s*</g>', '', svg)
        # 10. Remove title/desc elements (accessibility, but not always needed)
        svg = re.compile(r'<title[^>]*>.*?</title>', re.S).sub('', svg)
        svg = re.compile(r'<desc[^>]*>.*?</desc>', re.S).sub('', svg)
        # 11. Collapse consecutive whitespace in attributes
        svg = re.sub(r'="\s+', '="', svg)
        svg = re.sub(r'\s+"', '"', svg)
        # 12. Strip leading/trailing whitespace
        svg = svg.strip()

    optimized_size = len(svg.encode("utf-8"))
    savings = original_size - optimized_size
    pct = (savings / original_size * 100) if original_size > 0 else 0

    stats = {
        "original_size": original_size,
        "optimized_size": optimized_size,
        "savings_bytes": savings,
        "savings_pct": round(pct, 1),
    }

    return svg, stats


def main():
    ap = argparse.ArgumentParser(
        description="Remove bloat from SVG files."
    )
    ap.add_argument("paths", nargs="+", help="SVG files or directories to optimize")
    ap.add_argument("--output", "-o", default=None,
                    help="output directory for optimized files")
    ap.add_argument("--in-place", action="store_true",
                    help="overwrite input files with optimized version")
    ap.add_argument("--json", action="store_true", help="output JSON results")
    ap.add_argument("--aggressive", action="store_true",
                    help="apply more aggressive optimizations (remove titles, empty groups)")
    args = ap.parse_args()

    results = []
    for fp in _iter_targets(args.paths):
        try:
            content = Path(fp).read_text(encoding="utf-8")
        except Exception as e:
            results.append({"file": fp, "error": str(e)})
            continue

        optimized, stats = optimize_svg(content, aggressive=args.aggressive)
        stats["file"] = fp
        results.append(stats)

        if args.in_place:
            Path(fp).write_text(optimized, encoding="utf-8")
        elif args.output:
            out_dir = args.output
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, os.path.basename(fp))
            Path(out_path).write_text(optimized, encoding="utf-8")
            stats["output"] = out_path

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            if "error" in r:
                print(f"[ERROR] {r['file']}: {r['error']}")
            else:
                savings = r["savings_bytes"]
                pct = r["savings_pct"]
                status = "unchanged" if savings == 0 else f"saved {savings} bytes ({pct}%)"
                print(f"{r['file']}: {r['original_size']} -> {r['optimized_size']} ({status})")


if __name__ == "__main__":
    main()
