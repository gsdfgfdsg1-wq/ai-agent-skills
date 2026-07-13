---
name: http-status-codes
description: Look up common HTTP response status codes by code, category, or keyword with optional JSON output.
license: MIT
---

# HTTP Status Codes

> Query a built-in reference of common HTTP response status codes without network access or third-party packages.

## When to Use / Triggers

- Identify the meaning of an HTTP response code during debugging.
- Browse a response category such as 4xx client errors or 5xx server errors.
- Search for codes related to terms such as `timeout`, `redirect`, or `authentication`.
- Return structured status-code data for scripts or CI tooling.

## Capabilities

- Built-in reference for widely used informational, success, redirect, client-error, and server-error codes.
- Exact lookup with `--code`.
- Category filtering from `1xx` through `5xx` with `--category`.
- Case-insensitive keyword search across codes, phrases, categories, and descriptions.
- `--json` output using only the Python standard library.

## Usage

```bash
# Look up one code
python skills/http-status-codes/scripts/http_status_codes.py --code 404

# List server errors
python skills/http-status-codes/scripts/http_status_codes.py --category 5xx

# Search by keyword and return JSON
python skills/http-status-codes/scripts/http_status_codes.py --search timeout --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/http_status_codes.py --help` for all options.
