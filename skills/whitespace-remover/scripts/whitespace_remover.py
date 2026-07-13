#!/usr/bin/env python3
"""Remove trailing whitespace and collapse trailing blank lines in text files."""

import argparse
import sys
from pathlib import Path


def normalize_text(text):
    """Strip trailing spaces/tabs from every line and keep at most one final newline."""
    lines = text.splitlines()
    cleaned_lines = [line.rstrip(" \t") for line in lines]
    while cleaned_lines and not cleaned_lines[-1]:
        cleaned_lines.pop()
    return "\n".join(cleaned_lines) + ("\n" if cleaned_lines else "")


def read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError(f"cannot read '{path}': {error}") from error


def write_text(path, content):
    try:
        Path(path).write_text(content, encoding="utf-8")
    except OSError as error:
        raise ValueError(f"cannot write '{path}': {error}") from error


def main():
    parser = argparse.ArgumentParser(
        description="Remove trailing whitespace and collapse trailing blank lines."
    )
    parser.add_argument("input", help="Text file to normalize")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--in-place", action="store_true", help="Rewrite the input file")
    destination.add_argument("--output", help="Write normalized content to this path")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Exit 1 when normalization is needed")
    mode.add_argument("--dry-run", action="store_true", help="Print normalized content without writing")
    args = parser.parse_args()

    if args.output and (args.check or args.dry_run):
        parser.error("--output cannot be combined with --check or --dry-run")
    if args.in_place and (args.check or args.dry_run):
        parser.error("--in-place cannot be combined with --check or --dry-run")

    try:
        original = read_text(args.input)
        normalized = normalize_text(original)
        changed = original != normalized

        if args.check:
            if changed:
                print(f"needs normalization: {args.input}", file=sys.stderr)
                return 1
            print(f"already normalized: {args.input}")
            return 0

        if args.dry_run:
            sys.stdout.write(normalized)
            return 0

        if args.in_place:
            if changed:
                write_text(args.input, normalized)
            print(f"{'normalized' if changed else 'already normalized'}: {args.input}")
            return 0

        if args.output:
            write_text(args.output, normalized)
            print(f"wrote normalized content: {args.output}")
            return 0

        sys.stdout.write(normalized)
        return 0
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
