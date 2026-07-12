---
name: cron-validator
description: Validate standard 5-field and 6-field cron expressions, check field ranges and syntax, and compute next execution times without external dependencies.
license: MIT
---

# Cron Validator

> Validate cron expressions and preview their next fire times — catch mistakes before they reach production.

## When to Use / Triggers

- Verify cron schedules in config files before deployment.
- Debug why a cron job isn't running as expected.
- Document cron expressions with concrete next-run timestamps.
- CI check: reject invalid cron expressions in config PRs.

## Capabilities

- Supports standard 5-field (min hour dom month dow) and 6-field (sec min hour dom month dow) cron.
- Day-of-week names (MON–SUN) and month names (JAN–DEC).
- Ranges, steps, and lists (e.g., `1-15/2`, `MON-FRI`).
- `--next N` to compute the next N execution times.
- `--json` for machine-readable output.

## Usage

```bash
# Validate expression
python skills/cron-validator/scripts/validate_cron.py "0 9 * * MON-FRI"

# Show next 5 runs
python skills/cron-validator/scripts/validate_cron.py "*/15 * * * *" --next 5

# JSON output
python skills/cron-validator/scripts/validate_cron.py "0 0 1 1 *" --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/validate_cron.py --help` for all options.
