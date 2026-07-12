#!/usr/bin/env python3
"""Simplified JSONPath query engine — no external dependencies.

Supports:
    $           — root
    .key        — object key access
    [n]         — array index
    [*]         — iterate all array elements
    .key1.key2  — nested access
    ..key       — recursive descent

Subcommands:
    query   — query a JSON file
    extract — query a JSONL file (apply path to each line)
"""

import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(
    r"""
    \$                  # root
    | \.\.[A-Za-z_]\w*  # recursive descent  ..key
    | \.[A-Za-z_]\w*    # dot-access         .key
    | \[\*\]            # wildcard index     [*]
    | \[\d+\]           # numeric index      [0]
    """,
    re.VERBOSE,
)


def tokenize(path: str):
    """Return a list of tokens from a JSONPath expression.

    Raises SystemExit(2) on invalid path expressions.
    """
    if not path.startswith("$"):
        print(f"Error: path expression must start with '$': {path}", file=sys.stderr)
        sys.exit(2)

    tokens = []
    pos = 0
    while pos < len(path):
        m = _TOKEN_RE.match(path, pos)
        if m is None:
            print(
                f"Error: invalid path expression at position {pos}: {path!r}",
                file=sys.stderr,
            )
            sys.exit(2)
        tokens.append(m.group(0))
        pos = m.end()

    # Validate token ordering — root must be first
    if not tokens or tokens[0] != "$":
        print("Error: path expression must start with '$'", file=sys.stderr)
        sys.exit(2)

    return tokens


# ---------------------------------------------------------------------------
# Recursive descent helper
# ---------------------------------------------------------------------------

def _recursive_descent(obj, key):
    """Yield all values associated with *key* at any nesting depth."""
    if isinstance(obj, dict):
        if key in obj:
            yield obj[key]
        for v in obj.values():
            yield from _recursive_descent(v, key)
    elif isinstance(obj, list):
        for item in obj:
            yield from _recursive_descent(item, key)


# ---------------------------------------------------------------------------
# Query engine
# ---------------------------------------------------------------------------

def _resolve(tokens, obj):
    """Resolve a list of tokens against *obj*, yielding matched values."""
    current = [obj]  # list of candidate values

    for tok in tokens:
        if tok == "$":
            continue

        # Recursive descent  ..key
        if tok.startswith(".."):
            key = tok[2:]
            next_values = []
            for c in current:
                next_values.extend(_recursive_descent(c, key))
            current = next_values
            continue

        # Wildcard array  [*]
        if tok == "[*]":
            next_values = []
            for c in current:
                if isinstance(c, list):
                    next_values.extend(c)
                elif isinstance(c, dict):
                    next_values.extend(c.values())
            current = next_values
            continue

        # Numeric index  [n]
        if tok.startswith("[") and tok.endswith("]") and tok[1:-1].isdigit():
            idx = int(tok[1:-1])
            next_values = []
            for c in current:
                if isinstance(c, list):
                    if idx < len(c):
                        next_values.append(c[idx])
                    else:
                        print(
                            f"Error: index {idx} out of range (length {len(c)})",
                            file=sys.stderr,
                        )
                        sys.exit(4)
                else:
                    print(
                        f"Error: cannot index non-array with [{idx}]",
                        file=sys.stderr,
                    )
                    sys.exit(4)
            current = next_values
            continue

        # Dot-access  .key
        if tok.startswith("."):
            key = tok[1:]
            next_values = []
            for c in current:
                if isinstance(c, dict):
                    if key in c:
                        next_values.append(c[key])
                    else:
                        print(
                            f"Error: key {key!r} not found in object",
                            file=sys.stderr,
                        )
                        sys.exit(4)
                else:
                    print(
                        f"Error: cannot access key {key!r} on non-object ({type(c).__name__})",
                        file=sys.stderr,
                    )
                    sys.exit(4)
            current = next_values
            continue

    return current


def query(obj, path: str):
    """Apply a JSONPath expression to a parsed JSON object."""
    tokens = tokenize(path)
    return _resolve(tokens, obj)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def _format_value(v):
    """Format a single value for plain-text output."""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    return str(v)


def output(results, as_json=False):
    """Print results to stdout."""
    if as_json:
        print(json.dumps(results, ensure_ascii=False))
    else:
        for v in results:
            print(_format_value(v))


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_query(args):
    """Query a single JSON file."""
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            obj = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: malformed JSON in {args.file}: {exc}", file=sys.stderr)
        sys.exit(3)

    results = query(obj, args.path)
    output(results, as_json=args.json)


def cmd_extract(args):
    """Apply a path expression to each line of a JSONL file."""
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    all_results = []
    for lineno, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            print(
                f"Error: malformed JSON at line {lineno} in {args.file}: {exc}",
                file=sys.stderr,
            )
            sys.exit(3)
        results = query(obj, args.path)
        all_results.extend(results)

    output(all_results, as_json=args.json)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="json_path_query",
        description="Query JSON and JSONL files with JSONPath-like expressions.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # --- query ---
    q = subparsers.add_parser("query", help="Query a JSON file")
    q.add_argument("--file", required=True, help="Path to JSON file")
    q.add_argument("-p", "--path", required=True, help="JSONPath expression")
    q.add_argument(
        "--json", action="store_true", help="Output results as JSON array"
    )
    q.set_defaults(func=cmd_query)

    # --- extract ---
    e = subparsers.add_parser("extract", help="Query a JSONL file (apply path to each line)")
    e.add_argument("--file", required=True, help="Path to JSONL file")
    e.add_argument("-p", "--path", required=True, help="JSONPath expression")
    e.add_argument(
        "--json", action="store_true", help="Output results as JSON array"
    )
    e.set_defaults(func=cmd_extract)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
