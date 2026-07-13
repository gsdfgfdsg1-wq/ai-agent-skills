#!/usr/bin/env python3
"""Recursively sort JSON object keys alphabetically."""

import argparse
import json
import sys
from pathlib import Path


def sort_keys(obj, reverse=False, depth=-1, current_depth=0):
    """Recursively sort dictionary keys."""
    if isinstance(obj, dict):
        if depth != -1 and current_depth >= depth:
            return obj
        sorted_dict = {}
        for key in sorted(obj.keys(), reverse=reverse):
            sorted_dict[key] = sort_keys(obj[key], reverse, depth, current_depth + 1)
        return sorted_dict
    elif isinstance(obj, list):
        return [sort_keys(item, reverse, depth, current_depth + 1) for item in obj]
    return obj


def cmd_sort(args):
    # Read input
    if args.file:
        try:
            text = Path(args.file).read_text(encoding="utf-8")
        except (OSError, IOError) as e:
            print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    depth = args.depth if args.depth is not None else -1
    result = sort_keys(data, reverse=args.reverse, depth=depth)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.inplace and args.file:
        Path(args.file).write_text(output + "\n", encoding="utf-8")
        print(f"Sorted and written to: {args.file}")
    else:
        print(output)

    if args.json and not args.inplace:
        stats = {
            "file": str(args.file) if args.file else "stdin",
            "reverse": args.reverse,
            "depth": depth,
            "top_keys": len(result) if isinstance(result, dict) else len(result),
        }
        print("---")
        print(json.dumps(stats, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Recursively sort JSON keys.")
    sub = parser.add_subparsers(dest="command")

    p_sort = sub.add_parser("sort", help="Sort JSON keys")
    p_sort.add_argument("--file", help="Input JSON file (or stdin)")
    p_sort.add_argument("--reverse", action="store_true", help="Sort in descending order")
    p_sort.add_argument("--depth", type=int, help="Limit recursion depth")
    p_sort.add_argument("--inplace", action="store_true", help="Overwrite input file")
    p_sort.add_argument("--json", action="store_true", help="Also output stats as JSON")

    args = parser.parse_args()
    if args.command == "sort":
        cmd_sort(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
