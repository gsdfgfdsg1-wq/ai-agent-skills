#!/usr/bin/env python3
"""json-flattener: Flatten nested JSON to dot-notation pairs and unflatten back.

No external dependencies — stdlib only (json, argparse, sys, re).
"""

import argparse
import json
import re
import sys


# ---------------------------------------------------------------------------
# Flatten
# ---------------------------------------------------------------------------

def flatten(obj, parent_key="", sep="."):
    """Recursively flatten a nested dict/list into {dot.key: value} pairs."""
    items = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.update(flatten(v, new_key, sep))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_key = f"{parent_key}[{i}]"
            items.update(flatten(v, new_key, sep))
    else:
        items[parent_key] = obj
    return items


# ---------------------------------------------------------------------------
# Unflatten
# ---------------------------------------------------------------------------

def unflatten(flat_dict, sep="."):
    """Reconstruct a nested dict/list from flat dot-notation keys."""
    result = {}
    for compound_key, value in flat_dict.items():
        parts = _split_key(compound_key, sep)
        _set_nested(result, parts, value)
    return _convert_lists(result)


def _split_key(compound_key, sep):
    """Split a compound key on the separator, keeping array indices attached.

    Example with sep='.': 'a.b[2].c' -> ['a', 'b[2]', 'c']
    """
    # Split on separator but not inside brackets
    raw_parts = compound_key.split(sep)
    parts = []
    for part in raw_parts:
        if not part:
            raise ValueError(f"Empty key segment in '{compound_key}'")
        parts.append(part)
    return parts


def _set_nested(target, parts, value):
    """Set a value at a nested path, creating intermediate dicts."""
    current = target
    for i, part in enumerate(parts):
        is_last = i == len(parts) - 1
        base, index = _parse_part(part)

        # Root-level array element: base is "" — use index as key in current dict
        if base == "" and index is not None:
            idx_key = str(index)
            if is_last:
                current[idx_key] = value
            else:
                if idx_key not in current:
                    current[idx_key] = {}
                next_current = current[idx_key]
                if not isinstance(next_current, dict):
                    raise ValueError(
                        f"Key conflict: '[{index}]' is already a leaf but also used as container"
                    )
                current = next_current
            continue

        if is_last:
            if index is not None:
                # Array element at leaf
                if base not in current:
                    current[base] = {}
                bucket = current[base]
                if not isinstance(bucket, dict):
                    raise ValueError(
                        f"Key conflict: '{base}' is already a leaf but also used as array container"
                    )
                bucket[str(index)] = value
            else:
                if base in current and isinstance(current[base], dict):
                    raise ValueError(
                        f"Key conflict: '{base}' is already a container but also used as a leaf"
                    )
                current[base] = value
        else:
            if index is not None:
                # Intermediate array element — a.b[2].c
                if base not in current:
                    current[base] = {}
                bucket = current[base]
                if not isinstance(bucket, dict):
                    raise ValueError(
                        f"Key conflict: '{base}' is already a leaf but also used as array container"
                    )
                idx_key = str(index)
                if idx_key not in bucket:
                    bucket[idx_key] = {}
                next_current = bucket[idx_key]
                if not isinstance(next_current, dict):
                    raise ValueError(
                        f"Key conflict: '{base}[{index}]' is already a leaf but also used as container"
                    )
                current = next_current
            else:
                if base not in current:
                    current[base] = {}
                if not isinstance(current[base], dict):
                    raise ValueError(
                        f"Key conflict: '{base}' is already a leaf but also used as container"
                    )
                current = current[base]


_ARRAY_INDEX_RE = re.compile(r"^(.+)\[(\d+)\]$")
_ROOT_ARRAY_RE = re.compile(r"^\[(\d+)\]$")


def _parse_part(part):
    """Parse 'key[3]' into ('key', 3), '[3]' into ('', 3), or 'key' into ('key', None)."""
    m = _ARRAY_INDEX_RE.match(part)
    if m:
        return m.group(1), int(m.group(2))
    m = _ROOT_ARRAY_RE.match(part)
    if m:
        return "", int(m.group(1))
    return part, None


def _convert_lists(obj):
    """Post-process: convert dicts whose keys are all consecutive integers into lists."""
    if not isinstance(obj, dict):
        return obj
    # First recurse
    for k in list(obj.keys()):
        obj[k] = _convert_lists(obj[k])
    # Then check if this dict should be a list
    if not obj:
        return obj
    keys = list(obj.keys())
    if all(k.isdigit() for k in keys):
        indices = [int(k) for k in keys]
        if indices == list(range(max(indices) + 1)):
            return [obj[str(i)] for i in range(max(indices) + 1)]
    return obj


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def read_input(args):
    """Read and parse JSON input from --file or -s."""
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            _error(f"File not found: {args.file}")
        except OSError as e:
            _error(f"Cannot read file {args.file}: {e}")
    elif args.string is not None:
        text = args.string
    else:
        _error("Either --file or -s must be provided")

    text = text.strip()
    if not text:
        _error("Input is empty")
    return text


def parse_flat_pairs(text, sep):
    """Parse key=value lines or flat JSON into an ordered dict."""
    text = text.strip()
    # Try JSON first
    if text.startswith("{"):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    # Fall back to key=value lines
    result = {}
    for line_no, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        sep_pos = line.find("=")
        if sep_pos == -1:
            _error(f"Line {line_no}: missing '=' separator in '{line}'")
        key = line[:sep_pos].strip()
        val = line[sep_pos + 1:].strip()
        # Attempt to parse the value as JSON (for numbers, bools, null)
        try:
            val = json.loads(val)
        except (json.JSONDecodeError, ValueError):
            pass  # keep as string
        result[key] = val
    if not result:
        _error("No key=value pairs found in input")
    return result


def parse_json_input(text):
    """Parse text as JSON, exiting on failure."""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        _error(f"Invalid JSON: {e}")


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def format_output(data, as_json=False):
    """Format flat dict for output."""
    if as_json:
        return json.dumps(data, indent=2, ensure_ascii=False)
    lines = []
    for k, v in data.items():
        if isinstance(v, str):
            lines.append(f"{k}={v}")
        else:
            lines.append(f"{k}={json.dumps(v, ensure_ascii=False)}")
    return "\n".join(lines)


def _error(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="json_flattener",
        description="Flatten nested JSON to dot-notation pairs and unflatten back.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--file", "-f", help="Read input from a JSON file")
    parent.add_argument("-s", "--string", help="Provide input as a string")
    parent.add_argument(
        "--separator", default=".", help="Key separator (default: '.')"
    )
    parent.add_argument(
        "--json", action="store_true", help="Output as JSON instead of key=value"
    )

    subparsers.add_parser(
        "flatten", parents=[parent], help="Flatten nested JSON to flat key=value pairs"
    )
    subparsers.add_parser(
        "unflatten", parents=[parent], help="Unflatten key=value pairs to nested JSON"
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        text = read_input(args)
    except SystemExit:
        raise

    sep = args.separator

    if args.command == "flatten":
        data = parse_json_input(text)
        if not isinstance(data, (dict, list)):
            _error("Flatten input must be a JSON object or array")
        flat = flatten(data, sep=sep)
        print(format_output(flat, as_json=args.json))

    elif args.command == "unflatten":
        flat = parse_flat_pairs(text, sep)
        try:
            nested = unflatten(flat, sep=sep)
        except ValueError as e:
            _error(str(e))
        print(json.dumps(nested, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
