#!/usr/bin/env python3
"""openapi-to-markdown — convert OpenAPI 3 JSON to Markdown documentation.

Usage:
    python openapi2md.py OPENAPI_JSON [--output FILE] [--tag TAG] [--include-schemas]

Generates human-readable Markdown from an OpenAPI 3 specification file.
"""

import argparse
import json
import sys
from pathlib import Path


def _load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ValueError(f"cannot read JSON file {path}: {e}")


def _resolve_ref(spec, ref):
    """Resolve a $ref pointer within the spec."""
    if not ref.startswith("#/"):
        return None
    parts = ref[2:].split("/")
    node = spec
    for p in parts:
        node = node.get(p, {})
    return node if node else None


def _resolve_schema(spec, schema):
    """Resolve a schema, following $ref if present."""
    if not isinstance(schema, dict):
        return schema
    if "$ref" in schema:
        resolved = _resolve_ref(spec, schema["$ref"])
        if resolved:
            return resolved
    return schema


def _schema_to_md(spec, schema, depth=0):
    """Convert a schema object to a Markdown description string."""
    if not isinstance(schema, dict):
        return str(schema)

    schema = _resolve_schema(spec, schema)

    parts = []
    stype = schema.get("type", "any")

    if "title" in schema:
        parts.append(f"**{schema['title']}** ")

    if schema.get("nullable"):
        stype = f"{stype} | null"

    parts.append(f"`{stype}`")

    if "format" in schema:
        parts.append(f"(_{schema['format']}_)")

    if "enum" in schema:
        parts.append(f"enum: {schema['enum']}")

    if "description" in schema:
        parts.append(f"— {schema['description']}")

    if "default" in schema:
        parts.append(f"(default: `{schema['default']}`)")

    return " ".join(parts)


def _schema_to_table(spec, schema, depth=0):
    """Convert an object schema to a property table."""
    schema = _resolve_schema(spec, schema)
    if not isinstance(schema, dict):
        return ""

    props = schema.get("properties", {})
    required = set(schema.get("required", []))

    if not props:
        return ""

    lines = []
    indent = "  " * depth
    lines.append(f"\n{indent}| Property | Type | Required | Description |")
    lines.append(f"{indent}| --- | --- | --- | --- |")

    for name, prop_schema in props.items():
        prop_schema = _resolve_schema(spec, prop_schema)
        ptype = prop_schema.get("type", "any") if isinstance(prop_schema, dict) else "any"
        if isinstance(prop_schema, dict) and prop_schema.get("format"):
            ptype = f"{ptype} ({prop_schema['format']})"
        if isinstance(prop_schema, dict) and prop_schema.get("enum"):
            ptype = f"{ptype}, enum: {prop_schema['enum']}"
        req = "Yes" if name in required else "No"
        desc = prop_schema.get("description", "") if isinstance(prop_schema, dict) else ""
        lines.append(f"{indent}| `{name}` | `{ptype}` | {req} | {desc} |")

    return "\n".join(lines)


def _param_to_md(spec, param):
    """Convert a parameter to a table row string."""
    param = _resolve_schema(spec, param) if isinstance(param, dict) and "$ref" in param else param
    name = param.get("name", "?")
    p_in = param.get("in", "?")
    required = "Yes" if param.get("required") else "No"
    schema = param.get("schema", {})
    ptype = schema.get("type", "any") if isinstance(schema, dict) else "any"
    desc = param.get("description", "")
    return f"| `{name}` | {p_in} | `{ptype}` | {required} | {desc} |"


