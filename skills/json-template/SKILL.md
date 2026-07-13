---
name: json-template
description: Safely replace {{ dotted.path }} placeholders in a parsed JSON template using values from a JSON object, without external dependencies.
license: MIT
---

# json-template

Render a JSON template using values from a separate JSON variables file. Templates are parsed before rendering, so the rendered result is always serialized as valid JSON.

## When to Use

- Generate JSON configuration from environment-specific variables.
- Replace nested values such as `{{ service.host }}` in a JSON document.
- Preserve numbers, booleans, arrays, objects, and null values for placeholders that occupy an entire JSON string.
- Validate that all required variables exist before producing output.

## Capabilities

| Capability | Description |
|---|---|
| Dotted paths | Resolves placeholders like `{{ user.profile.name }}` from nested objects. |
| Type preservation | A string containing only one placeholder becomes the original JSON value type. |
| Inline replacement | Interpolates values into larger strings, including JSON representations for arrays and objects. |
| Missing-value errors | Fails with status `1` and the unresolved dotted path. |
| JSON validation | Rejects invalid template or variables JSON, and always emits serialized JSON. |
| Output control | Prints JSON by default, writes with `--output`, and supports compact `--json` output. |
| Zero dependencies | Uses only `argparse`, `json`, `pathlib`, `re`, and `sys`. |

## Usage

```bash
python scripts/json_template.py TEMPLATE --variables VARIABLES [--output PATH] [--json]
```

| Option | Description |
|---|---|
| `TEMPLATE` | Path to the JSON template file. |
| `--variables PATH` | Required path to a JSON object containing variables. |
| `--output PATH` | Write rendered JSON to this file instead of stdout. |
| `--json` | Emit compact JSON rather than indented JSON. |

## Examples

Render a template to stdout:

```bash
python scripts/json_template.py config.template.json --variables values.json
```

Write compact output:

```bash
python scripts/json_template.py config.template.json --variables values.json --output config.json --json
```

For a template value of `"port": "{{ service.port }}"`, a numeric `service.port` variable produces a JSON number. For `"url": "https://{{ service.host }}/v1"`, the variable is interpolated into the surrounding string.

## Reference

- Placeholder syntax is `{{ dotted.path }}`. Each path segment must start with a letter or underscore and may contain letters, digits, or underscores.
- Variables must be a JSON object. Array indexing is intentionally not supported in dotted paths.
- A placeholder that fills an entire JSON string preserves the source variable type.
- Missing variables and invalid JSON input cause a non-zero exit status. Because rendering operates on parsed JSON and serializes the result, emitted output is valid JSON.
- See `examples/usage.md` for complete examples.
