---
name: mime-type-checker
description: Detect file MIME types from content and extension with a built-in mapping database without external dependencies.
license: MIT
---

# mime-type-checker

A zero-dependency Python tool for detecting and looking up file MIME types. Uses both file extension mapping and content magic-byte analysis for accurate detection.

## When to Use

- You need to determine the MIME type of a file by inspecting its actual content (not just the extension).
- You want to look up the MIME type for a given file extension (e.g., what MIME type does `.py` map to?).
- You need to find all known file extensions for a given MIME type (e.g., what extensions correspond to `application/json`?).
- You are validating uploaded files and want to cross-check the extension against the real content type.
- You need MIME type information in CI/CD scripts or automation pipelines without installing third-party packages.
- You want a lightweight, stdlib-only alternative to `python-magic` or `file` command.

## Capabilities

- **`detect`** — Detect the MIME type of a file using extension-based lookup, content-based magic-byte inspection, or both (default). Reports confidence level and method used.
- **`lookup`** — Look up the MIME type for one or more file extensions using the built-in `mimetypes` database.
- **`ext`** — Reverse-lookup: find all known file extensions for a given MIME type.
- **Magic-byte detection** — Recognizes common binary formats by reading the first 8–16 bytes: PDF, PNG, JPEG, GIF, ZIP, RAR, 7z, BZ2, XML, HTML, JSON, and more.
- **JSON output** — All subcommands support a `--json` flag for machine-readable output.
- **Zero dependencies** — Uses only Python stdlib modules (`mimetypes`, `argparse`, `json`, `sys`, `os`, `struct`).

## Usage

```
python scripts/mime_type_checker.py <subcommand> [options]
```

### Subcommands

| Subcommand | Description |
|------------|-------------|
| `detect`   | Detect MIME type of a file |
| `lookup`   | Lookup MIME type by extension |
| `ext`      | Find extensions for a MIME type |

### `detect`

```
python scripts/mime_type_checker.py detect --file <PATH> [--method content|extension|both] [--json]
```

- `--file PATH` (required): Path to the file to detect.
- `--method` (default: `both`): Detection method — `content` (magic bytes), `extension` (file name), or `both`.
- `--json`: Output result as JSON.

### `lookup`

```
python scripts/mime_type_checker.py lookup -s <EXT> [--json]
```

- `-s EXTENSION` (required): File extension without leading dot (e.g., `py`, `json`).
- `--json`: Output result as JSON.

### `ext`

```
python scripts/mime_type_checker.py ext -s <MIME_TYPE> [--json]
```

- `-s MIME_TYPE` (required): MIME type string (e.g., `application/json`).
- `--json`: Output result as JSON.

## Examples

### Detect MIME type of a file (both methods)

```bash
python scripts/mime_type_checker.py detect --file report.pdf
```

### Detect using content magic bytes only

```bash
python scripts/mime_type_checker.py detect --file image.png --method content
```

### Lookup MIME type for an extension

```bash
python scripts/mime_type_checker.py lookup -s py
```

### Find extensions for a MIME type

```bash
python scripts/mime_type_checker.py ext -s application/json
```

### JSON output for scripting

```bash
python scripts/mime_type_checker.py detect --file data.json --json
```

## Reference

- Detection relies on Python's built-in `mimetypes` module for extension-based lookup.
- Content detection reads the first 8–16 bytes and matches against known magic-byte signatures.
- Supported magic-byte formats: PDF, PNG, JPEG, GIF, ZIP, RAR, 7z, BZ2, XML, HTML, JSON, SQLite, MP4, MS Office (OLE2/OpenXML).
- Exit codes: `0` for success, `1` for error (file not found, unknown extension/MIME type).
