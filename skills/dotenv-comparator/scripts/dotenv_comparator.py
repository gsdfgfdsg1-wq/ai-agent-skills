#!/usr/bin/env python3
"""dotenv-comparator — compare two .env files and report differences.

Usage:
    python dotenv_comparator.py FILE_A FILE_B [--ignore-values] [--json] [--strict]

Reports added, removed, and changed keys between two dotenv files.
"""

import argparse
import json
import sys


def parse_dotenv(filepath):
    """Parse a .env file into an ordered dict of key -> value."""
    result = {}
    try:
        with open(filepath, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                # Remove surrounding quotes
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                if key:
                    result[key] = value
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    return result


def compare_dotenv(file_a, file_b, ignore_values=False):
    """Compare two dotenv files and return differences."""
    env_a = parse_dotenv(file_a)
    env_b = parse_dotenv(file_b)

    keys_a = set(env_a.keys())
    keys_b = set(env_b.keys())

    added = sorted(keys_b - keys_a)
    removed = sorted(keys_a - keys_b)
    common = keys_a & keys_b

    changed = []
    unchanged = []
    for k in sorted(common):
        if ignore_values:
            unchanged.append(k)
        elif env_a[k] != env_b[k]:
            changed.append({"key": k, "value_a": env_a[k], "value_b": env_b[k]})
        else:
            unchanged.append(k)

    return {
        "file_a": file_a,
        "file_b": file_b,
        "added": [{"key": k, "value": env_b[k]} for k in added],
        "removed": [{"key": k, "value": env_a[k]} for k in removed],
        "changed": changed,
        "unchanged_count": len(unchanged),
    }


def main():
    ap = argparse.ArgumentParser(
        description="Compare two .env files and report differences."
    )
    ap.add_argument("file_a", help="first .env file (base)")
    ap.add_argument("file_b", help="second .env file (target)")
    ap.add_argument("--ignore-values", action="store_true",
                    help="only compare key names, not values")
    ap.add_argument("--json", action="store_true",
                    help="output JSON results")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if any differences found")
    args = ap.parse_args()

    result = compare_dotenv(args.file_a, args.file_b, ignore_values=args.ignore_values)

    has_diff = bool(result["added"] or result["removed"] or result["changed"])

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Comparing {args.file_a} vs {args.file_b}:")
        if result["added"]:
            print(f"\n  Added ({len(result['added'])}):")
            for item in result["added"]:
                print(f"    + {item['key']}={item['value']}")
        if result["removed"]:
            print(f"\n  Removed ({len(result['removed'])}):")
            for item in result["removed"]:
                print(f"    - {item['key']}={item['value']}")
        if result["changed"]:
            print(f"\n  Changed ({len(result['changed'])}):")
            for item in result["changed"]:
                print(f"    ~ {item['key']}: {item['value_a']!r} -> {item['value_b']!r}")
        if not has_diff:
            print(f"\n  No differences found ({result['unchanged_count']} keys match)")

    if args.strict and has_diff:
        sys.exit(1)


if __name__ == "__main__":
    main()
