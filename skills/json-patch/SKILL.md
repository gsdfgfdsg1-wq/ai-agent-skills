---
name: json-patch
description: Apply RFC 6902 JSON Patch operations (add, remove, replace, move, copy, test) without external dependencies.
license: MIT
---

# JSON Patch

> Apply RFC 6902 JSON Patch operations to JSON documents with validation and dry-run support.

## When to Use / Triggers

- Apply JSON Patch operations to configuration files.
- Validate patch operations before applying.
- Transform JSON documents programmatically.
- Implement delta-based updates.

## Capabilities

- `apply`: apply a JSON Patch to a document.
- `validate`: validate patch operations without applying.
- `--dry-run` show what would change without modifying.
- `--output` write result to file.
- `--json` machine-readable output.

## Usage

```bash
python skills/json-patch/scripts/json_patch.py apply --doc data.json --patch patch.json
python skills/json-patch/scripts/json_patch.py validate --patch patch.json
python skills/json-patch/scripts/json_patch.py apply --doc data.json --patch patch.json --dry-run
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/json_patch.py --help` for all options.
