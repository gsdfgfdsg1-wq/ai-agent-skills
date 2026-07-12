---
name: gzip-toolkit
description: Compress and decompress files with gzip, inspect archive metadata, and test integrity without external dependencies.
license: MIT
---

# gzip-toolkit

A self-contained Python toolkit for gzip compression, decompression, metadata inspection, and integrity testing. Uses only the Python standard library — no external dependencies required.

## When to Use

- Compress files to `.gz` format with configurable compression level
- Decompress `.gz` archives back to their original content
- Inspect gzip header metadata (original size, compressed size, ratio, modification time)
- Verify gzip file integrity without extracting
- Automate gzip operations in CI/CD pipelines or scripts (with `--json` output for machine parsing)
- Handle gzip tasks on systems where only Python is available

## Capabilities

| Subcommand | Description |
|---|---|
| `compress` | Compress a file to `.gz` with adjustable compression level (1-9) |
| `decompress` | Decompress a `.gz` file back to the original file |
| `inspect` | Read gzip header and report original size, compressed size, ratio, and mtime |
| `test` | Verify gzip file integrity by attempting decompression |

All subcommands support a `--json` flag for structured JSON output, making them suitable for programmatic use.

## Usage

```bash
python gzip_toolkit.py compress --file INPUT [--output PATH] [--level N] [--json]
python gzip_toolkit.py decompress --file INPUT [--output PATH] [--json]
python gzip_toolkit.py inspect --file INPUT [--json]
python gzip_toolkit.py test --file INPUT [--json]
```

### Common Options

| Option | Description |
|---|---|
| `--file PATH` | Input file path (required for all subcommands) |
| `--output PATH` | Output file path (optional; defaults vary by subcommand) |
| `--level N` | Compression level 1-9, default 6 (`compress` only) |
| `--json` | Output results as JSON instead of human-readable text |

## Examples

### Compress a file

```bash
python gzip_toolkit.py compress --file data.csv
```

### Compress with maximum compression

```bash
python gzip_toolkit.py compress --file data.csv --level 9 --output archive/data.csv.gz
```

### Decompress a gzip file

```bash
python gzip_toolkit.py decompress --file data.csv.gz
```

### Inspect gzip metadata

```bash
python gzip_toolkit.py inspect --file data.csv.gz
```

### Test integrity

```bash
python gzip_toolkit.py test --file data.csv.gz --json
```

## Reference

- Uses `gzip` module for compression/decompression and integrity testing
- Uses `struct` module to parse gzip header fields (modification time, OS byte)
- Uses `argparse` for CLI argument parsing with subcommands
- All error conditions return a non-zero exit code and a descriptive message
- JSON output includes a `"success"` boolean field for easy scripting
