#!/usr/bin/env python3
"""Deduplicate JSONL objects by a dotted key."""

import argparse
import json
import sys
from pathlib import Path


def parse_key(key):
    parts = key.split(".")
    if not key or any(not part for part in parts):
        raise ValueError("key must be a dot-separated path with non-empty segments")
    return parts


def key_value(record, parts, line_number):
    value = record
    for part in parts:
        if not isinstance(value, dict) or part not in value:
            raise ValueError("line {}: missing key {}".format(line_number, ".".join(parts)))
        value = value[part]
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def read_records(input_path, parts):
    try:
        lines = Path(input_path).read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ValueError("cannot read input file {}: {}".format(input_path, error))

    records = []
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError("line {}: invalid JSON: {}".format(line_number, error.msg))
        if not isinstance(record, dict):
            raise ValueError("line {}: JSONL record must be an object".format(line_number))
        records.append((line_number, record, key_value(record, parts, line_number)))
    return records


def deduplicate(records, keep):
    retained = {}
    if keep == "first":
        for position, item in enumerate(records):
            retained.setdefault(item[2], position)
    else:
        for position, item in enumerate(records):
            retained[item[2]] = position
    return [records[position][1] for position in sorted(retained.values())]


def write_output(path, records):
    try:
        with Path(path).open("w", encoding="utf-8", newline="\n") as stream:
            for record in records:
                stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
                stream.write("\n")
    except OSError as error:
        raise ValueError("cannot write output file {}: {}".format(path, error))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="path to input JSONL file")
    parser.add_argument("output", help="path for deduplicated JSONL output")
    parser.add_argument("--key", required=True, help="dotted object key used for identity")
    parser.add_argument("--keep", choices=("first", "last"), default="first",
                        help="duplicate record to retain (default: first)")
    parser.add_argument("--stats-json", help="optional path for JSON statistics")
    args = parser.parse_args()

    try:
        parts = parse_key(args.key)
        records = read_records(args.input, parts)
        output_records = deduplicate(records, args.keep)
        stats = {
            "input_records": len(records),
            "output_records": len(output_records),
            "duplicates_removed": len(records) - len(output_records),
            "key": args.key,
            "keep": args.keep,
        }
        write_output(args.output, output_records)
        if args.stats_json:
            Path(args.stats_json).write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
    except ValueError as error:
        print("error: {}".format(error), file=sys.stderr)
        return 2
    except OSError as error:
        print("error: cannot write stats file {}: {}".format(args.stats_json, error), file=sys.stderr)
        return 2

    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
