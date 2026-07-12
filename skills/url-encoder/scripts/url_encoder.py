#!/usr/bin/env python3
"""URL encoder/decoder/parser/builder with component-level control.

Usage:
    python url_encoder.py encode -s STRING [--component {full,query,fragment,path}] [--json]
    python url_encoder.py decode -s STRING [--component {full,query,fragment,path}] [--json]
    python url_encoder.py parse  -s URL [--json]
    python url_encoder.py build  --scheme SCHEME --host HOST [--port PORT] [--path PATH]
                                  [--query KEY=VAL ...] [--fragment FRAGMENT] [--json]
"""

import argparse
import json
import sys
from urllib.parse import (
    quote,
    quote_plus,
    unquote,
    unquote_plus,
    urlencode,
    urlparse,
    urlunparse,
    ParseResult,
)


# ---------------------------------------------------------------------------
# Encode
# ---------------------------------------------------------------------------

def _encode_component(s: str, component: str) -> str:
    if component == "query":
        return quote_plus(s, safe="=&")
    if component == "fragment":
        return quote(s, safe="")
    if component == "path":
        return quote(s, safe="/")
    # component == "full"
    return quote(s, safe=":/?#[]@!$&'()*+,;=-._~")


def cmd_encode(args: argparse.Namespace) -> int:
    if not args.string:
        print("Error: -s/--string is required", file=sys.stderr)
        return 1
    result = _encode_component(args.string, args.component)
    if args.json:
        print(json.dumps({"input": args.string, "component": args.component, "encoded": result}, ensure_ascii=False))
    else:
        print(result)
    return 0


# ---------------------------------------------------------------------------
# Decode
# ---------------------------------------------------------------------------

def _decode_component(s: str, component: str) -> str:
    try:
        if component == "query":
            return unquote_plus(s)
        return unquote(s)
    except Exception as exc:
        print(f"Error: decode failed: {exc}", file=sys.stderr)
        raise SystemExit(1)


def cmd_decode(args: argparse.Namespace) -> int:
    if not args.string:
        print("Error: -s/--string is required", file=sys.stderr)
        return 1
    result = _decode_component(args.string, args.component)
    if args.json:
        print(json.dumps({"input": args.string, "component": args.component, "decoded": result}, ensure_ascii=False))
    else:
        print(result)
    return 0


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------

def cmd_parse(args: argparse.Namespace) -> int:
    if not args.string:
        print("Error: -s/--string is required", file=sys.stderr)
        return 1
    parsed: ParseResult = urlparse(args.string)
    components = {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "params": parsed.params,
        "query": parsed.query,
        "fragment": parsed.fragment,
        "username": parsed.username,
        "password": parsed.password,
        "hostname": parsed.hostname,
        "port": parsed.port,
    }
    if args.json:
        print(json.dumps(components, ensure_ascii=False, indent=2))
    else:
        max_key_len = max(len(k) for k in components)
        for key, val in components.items():
            print(f"  {key:<{max_key_len}}  {val}")
    return 0


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def cmd_build(args: argparse.Namespace) -> int:
    if not args.scheme:
        print("Error: --scheme is required", file=sys.stderr)
        return 1
    if not args.host:
        print("Error: --host is required", file=sys.stderr)
        return 1

    scheme = args.scheme
    netloc = args.host
    if args.port:
        netloc = f"{netloc}:{args.port}"

    path = args.path or ""
    if path and not path.startswith("/"):
        path = "/" + path

    # Build query string from repeated --query KEY=VAL
    query_parts: list[tuple[str, str]] = []
    for q in (args.query or []):
        if "=" not in q:
            print(f"Error: invalid query parameter '{q}', expected KEY=VAL", file=sys.stderr)
            return 1
        key, _, val = q.partition("=")
        query_parts.append((key, val))
    query = urlencode(query_parts) if query_parts else ""

    fragment = args.fragment or ""

    url = urlunparse((scheme, netloc, path, "", query, fragment))

    if args.json:
        result = {
            "scheme": scheme,
            "host": args.host,
            "port": args.port,
            "path": path,
            "query": query,
            "fragment": fragment,
            "url": url,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(url)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="url_encoder",
        description="Encode, decode, parse, and build URLs with component-level control.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # -- encode --
    enc = subparsers.add_parser("encode", help="Encode a URL or component")
    enc.add_argument("-s", "--string", help="String to encode")
    enc.add_argument(
        "--component",
        choices=["full", "query", "fragment", "path"],
        default="full",
        help="Which component to encode (default: full)",
    )
    enc.add_argument("--json", action="store_true", help="Output as JSON")

    # -- decode --
    dec = subparsers.add_parser("decode", help="Decode a URL or component")
    dec.add_argument("-s", "--string", help="String to decode")
    dec.add_argument(
        "--component",
        choices=["full", "query", "fragment", "path"],
        default="full",
        help="Which component to decode (default: full)",
    )
    dec.add_argument("--json", action="store_true", help="Output as JSON")

    # -- parse --
    prs = subparsers.add_parser("parse", help="Parse a URL into components")
    prs.add_argument("-s", "--string", help="URL to parse")
    prs.add_argument("--json", action="store_true", help="Output as JSON")

    # -- build --
    bld = subparsers.add_parser("build", help="Build a URL from components")
    bld.add_argument("--scheme", help="URL scheme (e.g. https)")
    bld.add_argument("--host", help="Host name (e.g. example.com)")
    bld.add_argument("--port", type=int, help="Port number")
    bld.add_argument("--path", help="URL path")
    bld.add_argument("--query", action="append", help="Query param as KEY=VAL (repeatable)")
    bld.add_argument("--fragment", help="Fragment identifier")
    bld.add_argument("--json", action="store_true", help="Output as JSON")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    dispatch = {
        "encode": cmd_encode,
        "decode": cmd_decode,
        "parse": cmd_parse,
        "build": cmd_build,
    }
    return dispatch[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
