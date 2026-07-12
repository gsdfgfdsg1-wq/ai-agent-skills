#!/usr/bin/env python3
"""Color format converter — HEX, RGB, HSL with validation and auto-detection."""

import argparse
import json
import re
import sys


# --- Conversion functions ---

def hex_to_rgb(hex_str):
    """Convert HEX string to RGB tuple."""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", hex_str):
        raise ValueError(f"Invalid HEX color: #{hex_str}. Expected format #RRGGBB with 6 hex digits.")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return (r, g, b)


def rgb_to_hex(r, g, b):
    """Convert RGB values to HEX string."""
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r, g, b):
    """Convert RGB values to HSL tuple."""
    r_n, g_n, b_n = r / 255.0, g / 255.0, b / 255.0
    c_max = max(r_n, g_n, b_n)
    c_min = min(r_n, g_n, b_n)
    delta = c_max - c_min

    # Lightness
    l = (c_max + c_min) / 2.0

    # Saturation
    if delta == 0:
        s = 0.0
        h = 0.0
    else:
        s = delta / (1.0 - abs(2.0 * l - 1.0)) if (1.0 - abs(2.0 * l - 1.0)) != 0 else 0.0

        # Hue
        if c_max == r_n:
            h = ((g_n - b_n) / delta) % 6.0
        elif c_max == g_n:
            h = ((b_n - r_n) / delta) + 2.0
        else:
            h = ((r_n - g_n) / delta) + 4.0

        h *= 60.0
        if h < 0:
            h += 360.0

    h = round(h)
    s = round(s * 100)
    l = round(l * 100)

    return (h, s, l)


def hsl_to_rgb(h, s, l):
    """Convert HSL values to RGB tuple."""
    s_n = s / 100.0
    l_n = l / 100.0

    c = (1.0 - abs(2.0 * l_n - 1.0)) * s_n
    x = c * (1.0 - abs((h / 60.0) % 2.0 - 1.0))
    m = l_n - c / 2.0

    if h < 60:
        r1, g1, b1 = c, x, 0
    elif h < 120:
        r1, g1, b1 = x, c, 0
    elif h < 180:
        r1, g1, b1 = 0, c, x
    elif h < 240:
        r1, g1, b1 = 0, x, c
    elif h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x

    r = round((r1 + m) * 255)
    g = round((g1 + m) * 255)
    b = round((b1 + m) * 255)

    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def hsl_to_hex(h, s, l):
    """Convert HSL values to HEX string."""
    r, g, b = hsl_to_rgb(h, s, l)
    return rgb_to_hex(r, g, b)


# --- Validation helpers ---

def validate_rgb(r, g, b):
    """Validate RGB values are in range 0-255."""
    names = ("Red", "Green", "Blue")
    values = (r, g, b)
    for name, val in zip(names, values):
        if val < 0 or val > 255:
            raise ValueError(f"{name} value {val} is out of range (0-255).")


def validate_hsl(h, s, l):
    """Validate HSL values are in proper ranges."""
    if h < 0 or h > 360:
        raise ValueError(f"Hue value {h} is out of range (0-360).")
    if s < 0 or s > 100:
        raise ValueError(f"Saturation value {s} is out of range (0-100).")
    if l < 0 or l > 100:
        raise ValueError(f"Lightness value {l} is out of range (0-100).")


# --- Format detection ---

def detect_format(value):
    """Auto-detect color format from a string value."""
    value = value.strip()

    # HEX: #RRGGBB or RRGGBB
    if re.fullmatch(r"#?[0-9a-fA-F]{6}", value):
        return "hex"

    # rgb(R, G, B) or rgb(R,G,B)
    m = re.fullmatch(r"rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)", value)
    if m:
        return "rgb"

    # hsl(H, S%, L%) or hsl(H,S%,L%)
    m = re.fullmatch(r"hsl\(\s*(\d{1,3})\s*,\s*(\d{1,3})%?\s*,\s*(\d{1,3})%?\s*\)", value)
    if m:
        return "hsl"

    raise ValueError(f"Cannot detect color format for: '{value}'. Supported formats: #RRGGBB, rgb(R,G,B), hsl(H,S%,L%)")


def parse_detected(value, fmt):
    """Parse a detected format string into components."""
    value = value.strip()

    if fmt == "hex":
        return {"hex": value if value.startswith("#") else f"#{value}"}

    if fmt == "rgb":
        m = re.fullmatch(r"rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)", value)
        return {"r": int(m.group(1)), "g": int(m.group(2)), "b": int(m.group(3))}

    if fmt == "hsl":
        m = re.fullmatch(r"hsl\(\s*(\d{1,3})\s*,\s*(\d{1,3})%?\s*,\s*(\d{1,3})%?\s*\)", value)
        return {"h": int(m.group(1)), "s": int(m.group(2)), "l": int(m.group(3))}

    raise ValueError(f"Unknown format: {fmt}")


# --- Output formatting ---

def format_rgb(r, g, b, as_json=False):
    if as_json:
        return json.dumps({"rgb": [r, g, b]})
    return f"RGB: {r}, {g}, {b}"


def format_hsl(h, s, l, as_json=False):
    if as_json:
        return json.dumps({"hsl": [h, s, l]})
    return f"HSL: {h}, {s}%, {l}%"


def format_hex(hex_val, as_json=False):
    if as_json:
        return json.dumps({"hex": hex_val})
    return f"HEX: {hex_val}"


# --- Subcommand handlers ---

def cmd_hex2rgb(args):
    r, g, b = hex_to_rgb(args.s)
    print(format_rgb(r, g, b, args.json))


def cmd_hex2hsl(args):
    r, g, b = hex_to_rgb(args.s)
    h, s, l = rgb_to_hsl(r, g, b)
    print(format_hsl(h, s, l, args.json))


