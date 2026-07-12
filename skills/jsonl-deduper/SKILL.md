---
name: jsonl-deduper
description: This skill should be used when removing duplicate JSONL records by a specified dotted object key while keeping either the first or last occurrence and producing JSON statistics.
agent_created: true
---

# JSONL Deduper

Deduplicate a JSON Lines file with a deterministic standard-library Python script. Apply this skill before imports, exports, backfills, or data handoffs where records must be unique by a nested object key.

## Workflow

1. Identify the dotted object key that defines record identity, such as `id` or `customer.email`.
2. Run `scripts/dedupe_jsonl.py INPUT.jsonl OUTPUT.jsonl --key KEY`.
3. Use `--keep first` to preserve the earliest occurrence, or `--keep last` to preserve the latest occurrence while retaining output order by the kept record's original position.
4. Pass `--stats-json STATS.json` to persist structured counts. The script also writes the same statistics JSON to standard output.
5. Treat exit code `0` as success and `2` as an argument, input, or JSONL-shape error. The script never silently skips malformed rows or missing keys.

## Dotted Key Rules

Split the key on dots and require each segment to be non-empty. Resolve every segment through JSON objects only; array indexing is not supported. Treat the resolved JSON value as an identity using a canonical JSON representation, so strings, numbers, booleans, null, arrays, and objects remain type-distinct where JSON permits.

The output file is written only after all input rows are successfully validated. This prevents a partially written output when a later line is invalid. See [examples/usage.md](examples/usage.md) for commands and output statistics. Run `scripts/dedupe_jsonl.py --help` for all options.

## Statistics

Report `input_records`, `output_records`, `duplicates_removed`, `key`, and `keep`. Count non-empty lines only; empty lines are ignored.
