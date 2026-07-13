---
name: csv-filter
description: Filter CSV rows by column value conditions with comparison operators and regex matching without external dependencies.
license: MIT
---

# CSV Filter

> Filter CSV rows by column value conditions — equality, comparison, regex, and null checks without external dependencies.

## When to Use / Triggers

- Extract rows matching specific column values from CSV.
- Filter log exports or data dumps by criteria.
- Build data pipelines with CSV filtering steps.

## Capabilities

- `filter`: filter rows by column conditions.
- Supports operators: `eq`, `ne`, `gt`, `lt`, `gte`, `lte`, `contains`, `regex`, `empty`, `notempty`.
- Multiple conditions combined with AND logic.
- `--output` write to file instead of stdout.
- `--json` machine-readable output.

## Usage

```bash
python skills/csv-filter/scripts/csv_filter.py filter --file data.csv --column "status" --op eq --value "active"
python skills/csv-filter/scripts/csv_filter.py filter --file data.csv --column "age" --op gt --value "25"
python skills/csv-filter/scripts/csv_filter.py filter --file data.csv --column "name" --op regex --value "^J"
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/csv_filter.py --help` for all options.
