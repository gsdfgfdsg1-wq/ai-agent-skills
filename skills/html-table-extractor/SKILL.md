---
name: html-table-extractor
description: Extract table data from HTML files and convert to CSV or JSON without external dependencies.
license: MIT
---

# HTML Table Extractor

> Extract tables from HTML files and output as CSV or JSON with row/column indexing and multi-table support.

## When to Use / Triggers

- Extract tabular data from HTML pages or reports.
- Convert HTML tables to CSV for spreadsheet import.
- Programmatically access HTML table data as JSON.
- Scrape structured data from web pages saved locally.

## Capabilities

- `extract`: extract all tables from an HTML file.
- `--format` output format: csv, json (default: csv).
- `--table` extract a specific table by index (0-based).
- `--output` write to file instead of stdout.
- `--headers` include header row (default: auto-detect).

## Usage

```bash
python skills/html-table-extractor/scripts/html_table.py extract --file page.html
python skills/html-table-extractor/scripts/html_table.py extract --file page.html --format json --table 0
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/html_table.py --help` for all options.
