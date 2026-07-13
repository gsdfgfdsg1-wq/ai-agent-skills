---
name: toml-linter
description: Lint and validate TOML configuration files for common issues without external dependencies.
license: MIT
---

# TOML Linter

> Validate and lint TOML files for syntax errors, common issues, and best practices.

## When to Use / Triggers

- Validate TOML config files (pyproject.toml, Cargo.toml, etc.).
- Check TOML for common mistakes.
- Enforce TOML best practices.

## Capabilities

- `lint`: validate and check a TOML file.
- Checks: syntax validity, duplicate keys, mixed array types, missing required sections (pyproject.toml), etc.
- `--type` hint for known formats (pyproject, cargo, generic).
- `--json` machine-readable output.

## Usage

```bash
python skills/toml-linter/scripts/toml_linter.py lint --file pyproject.toml
python skills/toml-linter/scripts/toml_linter.py lint --file Cargo.toml --type cargo --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/toml_linter.py --help` for all options.
