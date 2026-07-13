---
name: ini-parser
description: Parse, validate, and query INI configuration files without external dependencies.
license: MIT
---

# INI Parser

> Parse, validate, and query INI configuration files with section/key lookup and diff support.

## When to Use / Triggers

- Parse INI config files for programmatic access.
- Validate INI files for syntax errors.
- Query specific sections or keys from INI configs.

## Capabilities

- `parse`: parse and display an INI file.
- `get`: get a specific key value from a section.
- `keys`: list all keys in a section.
- `sections`: list all sections.
- `--json` machine-readable output.
- `--strict` flag duplicate keys as errors.

## Usage

```bash
python skills/ini-parser/scripts/ini_parser.py parse --file config.ini
python skills/ini-parser/scripts/ini_parser.py get --file config.ini --section database --key host
python skills/ini-parser/scripts/ini_parser.py sections --file config.ini
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/ini_parser.py --help` for all options.
