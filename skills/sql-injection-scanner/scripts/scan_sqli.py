#!/usr/bin/env python3
"""sql-injection-scanner — scan source code for potential SQL injection patterns.

Usage:
    python scan_sqli.py PATH [PATH ...] [--severity high|medium|low] [--json] [--exit-code]

Detects common SQL injection patterns in Python, PHP, Java, JavaScript.
"""

import argparse
import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "__pycache__",
             ".venv", "venv", "target", "bin", "obj", ".tox", ".mypy_cache",
             ".pytest_cache", ".hg", ".svn"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf",
            ".eot", ".pdf", ".zip", ".gz", ".tar", ".lock", ".exe", ".dll",
            ".so", ".dylib", ".mp3", ".mp4", ".pyc", ".min.js", ".min.css"}
MAX_FILE = 2_000_000

# Pattern definitions: (regex, severity, description, languages)
PATTERNS = [
    # Python: string concat with SQL keywords
    (r'(?i)(?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE)\s+.*\+\s*(?:str\()?[\w\[\]]+',
     "high", "SQL string concatenation (Python)", {"py"}),
    # Python: format string SQL
    (r'(?i)(?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE)\s+.*\.format\s*\(',
     "high", "SQL with .format() (Python)", {"py"}),
    # Python: f-string SQL
    (r'(?i)f["\'](?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE)\s+.*\{',
     "high", "SQL f-string (Python)", {"py"}),
    # Python: % formatting SQL
    (r'(?i)(?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE)\s+.*%\s*[\(s]',
     "high", "SQL with % formatting (Python)", {"py"}),
    # Python: cursor.execute with string concat
    (r'cursor\.execute\s*\(\s*["\'].*\+',
     "high", "cursor.execute with concatenation (Python)", {"py"}),
    # Python: raw execute without params
    (r'(?i)\.execute\s*\(\s*(?:f["\']|["\'].*(?:%s|\{))',
     "medium", "execute with dynamic query (Python)", {"py"}),
    # PHP: string concat SQL
    (r'(?i)(?:SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*\.\s*\$',
     "high", "SQL string concatenation (PHP)", {"php"}),
    # PHP: double-quoted variable interpolation SQL
    (r'(?i)"(?:SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*\$\w',
     "high", "SQL with variable interpolation (PHP)", {"php"}),
    # Java: string concat SQL
    (r'(?i)(?:SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*\+\s*\w+',
     "high", "SQL string concatenation (Java)", {"java"}),
    # JavaScript: template literal SQL
    (r'(?i)`(?:SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*\$\{',
     "high", "SQL template literal (JavaScript)", {"js", "ts"}),
    # JavaScript: string concat SQL
    (r"(?i)(?:SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*'\s*\+",
     "high", "SQL string concatenation (JavaScript)", {"js", "ts"}),
    # Generic: raw_input / input in SQL context
    (r'(?i)(?:input|raw_input)\s*\(.*(?:SELECT|INSERT|UPDATE|DELETE|DROP)',
     "high", "User input directly in SQL", {"py"}),
    # ORM: unsafe extra / raw
    (r'(?i)\.raw\s*\(\s*(?:f["\']|["\'].*\+)',
     "medium", "ORM raw() with dynamic query", {"py"}),
    (r'(?i)\.extra\s*\(\s*where\s*=\s*\[?\s*(?:f["\']|["\'].*\+)',
     "medium", "ORM extra() with dynamic where (Python)", {"py"}),
]


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    ext = os.path.splitext(fn)[1].lower().lstrip(".")
                    if os.path.splitext(fn)[1].lower() in SKIP_EXT:
                        continue
                    yield os.path.join(root, fn)


def _scan_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return []
    if os.path.getsize(path) > MAX_FILE:
        return []

    ext = os.path.splitext(path)[1].lower().lstrip(".")
    findings = []

    for pattern, severity, description, langs in PATTERNS:
        if langs and ext not in langs:
            continue
        try:
            compiled = re.compile(pattern)
        except re.error:
            continue
        for i, line in enumerate(lines, 1):
            if compiled.search(line):
                findings.append({
                    "file": path,
                    "line": i,
                    "severity": severity,
                    "description": description,
                    "code": line.strip()[:120],
                })

    return findings


def main():
    ap = argparse.ArgumentParser(
        description="Scan source code for potential SQL injection patterns."
    )
    ap.add_argument("paths", nargs="+", help="files or directories to scan")
    ap.add_argument("--severity", choices=["high", "medium", "low"],
                    help="minimum severity to report")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit 1 if any findings")
    args = ap.parse_args()

    severity_rank = {"high": 0, "medium": 1, "low": 2}
    min_rank = severity_rank.get(args.severity, 2) if args.severity else 2

    all_findings = []
    for fp in _iter_targets(args.paths):
        findings = _scan_file(fp)
        for f in findings:
            if severity_rank.get(f["severity"], 2) <= min_rank:
                all_findings.append(f)

    # Deduplicate by file+line+description
    seen = set()
    unique = []
    for f in all_findings:
        key = (f["file"], f["line"], f["description"])
        if key not in seen:
            seen.add(key)
            unique.append(f)
    all_findings = unique

    # Sort by severity then file
    all_findings.sort(key=lambda f: (severity_rank.get(f["severity"], 2), f["file"], f["line"]))

    if args.json:
        print(json.dumps(all_findings, indent=2, ensure_ascii=False))
    elif not all_findings:
        print("No SQL injection patterns found.")
    else:
        print(f"Found {len(all_findings)} potential SQL injection pattern(s):\n")
        current_file = None
        for f in all_findings:
            if f["file"] != current_file:
                current_file = f["file"]
                print(f"  {current_file}")
            print(f"    L{f['line']} [{f['severity'].upper()}] {f['description']}")
            print(f"           {f['code']}")

    if args.exit_code and all_findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
