---
name: json-mask
description: Mask sensitive fields in JSON by key name patterns with configurable redaction strategies without external dependencies.
license: MIT
---

# JSON Mask

> Mask or redact sensitive fields in JSON data by key name patterns — supports exact match, prefix, suffix, regex, and nested dot-path targeting.

## When to Use / Triggers

- Sanitize JSON before logging or sharing.
- Redact PII (passwords, emails, phone numbers) from API responses.
- Prepare fixture data with sensitive values removed.

## Capabilities

- `mask`: mask sensitive fields in a JSON file or stdin.
- Supports strategies: `replace` (fixed string), `partial` (keep first/last chars), `hash` (SHA-256 prefix), `remove` (delete key).
- Key matching: exact, prefix, suffix, regex, dot-path.
- `--keys` specify field names to mask.
- `--json` machine-readable output.

## Usage

```bash
python skills/json-mask/scripts/json_mask.py mask --file data.json --keys password email
python skills/json-mask/scripts/json_mask.py mask --file data.json --keys "ssn" --strategy partial
python skills/json-mask/scripts/json_mask.py mask --file data.json --regex-keys ".*secret.*" --strategy hash
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/json_mask.py --help` for all options.
