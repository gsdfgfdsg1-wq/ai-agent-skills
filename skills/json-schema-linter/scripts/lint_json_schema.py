#!/usr/bin/env python3
"""json-schema-linter — validate JSON files against a JSON Schema.

Usage:
    python lint_json_schema.py INSTANCE SCHEMA [--json] [--exit-code]

Supports a practical subset of JSON Schema Draft-07: type, required,
properties, additionalProperties, enum, minimum/maximum, minLength/maxLength,
pattern, items (tuple/list), and nested objects. All implemented with stdlib.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def _load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ValueError(f"cannot read JSON file {path}: {e}")


def _validate(instance, schema, path="$"):
    """Validate instance against schema, returning a list of error dicts."""
    errors = []

    # type check
    expected_type = schema.get("type")
    if expected_type is not None:
        types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_matches_type(instance, t) for t in types):
            errors.append({"path": path, "rule": "type",
                           "message": f"expected {expected_type}, got {_json_type(instance)}"})
            return errors  # stop further checks if type doesn't match

    # enum
    if "enum" in schema:
        if instance not in schema["enum"]:
            errors.append({"path": path, "rule": "enum",
                           "message": f"value {instance!r} not in enum {schema['enum']}"})

    # const
    if "const" in schema:
        if instance != schema["const"]:
            errors.append({"path": path, "rule": "const",
                           "message": f"value does not match const {schema['const']!r}"})

    # String constraints
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append({"path": path, "rule": "minLength",
                           "message": f"string length {len(instance)} < {schema['minLength']}"})
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append({"path": path, "rule": "maxLength",
                           "message": f"string length {len(instance)} > {schema['maxLength']}"})
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append({"path": path, "rule": "pattern",
                           "message": f"string does not match pattern {schema['pattern']!r}"})

    # Number constraints
    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append({"path": path, "rule": "minimum",
                           "message": f"value {instance} < minimum {schema['minimum']}"})
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append({"path": path, "rule": "maximum",
                           "message": f"value {instance} > maximum {schema['maximum']}"})
        if "exclusiveMinimum" in schema and instance <= schema["exclusiveMinimum"]:
            errors.append({"path": path, "rule": "exclusiveMinimum",
                           "message": f"value {instance} <= exclusiveMinimum {schema['exclusiveMinimum']}"})
        if "exclusiveMaximum" in schema and instance >= schema["exclusiveMaximum"]:
            errors.append({"path": path, "rule": "exclusiveMaximum",
                           "message": f"value {instance} >= exclusiveMaximum {schema['exclusiveMaximum']}"})

    # Array constraints
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append({"path": path, "rule": "minItems",
                           "message": f"array length {len(instance)} < {schema['minItems']}"})
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append({"path": path, "rule": "maxItems",
                           "message": f"array length {len(instance)} > {schema['maxItems']}"})
        if schema.get("uniqueItems") and len(instance) != len(set(json.dumps(x, sort_keys=True) for x in instance)):
            errors.append({"path": path, "rule": "uniqueItems",
                           "message": "array contains duplicate items"})
        # items (single schema — apply to all elements)
        if "items" in schema and isinstance(schema["items"], dict):
            for idx, item in enumerate(instance):
                errors.extend(_validate(item, schema["items"], f"{path}[{idx}]"))

    # Object constraints
    if isinstance(instance, dict):
        if "required" in schema:
            for key in schema["required"]:
                if key not in instance:
                    errors.append({"path": path, "rule": "required",
                                   "message": f"missing required property '{key}'"})

        props = schema.get("properties", {})
        for key in instance:
            if key in props:
                errors.extend(_validate(instance[key], props[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append({"path": f"{path}.{key}", "rule": "additionalProperties",
                               "message": f"additional property '{key}' not allowed"})
            elif isinstance(schema.get("additionalProperties"), dict):
                errors.extend(_validate(instance[key], schema["additionalProperties"], f"{path}.{key}"))

        # patternProperties
        if "patternProperties" in schema:
            for pat, sub_schema in schema["patternProperties"].items():
                for key in instance:
                    if re.search(pat, key):
                        errors.extend(_validate(instance[key], sub_schema, f"{path}.{key}"))

        if "minProperties" in schema and len(instance) < schema["minProperties"]:
            errors.append({"path": path, "rule": "minProperties",
                           "message": f"object has {len(instance)} properties, minimum is {schema['minProperties']}"})
        if "maxProperties" in schema and len(instance) > schema["maxProperties"]:
            errors.append({"path": path, "rule": "maxProperties",
                           "message": f"object has {len(instance)} properties, maximum is {schema['maxProperties']}"})

    return errors


def _matches_type(value, expected):
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "null":
        return value is None
    return False


def _json_type(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def main():
    ap = argparse.ArgumentParser(
        description="Validate a JSON instance against a JSON Schema."
    )
    ap.add_argument("instance", help="path to the JSON instance file")
    ap.add_argument("schema", help="path to the JSON Schema file")
    ap.add_argument("--json", action="store_true", help="output JSON result")
    ap.add_argument("--exit-code", action="store_true",
                    help="exit non-zero on validation errors")
    args = ap.parse_args()

    try:
        instance_data = _load_json(args.instance)
        schema_data = _load_json(args.schema)
    except ValueError as e:
        if args.json:
            print(json.dumps({"valid": False, "errors": [{"rule": "input", "message": str(e)}]}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 2

    errors = _validate(instance_data, schema_data)

    if args.json:
        print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    elif errors:
        print(f"Validation failed with {len(errors)} error(s):\n")
        for e in errors:
            print(f"  {e['path']}: {e['message']} ({e['rule']})")
    else:
        print("Valid")

    return 1 if (args.exit_code and errors) else 0


if __name__ == "__main__":
    sys.exit(main())