def _generate_endpoint(spec, path, method, operation):
    lines = []
    method_upper = method.upper()
    op_id = operation.get("operationId", "")
    tags = operation.get("tags", [])
    summary = operation.get("summary", "")
    desc = operation.get("description", "")
    deprecated = operation.get("deprecated", False)

    header = f"### {method_upper} `{path}`"
    if deprecated:
        header += " _(deprecated)_"
    lines.append(header)
    lines.append("")

    if summary:
        lines.append(f"**{summary}**")
        lines.append("")

    if desc:
        lines.append(desc)
        lines.append("")

    if op_id:
        lines.append(f"- Operation ID: `{op_id}`")
    if tags:
        lines.append(f"- Tags: {', '.join(tags)}")
    lines.append("")

    # Parameters
    params = operation.get("parameters", [])
    if params:
        lines.append("**Parameters:**")
        lines.append("")
        lines.append("| Name | In | Type | Required | Description |")
        lines.append("| --- | --- | --- | --- | --- |")
        for p in params:
            lines.append(_param_to_md(spec, p))
        lines.append("")

    # Request body
    req_body = operation.get("requestBody")
    if req_body:
        req_body = _resolve_schema(spec, req_body) if isinstance(req_body, dict) and "$ref" in req_body else req_body
        lines.append("**Request Body:**")
        lines.append("")
        content = req_body.get("content", {})
        for ct, ct_schema in content.items():
            lines.append(f"Content-Type: `{ct}`")
            body_schema = ct_schema.get("schema", {})
            lines.append(_schema_to_md(spec, body_schema))
            lines.append(_schema_to_table(spec, body_schema))
            lines.append("")

    # Responses
    responses = operation.get("responses", {})
    if responses:
        lines.append("**Responses:**")
        lines.append("")
        for code, resp in sorted(responses.items()):
            resp = _resolve_schema(spec, resp) if isinstance(resp, dict) and "$ref" in resp else resp
            resp_desc = resp.get("description", "") if isinstance(resp, dict) else ""
            lines.append(f"- **{code}**: {resp_desc}")
            if isinstance(resp, dict) and "content" in resp:
                for ct, ct_schema in resp["content"].items():
                    body_schema = ct_schema.get("schema", {})
                    lines.append(f"  - `{ct}`: {_schema_to_md(spec, body_schema)}")
                    table = _schema_to_table(spec, body_schema, depth=1)
                    if table:
                        lines.append(table)
        lines.append("")

    return "\n".join(lines)


def convert(spec, tag_filter=None, include_schemas=False):
    """Convert an OpenAPI spec dict to Markdown string."""
    lines = []

    # Title and info
    info = spec.get("info", {})
    title = info.get("title", "API")
    version = info.get("version", "")
    lines.append(f"# {title}")
    lines.append("")
    if version:
        lines.append(f"**Version:** {version}")
    if info.get("description"):
        lines.append("")
        lines.append(info["description"])
    lines.append("")

    servers = spec.get("servers", [])
    if servers:
        lines.append("## Servers")
        lines.append("")
        for s in servers:
            lines.append(f"- `{s.get('url', '')}` — {s.get('description', '')}")
        lines.append("")

    # Endpoints grouped by tag
    paths = spec.get("paths", {})
    tag_ops = {}  # tag -> [(path, method, operation)]

    for path, path_item in paths.items():
        for method in ("get", "post", "put", "patch", "delete", "head", "options", "trace"):
            if method not in path_item:
                continue
            operation = path_item[method]
            tags = operation.get("tags", ["default"])
            for tag in tags:
                if tag_filter and tag != tag_filter:
                    continue
                tag_ops.setdefault(tag, []).append((path, method, operation))

    for tag in sorted(tag_ops):
        lines.append(f"## {tag}")
        lines.append("")
        for path, method, operation in tag_ops[tag]:
            lines.append(_generate_endpoint(spec, path, method, operation))
            lines.append("---")
            lines.append("")

    # Schemas
    if include_schemas:
        components = spec.get("components", {})
        schemas = components.get("schemas", {})
        if schemas:
            lines.append("## Schemas")
            lines.append("")
            for name, schema in sorted(schemas.items()):
                lines.append(f"### {name}")
                lines.append("")
                lines.append(_schema_to_md(spec, schema))
                lines.append(_schema_to_table(spec, schema))
                lines.append("")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Convert OpenAPI 3 JSON to Markdown documentation."
    )
    ap.add_argument("openapi", help="path to OpenAPI 3 JSON file")
    ap.add_argument("--output", "-o", default=None,
                    help="output file path (default: stdout)")
    ap.add_argument("--tag", default=None,
                    help="only include endpoints with this tag")
    ap.add_argument("--include-schemas", action="store_true",
                    help="include component schemas section")
    args = ap.parse_args()

    try:
        spec = _load_json(args.openapi)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    md = convert(spec, tag_filter=args.tag, include_schemas=args.include_schemas)

    if args.output:
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"Written to {args.output}")
    else:
        print(md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
