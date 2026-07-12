---
name: dotenv-comparator
description: Compare two .env files and report added, removed, and changed keys with value diff output without external dependencies.
license: MIT
---

# Dotenv Comparator

> Compare .env files across environments — spot missing, extra, and changed variables instantly.

## When to Use / Triggers

- Compare .env.development vs .env.production before deployment.
- Audit which environment variables differ between staging and production.
- CI: ensure .env.example covers all keys used in .env.
- Onboard new developers: check their .env against the template.

## Capabilities

- Parses standard KEY=VALUE .env format (ignores comments and blank lines).
- Reports: added keys (in file B only), removed keys (in file A only), changed values.
- `--ignore-values` to only compare key names, not values.
- `--json` for machine-readable output.
- `--strict` exit code: non-zero if any differences found.

## Usage

```bash
python skills/dotenv-comparator/scripts/dotenv_comparator.py .env.dev .env.prod
python skills/dotenv-comparator/scripts/dotenv_comparator.py .env.example .env --ignore-values --json
python skills/dotenv-comparator/scripts/dotenv_comparator.py .env.staging .env.production --strict
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/dotenv_comparator.py --help` for all options.
