#!/usr/bin/env python3
"""Compare two JSON configuration files and report added, removed, and changed values."""

import argparse
import json
import sys
from pathlib import Path


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("cannot read JSON file {}: {}".format(path, error))


def path_for(parent, key):
    escaped = str(key).replace("\\", "\\\\").replace(".", "\\.").replace("[", "\\[").replace("]", "\\]")
    return escaped if not parent else "{}.{}".format(parent, escaped)


MISSING = object()


def add_entry(entries, kind, path, old=MISSING, new=MISSING):
    entry = {"path": path}
    if old is not MISSING:
        entry["old"] = old
    if new is not MISSING:
        entry["new"] = new
    entries[kind].append(entry)


def compare(old, new, path, entries):
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(set(old) | set(new)):
            child_path = path_for(path, key)
            if key not in old:
                add_entry(entries, "added", child_path, new=new[key])
            elif key not in new:
                add_entry(entries, "removed", child_path, old=old[key])
            else:
                compare(old[key], new[key], child_path, entries)
    elif old != new or type(old) is not type(new):
        add_entry(entries, "changed", path or "$", old, new)


def format_value(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", help="path to the baseline JSON file")
    parser.add_argument("new", help="path to the updated JSON file")
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    args = parser.parse_args()
    try:
        old = load_json(args.old)
        new = load_json(args.new)
    except ValueError as error:
        if args.json:
            print(json.dumps({"error": str(error)}))
        else:
            print("error: {}".format(error), file=sys.stderr)
        return 2
    entries = {"added": [], "removed": [], "changed": []}
    compare(old, new, "", entries)
    if args.json:
        print(json.dumps(entries, ensure_ascii=False, indent=2, sort_keys=True))
    elif not any(entries.values()):
        print("no differences")
    else:
        for kind in ("added", "removed", "changed"):
            for entry in entries[kind]:
                if kind == "added":
                    print("added {} = {}".format(entry["path"], format_value(entry["new"])))
                elif kind == "removed":
                    print("removed {} = {}".format(entry["path"], format_value(entry["old"])))
                else:
                    print("changed {}: {} -> {}".format(entry["path"], format_value(entry["old"]), format_value(entry["new"])))
    return 1 if any(entries.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
