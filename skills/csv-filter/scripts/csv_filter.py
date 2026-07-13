#!/usr/bin/env python3
"""Filter CSV rows by column value conditions without external dependencies."""

import argparse
import csv
import json
import re
import sys


OPERATORS = ["eq", "ne", "gt", "lt", "gte", "lte", "contains", "regex", "empty", "notempty"]


def try_number(val):
    """Try to convert value to a number for comparison."""
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return None


def check_condition(row_value, op, filter_value):
    """Check if a row value satisfies a filter condition."""
    if op == "empty":
        return row_value is None or row_value.strip() == ""
    if op == "notempty":
        return row_value is not None and row_value.strip() != ""

    if row_value is None:
        return False

    if op == "eq":
        return row_value == filter_value
    elif op == "ne":
        return row_value != filter_value
    elif op == "contains":
        return filter_value in row_value
    elif op == "regex":
        try:
            return bool(re.search(filter_value, row_value))
        except re.error:
            return False
    elif op in ("gt", "lt", "gte", "lte"):
        # Try numeric comparison
        rv = try_number(row_value)
        fv = try_number(filter_value)
        if rv is not None and fv is not None:
            if op == "gt":
                return rv > fv
            elif op == "lt":
                return rv < fv
            elif op == "gte":
                return rv >= fv
            elif op == "lte":
                return rv <= fv
        # Fall back to string comparison
        if op == "gt":
            return row_value > filter_value
        elif op == "lt":
            return row_value < filter_value
        elif op == "gte":
            return row_value >= filter_value
        elif op == "lte":
            return row_value <= filter_value
    return False


def cmd_filter(args):
    try:
        with open(args.file, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            rows = list(reader)
    except OSError as e:
        print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse conditions
    conditions = []
    # Primary condition
    conditions.append((args.column, args.op, args.value or ""))
    # Additional --and conditions
    if args.and_cond:
        for cond_str in args.and_cond:
            parts = cond_str.split(":", 2)
            if len(parts) != 3:
                print(f"Error: invalid --and format '{cond_str}' — expected column:op:value", file=sys.stderr)
                sys.exit(1)
            col, op, val = parts
            if op not in OPERATORS:
                print(f"Error: unknown operator '{op}' in --and condition", file=sys.stderr)
                sys.exit(1)
            conditions.append((col, op, val))

    # Validate columns exist
    for col, op, val in conditions:
        if col not in headers:
            print(f"Error: column '{col}' not found in CSV. Available: {', '.join(headers)}", file=sys.stderr)
            sys.exit(1)

    # Filter
    matched = []
    for row in rows:
        if all(check_condition(row.get(col), op, val) for col, op, val in conditions):
            matched.append(row)

    if args.json:
        print(json.dumps({"matched": len(matched), "total": len(rows), "rows": matched}, indent=2))
        return

    # CSV output
    output = sys.stdout
    close_output = False
    if args.output:
        try:
            output = open(args.output, "w", encoding="utf-8", newline="")
            close_output = True
        except OSError as e:
            print(f"Error: cannot write {args.output}: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        for row in matched:
            writer.writerow(row)
    finally:
        if close_output:
            output.close()

    if not args.output:
        summary = f"\n--- {len(matched)}/{len(rows)} rows matched ---"
        print(summary, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Filter CSV rows by column conditions.")
    sub = parser.add_subparsers(dest="command")

    p_filter = sub.add_parser("filter", help="Filter rows by condition")
    p_filter.add_argument("--file", required=True, help="CSV file to filter")
    p_filter.add_argument("--column", required=True, help="Column name to filter on")
    p_filter.add_argument("--op", required=True, choices=OPERATORS, help="Comparison operator")
    p_filter.add_argument("--value", help="Value to compare against (not needed for empty/notempty)")
    p_filter.add_argument("--and", dest="and_cond", action="append", help="Additional condition: column:op:value")
    p_filter.add_argument("--output", help="Output file (default: stdout)")
    p_filter.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "filter":
        cmd_filter(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
