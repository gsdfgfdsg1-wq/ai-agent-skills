#!/usr/bin/env python3
"""Escape and unescape strings for C, Python, HTML, JavaScript, and JSON contexts without external dependencies."""

import argparse
import json
import sys

CONTEXTS = ["c", "python", "html", "js", "json"]


def escape_text(text, context):
    """Escape text for the given context."""
    if context == "json":
        return json.dumps(text)
    elif context == "python":
        return repr(text)
    elif context == "c":
        result = text.replace("\\", "\\\\")
        result = result.replace('"', '\\"')
        result = result.replace("'", "\\'")
        result = result.replace("\n", "\\n")
        result = result.replace("\r", "\\r")
        result = result.replace("\t", "\\t")
        result = result.replace("\0", "\\0")
        return '"' + result + '"'
    elif context == "html":
        result = text.replace("&", "&amp;")
        result = result.replace("<", "&lt;")
        result = result.replace(">", "&gt;")
        result = result.replace('"', "&quot;")
        result = result.replace("'", "&#x27;")
        return result
    elif context == "js":
        result = text.replace("\\", "\\\\")
        result = result.replace('"', '\\"')
        result = result.replace("'", "\\'")
        result = result.replace("\n", "\\n")
        result = result.replace("\r", "\\r")
        result = result.replace("\t", "\\t")
        return '"' + result + '"'
    else:
        print(f"Error: unknown context '{context}'", file=sys.stderr)
        sys.exit(1)


def unescape_text(text, context):
    """Unescape text from the given context."""
    if context == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON string: {e}", file=sys.stderr)
            sys.exit(1)
    elif context == "python":
        # Use ast.literal_eval for safety
        try:
            import ast
            return ast.literal_eval(text)
        except (ValueError, SyntaxError) as e:
            print(f"Error: invalid Python literal: {e}", file=sys.stderr)
            sys.exit(1)
    elif context == "c":
        # Strip surrounding quotes
        s = text.strip()
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1]
        result = s.replace("\\\\", "\x00BACKSLASH\x00")
        result = result.replace('\\"', '"')
        result = result.replace("\\'", "'")
        result = result.replace("\\n", "\n")
        result = result.replace("\\r", "\r")
        result = result.replace("\\t", "\t")
        result = result.replace("\\0", "\0")
        result = result.replace("\x00BACKSLASH\x00", "\\")
        return result
    elif context == "html":
        result = text.replace("&amp;", "&")
        result = result.replace("&lt;", "<")
        result = result.replace("&gt;", ">")
        result = result.replace("&quot;", '"')
        result = result.replace("&#x27;", "'")
        result = result.replace("&#39;", "'")
        result = result.replace("&#x2F;", "/")
        result = result.replace("&#47;", "/")
        # Handle numeric entities
        import re
        def replace_numeric(m):
            try:
                if m.group(1).startswith("x") or m.group(1).startswith("X"):
                    return chr(int(m.group(1)[1:], 16))
                return chr(int(m.group(1)))
            except (ValueError, OverflowError):
                return m.group(0)
        result = re.sub(r"&#(x?[0-9a-fA-F]+);", replace_numeric, result)
        return result
    elif context == "js":
        s = text.strip()
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1]
        elif s.startswith("'") and s.endswith("'"):
            s = s[1:-1]
        result = s.replace("\\\\", "\x00BACKSLASH\x00")
        result = result.replace('\\"', '"')
        result = result.replace("\\'", "'")
        result = result.replace("\\n", "\n")
        result = result.replace("\\r", "\r")
        result = result.replace("\\t", "\t")
        result = result.replace("\x00BACKSLASH\x00", "\\")
        return result
    else:
        print(f"Error: unknown context '{context}'", file=sys.stderr)
        sys.exit(1)


def cmd_escape(args):
    result = escape_text(args.text, args.context)
    if args.json:
        print(json.dumps({"input": args.text, "context": args.context, "output": result}, indent=2))
    else:
        print(result)


def cmd_unescape(args):
    result = unescape_text(args.text, args.context)
    if args.json:
        print(json.dumps({"input": args.text, "context": args.context, "output": result}, indent=2))
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Escape and unescape strings across language contexts.")
    sub = parser.add_subparsers(dest="command")

    p_esc = sub.add_parser("escape", help="Escape a string")
    p_esc.add_argument("--text", required=True, help="Text to escape")
    p_esc.add_argument("--context", required=True, choices=CONTEXTS, help="Target context")
    p_esc.add_argument("--json", action="store_true", help="JSON output")

    p_unesc = sub.add_parser("unescape", help="Unescape a string")
    p_unesc.add_argument("--text", required=True, help="Text to unescape")
    p_unesc.add_argument("--context", required=True, choices=CONTEXTS, help="Source context")
    p_unesc.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "escape":
        cmd_escape(args)
    elif args.command == "unescape":
        cmd_unescape(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
