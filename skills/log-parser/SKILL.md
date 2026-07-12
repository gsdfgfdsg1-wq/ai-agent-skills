---
name: log-parser
description: Parse and summarize log files by level and pattern — supports Python logging, Apache, nginx, and plain prefix formats with level filtering, regex matching, and JSON output.
license: MIT
---

# Log Parser

> Quickly sift through log files, count entries by severity, and filter by pattern — no grep wizardry required.

## When to Use / Triggers

- Investigating production incidents: count errors by level.
- CI: fail if any ERROR or CRITICAL logs appear in test output.
- Pre-rotate audit: summarize what's in a log before archiving.
- Monitoring prep: identify the noisiest log sources.

## Capabilities

- Detects log levels in Python logging, Apache, nginx, and plain-prefix formats.
- Filter by level (`--levels`) or regex pattern (`--pattern`).
- `--summary` for quick level counts; `--top N` to limit output.
- `--json` for machine-readable output.
- Auto-skips files over 10 MB.

## Usage

```bash
# Summarize all logs in a directory
python skills/log-parser/scripts/parse_logs.py /var/log/app/ --summary

# Show only errors
python skills/log-parser/scripts/parse_logs.py app.log --levels error,critical

# Pattern filter
python skills/log-parser/scripts/parse_logs.py app.log --pattern "timeout|refused"
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/parse_logs.py --help` for all options.
