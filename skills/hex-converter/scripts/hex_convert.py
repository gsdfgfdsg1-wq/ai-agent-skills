#!/usr/bin/env python3
"""Convert numbers between hex, binary, decimal, and octal without external dependencies."""

import argparse
import json
import re
import sys


def detect_base(value_str):
    """Auto-detect the base of a number string."""
    s = value_str.strip().lower()
    if s.startswith("0x"):
        return 16
    if s.startswith("0o"):
        return 8
    if s.startswith("0b"):
        return 2
    # Try decimal
    try:
        int(s, 10)
        return 10
    except ValueError:
        return None


def parse_value(value_str, base=None):
    """Parse a value string to an integer."""
    s = value_str.strip()
    if base is None:
        base = detect_base(s)
    if base is None:
        print(f"Error: cannot determine base for '{value_str}'", file=sys.stderr)
        sys.exit(1)
    try:
        return int(s, base)
    except ValueError:
        print(f"Error: invalid number '{value_str}' for base {base}", file=sys.stderr)
        sys.exit(1)


def format_all_bases(value):
    """Format a value in all four bases."""
    return {
        "decimal": str(value),
        "hexadecimal": hex(value),
        "octal": oct(value),
        "binary": bin(value),
    }


def cmd_convert(args):
    value = parse_value(args.value, args.base)
    result = format_all_bases(value)

    if args.json:
        result["input"] = args.value
        print(json.dumps(result, indent=2))
    else:
        print(f"Input:  {args.value}")
        print(f"  Dec: {result['decimal']}")
        print(f"  Hex: {result['hexadecimal']}")
        print(f"  Oct: {result['octal']}")
        print(f"  Bin: {result['binary']}")


def cmd_bits(args):
    value = parse_value(args.value, args.base)
    if value < 0:
        print("Error: bits display only supports non-negative values", file=sys.stderr)
        sys.exit(1)

    # Determine bit width
    if args.width:
        width = args.width
    else:
        width = max(value.bit_length(), 8)
        # Round up to multiple of 8
        width = ((width + 7) // 8) * 8

    binary = format(value, f'0{width}b')
    # Group by 4 bits
    groups = [binary[i:i+4] for i in range(0, len(binary), 4)]
    grouped = ' '.join(groups)

    if args.json:
        print(json.dumps({"value": value, "binary": binary, "grouped": grouped, "width": width}, indent=2))
    else:
        print(f"Value:  {value} ({hex(value)})")
        print(f"Binary: {grouped}")
        print(f"Width:  {width} bits")


def cmd_mask(args):
    a = parse_value(args.value_a, args.base_a)
    b = parse_value(args.value_b, args.base_b)

    op = args.op.lower()
    if op == "and":
        result = a & b
    elif op == "or":
        result = a | b
    elif op == "xor":
        result = a ^ b
    elif op == "not":
        # NOT on a only
        result = ~a
    elif op == "lshift":
        result = a << b
    elif op == "rshift":
        result = a >> b
    else:
        print(f"Error: unknown operation '{op}'", file=sys.stderr)
        sys.exit(1)

    all_a = format_all_bases(a)
    all_b = format_all_bases(b)
    all_r = format_all_bases(result)

    if args.json:
        print(json.dumps({"a": a, "b": b, "op": op, "result": result, "a_formats": all_a, "b_formats": all_b, "result_formats": all_r}, indent=2))
    else:
        print(f"A: {all_a['decimal']} ({all_a['hexadecimal']})")
        print(f"B: {all_b['decimal']} ({all_b['hexadecimal']})")
        print(f"Op: {op.upper()}")
        print(f"Result: {all_r['decimal']} ({all_r['hexadecimal']})")
        print(f"  Bin: {all_r['binary']}")


def main():
    parser = argparse.ArgumentParser(description="Convert numbers between hex, binary, decimal, and octal.")
    sub = parser.add_subparsers(dest="command")

    p_conv = sub.add_parser("convert", help="Convert a number to all bases")
    p_conv.add_argument("--value", required=True, help="Number to convert (0x/0b/0o prefix auto-detected)")
    p_conv.add_argument("--base", type=int, choices=[2, 8, 10, 16], help="Input base (auto-detect if omitted)")
    p_conv.add_argument("--json", action="store_true", help="JSON output")

    p_bits = sub.add_parser("bits", help="Show binary bit layout")
    p_bits.add_argument("--value", required=True, help="Number to display")
    p_bits.add_argument("--base", type=int, choices=[2, 8, 10, 16], help="Input base")
    p_bits.add_argument("--width", type=int, help="Bit width (default: auto, multiple of 8)")
    p_bits.add_argument("--json", action="store_true", help="JSON output")

    p_mask = sub.add_parser("mask", help="Bitwise operation on two values")
    p_mask.add_argument("--value-a", required=True, help="First value")
    p_mask.add_argument("--value-b", required=True, help="Second value")
    p_mask.add_argument("--base-a", type=int, choices=[2, 8, 10, 16], help="Base of value-a")
    p_mask.add_argument("--base-b", type=int, choices=[2, 8, 10, 16], help="Base of value-b")
    p_mask.add_argument("--op", required=True, choices=["and", "or", "xor", "not", "lshift", "rshift"], help="Bitwise operation")
    p_mask.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "convert":
        cmd_convert(args)
    elif args.command == "bits":
        cmd_bits(args)
    elif args.command == "mask":
        cmd_mask(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
