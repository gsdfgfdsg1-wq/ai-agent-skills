#!/usr/bin/env python3
"""Rank recursively discovered file sizes in a directory."""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path


def non_negative_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a non-negative integer") from error
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be a non-negative integer")
    return parsed


def collect_records(target: Path, includes: list[str]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for file_path in target.rglob("*"):
        if not file_path.is_file():
            continue
        relative_path = file_path.relative_to(target).as_posix()
        if includes and not any(fnmatch.fnmatchcase(relative_path, glob) for glob in includes):
            continue
        records.append({"path": relative_path, "size_bytes": file_path.stat().st_size})
    return sorted(records, key=lambda record: (-int(record["size_bytes"]), str(record["path"])))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="directory to inspect recursively")
    parser.add_argument(
        "--top",
        type=non_negative_int,
        default=None,
        metavar="N",
        help="report at most N largest files; 0 reports no files",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        metavar="GLOB",
        help="include paths matching this relative-path glob, repeatable",
    )
    parser.add_argument("--json", action="store_true", help="emit a single JSON result object")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.target.is_dir():
        parser.error(f"target is not a readable directory: {args.target}")

    target = args.target.resolve()
    records = collect_records(target, args.include)
    reported = records if args.top is None else records[: args.top]
    summary = {
        "total_files": len(records),
        "total_size_bytes": sum(int(record["size_bytes"]) for record in records),
        "reported_files": len(reported),
        "reported_size_bytes": sum(int(record["size_bytes"]) for record in reported),
    }

    if args.json:
        print(
            json.dumps(
                {
                    "target": str(target),
                    "includes": args.include,
                    "top": args.top,
                    "files": reported,
                    "summary": summary,
                },
                sort_keys=True,
            )
        )
    else:
        for record in reported:
            print(f"{record['size_bytes']:>8} B  {record['path']}")
        print(
            "Summary: {reported_files} reported of {total_files} included files; "
            "{reported_size_bytes} B reported, {total_size_bytes} B total".format(**summary)
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
