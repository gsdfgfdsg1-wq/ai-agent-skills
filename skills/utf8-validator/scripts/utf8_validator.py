#!/usr/bin/env python3
"""Validate files for correct UTF-8 encoding and report byte-level errors."""

import argparse
import json
import sys
from pathlib import Path


def validate_utf8(filepath, check_bom=False):
    """Validate a file for UTF-8 correctness. Returns list of errors."""
    try:
        raw = Path(filepath).read_bytes()
    except (OSError, IOError) as e:
        return [{"error": "cannot_read", "message": str(e)}]

    errors = []

    # Check BOM
    if check_bom:
        has_bom = raw[:3] == b"\xef\xbb\xbf"
        if has_bom:
            errors.append({
                "offset": 0,
                "type": "bom",
                "message": "UTF-8 BOM (EF BB BF) detected — usually unnecessary",
            })

    # Validate UTF-8 by trying to decode
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as e:
        errors.append({
            "offset": e.start,
            "type": "invalid_byte",
            "message": f"invalid UTF-8 byte at offset {e.start}: {raw[e.start:e.end].hex(' ')} — {str(e)}",
        })

        # Find all errors by decoding with replacement
        all_errors = []
        pos = 0
        while pos < len(raw):
            try:
                chunk = raw[pos:pos + 8192]
                chunk.decode("utf-8")
                pos += 8192
            except UnicodeDecodeError as ue:
                all_errors.append({
                    "offset": pos + ue.start,
                    "type": "invalid_byte",
                    "message": f"invalid UTF-8 at offset {pos + ue.start}: {raw[pos + ue.start:pos + ue.end].hex(' ')}",
                })
                pos += ue.end

        if len(all_errors) > 1 or (all_errors and all_errors[0] != errors[-1] if errors else True):
            errors = [e for e in errors if e.get("type") == "bom"] + all_errors

    return errors


def cmd_validate(args):
    errors = validate_utf8(args.file, check_bom=args.bom)

    if args.json:
        result = {
            "file": str(args.file),
            "valid": len([e for e in errors if e.get("type") != "bom"]) == 0,
            "errors": errors,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if not errors:
            print(f"✓ {args.file} is valid UTF-8")
        else:
            print(f"Issues in {args.file}:")
            for error in errors:
                offset = error.get("offset", "?")
                print(f"  ✗ offset {offset}: {error['message']}")

    non_bom_errors = [e for e in errors if e.get("type") != "bom"]
    if non_bom_errors:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Validate files for UTF-8 encoding.")
    sub = parser.add_subparsers(dest="command")

    p_validate = sub.add_parser("validate", help="Validate a file for UTF-8")
    p_validate.add_argument("--file", required=True, help="File to validate")
    p_validate.add_argument("--bom", action="store_true", help="Check for UTF-8 BOM")
    p_validate.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "validate":
        cmd_validate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
