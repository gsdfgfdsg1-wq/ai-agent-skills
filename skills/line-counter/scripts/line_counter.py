#!/usr/bin/env python3
"""Count lines of code, blank lines, and comment lines by file extension without external dependencies."""

import argparse
import json
import os
import sys


COMMENT_STYLES = {
    ".py": ("#", '"""', '"""'),
    ".rb": ("#", "=begin", "=end"),
    ".sh": ("#", None, None),
    ".bash": ("#", None, None),
    ".zsh": ("#", None, None),
    ".yaml": ("#", None, None),
    ".yml": ("#", None, None),
    ".toml": ("#", None, None),
    ".r": ("#", None, None),
    ".R": ("#", None, None),
    ".pl": ("#", None, None),
    ".sql": ("--", "/*", "*/"),
    ".js": ("//", "/*", "*/"),
    ".ts": ("//", "/*", "*/"),
    ".jsx": ("//", "/*", "*/"),
    ".tsx": ("//", "/*", "*/"),
    ".java": ("//", "/*", "*/"),
    ".c": ("//", "/*", "*/"),
    ".cpp": ("//", "/*", "*/"),
    ".h": ("//", "/*", "*/"),
    ".hpp": ("//", "/*", "*/"),
    ".cs": ("//", "/*", "*/"),
    ".go": ("//", "/*", "*/"),
    ".swift": ("//", "/*", "*/"),
    ".kt": ("//", "/*", "*/"),
    ".rs": ("//", "/*", "*/"),
    ".scala": ("//", "/*", "*/"),
    ".css": (None, "/*", "*/"),
    ".html": (None, "<!--", "-->"),
    ".htm": (None, "<!--", "-->"),
    ".xml": (None, "<!--", "-->"),
    ".lua": ("--", "--[[", "]]"),
    ".vim": ('"', None, None),
    ".el": (";;", None, None),
    ".clj": (";;", None, None),
    ".erl": ("%", None, None),
    ".hs": ("--", "{-", "-}"),
    ".ada": ("--", None, None),
    ".ini": (";", None, None),
    ".cfg": (";", None, None),
    ".conf": ("#", None, None),
    ".md": (None, None, None),
    ".txt": (None, None, None),
}


def count_file_lines(filepath):
    """Count total, code, blank, and comment lines in a single file."""
    ext = os.path.splitext(filepath)[1].lower()
    style = COMMENT_STYLES.get(ext)
    line_comment, block_start, block_end = (None, None, None) if style is None else style

    total = 0
    code = 0
    blank = 0
    comment = 0
    in_block = False

    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            for raw_line in f:
                total += 1
                line = raw_line.strip()

                if not line:
                    blank += 1
                    continue

                if in_block:
                    comment += 1
                    if block_end and block_end in line:
                        in_block = False
                    continue

                if block_start and line.startswith(block_start):
                    comment += 1
                    if block_end and block_end not in line[len(block_start):]:
                        in_block = True
                    continue

                if line_comment and line.startswith(line_comment):
                    comment += 1
                    continue

                code += 1
    except OSError:
        return None

    return {"total": total, "code": code, "blank": blank, "comment": comment}


def walk_directory(path, extensions=None, exclude=None):
    """Walk directory and collect line counts by extension."""
    exclude = exclude or []
    results = {}

    for root, dirs, files in os.walk(path):
        # Filter excluded dirs
        dirs[:] = [d for d in dirs if not any(d == pat or d.startswith(".") for pat in (exclude or [".git", "node_modules", "__pycache__", ".venv", "venv"]))]

        for fn in files:
            fp = os.path.join(root, fn)
            ext = os.path.splitext(fn)[1].lower()
            if not ext:
                continue
            if extensions and ext not in extensions:
                continue

            counts = count_file_lines(fp)
            if counts is None:
                continue

            if ext not in results:
                results[ext] = {"total": 0, "code": 0, "blank": 0, "comment": 0, "files": 0}
            for k in ("total", "code", "blank", "comment"):
                results[ext][k] += counts[k]
            results[ext]["files"] += 1

    return results


