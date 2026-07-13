#!/usr/bin/env python3
"""Look up ASCII values and print ASCII ranges."""

import argparse
import json
import sys
from typing import Any


CONTROL_NAMES = {
    0: "NUL", 1: "SOH", 2: "STX", 3: "ETX", 4: "EOT", 5: "ENQ", 6: "ACK",
    7: "BEL", 8: "BS", 9: "TAB", 10: "LF", 11: "VT", 12: "FF", 13: "CR",
    14: "SO", 15: "SI", 16: "DLE", 17: "DC1", 18: "DC2", 19: "DC3", 20: "DC4",
    21: "NAK", 22: "SYN", 23: "ETB", 24: "CAN", 25: "EM", 26: "SUB", 27: "ESC",
    28: "FS", 29: "GS", 30: "RS", 31: "US", 127: "DEL",
}


def ascii_entry(value: int) -> dict[str, Any]:
    """Return a serializable representation of a 7-bit ASCII value."""
    if not 0 <= value <= 127:
        raise ValueError("ASCII value must be between 0 and 127")

    if value in CONTROL_NAMES:
        character = None
        display = CONTROL_NAMES[value]
        category = "control"
    elif value == 32:
        character = " "
        display = "SPACE"
        category = "printable"
    else:
        character = chr(value)
        display = character
        category = "printable"

    return {
        "decimal": value,
        "hexadecimal": f"0x{value:02X}",
        "binary": f"0b{value:07b}",
        "character": character,
        "display": display,
        "category": category,
    }


def parse_decimal(value: str) -> int:
    try:
        return int(value, 10)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid decimal ASCII value: {value}") from exc


def parse_hexadecimal(value: str) -> int:
    normalized = value[2:] if value.lower().startswith("0x") else value
    try:
        return int(normalized, 16)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid hexadecimal ASCII value: {value}") from exc


def parse_character(value: str) -> int:
    if len(value) != 1:
        raise argparse.ArgumentTypeError("character input must contain exactly one character")
    codepoint = ord(value)
    if codepoint > 127:
        raise argparse.ArgumentTypeError("character input must be a 7-bit ASCII character")
    return codepoint


def output(entries: list[dict[str, Any]], as_json: bool) -> None:
    if as_json:
        print(json.dumps(entries[0] if len(entries) == 1 else entries, indent=2))
        return

    print(f"{'Dec':>3}  {'Hex':<4}  {'Binary':<9}  {'Character':<9}  Category")
    print("---  ----  ---------  ---------  --------")
    for entry in entries:
        print(
            f"{entry['decimal']:>3}  {entry['hexadecimal']:<4}  "
            f"{entry['binary']:<9}  {entry['display']:<9}  {entry['category']}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Look up ASCII values or print an ASCII range.")
    commands = parser.add_subparsers(dest="command", required=True)

    lookup = commands.add_parser("lookup", help="look up one ASCII value")
    input_group = lookup.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--decimal", type=parse_decimal, help="decimal ASCII value (0-127)")
    input_group.add_argument("--hex", dest="hexadecimal", type=parse_hexadecimal, help="hexadecimal ASCII value")
    input_group.add_argument("--char", type=parse_character, help="single ASCII character")
    lookup.add_argument("--json", action="store_true", help="print JSON output")

    range_parser = commands.add_parser("range", help="print an inclusive ASCII range")
    range_parser.add_argument("start", type=parse_decimal, help="start decimal ASCII value (0-127)")
    range_parser.add_argument("end", type=parse_decimal, help="end decimal ASCII value (0-127)")
    range_parser.add_argument("--json", action="store_true", help="print JSON output")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "lookup":
            value = args.decimal
            if value is None:
                value = args.hexadecimal
            if value is None:
                value = args.char
            entries = [ascii_entry(value)]
        else:
            if args.start > args.end:
                raise ValueError("range start must not exceed range end")
            entries = [ascii_entry(value) for value in range(args.start, args.end + 1)]
        output(entries, args.json)
        return 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
