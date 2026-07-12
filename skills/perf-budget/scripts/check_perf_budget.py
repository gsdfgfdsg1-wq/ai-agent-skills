#!/usr/bin/env python3
"""Check recursively discovered file sizes against glob-based performance budgets."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

LIMIT_PATTERN = re.compile(r"^(0|[1-9][0-9]*)(B|KiB|MiB|GiB)?$")
MULTIPLIERS = {"B": 1, "KiB": 1024, "MiB": 1024**2, "GiB": 1024**3}


@dataclass(frozen=True)
class Rule:
    glob: str
    limit_bytes: int


def parse_limit(value: str) -> int:
    match = LIMIT_PATTERN.fullmatch(value)
    if not match:
        raise ValueError("limit must be a non-negative integer followed by B, KiB, MiB, or GiB")
    amount, unit = match.groups()
    return int(amount) * MULTIPLIERS[unit or "B"]


def parse_rule(value: str) -> Rule:
    if "=" not in value:
        raise ValueError("rule must use GLOB=LIMIT")
    glob, limit = value.rsplit("=", 1)
    if not glob:
        raise ValueError("rule glob must not be empty")
    return Rule(glob=glob, limit_bytes=parse_limit(limit))


def collect_records(target: Path, rules: list[Rule]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for file_path in sorted(path for path in target.rglob("*") if path.is_file()):
        relative_path = file_path.relative_to(target).as_posix()
        matches = [rule for rule in rules if fnmatch.fnmatchcase(relative_path, rule.glob)]
        size_bytes = file_path.stat().st_size
        if not matches:
            records.append(
                {
                    "path": relative_path,
                    "size_bytes": size_bytes,
                    "matched_rules": [],
                    "limit_bytes": None,
                    "status": "unmatched",
                }
            )
            continue

        limit_bytes = min(rule.limit_bytes for rule in matches)
        records.append(
            {
                "path": relative_path,
                "size_bytes": size_bytes,
                "matched_rules": [rule.glob for rule in matches],
                "limit_bytes": limit_bytes,
                "status": "pass" if size_bytes <= limit_bytes else "violation",
            }
        )
    return records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="directory to inspect recursively")
    parser.add_argument(
        "--rule",
        action="append",
        default=[],
        metavar="GLOB=LIMIT",
        help="glob and maximum size, repeatable; limit uses B, KiB, MiB, or GiB",
    )
    parser.add_argument("--json", action="store_true", help="emit a single JSON result object")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.target.is_dir():
        parser.error(f"target is not a readable directory: {args.target}")
    if not args.rule:
        parser.error("at least one --rule is required")

    try:
        rules = [parse_rule(value) for value in args.rule]
    except ValueError as error:
        parser.error(str(error))

    target = args.target.resolve()
    records = collect_records(target, rules)
    summary = {
        "checked": len(records),
        "passing": sum(record["status"] == "pass" for record in records),
        "violations": sum(record["status"] == "violation" for record in records),
        "unmatched": sum(record["status"] == "unmatched" for record in records),
    }

    if args.json:
        print(
            json.dumps(
                {
                    "target": str(target),
                    "rules": [rule.__dict__ for rule in rules],
                    "files": records,
                    "summary": summary,
                },
                sort_keys=True,
            )
        )
    else:
        for record in records:
            status = str(record["status"]).upper()
            limit = record["limit_bytes"]
            if limit is None:
                print(f"{status:<9} {record['size_bytes']:>8} B              {record['path']}")
            else:
                comparison = "<=" if record["status"] == "pass" else ">"
                print(
                    f"{status:<9} {record['size_bytes']:>8} B {comparison} {limit:>8} B  {record['path']}"
                )
        print(
            "Summary: {checked} checked, {passing} passing, {violations} violation, {unmatched} unmatched".format(
                **summary
            )
        )

    return 1 if summary["violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
