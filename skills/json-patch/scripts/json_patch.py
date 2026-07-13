#!/usr/bin/env python3
"""Apply RFC 6902 JSON Patch operations without external dependencies."""

import argparse
import copy
import json
import sys
from pathlib import Path


def resolve_path(doc, path):
    """Resolve a JSON Pointer (RFC 6901) to get a value."""
    if path == "":
        return doc
    tokens = path.split("/")
    # First token should be empty (absolute path starts with /)
    if tokens and tokens[0] == "":
        tokens = tokens[1:]
    current = doc
    for token in tokens:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                raise KeyError(f"Key '{token}' not found at path '{path}'")
            current = current[token]
        elif isinstance(current, list):
            try:
                idx = int(token)
            except ValueError:
                raise KeyError(f"Invalid array index '{token}' at path '{path}'")
            if idx < 0 or idx >= len(current):
                raise KeyError(f"Array index {idx} out of range at path '{path}'")
            current = current[idx]
        else:
            raise KeyError(f"Cannot traverse into {type(current).__name__} at path '{path}'")
    return current


def set_path(doc, path, value):
    """Set a value at a JSON Pointer path, creating intermediate dicts."""
    tokens = path.split("/")
    if tokens and tokens[0] == "":
        tokens = tokens[1:]
    if not tokens:
        return value
    current = doc
    for i, token in enumerate(tokens[:-1]):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                current[token] = {}
            current = current[token]
        elif isinstance(current, list):
            idx = int(token)
            current = current[idx]
        else:
            raise KeyError(f"Cannot traverse into {type(current).__name__}")
    last = tokens[-1].replace("~1", "/").replace("~0", "~")
    if isinstance(current, dict):
        current[last] = value
    elif isinstance(current, list):
        idx = int(last) if last != "-" else len(current)
        if last == "-":
            current.append(value)
        else:
            current[idx] = value
    return doc


def remove_path(doc, path):
    """Remove a value at a JSON Pointer path."""
    tokens = path.split("/")
    if tokens and tokens[0] == "":
        tokens = tokens[1:]
    if not tokens:
        raise ValueError("Cannot remove root")
    current = doc
    for token in tokens[:-1]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            current = current[token]
        elif isinstance(current, list):
            current = current[int(token)]
    last = tokens[-1].replace("~1", "/").replace("~0", "~")
    if isinstance(current, dict):
        del current[last]
    elif isinstance(current, list):
        del current[int(last)]
    return doc


def op_add(doc, op):
    """RFC 6902 add operation."""
    path = op["path"]
    value = op.get("value")
    if path == "":
        return value
    tokens = path.split("/")
    if tokens and tokens[0] == "":
        tokens = tokens[1:]
    current = doc
    for token in tokens[:-1]:
        token = token.replace("~1", "/").replace("~0", "~")
        current = current[token] if isinstance(current, dict) else current[int(token)]
    last = tokens[-1].replace("~1", "/").replace("~0", "~")
    if isinstance(current, dict):
        current[last] = value
    elif isinstance(current, list):
        idx = len(current) if last == "-" else int(last)
        current.insert(idx, value)
    return doc


def op_remove(doc, op):
    """RFC 6902 remove operation."""
    return remove_path(doc, op["path"])


def op_replace(doc, op):
    """RFC 6902 replace operation."""
    resolve_path(doc, op["path"])  # verify exists
    set_path(doc, op["path"], op["value"])
    return doc


def op_move(doc, op):
    """RFC 6902 move operation."""
    value = resolve_path(doc, op["from"])
    doc = remove_path(doc, op["from"])
    return op_add(doc, {"op": "add", "path": op["path"], "value": value})


def op_copy(doc, op):
    """RFC 6902 copy operation."""
    value = copy.deepcopy(resolve_path(doc, op["from"]))
    return op_add(doc, {"op": "add", "path": op["path"], "value": value})


def op_test(doc, op):
    """RFC 6902 test operation."""
    actual = resolve_path(doc, op["path"])
    expected = op["value"]
    if actual != expected:
        raise ValueError(f"Test failed at '{op['path']}': expected {json.dumps(expected)}, got {json.dumps(actual)}")
    return doc


OPERATIONS = {
    "add": op_add,
    "remove": op_remove,
    "replace": op_replace,
    "move": op_move,
    "copy": op_copy,
    "test": op_test,
}


def apply_patch(doc, patch_ops):
    """Apply a sequence of RFC 6902 operations to a document."""
    doc = copy.deepcopy(doc)
    for op in patch_ops:
        op_name = op.get("op")
        if op_name not in OPERATIONS:
            raise ValueError(f"Unknown operation: {op_name}")
        if "path" not in op:
            raise ValueError(f"Missing 'path' in operation: {op}")
        doc = OPERATIONS[op_name](doc, op)
    return doc


def validate_patch(patch_ops):
    """Validate patch operations structure without applying."""
    errors = []
    for i, op in enumerate(patch_ops):
        op_name = op.get("op")
        if not op_name:
            errors.append(f"Op {i}: missing 'op'")
            continue
        if op_name not in OPERATIONS:
            errors.append(f"Op {i}: unknown op '{op_name}'")
            continue
        if "path" not in op:
            errors.append(f"Op {i}: missing 'path'")
        if op_name in ("add", "replace", "test") and "value" not in op:
            errors.append(f"Op {i}: op '{op_name}' requires 'value'")
        if op_name in ("move", "copy") and "from" not in op:
            errors.append(f"Op {i}: op '{op_name}' requires 'from'")
    return errors


def load_json(filepath):
    """Load a JSON file."""
    try:
        return json.loads(Path(filepath).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"Error: cannot read {filepath}: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_apply(args):
    doc = load_json(args.doc)
    patch = load_json(args.patch)

    if not isinstance(patch, list):
        print("Error: patch must be a JSON array of operations", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        try:
            result = apply_patch(doc, patch)
            if args.json:
                print(json.dumps({"dry_run": True, "result": result}, indent=2, ensure_ascii=False))
            else:
                print("Dry run OK. Result would be:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
        except (KeyError, ValueError, IndexError) as e:
            print(f"Dry run FAILED: {e}", file=sys.stderr)
            sys.exit(1)
        return

    try:
        result = apply_patch(doc, patch)
    except (KeyError, ValueError, IndexError) as e:
        print(f"Error applying patch: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Written to {args.output}")
    elif args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_validate(args):
    patch = load_json(args.patch)
    if not isinstance(patch, list):
        print("Error: patch must be a JSON array", file=sys.stderr)
        sys.exit(1)
    errors = validate_patch(patch)
    if errors:
        print(f"Validation FAILED: {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"Validation PASSED: {len(patch)} operation(s) OK")


def main():
    parser = argparse.ArgumentParser(description="Apply RFC 6902 JSON Patch operations.")
    sub = parser.add_subparsers(dest="command")

    p_apply = sub.add_parser("apply", help="Apply patch to document")
    p_apply.add_argument("--doc", required=True, help="Input JSON document")
    p_apply.add_argument("--patch", required=True, help="JSON Patch file")
    p_apply.add_argument("--output", help="Output file")
    p_apply.add_argument("--dry-run", action="store_true", help="Preview without applying")
    p_apply.add_argument("--json", action="store_true", help="JSON output")

    p_val = sub.add_parser("validate", help="Validate patch file structure")
    p_val.add_argument("--patch", required=True, help="JSON Patch file")

    args = parser.parse_args()
    if args.command == "apply":
        cmd_apply(args)
    elif args.command == "validate":
        cmd_validate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
