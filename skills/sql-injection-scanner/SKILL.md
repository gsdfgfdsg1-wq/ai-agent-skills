---
name: sql-injection-scanner
description: Scan source code for potential SQL injection patterns including string concatenation, format strings, and unsafe ORM usage with JSON and CI support.
license: MIT
---

# SQL Injection Scanner

> Statically scan source code for common SQL injection patterns — string concatenation, format strings, f-strings, and unsafe ORM calls.

## When to Use / Triggers

- Security audit, find SQL injection risks before they reach production.
- Code review, flag potentially unsafe database query patterns.
- CI pipeline, enforce zero-tolerance for string-concatenated SQL.
- Onboarding, educate developers on safe SQL patterns.

## Capabilities

- Detects 8+ patterns: string concat SQL, format strings, f-strings, raw cursor.execute, unsafe ORM filters, etc.
- Supports Python, PHP, Java, JavaScript/TypeSQL patterns.
- `--severity` to filter by confidence level (high/medium/low).
- `--json` for machine-readable output.
- `--exit-code` for CI integration.
- Auto-skips binary files, `.git`, `node_modules`, etc.

## Usage

```bash
# Scan project
python skills/sql-injection-scanner/scripts/scan_sqli.py src/

# Only high confidence
python skills/sql-injection-scanner/scripts/scan_sqli.py src/ --severity high

# JSON output
python skills/sql-injection-scanner/scripts/scan_sqli.py . --json

# CI gate
python skills/sql-injection-scanner/scripts/scan_sqli.py . --exit-code
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/scan_sqli.py --help` for all options.
