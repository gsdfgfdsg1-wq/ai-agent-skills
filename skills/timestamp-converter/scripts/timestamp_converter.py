#!/usr/bin/env python3
"""Timestamp Converter — convert between Unix timestamps, ISO 8601, and human-readable dates.

No external dependencies; uses only the Python standard library.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone, timedelta


def parse_tz_offset(tz_str: str) -> timezone:
    """Parse a timezone offset string like '+8', '-5', '+530' into a timezone."""
    m = re.match(r'^([+-])(\d{1,2})(?::?(\d{2}))?$', tz_str)
    if not m:
        print(f"Error: invalid timezone offset '{tz_str}'. Use format like +8, -5, +5:30.", file=sys.stderr)
        sys.exit(1)
    sign = 1 if m.group(1) == '+' else -1
    hours = int(m.group(2))
    minutes = int(m.group(3) or 0)
    if hours > 23 or minutes > 59:
        print(f"Error: timezone offset out of range: '{tz_str}'.", file=sys.stderr)
        sys.exit(1)
    return timezone(timedelta(hours=sign * hours, minutes=sign * minutes))


def format_output(dt: datetime, fmt: str, use_json: bool) -> str:
    """Format a datetime object according to the requested format."""
    iso_str = dt.isoformat()
    readable = dt.strftime("%A, %B %d, %Y %I:%M:%S %p %Z")
    epoch = dt.timestamp()

    if fmt == "iso":
        result = {"iso": iso_str}
    elif fmt == "epoch":
        result = {"epoch": epoch}
    else:  # both
        result = {"iso": iso_str, "epoch": epoch, "readable": readable}

    if use_json:
        return json.dumps(result, indent=2)
    else:
        lines = []
        for key, value in result.items():
            lines.append(f"{key:>10}: {value}")
        return "\n".join(lines)


def cmd_from_unix(args: argparse.Namespace) -> None:
    """Convert a Unix timestamp to ISO 8601 / readable date."""
    tz = parse_tz_offset(args.tz) if args.tz else timezone.utc

    try:
        timestamp = float(args.timestamp)
    except ValueError:
        print(f"Error: invalid timestamp '{args.timestamp}'. Must be an integer or float.", file=sys.stderr)
        sys.exit(1)

    try:
        dt = datetime.fromtimestamp(timestamp, tz=tz)
    except (OSError, OverflowError, ValueError) as e:
        print(f"Error: timestamp out of range: {e}", file=sys.stderr)
        sys.exit(1)

    print(format_output(dt, args.format, args.json))


def cmd_from_iso(args: argparse.Namespace) -> None:
    """Convert an ISO 8601 string to Unix timestamp / readable date."""
    iso_str = args.iso_string

    # Try parsing with various ISO 8601 formats
    dt = None

    # Replace trailing Z with +00:00 for fromisoformat compatibility
    normalized = iso_str.replace("Z", "+00:00")

    # Try datetime.fromisoformat (Python 3.7+)
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        pass

    # Try common formats as fallback
    if dt is None:
        patterns = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ]
        for pattern in patterns:
            try:
                dt = datetime.strptime(iso_str, pattern)
                break
            except ValueError:
                continue

    if dt is None:
        print(f"Error: invalid ISO 8601 string '{iso_str}'.", file=sys.stderr)
        sys.exit(1)

    # If no timezone info, treat as UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    print(format_output(dt, args.format, args.json))


def cmd_now(args: argparse.Namespace) -> None:
    """Show current time in all formats."""
    tz = parse_tz_offset(args.tz) if args.tz else timezone.utc
    dt = datetime.now(tz=tz)
    print(format_output(dt, args.format, args.json))


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="timestamp_converter",
        description="Convert between Unix timestamps, ISO 8601, and human-readable date formats.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # --- from_unix ---
    p_unix = subparsers.add_parser(
        "from_unix",
        help="Convert a Unix timestamp to ISO 8601 / readable date.",
    )
    p_unix.add_argument(
        "-t", "--timestamp",
        required=True,
        help="Unix timestamp (integer or float, e.g. 1700000000 or 1700000000.123).",
    )
    p_unix.add_argument(
        "--format",
        choices=["iso", "epoch", "both"],
        default="both",
        help="Output format (default: both).",
    )
    p_unix.add_argument(
        "--tz",
        default=None,
        help="Timezone offset, e.g. +8 for CST, -5 for EST (default: UTC).",
    )
    p_unix.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format.",
    )

    # --- from_iso ---
    p_iso = subparsers.add_parser(
        "from_iso",
        help="Convert an ISO 8601 string to Unix timestamp.",
    )
    p_iso.add_argument(
        "-s", "--iso-string",
        required=True,
        help="ISO 8601 date string, e.g. '2023-11-14T22:13:20Z'.",
    )
    p_iso.add_argument(
        "--format",
        choices=["iso", "epoch", "both"],
        default="both",
        help="Output format (default: both).",
    )
    p_iso.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format.",
    )

    # --- now ---
    p_now = subparsers.add_parser(
        "now",
        help="Show current time in all formats.",
    )
    p_now.add_argument(
        "--format",
        choices=["iso", "epoch", "both"],
        default="both",
        help="Output format (default: both).",
    )
    p_now.add_argument(
        "--tz",
        default=None,
        help="Timezone offset, e.g. +8 for CST, -5 for EST (default: UTC).",
    )
    p_now.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    dispatch = {
        "from_unix": cmd_from_unix,
        "from_iso": cmd_from_iso,
        "now": cmd_now,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
