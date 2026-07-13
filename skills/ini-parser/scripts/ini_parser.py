#!/usr/bin/env python3
"""Parse, validate, and query INI configuration files."""

import argparse
import configparser
import json
import sys
from pathlib import Path


def load_ini(filepath, strict=False):
    """Load and parse an INI file."""
    try:
        text = Path(filepath).read_text(encoding="utf-8", errors="replace")
    except (OSError, IOError) as e:
        print(f"Error: cannot read {filepath}: {e}", file=sys.stderr)
        sys.exit(1)

    config = configparser.ConfigParser(
        interpolation=None,
        strict=strict,
    )
    try:
        config.read_string(text)
    except configparser.DuplicateSectionError as e:
        print(f"Error: duplicate section: {e}", file=sys.stderr)
        sys.exit(1)
    except configparser.DuplicateOptionError as e:
        print(f"Error: duplicate key: {e}", file=sys.stderr)
        sys.exit(1)
    except configparser.Error as e:
        print(f"Error: invalid INI: {e}", file=sys.stderr)
        sys.exit(1)
    return config


def config_to_dict(config):
    """Convert ConfigParser to nested dict."""
    result = {}
    for section in config.sections():
        result[section] = dict(config[section])
    return result


def cmd_parse(args):
    config = load_ini(args.file, strict=args.strict)
    data = config_to_dict(config)

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for section, keys in data.items():
            print(f"[{section}]")
            for k, v in keys.items():
                print(f"  {k} = {v}")
            print()


def cmd_get(args):
    config = load_ini(args.file)
    if not config.has_section(args.section):
        print(f"Error: section '{args.section}' not found", file=sys.stderr)
        sys.exit(1)
    if not config.has_option(args.section, args.key):
        print(f"Error: key '{args.key}' not found in section '{args.section}'", file=sys.stderr)
        sys.exit(1)

    value = config.get(args.section, args.key)
    if args.json:
        print(json.dumps({"section": args.section, "key": args.key, "value": value}, indent=2))
    else:
        print(value)


def cmd_keys(args):
    config = load_ini(args.file)
    if not config.has_section(args.section):
        print(f"Error: section '{args.section}' not found", file=sys.stderr)
        sys.exit(1)

    keys = list(config[args.section].keys())
    if args.json:
        print(json.dumps({"section": args.section, "keys": keys}, indent=2))
    else:
        for k in keys:
            print(k)


def cmd_sections(args):
    config = load_ini(args.file)
    sections = config.sections()
    if args.json:
        print(json.dumps({"sections": sections}, indent=2))
    else:
        for s in sections:
            print(s)


def main():
    parser = argparse.ArgumentParser(description="Parse, validate, and query INI files.")
    sub = parser.add_subparsers(dest="command")

    p_parse = sub.add_parser("parse", help="Parse and display INI file")
    p_parse.add_argument("--file", required=True, help="INI file")
    p_parse.add_argument("--json", action="store_true", help="JSON output")
    p_parse.add_argument("--strict", action="store_true", help="Flag duplicate keys")

    p_get = sub.add_parser("get", help="Get a key value")
    p_get.add_argument("--file", required=True, help="INI file")
    p_get.add_argument("--section", required=True, help="Section name")
    p_get.add_argument("--key", required=True, help="Key name")
    p_get.add_argument("--json", action="store_true", help="JSON output")

    p_keys = sub.add_parser("keys", help="List keys in a section")
    p_keys.add_argument("--file", required=True, help="INI file")
    p_keys.add_argument("--section", required=True, help="Section name")
    p_keys.add_argument("--json", action="store_true", help="JSON output")

    p_sections = sub.add_parser("sections", help="List all sections")
    p_sections.add_argument("--file", required=True, help="INI file")
    p_sections.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if args.command == "parse":
        cmd_parse(args)
    elif args.command == "get":
        cmd_get(args)
    elif args.command == "keys":
        cmd_keys(args)
    elif args.command == "sections":
        cmd_sections(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
