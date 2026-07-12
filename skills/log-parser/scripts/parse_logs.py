#!/usr/bin/env python3
"""log-parser — parse and summarize log files by level and pattern.

Usage:
    python parse_logs.py PATH [PATH ...] [--levels L1,L2] [--pattern REGEX] [--top N] [--json] [--summary]

Supports common log formats: plain level prefixes (ERROR, WARN, INFO, DEBUG),
timestamp-prefixed (ISO 8601, Apache, nginx), and Python logging format.
"""

import argparse
import json
import os
import re
import sys

LEVEL_MAP = {
    "CRITICAL": "critical", "FATAL": "critical", "CRIT": "critical",
    "ERROR": "error", "ERR": "error",
    "WARNING": "warning", "WARN": "warning",
    "INFO": "info",
    "DEBUG": "debug", "TRACE": "trace",
}

LEVEL_RANK = {
    "critical": 0, "error": 1, "warning": 2, "info": 3, "debug": 4, "trace": 5,
}

# Patterns to detect log level in a line
LEVEL_PATTERNS = [
    # Python logging: 2024-01-01 12:00:00,000 ERROR message
    re.compile(r'(?:\d{4}[-/]\d{2}[-/]\d{2}[\sT]\d{2}:\d{2}:\d{2}(?:[,\.]\d+)?\s*)(CRITICAL|FATAL|ERROR|WARNING|WARN|INFO|DEBUG|TRACE)\b', re.I),
    # Apache: [error] or [warn]
    re.compile(r'\[(crit|error|warn|info|debug|notice|trace)\]', re.I),
    # Standalone: ERROR: or [ERROR] or ERROR -
    re.compile(r'(?:^|\s)(?:\[)?(CRITICAL|FATAL|ERROR|ERR|WARNING|WARN|INFO|DEBUG|TRACE)(?:\]?)[:\s-]', re.I),
    # Simple prefix: LEVEL message
    re.compile(r'^(CRITICAL|FATAL|ERROR|ERR|WARNING|WARN|INFO|DEBUG|TRACE)\b', re.I),
]

SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__", ".tox"}
LOG_EXT = {".log", ".txt", ".out", ".err"}
MAX_FILE = 10_000_000  # 10 MB


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    ext = os.path.splitext(fn)[1].lower()
                    if ext in LOG_EXT or fn.endswith(".log"):
                        yield os.path.join(root, fn)


def _detect_level(line):
    for pat in LEVEL_PATTERNS:
        m = pat.search(line)
        if m:
            raw = m.group(1).upper()
            return LEVEL_MAP.get(raw, "info")
    return None


def _parse_file(path, level_filter, pattern):
    try:
        size = os.path.getsize(path)
        if size > MAX_FILE:
            return [], f"file too large ({size} bytes)"
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        return [], str(e)

    entries = []
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        if not line.strip():
            continue

        level = _detect_level(line)
        if level is None:
            level = "info"  # default for unrecognized lines

        if level_filter and level not in level_filter:
            continue

        if pattern and not re.search(pattern, line, re.I):
            continue

        entries.append({
            "line": i,
            "level": level,
            "text": line[:200] + ("..." if len(line) > 200 else ""),
            "file": path,
        })

    return entries, None


def main():
    ap = argparse.ArgumentParser(
        description="Parse and summarize log files by level and pattern."
    )
    ap.add_argument("paths", nargs="+", help="log files or directories to parse")
    ap.add_argument("--levels", default=None,
                    help="comma-separated levels to include (critical,error,warning,info,debug,trace)")
    ap.add_argument("--pattern", default=None,
                    help="regex pattern to filter log lines")
    ap.add_argument("--top", type=int, default=20,
                    help="max lines to show per level (default: 20)")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--summary", action="store_true",
                    help="show summary counts only")
    args = ap.parse_args()

    level_filter = None
    if args.levels:
        level_filter = set(l.strip().lower() for l in args.levels.split(","))

    all_entries = []
    errors = []
    for fp in _iter_targets(args.paths):
        entries, err = _parse_file(fp, level_filter, args.pattern)
        all_entries.extend(entries)
        if err:
            errors.append({"file": fp, "error": err})

    if args.json:
        result = {"entries": all_entries[:args.top], "errors": errors}
        counts = {}
        for e in all_entries:
            counts[e["level"]] = counts.get(e["level"], 0) + 1
        result["summary"] = counts
        result["total"] = len(all_entries)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.summary:
        counts = {}
        for e in all_entries:
            counts[e["level"]] = counts.get(e["level"], 0) + 1
        if not counts:
            print("No matching log entries found.")
        else:
            print("Log level summary:")
            for lvl in sorted(counts, key=lambda l: LEVEL_RANK.get(l, 99)):
                print(f"  {lvl}: {counts[lvl]}")
            print(f"  Total: {len(all_entries)}")
    elif not all_entries:
        print("No matching log entries found.")
    else:
        print(f"Found {len(all_entries)} matching log entries:\n")

        # Group by level
        by_level = {}
        for e in all_entries:
            by_level.setdefault(e["level"], []).append(e)

        for lvl in sorted(by_level, key=lambda l: LEVEL_RANK.get(l, 99)):
            entries = by_level[lvl]
            print(f"[{lvl.upper()}] ({len(entries)} entries)")
            for e in entries[:args.top]:
                print(f"  {e['file']}:{e['line']} | {e['text'][:100]}")
            if len(entries) > args.top:
                print(f"  ... and {len(entries) - args.top} more")
            print()

    if errors:
        for e in errors:
            print(f"Warning: skipped {e['file']}: {e['error']}", file=sys.stderr)


if __name__ == "__main__":
    main()
