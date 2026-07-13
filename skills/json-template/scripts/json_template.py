#!/usr/bin/env python3
"""Render JSON templates using values from a JSON variables object."""

import argparse
import json
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\s*\}\}")


def read_json(path, label):
    try:
        content = Path(path).read_text(encoding="utf-8")
    except OSError as error:
        raise ValueError(f"cannot read {label} '{path}': {error}") from error
    try:
        return json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {label} '{path}': {error.msg} at line {error.lineno}, column {error.colno}") from error


def resolve_path(variables, path):
    value = variables
    for segment in path.split("."):
        if not isinstance(value, dict) or segment not in value:
            raise ValueError(f"missing variable: {path}")
        value = value[segment]
    return value


def render_string(value, variables):
    full_match = PLACEHOLDER.fullmatch(value)
    if full_match:
        return resolve_path(variables, full_match.group(1))

    def replace(match):
        resolved = resolve_path(variables, match.group(1))
        if isinstance(resolved, (dict, list)):
            return json.dumps(resolved, ensure_ascii=False, separators=(",", ":"))
        if resolved is None:
            return "null"
        if isinstance(resolved, bool):
            return "true" if resolved else "false"
        return str(resolved)

    return PLACEHOLDER.sub(replace, value)


def render_value(value, variables):
    if isinstance(value, dict):
        return {key: render_value(item, variables) for key, item in value.items()}
    if isinstance(value, list):
        return [render_value(item, variables) for item in value]
    if isinstance(value, str):
        return render_string(value, variables)
    return value


def main():
    parser = argparse.ArgumentParser(
        description="Render {{ dotted.path }} placeholders in a JSON template."
    )
    parser.add_argument("template", help="Path to a JSON template")
    parser.add_argument("--variables", required=True, help="Path to a JSON variables object")
    parser.add_argument("--output", help="Write rendered JSON to this path instead of stdout")
    parser.add_argument("--json", action="store_true", help="Emit compact JSON")
    args = parser.parse_args()

    try:
        template = read_json(args.template, "template")
        variables = read_json(args.variables, "variables")
        if not isinstance(variables, dict):
            raise ValueError("variables JSON must be an object")
        rendered = render_value(template, variables)
        rendered_text = json.dumps(
            rendered,
            ensure_ascii=False,
            separators=(",", ":") if args.json else None,
            indent=None if args.json else 2,
        ) + "\n"
        if args.output:
            try:
                Path(args.output).write_text(rendered_text, encoding="utf-8")
            except OSError as error:
                raise ValueError(f"cannot write output '{args.output}': {error}") from error
        else:
            sys.stdout.write(rendered_text)
        return 0
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
