---
name: envdoc
description: Generate documentation from .env files with variable names, defaults, and comments without external dependencies.
license: MIT
---

# Dotenv Documentation Generator

> Parse .env files and generate Markdown documentation with variable names, default values, descriptions, and required/optional status.

## When to Use / Triggers

- Document environment variables for team onboarding.
- Generate .env.example with inline descriptions.
- Audit which env vars are required vs optional.
- Keep documentation in sync with .env files.

## Capabilities

- `generate`: generate Markdown docs from a .env file.
- `example`: generate .env.example with comments.
- `audit`: check for missing required variables.
- `--required` mark variables as required (comma-separated list).
- `--output` write to file.

## Usage

```bash
python skills/envdoc/scripts/envdoc.py generate --file .env
python skills/envdoc/scripts/envdoc.py example --file .env --output .env.example
python skills/envdoc/scripts/envdoc.py audit --file .env --required DB_HOST,API_KEY
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/envdoc.py --help` for all options.
