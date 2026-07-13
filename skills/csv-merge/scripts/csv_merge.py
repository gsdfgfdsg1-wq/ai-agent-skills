#!/usr/bin/env python3
"""Merge multiple CSV files by a common key column."""

import argparse
import csv
import json
import sys
from pathlib import Path


def read_csv(filepath):
    """Read a CSV file and return (headers, rows_as_dicts)."""
    try:
        with open(filepath, newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            headers = list(reader.fieldnames or [])
            rows = [dict(row) for row in reader]
    except (OSError, IOError) as e:
        print(f"Error: cannot read {filepath}: {e}", file=sys.stderr)
        sys.exit(1)
    return headers, rows


def merge_two(left_headers, left_rows, right_headers, right_rows, key, how):
    """Merge two CSV datasets on a key column."""
    # Build lookup from right side
    right_lookup = {}
    for row in right_rows:
        k = row.get(key, "")
        if k not in right_lookup:
            right_lookup[k] = []
        right_lookup[k].append(row)

    # Compute merged headers
    right_only_headers = [h for h in right_headers if h != key and h not in left_headers]
    merged_headers = left_headers + right_only_headers

    # Track used right keys for outer join
    used_right_keys = set()
    result = []

    # Process left rows
    for left_row in left_rows:
        k = left_row.get(key, "")
        right_matches = right_lookup.get(k, [])
        if right_matches:
            used_right_keys.add(k)
            for right_row in right_matches:
                merged = dict(left_row)
                for h in right_only_headers:
                    merged[h] = right_row.get(h, "")
                result.append(merged)
        elif how in ("left", "outer"):
            merged = dict(left_row)
            for h in right_only_headers:
                merged[h] = ""
            result.append(merged)
        # inner: skip if no match

    # Outer: add unmatched right rows
    if how == "outer":
        for k, right_rows_list in right_lookup.items():
            if k not in used_right_keys:
                for right_row in right_rows_list:
                    merged = {h: "" for h in merged_headers}
                    merged[key] = k
                    for h in right_only_headers:
                        merged[h] = right_row.get(h, "")
                    # Fill left columns from right if they exist
                    for h in left_headers:
                        if h in right_row:
                            merged[h] = right_row[h]
                    result.append(merged)

    return merged_headers, result


def cmd_merge(args):
    files = args.files
    if len(files) < 2:
        print("Error: at least 2 files required for merge", file=sys.stderr)
        sys.exit(1)

    key = args.key
    how = args.how

    # Read all files
    headers, rows = read_csv(files[0])
    if key not in headers:
        print(f"Error: key column '{key}' not found in {files[0]}", file=sys.stderr)
        sys.exit(1)

    for fpath in files[1:]:
        r_headers, r_rows = read_csv(fpath)
        if key not in r_headers:
            print(f"Error: key column '{key}' not found in {fpath}", file=sys.stderr)
            sys.exit(1)
        headers, rows = merge_two(headers, rows, r_headers, r_rows, key, how)

    # Output
    if args.json:
        print(json.dumps({"headers": headers, "rows": rows, "count": len(rows)}, indent=2, ensure_ascii=False))
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    if args.output:
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nWritten to: {args.output}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Merge CSV files by a common key column.")
    sub = parser.add_subparsers(dest="command")

    p_merge = sub.add_parser("merge", help="Merge CSV files")
    p_merge.add_argument("--key", required=True, help="Key column for joining")
    p_merge.add_argument("--how", choices=["inner", "left", "outer"], default="inner", help="Join type")
    p_merge.add_argument("--files", nargs="+", required=True, help="CSV files to merge")
    p_merge.add_argument("--output", help="Output file path")
    p_merge.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "merge":
        cmd_merge(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
