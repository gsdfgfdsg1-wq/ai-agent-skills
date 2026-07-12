#!/usr/bin/env python3
"""List methods, paths, operation IDs, and tags from an OpenAPI JSON document."""

import argparse
import json
import sys
from pathlib import Path


METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace")


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("cannot read JSON file {}: {}".format(path, error))


def inventory(document, requested_tags):
    paths = document.get("paths") if isinstance(document, dict) else None
    if not isinstance(paths, dict):
        raise ValueError("OpenAPI document must contain a top-level object named paths")

    entries = []
    for path in sorted(paths):
        path_item = paths[path]
        if not isinstance(path_item, dict):
            continue
        for method in METHODS:
            operation = path_item.get(method)
            if not isinstance(operation, dict):
                continue
            tags = operation.get("tags", [])
            if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
                tags = []
            if requested_tags and not set(tags).intersection(requested_tags):
                continue
            operation_id = operation.get("operationId", "")
            entries.append({
                "method": method.upper(),
                "path": path,
                "operationId": operation_id if isinstance(operation_id, str) else "",
                "tags": tags,
            })
    return entries


def print_table(entries):
    for entry in entries:
        print("{}\t{}\t{}\t{}".format(
            entry["method"],
            entry["path"],
            entry["operationId"],
            ",".join(entry["tags"]),
        ))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="path to an OpenAPI JSON document")
    parser.add_argument("--tag", action="append", default=[], help="retain operations with this tag; repeatable, any match")
    parser.add_argument("--json", action="store_true", help="emit a JSON array")
    args = parser.parse_args()

    try:
        entries = inventory(load_json(args.input), set(args.tag))
    except ValueError as error:
        if args.json:
            print(json.dumps({"error": str(error)}))
        else:
            print("error: {}".format(error), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
    else:
        print_table(entries)
    return 0 if entries else 2


if __name__ == "__main__":
    sys.exit(main())
