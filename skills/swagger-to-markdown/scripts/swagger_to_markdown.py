#!/usr/bin/env python3
"""swagger-to-markdown — convert Swagger/OpenAPI 2.0 JSON to Markdown.

Usage:
    python swagger_to_markdown.py SPEC [SPEC ...] [--output FILE] [--include-models]

Reads Swagger 2.0 JSON files and produces human-readable Markdown documentation.
"""

import argparse
import json
import os
import sys


def _ref_name(ref_str):
    """Extract the name from a $ref string like '#/definitions/Pet'."""
    if not ref_str:
        return None
    return ref_str.split("/")[-1]


def _resolve_ref(spec, ref_str):
    """Resolve a $ref pointer within the spec."""
    if not ref_str or not ref_str.startswith("#/"):
        return None
    parts = ref_str[2:].split("/")
    current = spec
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
        if current is None:
            return None
    return current


def _format_schema(schema, spec, indent=0):
    """Format a Swagger schema into Markdown description."""
    if not schema:
        return "_No schema_"

    lines = []
    ref = schema.get("$ref")
    if ref:
        name = _ref_name(ref)
        lines.append(f"`{name}`" if name else f"`{ref}`")
        return "\n".join(lines)

    schema_type = schema.get("type", "object")

    if schema_type == "array":
        items = schema.get("items", {})
        item_ref = items.get("$ref")
        if item_ref:
            lines.append(f"Array of `{_ref_name(item_ref)}`")
        else:
            lines.append(f"Array of `{items.get('type', 'object')}`")
        return "\n".join(lines)

    props = schema.get("properties", {})
    if props:
        lines.append("")
        lines.append("| Field | Type | Required | Description |")
        lines.append("| --- | --- | --- | --- |")
        required_fields = schema.get("required", [])
        for pname, pval in props.items():
            ptype = pval.get("type", "object")
            pref = pval.get("$ref")
            if pref:
                ptype = f"`{_ref_name(pref)}`"
            elif ptype == "array":
                items_ref = pval.get("items", {}).get("$ref")
                if items_ref:
                    ptype = f"`{_ref_name(items_ref)}[]`"
                else:
                    ptype = f"{pval.get('items', {}).get('type', 'object')}[]"
            req = "Yes" if pname in required_fields else "No"
            desc = pval.get("description", "").replace("|", "\\|")
            lines.append(f"| `{pname}` | {ptype} | {req} | {desc} |")
        return "\n".join(lines)

    return f"`{schema_type}`"


def _format_param(param, spec):
    """Format a single parameter into a table row."""
    # Resolve $ref
    if "$ref" in param:
        resolved = _resolve_ref(spec, param["$ref"])
        if resolved:
            param = resolved

    name = param.get("name", "?")
    p_in = param.get("in", "?")
    ptype = param.get("type", param.get("schema", {}).get("type", "?"))
    ref = param.get("schema", {}).get("$ref") if "schema" in param else None
    if ref:
        ptype = f"`{_ref_name(ref)}`"
    required = "Yes" if param.get("required") else "No"
    desc = param.get("description", "").replace("|", "\\|")
    return f"| `{name}` | {p_in} | {ptype} | {required} | {desc} |"


def convert_spec(spec):
    """Convert a full Swagger 2.0 spec dict to Markdown string."""
    lines = []

    # Title & Info
    info = spec.get("info", {})
    title = info.get("title", "API Documentation")
    version = info.get("version", "")
    lines.append(f"# {title}")
    lines.append("")
    if version:
        lines.append(f"**Version:** {version}")
    desc = info.get("description", "")
    if desc:
        lines.append("")
        lines.append(desc)

    host = spec.get("host", "")
    base_path = spec.get("basePath", "")
    if host or base_path:
        lines.append("")
        lines.append(f"**Base URL:** `{host}{base_path}`")

    schemes = spec.get("schemes", [])
    if schemes:
        lines.append(f"**Schemes:** {', '.join(schemes)}")

    # Security Definitions
    sec_defs = spec.get("securityDefinitions", {})
    if sec_defs:
        lines.append("")
        lines.append("## Security")
        lines.append("")
        for sname, sdef in sec_defs.items():
            stype = sdef.get("type", "")
            lines.append(f"- **{sname}** ({stype})")
            if sdef.get("description"):
                lines.append(f"  - {sdef['description']}")
            if stype == "apiKey":
                lines.append(f"  - In: {sdef.get('in', '?')}, Name: {sdef.get('name', '?')}")

    # Paths
    paths = spec.get("paths", {})
    if paths:
        lines.append("")
        lines.append("## Endpoints")
        for path, methods in paths.items():
            lines.append("")
            lines.append(f"### `{path}`")
            lines.append("")

            for method, details in methods.items():
                if method.startswith("x-") or method == "parameters":
                    continue
                method_upper = method.upper()
                summary = details.get("summary", "")
                desc = details.get("description", "")

                lines.append(f"#### {method_upper} {path}")
                if summary:
                    lines.append("")
                    lines.append(f"**{summary}**")
                if desc:
                    lines.append("")
                    lines.append(desc)
                lines.append("")

                # Parameters
                params = details.get("parameters", [])
                if params:
                    lines.append("**Parameters:**")
                    lines.append("")
                    lines.append("| Name | In | Type | Required | Description |")
                    lines.append("| --- | --- | --- | --- | --- |")
                    for p in params:
                        lines.append(_format_param(p, spec))
                    lines.append("")

                # Responses
                responses = details.get("responses", {})
                if responses:
                    lines.append("**Responses:**")
                    lines.append("")
                    lines.append("| Code | Description |")
                    lines.append("| --- | --- |")
                    for code, rdetails in responses.items():
                        rdesc = rdetails.get("description", "")
                        rschema = rdetails.get("schema", {})
                        if rschema:
                            ref = rschema.get("$ref")
                            rtype = _ref_name(ref) if ref else rschema.get("type", "")
                            rdesc += f" (`{rtype}`)" if rtype else ""
                        lines.append(f"| {code} | {rdesc} |")
                    lines.append("")

    # Definitions (models)
    definitions = spec.get("definitions", {})
    if definitions:
        lines.append("")
        lines.append("## Definitions")
        for dname, ddef in definitions.items():
            lines.append("")
            lines.append(f"### {dname}")
            ddesc = ddef.get("description", "")
            if ddesc:
                lines.append("")
                lines.append(ddesc)
            lines.append("")
            lines.append(_format_schema(ddef, spec))
            lines.append("")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Convert Swagger/OpenAPI 2.0 JSON to Markdown."
    )
    ap.add_argument("specs", nargs="+", help="Swagger 2.0 JSON file(s)")
    ap.add_argument("--output", "-o", default=None,
                    help="output file (default: stdout)")
    ap.add_argument("--include-models", action="store_true",
                    help="include full model definitions section (included by default for Swagger 2.0)")
    args = ap.parse_args()

    all_md = []
    for spec_path in args.specs:
        try:
            with open(spec_path, encoding="utf-8") as f:
                spec = json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] File not found: {spec_path}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in {spec_path}: {e}", file=sys.stderr)
            sys.exit(1)

        swagger_ver = spec.get("swagger", "")
        if not swagger_ver.startswith("2"):
            print(f"[WARNING] {spec_path} does not appear to be Swagger 2.0 (found: {swagger_ver})", file=sys.stderr)

        md = convert_spec(spec)
        all_md.append(md)

    output = "\n\n---\n\n".join(all_md)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
