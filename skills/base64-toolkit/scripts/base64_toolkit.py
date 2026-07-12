#!/usr/bin/env python3
"""base64-toolkit — encode, decode, and detect Base64 strings.

Usage:
    python base64_toolkit.py encode -s TEXT [--urlsafe] [--json]
    python base64_toolkit.py decode -s B64 [--urlsafe] [--json]
    python base64_toolkit.py detect -s B64 [--json]
    python base64_toolkit.py encode --file PATH [--urlsafe] [--json]
    python base64_toolkit.py decode --file PATH [--urlsafe] [--json]

Supports standard and URL-safe Base64, auto-detection, and file input.
"""

import argparse
import base64
import json
import re
import sys


B64_PATTERN = re.compile(r'^[A-Za-z0-9+/\-_]+=*$')


def _is_valid_b64(s, urlsafe=False):
    """Check if a string is valid Base64."""
    s = s.strip()
    if not s:
        return False
    # URL-safe: replace - with + and _ with /
    if urlsafe or '-' in s or '_' in s:
        s = s.replace('-', '+').replace('_', '/')
    if not B64_PATTERN.match(s):
        return False
    if len(s) % 4 != 0:
        # Try padding
        s += '=' * (4 - len(s) % 4)
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False


def _detect_type(s):
    """Detect Base64 type: standard, urlsafe, or not valid."""
    s = s.strip()
    if _is_valid_b64(s, urlsafe=False):
        if '-' in s or '_' in s:
            return "urlsafe"
        return "standard"
    if _is_valid_b64(s, urlsafe=True):
        return "urlsafe"
    return "invalid"


def cmd_encode(args):
    """Encode a string or file to Base64."""
    if args.file:
        try:
            with open(args.file, "rb") as f:
                data = f.read()
        except FileNotFoundError:
            return {"error": f"File not found: {args.file}"}
    elif args.string:
        data = args.string.encode("utf-8")
    else:
        return {"error": "Provide --string or --file"}

    if args.urlsafe:
        encoded = base64.urlsafe_b64encode(data).decode("ascii")
    else:
        encoded = base64.b64encode(data).decode("ascii")

    return {"action": "encode", "input_length": len(data), "output": encoded, "urlsafe": args.urlsafe}


def cmd_decode(args):
    """Decode a Base64 string."""
    s = args.string
    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                s = f.read().strip()
        except FileNotFoundError:
            return {"error": f"File not found: {args.file}"}

    if not s:
        return {"error": "No input to decode"}

    s = s.strip()
    # Auto-detect and normalize URL-safe
    if args.urlsafe or '-' in s or '_' in s:
        s = s.replace('-', '+').replace('_', '/')

    # Add padding if needed
    missing = len(s) % 4
    if missing:
        s += '=' * (4 - missing)

    try:
        decoded_bytes = base64.b64decode(s)
        # Try to decode as UTF-8 text
        try:
            decoded_text = decoded_bytes.decode("utf-8")
            is_text = True
        except UnicodeDecodeError:
            decoded_text = None
            is_text = False

        result = {
            "action": "decode",
            "output_bytes": len(decoded_bytes),
            "is_text": is_text,
        }
        if is_text:
            result["output"] = decoded_text
        else:
            result["output_hex"] = decoded_bytes.hex()
        return result
    except Exception as e:
        return {"error": f"Decode failed: {e}"}


def cmd_detect(args):
    """Detect if a string is valid Base64."""
    s = (args.string or "").strip()
    if not s:
        return {"error": "No input to detect"}

    b64_type = _detect_type(s)
    result = {
        "action": "detect",
        "is_base64": b64_type != "invalid",
        "type": b64_type,
    }

    if b64_type != "invalid":
        # Try to decode for preview
        norm = s.replace('-', '+').replace('_', '/')
        missing = len(norm) % 4
        if missing:
            norm += '=' * (4 - missing)
        try:
            decoded = base64.b64decode(norm)
            try:
                result["decoded_preview"] = decoded.decode("utf-8")[:200]
            except UnicodeDecodeError:
                result["decoded_preview"] = f"<binary, {len(decoded)} bytes>"
        except Exception:
            result["decoded_preview"] = None

    return result


def main():
    ap = argparse.ArgumentParser(
        description="Encode, decode, and detect Base64 strings."
    )
    sub = ap.add_subparsers(dest="command", help="sub-command")

    # encode
    p_enc = sub.add_parser("encode", help="Encode to Base64")
    p_enc.add_argument("-s", "--string", default=None, help="string to encode")
    p_enc.add_argument("--file", default=None, help="file to encode")
    p_enc.add_argument("--urlsafe", action="store_true", help="use URL-safe Base64")
    p_enc.add_argument("--json", action="store_true", help="JSON output")

    # decode
    p_dec = sub.add_parser("decode", help="Decode from Base64")
    p_dec.add_argument("-s", "--string", default=None, help="Base64 string to decode")
    p_dec.add_argument("--file", default=None, help="file with Base64 to decode")
    p_dec.add_argument("--urlsafe", action="store_true", help="use URL-safe Base64")
    p_dec.add_argument("--json", action="store_true", help="JSON output")

    # detect
    p_det = sub.add_parser("detect", help="Detect if string is Base64")
    p_det.add_argument("-s", "--string", default=None, help="string to check")
    p_det.add_argument("--json", action="store_true", help="JSON output")

    args = ap.parse_args()

    if not args.command:
        ap.print_help()
        sys.exit(1)

    if args.command == "encode":
        result = cmd_encode(args)
    elif args.command == "decode":
        result = cmd_decode(args)
    elif args.command == "detect":
        result = cmd_detect(args)
    else:
        ap.print_help()
        sys.exit(1)

    if "error" in result:
        print(f"[ERROR] {result['error']}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "json", False):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if args.command == "encode":
            print(result["output"])
        elif args.command == "decode":
            if result.get("is_text"):
                print(result["output"])
            else:
                print(f"<binary, {result['output_bytes']} bytes>")
                print(f"hex: {result['output_hex']}")
        elif args.command == "detect":
            status = "VALID" if result["is_base64"] else "INVALID"
            b64_type = result["type"]
            print(f"{status} Base64 ({b64_type})")
            if result.get("decoded_preview"):
                print(f"preview: {result['decoded_preview']}")


if __name__ == "__main__":
    main()
