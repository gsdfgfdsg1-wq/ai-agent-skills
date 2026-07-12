#!/usr/bin/env python3
"""regex-tester — test regular expressions against sample strings.

Usage:
    python regex_tester.py -p PATTERN -s STRING [STRING ...] [--flags F1,F2] [--findall] [--json]
    python regex_tester.py -p PATTERN -f FILE [--flags F1,F2] [--findall] [--json]

Reports match/nomatch, groups, positions, and matched text.
"""

import argparse
import json
import re
import sys


FLAG_MAP = {
    "IGNORECASE": re.IGNORECASE,
    "I": re.IGNORECASE,
    "DOTALL": re.DOTALL,
    "S": re.DOTALL,
    "MULTILINE": re.MULTILINE,
    "M": re.MULTILINE,
    "VERBOSE": re.VERBOSE,
    "X": re.VERBOSE,
    "ASCII": re.ASCII,
    "A": re.ASCII,
}


def _parse_flags(flag_str):
    """Parse comma-separated flag names into a combined re flag."""
    combined = 0
    if not flag_str:
        return combined
    for name in flag_str.split(","):
        name = name.strip().upper()
        if name in FLAG_MAP:
            combined |= FLAG_MAP[name]
        else:
            print(f"[WARNING] Unknown regex flag: {name}", file=sys.stderr)
    return combined


def test_pattern(pattern, strings, flags=0, findall=False):
    """Test a compiled regex against a list of strings, returning results."""
    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        return [{"error": f"Invalid regex: {e}"}]

    results = []
    for s in strings:
        entry = {"pattern": pattern, "input": s}

        if findall:
            matches = compiled.findall(s)
            entry["match"] = bool(matches)
            entry["findall"] = matches
        else:
            m = compiled.search(s)
            if m:
                entry["match"] = True
                entry["matched_text"] = m.group(0)
                entry["start"] = m.start()
                entry["end"] = m.end()
                groups = m.groups()
                if groups:
                    entry["groups"] = [
                        {"text": g, "start": m.start(i + 1), "end": m.end(i + 1)}
                        for i, g in enumerate(groups)
                    ]
                named = m.groupdict()
                if named:
                    entry["named_groups"] = named
            else:
                entry["match"] = False

        results.append(entry)

    return results


def main():
    ap = argparse.ArgumentParser(
        description="Test regular expressions against sample strings."
    )
    ap.add_argument("-p", "--pattern", required=True,
                    help="regex pattern to test")
    ap.add_argument("-s", "--strings", nargs="*", default=[],
                    help="test strings (mutually exclusive with -f)")
    ap.add_argument("-f", "--file", default=None,
                    help="file with test strings (one per line)")
    ap.add_argument("--flags", default=None,
                    help="comma-separated regex flags (IGNORECASE, DOTALL, MULTILINE, VERBOSE, ASCII)")
    ap.add_argument("--findall", action="store_true",
                    help="find all non-overlapping matches instead of first")
    ap.add_argument("--json", action="store_true",
                    help="output JSON results")
    args = ap.parse_args()

    if not args.strings and not args.file:
        ap.error("Provide at least one test string (-s) or a file (-f)")

    strings = list(args.strings) if args.strings else []
    if args.file:
        try:
            with open(args.file, encoding="utf-8") as fh:
                for line in fh:
                    line = line.rstrip("\n")
                    if line:
                        strings.append(line)
        except FileNotFoundError:
            print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
            sys.exit(1)

    flags = _parse_flags(args.flags)
    results = test_pattern(args.pattern, strings, flags=flags, findall=args.findall)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            if "error" in r:
                print(f"[ERROR] {r['error']}")
                continue
            status = "MATCH" if r["match"] else "NO MATCH"
            print(f"{status}: {r['input']!r}")
            if r["match"]:
                if "findall" in r:
                    for i, m in enumerate(r["findall"]):
                        print(f"  [{i}] {m!r}")
                else:
                    print(f"  text: {r['matched_text']!r} (pos {r['start']}-{r['end']})")
                    if "groups" in r:
                        for i, g in enumerate(r["groups"]):
                            print(f"  group({i+1}): {g['text']!r} (pos {g['start']}-{g['end']})")
                    if "named_groups" in r:
                        for k, v in r["named_groups"].items():
                            print(f"  group({k}): {v!r}")


if __name__ == "__main__":
    main()