def cmd_rgb2hex(args):
    validate_rgb(args.r, args.g, args.b)
    print(format_hex(rgb_to_hex(args.r, args.g, args.b), args.json))


def cmd_rgb2hsl(args):
    validate_rgb(args.r, args.g, args.b)
    h, s, l = rgb_to_hsl(args.r, args.g, args.b)
    print(format_hsl(h, s, l, args.json))


def cmd_hsl2hex(args):
    validate_hsl(args.h, args.s, args.l)
    print(format_hex(hsl_to_hex(args.h, args.s, args.l), args.json))


def cmd_hsl2rgb(args):
    validate_hsl(args.h, args.s, args.l)
    r, g, b = hsl_to_rgb(args.h, args.s, args.l)
    print(format_rgb(r, g, b, args.json))


def cmd_convert(args):
    fmt = detect_format(args.s)
    parsed = parse_detected(args.s, fmt)

    result = {}

    if fmt == "hex":
        r, g, b = hex_to_rgb(parsed["hex"])
        h, s, l = rgb_to_hsl(r, g, b)
        result = {"hex": parsed["hex"], "rgb": [r, g, b], "hsl": [h, s, l]}
    elif fmt == "rgb":
        r, g, b = parsed["r"], parsed["g"], parsed["b"]
        validate_rgb(r, g, b)
        h, s, l = rgb_to_hsl(r, g, b)
        result = {"hex": rgb_to_hex(r, g, b), "rgb": [r, g, b], "hsl": [h, s, l]}
    elif fmt == "hsl":
        h, s, l = parsed["h"], parsed["s"], parsed["l"]
        validate_hsl(h, s, l)
        r, g, b = hsl_to_rgb(h, s, l)
        result = {"hex": rgb_to_hex(r, g, b), "rgb": [r, g, b], "hsl": [h, s, l]}

    if args.json:
        result["detected_format"] = fmt
        print(json.dumps(result))
    else:
        print(f"Detected format: {fmt.upper()}")
        if fmt != "hex":
            print(f"HEX: {result['hex']}")
        if fmt != "rgb":
            print(f"RGB: {result['rgb'][0]}, {result['rgb'][1]}, {result['rgb'][2]}")
        if fmt != "hsl":
            print(f"HSL: {result['hsl'][0]}, {result['hsl'][1]}%, {result['hsl'][2]}%")


# --- Argument parser ---

def build_parser():
    parser = argparse.ArgumentParser(
        prog="color_converter",
        description="Convert between HEX, RGB, and HSL color formats.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Conversion subcommand")

    # hex2rgb
    p = subparsers.add_parser("hex2rgb", help="Convert HEX to RGB")
    p.add_argument("-s", required=True, help="HEX color string (e.g. #FF5733)")
    p.add_argument("--json", action="store_true", help="Output in JSON format")
    p.set_defaults(func=cmd_hex2rgb)

    # hex2hsl
    p = subparsers.add_parser("hex2hsl", help="Convert HEX to HSL")
    p.add_argument("-s", required=True, help="HEX color string (e.g. #FF5733)")
    p.add_argument("--json", action="store_true", help="Output in JSON format")
    p.set_defaults(func=cmd_hex2hsl)

    # rgb2hex
    p = subparsers.add_parser("rgb2hex", help="Convert RGB to HEX")
    p.add_argument("-r", type=int, required=True, help="Red channel (0-255)")
    p.add_argument("-g", type=int, required=True, help="Green channel (0-255)")
    p.add_argument("-b", type=int, required=True, help="Blue channel (0-255)")
    p.add_argument("--json", action="store_true", help="Output in JSON format")
    p.set_defaults(func=cmd_rgb2hex)

    # rgb2hsl
    p = subparsers.add_parser("rgb2hsl", help="Convert RGB to HSL")
    p.add_argument("-r", type=int, required=True, help="Red channel (0-255)")
    p.add_argument("-g", type=int, required=True, help="Green channel (0-255)")
    p.add_argument("-b", type=int, required=True, help="Blue channel (0-255)")
    p.add_argument("--json", action="store_true", help="Output in JSON format")
    p.set_defaults(func=cmd_rgb2hsl)

    # hsl2hex
    p = subparsers.add_parser("hsl2hex", help="Convert HSL to HEX", add_help=False)
    p.add_argument("--help", action="help", default=argparse.SUPPRESS, help="Show this help message")
    p.add_argument("-h", type=int, required=True, help="Hue (0-360)")
    p.add_argument("-s", type=int, required=True, help="Saturation (0-100)")
    p.add_argument("-l", type=int, required=True, help="Lightness (0-100)")
    p.add_argument("--json", action="store_true", help="Output in JSON format")
    p.set_defaults(func=cmd_hsl2hex)

    # hsl2rgb
    p = subparsers.add_parser("hsl2rgb", help="Convert HSL to RGB", add_help=False)
    p.add_argument("--help", action="help", default=argparse.SUPPRESS, help="Show this help message")
    p.add_argument("-h", type=int, required=True, help="Hue (0-360)")
    p.add_argument("-s", type=int, required=True, help="Saturation (0-100)")
    p.add_argument("-l", type=int, required=True, help="Lightness (0-100)")
    p.add_argument("--json", action="store_true", help="Output in JSON format")
    p.set_defaults(func=cmd_hsl2rgb)

    # convert (auto-detect)
    p = subparsers.add_parser("convert", help="Auto-detect format and convert to all others")
    p.add_argument("-s", required=True, help="Color value (e.g. #FF5733, rgb(255,87,51), hsl(11,100%,60%))")
    p.add_argument("--json", action="store_true", help="Output in JSON format")
    p.set_defaults(func=cmd_convert)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
