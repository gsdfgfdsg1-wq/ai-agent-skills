---
name: csv-schema-audit
description: This skill should be used when auditing CSV headers and null values against a small JSON column schema, including required columns and duplicate-header detection.
agent_created: true
---

# CSV Schema Audit

Audit a CSV file deterministically with a standard-library Python script. Apply this skill to ingestion checks, CI validation, or pre-import reviews where a full JSON Schema implementation is unnecessary.

## Workflow

1. Create a small schema JSON file with `required_columns` and optional `columns` nullability rules.
2. Run `scripts/audit_csv.py CSV_FILE SCHEMA_FILE`.
3. Treat exit code `0` as a passing audit, `1` as one or more CSV schema violations, and `2` as an invalid argument, schema, or unreadable/malformed input.
4. Pass `--json` for structured output suitable for CI or another program.

## Schema Format

Use a JSON object with these optional fields:

- `required_columns`: an array of unique column-name strings that must occur in the header.
- `columns`: an object keyed by column name. Each value is an object with `nullable`, a boolean. Set it to `false` to reject empty cells in that column; omit the rule or set it to `true` to permit empty cells.

Treat a cell containing only whitespace as null. Audit every data row after the header. Detect duplicate header names independently of the schema. Report rows as one-based CSV line numbers, where the header is line 1.

See [examples/usage.md](examples/usage.md) for a schema, commands, and expected behavior. Run `scripts/audit_csv.py --help` for all options.

## Limits

Keep this format intentionally focused. It validates column presence, exact duplicate headers, and nullability only. It does not infer types, rename columns, or modify the CSV.
