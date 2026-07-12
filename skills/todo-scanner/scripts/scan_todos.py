#!/usr/bin/env python3
"""todo-scanner — scan a codebase for TODO / FIXME / HACK / XXX comments.

Usage:
    python scan_todos.py PATH [PATH ...] [--tags TAG1,TAG2] [--json] [--summary] [--exit-code]

Outputs a structured report of code annotations grouped by tag and file.
"""

import argparse
import json
import os
import re
import sys

DEFAULT_TAGS = ("TODO", "FIXME", "HACK", "XXX", "BUG", "NOTE")

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "__pycache__",
             ".venv", "venv", "target", "bin", "obj", ".tox", ".mypy_cache",
             ".pytest_cache", ".hg", ".svn"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf",
            ".eot", ".pdf", ".zip", ".gz", ".tar", ".lock", ".exe", ".dll",
            ".so", ".dylib", ".mp3", ".mp4", ".wav", ".avi", ".pyc"}
MAX_FILE = 2_000_000


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    if os.path.splitext(fn)[1].lower() in SKIP_EXT:
                        continue
                    yield os.path.join(root, fn)


def _scan_file(path, tags):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return []
    if os.path.getsize(path) > MAX_FILE:
        return []

    pattern = re.compile(
        r"(?i)\b(" + "|".join(re.escape(t) for t in tags) + r")\b[:\s]*(.*)"
    )
    findings = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"):
            comment_text = stripped
        else:
            comment_text = stripped
        m = pattern.search(comment_text)
        if m:
            tag = m.group(1).upper()
            text = m.group(2).strip()
            if len(text) > 120:
                text = text[:117] + "..."
            findings.append({
                "tag": tag,
                "line": i,
                "text": text,
                "file": path,
            })
    return findings


def main():
    ap = argparse.ArgumentParser(
        description="Scan a codebase for TODO / FIXME / HACK / XXX comments."
    )
    ap.add_argument("paths", nargs="+", help="files or directories to scan")
    ap.add_argument("--tags", default=",".join(DEFAULT_TAGS),
                    help="comma-separated tags to look for (default: %(default)s)")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--summary", action="store_true",
                    help="show summary counts only")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit non-zero when any TODO items are found")
    args = ap.parse_args()

    tags = [t.strip().upper() for t in args.tags.split(",") if t.strip()]
    all_findings = []
    for fp in _iter_targets(args.paths):
        all_findings.extend(_scan_file(fp, tags))

    # Sort by tag priority then file
    tag_rank = {t: i for i, t in enumerate(DEFAULT_TAGS)}
    all_findings.sort(key=lambda f: (tag_rank.get(f["tag"], 99), f["file"], f["line"]))

    if args.json:
        print(json.dumps(all_findings, indent=2, ensure_ascii=False))
    elif args.summary:
        counts = {}
        for f in all_findings:
            counts[f["tag"]] = counts.get(f["tag"], 0) + 1
        if not counts:
            print("No TODO items found.")
        else:
            print("TODO item summary:")
            for tag in sorted(counts, key=lambda t: tag_rank.get(t, 99)):
                print(f"  {tag}: {counts[tag]}")
            print(f"  Total: {len(all_findings)}")
    elif not all_findings:
        print("No TODO items found.")
    else:
        print(f"Found {len(all_findings)} TODO item(s):\n")
        current_file = None
        for f in all_findings:
            if f["file"] != current_file:
                current_file = f["file"]
                print(f"  {current_file}")
            print(f"    L{f['line']} [{f['tag']}] {f['text']}")

    if args.exit_code and all_findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
