#!/usr/bin/env python3
"""xml_to_json.py — Convert XML files to JSON format.

Uses only Python standard library (xml.etree.ElementTree, json, argparse, sys, os, re).
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET


def _element_to_dict(element, text_key="#text", attr_prefix="@", include_attrs=True):
    """Recursively convert an xml.etree.ElementTree element to a dict."""
    result = {}

    # Attributes
    if include_attrs and element.attrib:
        for key, value in element.attrib.items():
            result[attr_prefix + key] = value

    # Children — collect by tag to detect repeated elements (arrays)
    children_by_tag = {}
    for child in element:
        children_by_tag.setdefault(child.tag, []).append(child)

    for tag, children in children_by_tag.items():
        converted = [
            _element_to_dict(c, text_key=text_key, attr_prefix=attr_prefix, include_attrs=include_attrs)
            for c in children
        ]
        if len(converted) == 1:
            result[tag] = converted[0]
        else:
            result[tag] = converted

    # Text content
    text = (element.text or "").strip()
    if text:
        # If there are already child keys, store text under text_key
        if result:
            result[text_key] = text
        else:
            # Leaf element with only text — return text directly unless there are attributes
            if not include_attrs or not element.attrib:
                return text
            result[text_key] = text

    # If result is empty (no attributes, no children, no text)
    if not result:
        return None

    return result


def xml_to_dict(xml_string, text_key="#text", attr_prefix="@", include_attrs=True):
    """Parse an XML string and return a Python dict."""
    root = ET.fromstring(xml_string)
    return {root.tag: _element_to_dict(root, text_key=text_key, attr_prefix=attr_prefix, include_attrs=include_attrs)}


def _collect_structure(element, depth=0, tags=None, attrs=None, max_depth=0):
    """Walk the tree and collect tag names, attributes, and max depth."""
    if tags is None:
        tags = {}
    if attrs is None:
        attrs = {}

    tag = element.tag
    # Strip namespace for display
    display_tag = re.sub(r"\{[^}]+\}", "", tag)
    tags.setdefault(display_tag, 0)
    tags[display_tag] += 1

    if element.attrib:
        attr_names = [re.sub(r"\{[^}]+\}", "", a) for a in element.attrib]
        attrs.setdefault(display_tag, set()).update(attr_names)

    if depth > max_depth:
        max_depth = depth

    for child in element:
        _, _, max_depth = _collect_structure(child, depth + 1, tags, attrs, max_depth)

    return tags, attrs, max_depth


def inspect_xml(xml_string):
    """Return a structure summary dict for the given XML string."""
    root = ET.fromstring(xml_string)
    tags, attrs, max_depth = _collect_structure(root)
    # Convert sets to sorted lists for JSON serialization
    attrs_serializable = {k: sorted(v) for k, v in attrs.items()}
    return {
        "root_tag": re.sub(r"\{[^}]+\}", "", root.tag),
        "max_depth": max_depth,
        "element_counts": tags,
        "attributes_by_tag": attrs_serializable,
    }


def cmd_convert(args):
    """Handle the 'convert' subcommand."""
    # Read XML input
    if args.file:
        if not os.path.isfile(args.file):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                xml_string = f.read()
        except OSError as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.string is not None:
        xml_string = args.string
    else:
        print("Error: Provide --file or -s with XML input.", file=sys.stderr)
        sys.exit(2)

    if not xml_string.strip():
        print("Error: Empty XML input.", file=sys.stderr)
        sys.exit(1)

    # Parse and convert
    try:
        result = xml_to_dict(
            xml_string,
            text_key=args.text_key,
            attr_prefix=args.attr_prefix,
            include_attrs=args.attrs,
        )
    except ET.ParseError as e:
        print(f"Error: Malformed XML — {e}", file=sys.stderr)
        sys.exit(1)

    indent = 2 if args.pretty else None
    json_str = json.dumps(result, indent=indent, ensure_ascii=False)

    # Output
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_str)
                f.write("\n")
        except OSError as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(json_str)

    # Stats
    if args.json_stats:
        stats = {
            "input_file": args.file or "<string>",
            "root_tag": list(result.keys())[0] if result else None,
            "output_file": args.output or "<stdout>",
            "pretty": args.pretty,
            "include_attrs": args.attrs,
            "text_key": args.text_key,
            "attr_prefix": args.attr_prefix,
        }
        print(json.dumps(stats, indent=2, ensure_ascii=False))


def cmd_inspect(args):
    """Handle the 'inspect' subcommand."""
    if not args.file:
        print("Error: --file is required for inspect.", file=sys.stderr)
        sys.exit(2)

    if not os.path.isfile(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            xml_string = f.read()
    except OSError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    if not xml_string.strip():
        print("Error: Empty XML input.", file=sys.stderr)
        sys.exit(1)

    try:
        summary = inspect_xml(xml_string)
    except ET.ParseError as e:
        print(f"Error: Malformed XML — {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(summary, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        prog="xml_to_json",
        description="Convert XML files to JSON format with attribute and namespace handling.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- convert ---
    convert_parser = subparsers.add_parser("convert", help="Convert XML to JSON")
    convert_parser.add_argument("--file", metavar="PATH", help="Path to XML input file")
    convert_parser.add_argument("-s", "--string", metavar="STRING", help="XML string input")
    convert_parser.add_argument("--output", metavar="PATH", help="Output file path (default: stdout)")
    convert_parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    convert_parser.add_argument(
        "--attrs", action="store_true", default=True, dest="attrs",
        help="Include attributes in output (default: True)",
    )
    convert_parser.add_argument(
        "--no-attrs", action="store_false", dest="attrs",
        help="Exclude attributes from output",
    )
    convert_parser.add_argument(
        "--text-key", default="#text", metavar="KEY",
        help="Key name for text content (default: #text)",
    )
    convert_parser.add_argument(
        "--attr-prefix", default="@", metavar="PREFIX",
        help="Prefix for attribute keys (default: @)",
    )
    convert_parser.add_argument(
        "--json", action="store_true", dest="json_stats",
        help="Print conversion stats as JSON after output",
    )
    convert_parser.set_defaults(func=cmd_convert)

    # --- inspect ---
    inspect_parser = subparsers.add_parser("inspect", help="Show XML structure summary")
    inspect_parser.add_argument("--file", required=True, metavar="PATH", help="Path to XML file")
    inspect_parser.set_defaults(func=cmd_inspect)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(2)

    args.func(args)


if __name__ == "__main__":
    main()
