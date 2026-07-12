---
name: csv-to-json
description: Convert CSV files to JSON with automatic type inference and flexible delimiter support without external dependencies.
license: MIT
---

# csv-to-json

Convert CSV files to JSON arrays of objects using the first row as keys. Supports automatic type inference, custom delimiters, and flexible output options — all with zero external dependencies.

## When to Use

- You need to convert CSV data to JSON for API consumption, web applications, or data pipelines.
- You want automatic detection of integers, floats, booleans, and null values instead of treating everything as strings.
- You are working with tab-separated, semicolon-separated, or other non-comma-delimited files.
- You need a lightweight, dependency-free conversion tool that runs on any standard Python installation.
- You want structured stats about the conversion (row count, column count, type distribution) for logging or monitoring.
- You need to handle edge cases like empty CSVs, header-only files, or files with encoding issues.

## Capabilities

- **CSV to JSON conversion**: First row is used as object keys; each subsequent row becomes a JSON object.
- **Automatic type inference**: Detects integers, floats, booleans (`true`/`false`/`yes`/`no`), and null values (empty strings or the literal `"null"`).
- **Custom delimiters**: Supports comma (default), tab, semicolon, pipe, or any single-character delimiter.
- **Output flexibility**: Write to a file or stdout; optional pretty-printed JSON output.
- **Stats reporting**: Optional `--json` flag outputs conversion statistics as a JSON object.
- **No-infer mode**: `--no-infer` flag keeps all values as strings when type detection is not desired.
- **Robust error handling**: Graceful messages for file-not-found, empty CSV, header-only CSV, and encoding errors.
- **Zero dependencies**: Uses only Python standard library modules (`csv`, `json`, `argparse`, `sys`, `os`).

## Usage

```
python scripts/csv_to_json.py --file <CSV_PATH> [OPTIONS]
```

### Options

| Option          | Default  | Description                                          |
|-----------------|----------|------------------------------------------------------|
| `--file`        | required | Path to the input CSV file                           |
| `--output`      | stdout   | Path to the output JSON file                         |
| `--delimiter`   | `,`      | Single-character field delimiter                     |
| `--no-infer`    | off      | Disable type inference; keep all values as strings   |
| `--pretty`      | off      | Pretty-print the JSON output with indentation        |
| `--json`        | off      | Output conversion statistics as a JSON object        |

Run `python scripts/csv_to_json.py --help` for full usage information.

## Examples

### Basic conversion

```bash
python scripts/csv_to_json.py --file data.csv
```

### Pretty-printed output to a file

```bash
python scripts/csv_to_json.py --file data.csv --output result.json --pretty
```

### Tab-separated file with stats

```bash
python scripts/csv_to_json.py --file data.tsv --delimiter "\t" --json
```

### Keep all values as strings

```bash
python scripts/csv_to_json.py --file data.csv --no-infer
```

## Reference

### Type Inference Rules

When type inference is enabled (default), values are converted in the following order:

1. **Null**: empty string or literal `"null"` → JSON `null`
2. **Boolean**: `true`, `false`, `yes`, `no` (case-insensitive) → JSON `true` / `false`
3. **Integer**: strings matching `^-?\d+$` → JSON integer
4. **Float**: strings matching `^-?\d+\.\d+$` → JSON float
5. **String**: everything else remains a string

When `--no-infer` is set, all values remain strings except empty strings and `"null"`, which still become `null`.

### Exit Codes

| Code | Meaning                        |
|------|--------------------------------|
| 0    | Successful conversion          |
| 1    | Input file not found           |
| 2    | Empty CSV (0 bytes / no rows)  |
| 3    | CSV contains only headers      |
| 4    | Encoding error                 |

### Dependencies

None. The script uses only Python standard library modules: `csv`, `json`, `argparse`, `sys`, `os`.
