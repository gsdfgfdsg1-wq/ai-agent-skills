---
name: json-schema-linter
description: Validate JSON files against a JSON Schema — supports type, required, properties, additionalProperties, enum, min/max, pattern, items, and nested objects using only the Python standard library.
license: MIT
---

# JSON Schema Linter

> Validate your JSON config, fixtures, and API responses against a schema — no pip install required.

## When to Use / Triggers

- Validate config files before deployment.
- Ensure API response fixtures conform to their contract.
- CI: reject PRs that break the JSON schema.
- Quick schema checks without setting up a full validation framework.

## Capabilities

- Practical JSON Schema Draft-07 subset: `type`, `required`, `properties`, `additionalProperties`, `enum`, `const`, `minimum`/`maximum`, `minLength`/`maxLength`, `pattern`, `items`, `minItems`/`maxItems`, `uniqueItems`, `minProperties`/`maxProperties`, `patternProperties`.
- Recursive validation of nested objects and arrays.
- Clear error paths (e.g., `$.users[0].name`).
- `--json` for programmatic output; `--exit-code` for CI.

## Usage

```bash
# Basic validation
python skills/json-schema-linter/scripts/lint_json_schema.py config.json schema.json

# CI mode
python skills/json-schema-linter/scripts/lint_json_schema.py data.json schema.json --exit-code

# JSON output
python skills/json-schema-linter/scripts/lint_json_schema.py config.json schema.json --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/lint_json_schema.py --help` for all options.
