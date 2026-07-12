---
name: yaml-linter
description: Check YAML files for common issues — tabs in indentation, trailing whitespace, inconsistent indent, duplicate keys, missing document markers, long lines, and colon spacing — without a full parser or external dependencies.
license: MIT
---

# YAML Linter

> A zero-dependency YAML linting tool that catches the most common YAML pitfalls without needing a full parser.

## When to Use / Triggers

- Validate YAML config files (Kubernetes, CI, docker-compose) before committing.
- CI pipeline needs a fast YAML linter with no external dependencies.
- Debug YAML parsing failures by catching structural issues early.
- Code review: flag common YAML anti-patterns automatically.

## Capabilities

- 7 built-in rules: tab indentation (Y001), trailing whitespace (Y002), long lines (Y003), inconsistent indent (Y004), duplicate keys (Y005), colon spacing (Y006), missing document start (Y007).
- Works on `.yaml` and `.yml` files.
- `--json` machine-readable output; `--severity` filter; `--exit-code` for CI.

## Usage

```bash
# Check all YAML files in project
python skills/yaml-linter/scripts/lint_yaml.py .

# Only errors and warnings
python skills/yaml-linter/scripts/lint_yaml.py config/ --severity warning

# CI mode
python skills/yaml-linter/scripts/lint_yaml.py . --exit-code --severity warning

# JSON output
python skills/yaml-linter/scripts/lint_yaml.py docker-compose.yml --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/lint_yaml.py --help` for all options.