def cmd_count(args):
    if os.path.isfile(args.path):
        ext = os.path.splitext(args.path)[1].lower()
        counts = count_file_lines(args.path)
        if counts is None:
            print(f"Error: cannot read {args.path}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps({ext: {**counts, "files": 1}}, indent=2))
        else:
            print(f"File: {args.path}")
            print(f"  Extension: {ext}")
            print(f"  Total:     {counts['total']}")
            print(f"  Code:      {counts['code']}")
            print(f"  Blank:     {counts['blank']}")
            print(f"  Comment:   {counts['comment']}")
        return

    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a file or directory", file=sys.stderr)
        sys.exit(1)

    extensions = [e if e.startswith(".") else f".{e}" for e in args.ext] if args.ext else None
    exclude = args.exclude or [".git", "node_modules", "__pycache__", ".venv", "venv"]
    results = walk_directory(args.path, extensions, exclude)

    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
    else:
        if not results:
            print("No files found matching criteria.")
            return
        print(f"{'Extension':<12} {'Files':>6} {'Total':>8} {'Code':>8} {'Blank':>8} {'Comment':>8}")
        print("-" * 56)
        for ext in sorted(results):
            r = results[ext]
            print(f"{ext:<12} {r['files']:>6} {r['total']:>8} {r['code']:>8} {r['blank']:>8} {r['comment']:>8}")


def cmd_summary(args):
    if os.path.isfile(args.path):
        counts = count_file_lines(args.path)
        if counts is None:
            print(f"Error: cannot read {args.path}", file=sys.stderr)
            sys.exit(1)
        total = counts["total"]
        if total:
            code_pct = counts["code"] / total * 100
            blank_pct = counts["blank"] / total * 100
            comment_pct = counts["comment"] / total * 100
        else:
            code_pct = blank_pct = comment_pct = 0

        if args.json:
            print(json.dumps({**counts, "code_pct": round(code_pct, 1), "blank_pct": round(blank_pct, 1), "comment_pct": round(comment_pct, 1)}, indent=2))
        else:
            print(f"Total lines:   {total}")
            print(f"Code lines:    {counts['code']} ({code_pct:.1f}%)")
            print(f"Blank lines:   {counts['blank']} ({blank_pct:.1f}%)")
            print(f"Comment lines: {counts['comment']} ({comment_pct:.1f}%)")
        return

    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a file or directory", file=sys.stderr)
        sys.exit(1)

    extensions = [e if e.startswith(".") else f".{e}" for e in args.ext] if args.ext else None
    exclude = args.exclude or [".git", "node_modules", "__pycache__", ".venv", "venv"]
    results = walk_directory(args.path, extensions, exclude)

    agg = {"total": 0, "code": 0, "blank": 0, "comment": 0, "files": 0, "extensions": len(results)}
    for r in results.values():
        for k in ("total", "code", "blank", "comment", "files"):
            agg[k] += r[k]

    total = agg["total"]
    if total:
        code_pct = agg["code"] / total * 100
        blank_pct = agg["blank"] / total * 100
        comment_pct = agg["comment"] / total * 100
    else:
        code_pct = blank_pct = comment_pct = 0

    if args.json:
        print(json.dumps({**agg, "code_pct": round(code_pct, 1), "blank_pct": round(blank_pct, 1), "comment_pct": round(comment_pct, 1)}, indent=2))
    else:
        print(f"Extensions:    {agg['extensions']}")
        print(f"Files:         {agg['files']}")
        print(f"Total lines:   {total}")
        print(f"Code lines:    {agg['code']} ({code_pct:.1f}%)")
        print(f"Blank lines:   {agg['blank']} ({blank_pct:.1f}%)")
        print(f"Comment lines: {agg['comment']} ({comment_pct:.1f}%)")


def main():
    parser = argparse.ArgumentParser(description="Count lines of code by file extension.")
    sub = parser.add_subparsers(dest="command")

    p_count = sub.add_parser("count", help="Count lines grouped by extension")
    p_count.add_argument("--path", required=True, help="Directory or file to scan")
    p_count.add_argument("--ext", nargs="+", help="Only count these extensions (e.g. .py .js)")
    p_count.add_argument("--exclude", nargs="+", help="Directory names to skip")
    p_count.add_argument("--json", action="store_true", help="JSON output")

    p_summary = sub.add_parser("summary", help="Aggregate summary across all extensions")
    p_summary.add_argument("--path", required=True, help="Directory or file to scan")
    p_summary.add_argument("--ext", nargs="+", help="Only count these extensions")
    p_summary.add_argument("--exclude", nargs="+", help="Directory names to skip")
    p_summary.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "count":
        cmd_count(args)
    elif args.command == "summary":
        cmd_summary(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
