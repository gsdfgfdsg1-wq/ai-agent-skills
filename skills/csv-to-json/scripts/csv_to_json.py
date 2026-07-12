#!/usr/bin/env python3
"""Convert CSV files to JSON with automatic type inference and flexible delimiter support.

No external dependencies — uses only Python standard library modules.
"""

import argparse
import csv
import json
import os
import sys


def infer_value(value, no_infer=False):
    """Infer the Python type of a CSV cell value.

    Args:
        value: The raw string value from the CSV cell.
        no_infer: If True, keep all values as strings (null conversion still applies).

    Returns:
        The converted value (int, float, bool, None, or str).
    """
    if value == "" or value.lower() == "null":
        return None

    if no_infer:
        return value

    lower = value.lower()
    if lower in ("true", "yes"):
        return True
    if lower in ("false", "no"):
        return False

    # Integer check
    if value.lstrip("-").isdigit() and value != "-":
        return int(value)

    # Float check
    try:
        parts = value.lstrip("-").split(".", 1)
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return float(value)
    except ValueError:
        pass

    return value


def convert_csv_to_json(filepath, delimiter=",", no_infer=False):
    """Read a CSV file and convert it to a list of dictionaries.

    Args:
        filepath: Path to the CSV file.
        delimiter: Field delimiter character.
        no_infer: If True, skip type inference.

    Returns:
        Tuple of (rows, headers) where rows is a list of dicts and
        headers is the list of column names.

    Raises:
        FileNotFoundError: If the input file does not exist.
        UnicodeDecodeError: If the file cannot be decoded as UTF-8.
        ValueError: If the CSV is empty or contains only headers.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")

    try:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=delimiter)
            try:
                headers = next(reader)
            except StopIteration:
                raise ValueError("empty")

            # Strip whitespace from headers
            headers = [h.strip() for h in headers]

            rows = []
            for row in reader:
                record = {}
                for i, header in enumerate(headers):
                    cell = row[i] if i < len(row) else ""
                    record[header] = infer_value(cell, no_infer=no_infer)
                rows.append(record)

    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError(
            exc.encoding, exc.object, exc.start, exc.end,
            f"Encoding error reading {filepath}: {exc.reason}"
        )

    if not rows:
        raise ValueError("headers_only")

    return rows, headers


def build_stats(rows, headers, filepath, delimiter, no_infer):
    """Build a statistics dictionary from the conversion result.

    Args:
        rows: List of converted row dicts.
        headers: List of column names.
        filepath: Input file path.
        delimiter: Delimiter used.
        no_infer: Whether type inference was disabled.

    Returns:
        Dict with conversion statistics.
    """
    type_counts = {}
    for row in rows:
        for key, val in row.items():
            type_name = type(val).__name__
            type_counts[type_name] = type_counts.get(type_name, 0) + 1

    return {
        "input_file": filepath,
        "delimiter": delimiter,
        "no_infer": no_infer,
        "row_count": len(rows),
        "column_count": len(headers),
        "columns": headers,
        "type_distribution": type_counts,
    }


def parse_args(argv=None):
    """Parse command-line arguments.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        argparse.Namespace with parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="csv_to_json",
        description="Convert CSV files to JSON with automatic type inference "
                    "and flexible delimiter support.",
        epilog="No external dependencies required. Uses only Python standard library.",
    )
    parser.add_argument(
        "--file",
        required=True,
        metavar="PATH",
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "--output",
        metavar="PATH",
        default=None,
        help="Path to the output JSON file (default: stdout)",
    )
    parser.add_argument(
        "--delimiter",
        metavar="CHAR",
        default=",",
        help="Field delimiter character (default: comma)",
    )
    parser.add_argument(
        "--no-infer",
        action="store_true",
        default=False,
        help="Disable type inference; keep all values as strings",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=False,
        help="Pretty-print the JSON output with indentation",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="Output conversion statistics as a JSON object",
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Entry point for the CSV-to-JSON converter."""
    args = parse_args(argv)

    try:
        rows, headers = convert_csv_to_json(
            filepath=args.file,
            delimiter=args.delimiter,
            no_infer=args.no_infer,
        )
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        if str(exc) == "empty":
            print("Error: CSV file is empty (no data rows found)", file=sys.stderr)
            sys.exit(2)
        elif str(exc) == "headers_only":
            print("Error: CSV file contains only headers (no data rows)", file=sys.stderr)
            sys.exit(3)
        else:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
    except UnicodeDecodeError as exc:
        print(f"Error: Encoding issue — {exc}", file=sys.stderr)
        sys.exit(4)

    indent = 2 if args.pretty else None

    if args.json:
        stats = build_stats(rows, headers, args.file, args.delimiter, args.no_infer)
        output = json.dumps(stats, indent=indent, ensure_ascii=False)
    else:
        output = json.dumps(rows, indent=indent, ensure_ascii=False)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
                f.write("\n")
        except OSError as exc:
            print(f"Error: Cannot write to {args.output} — {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()
