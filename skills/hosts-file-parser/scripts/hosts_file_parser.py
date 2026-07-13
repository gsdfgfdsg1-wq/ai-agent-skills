#!/usr/bin/env python3
"""Parse and validate hosts-format text using only the Python standard library."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from pathlib import Path
from typing import Any

HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}\.?$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)*"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.?$"
)


def is_valid_alias(alias: str) -> bool:
    """Return whether alias is a hosts-compatible hostname."""
    return alias.lower() == "localhost" or bool(HOSTNAME_RE.fullmatch(alias))


def parse_hosts(text: str) -> dict[str, Any]:
    """Parse hosts text into records, duplicates, and invalid entries."""
    records: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    invalid_entries: list[dict[str, Any]] = []
    seen_pairs: set[tuple[str, str]] = set()

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        content = raw_line.split("#", 1)[0].strip()
        if not content:
            continue

        tokens = content.split()
        address = tokens[0]
        aliases = tokens[1:]
        try:
            normalized_address = str(ipaddress.ip_address(address))
        except ValueError:
            invalid_entries.append(
                {"line": line_number, "reason": "invalid_address", "value": address, "raw": raw_line}
            )
            continue

        if not aliases:
            invalid_entries.append(
                {"line": line_number, "reason": "missing_alias", "value": address, "raw": raw_line}
            )
            continue

        valid_aliases: list[str] = []
        for alias in aliases:
            if not is_valid_alias(alias):
                invalid_entries.append(
                    {"line": line_number, "reason": "invalid_alias", "value": alias, "raw": raw_line}
                )
                continue
            normalized_alias = alias.lower().rstrip(".")
            pair = (normalized_address, normalized_alias)
            if pair in seen_pairs:
                duplicates.append(
                    {"line": line_number, "address": normalized_address, "alias": normalized_alias}
                )
                continue
            seen_pairs.add(pair)
            valid_aliases.append(normalized_alias)

        if valid_aliases:
            records.append(
                {"line": line_number, "address": normalized_address, "aliases": valid_aliases}
            )

    return {
        "records": records,
        "duplicates": duplicates,
        "invalid_entries": invalid_entries,
        "summary": {
            "record_count": len(records),
            "mapping_count": len(seen_pairs),
            "duplicate_count": len(duplicates),
            "invalid_count": len(invalid_entries),
        },
    }


def read_input(source: str) -> str:
    """Read hosts data from stdin or a UTF-8 text file."""
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8")


def format_text(report: dict[str, Any]) -> str:
    """Format the report for terminal output."""
    lines = ["Records:"]
    for record in report["records"]:
        lines.append(f"  {record['address']} {' '.join(record['aliases'])} (line {record['line']})")

    lines.append("Duplicates:")
    for duplicate in report["duplicates"]:
        lines.append(f"  {duplicate['address']} {duplicate['alias']} (line {duplicate['line']})")

    lines.append("Invalid entries:")
    for entry in report["invalid_entries"]:
        lines.append(f"  line {entry['line']}: {entry['reason']} ({entry['value']})")

    summary = report["summary"]
    lines.append(
        "Summary: "
        f"{summary['record_count']} records, {summary['mapping_count']} mappings, "
        f"{summary['duplicate_count']} duplicates, {summary['invalid_count']} invalid"
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse and validate a hosts-format file.")
    parser.add_argument("source", help="Path to a hosts file, or - to read stdin")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON output")
    args = parser.parse_args()

    try:
        report = parse_hosts(read_input(args.source))
    except (OSError, UnicodeError) as error:
        parser.error(str(error))

    if args.as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))
    return 1 if report["invalid_entries"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
