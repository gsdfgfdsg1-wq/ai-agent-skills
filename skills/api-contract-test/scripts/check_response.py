#!/usr/bin/env python3
"""Validate an HTTP response fixture against an OpenAPI 3 JSON document.

Supported schema keywords: type, required, properties, items, enum, nullable,
minimum, maximum, minLength, maxLength. YAML is intentionally not supported so
the script remains dependency-free.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: str) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot load JSON from {path}: {exc}") from exc


def resolve_ref(spec: dict[str, Any], node: Any) -> Any:
    while isinstance(node, dict) and "$ref" in node:
        ref = node["$ref"]
        if not ref.startswith("#/"):
            raise ValueError(f"Only local refs are supported: {ref}")
        current: Any = spec
        for part in ref[2:].split("/"):
            current = current[part.replace("~1", "/").replace("~0", "~")]
        node = current
    return node


def openapi_path_matches(template: str, requested: str) -> bool:
    pattern = re.sub(r"\{[^}]+\}", r"[^/]+", template)
    return bool(re.fullmatch(pattern, requested))


def find_operation(spec: dict[str, Any], method: str, path: str) -> tuple[str, dict[str, Any]]:
    for template, item in spec.get("paths", {}).items():
        if openapi_path_matches(template, path):
            operation = item.get(method.lower())
            if operation:
                return template, operation
    raise ValueError(f"No {method.upper()} operation found for {path}")


def type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate_schema(spec: dict[str, Any], schema: Any, value: Any, at: str = "$") -> list[str]:
    schema = resolve_ref(spec, schema)
    if not isinstance(schema, dict):
        return []
    errors: list[str] = []

    if value is None and schema.get("nullable"):
        return []

    expected = schema.get("type")
    if expected and not type_matches(value, expected):
        return [f"{at}: expected {expected}, got {type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{at}: value {value!r} is not in enum {schema['enum']!r}")

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{at}: missing required property {key!r}")
        for key, child in schema.get("properties", {}).items():
            if key in value:
                errors.extend(validate_schema(spec, child, value[key], f"{at}.{key}"))

    if isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value):
            errors.extend(validate_schema(spec, schema["items"], item, f"{at}[{index}]") )

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{at}: string length is below minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{at}: string length exceeds maxLength {schema['maxLength']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{at}: value is below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{at}: value exceeds maximum {schema['maximum']}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an HTTP response against OpenAPI 3 JSON.")
    parser.add_argument("--spec", required=True, help="OpenAPI 3 JSON document")
    parser.add_argument("--method", required=True, help="HTTP method, e.g. GET")
    parser.add_argument("--path", required=True, help="Request path, e.g. /users/42")
    parser.add_argument("--status", required=True, help="Observed HTTP response status, e.g. 200")
    parser.add_argument("--body", required=True, help="Response body JSON file")
    parser.add_argument("--content-type", default="application/json", help="Observed response Content-Type")
    args = parser.parse_args()

    try:
        spec = load_json(args.spec)
        body = load_json(args.body)
        template, operation = find_operation(spec, args.method, args.path)
        responses = operation.get("responses", {})
        response = responses.get(str(args.status)) or responses.get("default")
        if not response:
            raise ValueError(f"{args.method.upper()} {template} does not document status {args.status}")
        response = resolve_ref(spec, response)
        content = response.get("content", {})
        media_type = args.content_type.split(";", 1)[0].strip().lower()
        media = content.get(media_type)
        if not media:
            available = ", ".join(content) or "none"
            raise ValueError(f"Status {args.status} does not document content type {media_type} (available: {available})")
        errors = validate_schema(spec, media.get("schema", {}), body)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2)

    if errors:
        print(f"FAIL: {len(errors)} contract violation(s) for {args.method.upper()} {args.path} -> {args.status}")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)

    print(f"PASS: {args.method.upper()} {args.path} -> {args.status} matches the OpenAPI contract.")


if __name__ == "__main__":
    main()
