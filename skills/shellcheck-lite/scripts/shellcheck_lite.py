#!/usr/bin/env python3
"""shellcheck-lite — lightweight static checker for shell scripts.

Usage:
    python shellcheck_lite.py PATH [PATH ...] [--json] [--severity MIN] [--exit-code]

Checks for common pitfalls: unquoted variables, missing shebang, unsafe
arithmetic, deprecated syntax, and more — all without external dependencies.
"""

import argparse
import json
import os
import re
import sys

SEV_RANK = {"info": 0, "warning": 1, "error": 2}

SKIP_DIRS = {".git", "node_modules", "vendor", "__pycache__", ".tox", ".mypy_cache"}
SH_EXT = {".sh", ".bash", ".ksh", ".zsh"}


def _iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        else:
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for fn in files:
                    fp = os.path.join(root, fn)
                    ext = os.path.splitext(fn)[1].lower()
                    # Also check files without extension that start with #!/bin/bash etc.
                    if ext in SH_EXT:
                        yield fp
                    elif ext == "" and os.path.isfile(fp):
                        try:
                            with open(fp, "rb") as f:
                                head = f.read(64)
                            if head.startswith(b"#!/bin/sh") or head.startswith(b"#!/bin/bash") \
                               or head.startswith(b"#!/usr/bin/env bash") \
                               or head.startswith(b"#!/usr/bin/env sh"):
                                yield fp
                        except Exception:
                            pass


def _check_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return []

    findings = []

    # SC1000: Missing shebang
    if not lines or not lines[0].strip().startswith("#!"):
        findings.append({"rule": "SC1000", "severity": "error",
                         "line": 1, "message": "missing shebang line (#!/bin/sh or #!/bin/bash)",
                         "file": path})

    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")

        # SC1001: trailing whitespace after line continuation
        if raw.rstrip("\n") != raw.rstrip() and raw.rstrip("\n").endswith("\\"):
            findings.append({"rule": "SC1001", "severity": "warning",
                             "line": i, "message": "trailing whitespace after line continuation",
                             "file": path})

        # SC1002: unquoted $VAR in string context (not in [[ ]] or (( )))
        stripped = line.strip()
        if stripped.startswith("#"):
            continue

        # Skip [[ ... ]] and (( ... )) contexts
        in_double_bracket = "[[" in stripped and "]]" in stripped
        in_double_paren = "((" in stripped and "))" in stripped

        if not in_double_bracket and not in_double_paren:
            # Check for $VAR outside quotes (but not $() command substitution)
            for m in re.finditer(r'\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?', stripped):
                var_name = m.group(1)
                # Skip well-known special vars
                if var_name in ("@", "*", "#", "?", "!", "$", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                    continue
                pos = m.start()
                # Check if already inside double quotes
                before = stripped[:pos]
                dq_count = before.count('"') - before.count('\\"')
                if dq_count % 2 == 0:
                    # Not inside double quotes
                    # Check if it's inside single quotes
                    sq_count = before.count("'") - before.count("\\'")
                    if sq_count % 2 == 0:
                        # Not inside quotes at all — potential issue
                        findings.append({"rule": "SC1002", "severity": "warning",
                                         "line": i, "message": f"unquoted variable ${var_name}",
                                         "file": path})
                        break  # one per line

        # SC1003: deprecated backtick syntax
        if re.search(r'`[^`]+`', stripped) and not stripped.startswith("#"):
            # Exclude if inside double quotes of echo (common)
            findings.append({"rule": "SC1003", "severity": "info",
                             "line": i, "message": "consider $(...) instead of backticks `...`",
                             "file": path})

        # SC1004: use == in [ ] instead of =
        if re.match(r'\[.*=\s*[^\]]+\]', stripped) and "==" not in stripped:
            if re.search(r'\[\s*\$\w+\s*=\s*', stripped):
                findings.append({"rule": "SC1004", "severity": "info",
                                 "line": i, "message": "use == for string comparison in [ ]",
                                 "file": path})

        # SC1005: cd without || exit or && in same line
        if re.match(r'^\s*cd\s+', stripped) and "&&" not in stripped and "||" not in stripped:
            findings.append({"rule": "SC1005", "severity": "warning",
                             "line": i, "message": "cd without error handling (use cd ... || exit)",
                             "file": path})

        # SC1006: cat followed by pipe (useless cat)
        if re.match(r'^\s*cat\s+\S+\s*\|\s*', stripped):
            findings.append({"rule": "SC1006", "severity": "info",
                             "line": i, "message": "useless cat — consider redirecting input directly",
                             "file": path})

        # SC1007: echo without -n or -e but with escape
        if re.match(r'^\s*echo\s+"[^"]*\\[nt]', stripped):
            findings.append({"rule": "SC1007", "severity": "info",
                             "line": i, "message": "echo with escape sequences — consider echo -e or printf",
                             "file": path})

        # SC1008: test with -a / -o (prefer && / ||)
        if re.search(r'\[\s.*\s-a\s|\s-o\s.*\]', stripped):
            findings.append({"rule": "SC1008", "severity": "info",
                             "line": i, "message": "prefer && / || over -a / -o in [ ]",
                             "file": path})

    return findings


def main():
    ap = argparse.ArgumentParser(
        description="Lightweight static checker for shell scripts."
    )
    ap.add_argument("paths", nargs="+", help="shell scripts or directories to check")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--severity", default="info", choices=list(SEV_RANK),
                    help="minimum severity to report (default: info)")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit non-zero when findings >= --severity")
    args = ap.parse_args()

    all_findings = []
    for fp in _iter_targets(args.paths):
        all_findings.extend(_check_file(fp))

    # Deduplicate
    seen = set()
    uniq = []
    for f in all_findings:
        key = (f["file"], f["line"], f["rule"])
        if key not in seen:
            seen.add(key)
            uniq.append(f)

    min_rank = SEV_RANK[args.severity]
    shown = [f for f in uniq if SEV_RANK[f["severity"]] >= min_rank]

    if args.json:
        print(json.dumps(shown, indent=2, ensure_ascii=False))
    elif not shown:
        print(f"No issues found (>= {args.severity}).")
    else:
        print(f"Found {len(shown)} issue(s):\n")
        for f in sorted(shown, key=lambda x: -SEV_RANK[x["severity"]]):
            print(f"[{f['severity'].upper()}] {f['rule']} {f['file']}:{f['line']}")
            print(f"  {f['message']}\n")

    if args.exit_code and shown:
        sys.exit(1)


if __name__ == "__main__":
    main()
