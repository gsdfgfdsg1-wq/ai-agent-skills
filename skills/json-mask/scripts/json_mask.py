#!/usr/bin/env python3
"""Mask sensitive fields in JSON by key name patterns without external dependencies."""

import argparse
import hashlib
import json
import re
import sys


def mask_value(value, strategy, replacement="***"):
    """Apply a masking strategy to a value."""
    if value is None:
        return None

    if strategy == "replace":
        return replacement
    elif strategy == "remove":
        return None  # Signal to remove the key
    elif strategy == "partial":
        s = str(value)
        if len(s) <= 2:
            return replacement
        half = max(1, len(s) // 4)
        return s[:half] + replacement + s[-half:]
    elif strategy == "hash":
        h = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
        return f"[masked:{h[:8]}]"
    else:
        return replacement


def mask_recursive(obj, key_matcher, strategy, replacement, dot_paths=None):
    """Recursively mask matching keys in a JSON object."""
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            # Check dot-path match
            if dot_paths and key in dot_paths:
                if strategy == "remove":
                    continue
                result[key] = mask_value(value, strategy, replacement)
            elif key_matcher(key):
                if strategy == "remove":
                    continue
                result[key] = mask_value(value, strategy, replacement)
            else:
                result[key] = mask_recursive(value, key_matcher, strategy, replacement, dot_paths)
        return result
    elif isinstance(obj, list):
        return [mask_recursive(item, key_matcher, strategy, replacement, dot_paths) for item in obj]
    else:
        return obj


def build_key_matcher(keys, regex_keys, prefix_keys, suffix_keys):
    """Build a function that checks if a key should be masked."""
    matchers = []

    if keys:
        key_set = set(keys)
        matchers.append(lambda k: k in key_set)

    if regex_keys:
        compiled = [re.compile(p) for p in regex_keys]
        matchers.append(lambda k: any(r.search(k) for r in compiled))

    if prefix_keys:
        matchers.append(lambda k: any(k.startswith(p) for p in prefix_keys))

    if suffix_keys:
        matchers.append(lambda k: any(k.endswith(s) for s in suffix_keys))

    if not matchers:
        return lambda k: False

    return lambda k: any(m(k) for m in matchers)


def cmd_mask(args):
    # Read input
    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error: cannot read {args.file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON on stdin: {e}", file=sys.stderr)
            sys.exit(1)

    key_matcher = build_key_matcher(args.keys, args.regex_keys, args.prefix_keys, args.suffix_keys)
    dot_paths = set(args.dot_paths) if args.dot_paths else None

    result = mask_recursive(data, key_matcher, args.strategy, args.replacement, dot_paths)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"Error: cannot write {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.json:
        # Output metadata about the masking operation
        meta = {
            "strategy": args.strategy,
            "keys": args.keys or [],
            "regex_keys": args.regex_keys or [],
            "masked_fields": len(args.keys or []) + len(args.regex_keys or []),
        }
        print(f"\n--- Masking metadata ---", file=sys.stderr)
        print(json.dumps(meta, indent=2), file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Mask sensitive fields in JSON.")
    sub = parser.add_subparsers(dest="command")

    p_mask = sub.add_parser("mask", help="Mask sensitive fields in JSON")
    p_mask.add_argument("--file", help="JSON file (reads stdin if omitted)")
    p_mask.add_argument("--keys", nargs="+", help="Exact key names to mask")
    p_mask.add_argument("--regex-keys", nargs="+", help="Regex patterns for key names")
    p_mask.add_argument("--prefix-keys", nargs="+", help="Key name prefixes to mask")
    p_mask.add_argument("--suffix-keys", nargs="+", help="Key name suffixes to mask")
    p_mask.add_argument("--dot-paths", nargs="+", help="Dot-notation paths (e.g. user.password)")
    p_mask.add_argument("--strategy", default="replace", choices=["replace", "partial", "hash", "remove"], help="Masking strategy (default: replace)")
    p_mask.add_argument("--replacement", default="***", help="Replacement string for replace strategy (default: ***)")
    p_mask.add_argument("--output", help="Output file (default: stdout)")
    p_mask.add_argument("--json", action="store_true", help="Show masking metadata")

    args = parser.parse_args()
    if args.command == "mask":
        cmd_mask(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
