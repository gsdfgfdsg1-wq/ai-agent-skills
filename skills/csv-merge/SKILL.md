---
name: csv-merge
description: Merge multiple CSV files by a common key column without external dependencies.
license: MIT
---

# CSV Merge

> Merge (join) multiple CSV files on a shared key column, supporting inner, left, and outer joins.

## When to Use / Triggers

- Combine data from multiple CSV sources.
- Join tables by a common column (like SQL JOIN).
- Merge reports with a shared ID column.

## Capabilities

- `merge`: merge CSV files on a key column.
- `--key` specify the join column name (required).
- `--how` join type: inner (default), left, outer.
- `--output` write result to a file.
- `--json` output as JSON.

## Usage

```bash
python skills/csv-merge/scripts/csv_merge.py merge --key id --files a.csv b.csv
python skills/csv-merge/scripts/csv_merge.py merge --key email --how left --files users.csv orders.csv --output merged.csv
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/csv_merge.py --help` for all options.
