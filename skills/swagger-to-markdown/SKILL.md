---
name: swagger-to-markdown
description: Convert Swagger/OpenAPI 2.0 JSON specifications to human-readable Markdown documentation without external dependencies.
license: MIT
---

# Swagger to Markdown

> Turn Swagger 2.0 specs into clean Markdown — no Node.js or external tools needed.

## When to Use / Triggers

- Generate readable API documentation from Swagger 2.0 JSON.
- Convert legacy Swagger specs (OpenAPI 2.0) before migrating to OpenAPI 3.
- CI: auto-generate docs on spec changes.
- Review API contracts in a human-friendly format.

## Capabilities

- Parses Swagger 2.0 JSON (info, paths, definitions, parameters, security).
- Documents endpoints with method, path, description, parameters, responses.
- Resolves `$ref` references to definitions and parameters.
- `--output` to write to a file (default: stdout).
- `--include-models` to include full model definitions section.

## Usage

```bash
python skills/swagger-to-markdown/scripts/swagger_to_markdown.py swagger.json
python skills/swagger-to-markdown/scripts/swagger_to_markdown.py api.json --output docs.md --include-models
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/swagger_to_markdown.py --help` for all options.
