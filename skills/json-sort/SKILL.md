---
name: json-sort
description: Recursively sort JSON object keys alphabetically without external dependencies.
license: MIT
---

# JSON Sort

> Recursively sort JSON object keys alphabetically for consistent, diffable output.

## When to Use / Triggers

- Sort JSON keys for consistent, version-control-friendly output.
- Normalize JSON config files for comparison.
- Prepare JSON for deterministic hashing or diffing.

## Capabilities

- `sort`: sort JSON keys recursively.
- `--reverse` sort keys in descending order.
- `--depth` limit recursion depth.
- `--inplace` overwrite the input file.
- `--json` output as formatted JSON.
- Reads from file or stdin.

## Usage

```bash
python skills/json-sort/scripts/json_sort.py sort --file config.json
python skills/json-sort/scripts/json_sort.py sort --file data.json --reverse
cat data.json | python skills/json-sort/scripts/json_sort.py sort
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/json_sort.py --help` for all options.
