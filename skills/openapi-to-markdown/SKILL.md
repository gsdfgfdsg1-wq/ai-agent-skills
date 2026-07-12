---
name: openapi-to-markdown
description: Convert OpenAPI 3 JSON specifications to human-readable Markdown documentation — covers info, servers, endpoints, parameters, request/response schemas, and component definitions without external dependencies.
license: MIT
---

# OpenAPI to Markdown

> Turn your OpenAPI spec into readable Markdown docs — no renderers, no plugins, just text.

## When to Use / Triggers

- Generate API documentation from an OpenAPI spec for a README or wiki.
- Review API changes by diffing the generated Markdown.
- Create lightweight API references without setting up Swagger UI.
- CI: auto-generate docs on spec changes.

## Capabilities

- Parses OpenAPI 3.0 JSON (YAML needs prior conversion).
- Generates Markdown with info, servers, endpoints grouped by tag, parameters, request/response bodies, and component schemas.
- `--tag` to filter by tag; `--include-schemas` for component definitions.
- `--output` to write to file; defaults to stdout.
- Resolves `$ref` pointers within the spec.

## Usage

```bash
# Generate docs to stdout
python skills/openapi-to-markdown/scripts/openapi2md.py api.json

# Write to file
python skills/openapi-to-markdown/scripts/openapi2md.py api.json -o API.md

# Filter by tag
python skills/openapi-to-markdown/scripts/openapi2md.py api.json --tag users

# Include schema definitions
python skills/openapi-to-markdown/scripts/openapi2md.py api.json --include-schemas
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/openapi2md.py --help` for all options.
