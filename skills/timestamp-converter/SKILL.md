---
name: timestamp-converter
description: Convert between Unix timestamps, ISO 8601, and human-readable date formats without external dependencies.
license: MIT
---

# Timestamp Converter

> Convert between Unix timestamps, ISO 8601, and human-readable dates.

## When to Use / Triggers
- Convert a Unix epoch to an ISO 8601 date string.
- Parse an ISO 8601 string to a Unix timestamp.
- Get current time in multiple formats.

## Capabilities
- `from_unix`: convert Unix timestamp to ISO 8601 / readable date.
- `from_iso`: convert ISO 8601 string to Unix timestamp.
- `now`: show current time in all formats.
- `--tz` for timezone offset (e.g. +8 for CST).
- `--json` for machine-readable output.

## Usage
```bash
python skills/timestamp-converter/scripts/timestamp_converter.py from_unix -t 1700000000
python skills/timestamp-converter/scripts/timestamp_converter.py from_iso -s '2023-11-14T22:13:20Z'
python skills/timestamp-converter/scripts/timestamp_converter.py now --tz +8
```

## Examples
See `examples/usage.md`.

## Reference
Run `scripts/timestamp_converter.py --help` for all options.
