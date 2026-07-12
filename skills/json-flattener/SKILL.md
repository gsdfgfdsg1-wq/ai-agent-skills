---
name: json-flattener
description: Flatten nested JSON objects to dot-notation key-value pairs and unflatten them back without external dependencies.
license: MIT
---

# json-flattener

Flatten nested JSON objects into flat dot-notation key-value pairs and reconstruct them back — no external dependencies required.

## When to Use

- You need to compare deeply nested JSON structures and want a flat representation for easier diffing.
- You are preparing JSON data for CSV/TSV export and need every leaf value accessible as a simple column.
- You want to store nested configuration in environment variables or flat key-value stores (`.env`, Consul, etc.) that only support string keys.
- You are debugging API responses and need a quick overview of every field path and its value.
- You need to reconstruct a nested object from a flat source such as spreadsheet rows, CLI flags, or form submissions.

## Capabilities

| Capability | Description |
|---|---|
| **Flatten** | Recursively walk a nested JSON object and emit `parent.child.leaf = value` pairs. Arrays use `key[0]` indexing. |
| **Unflatten** | Reverse the process — parse flat dot-notation keys back into a nested JSON object. |
| **File or string input** | Accept input from `--file PATH` or `-s STRING`. |
| **Custom separator** | Change the default `.` separator to any string (e.g. `_`, `/`). |
| **JSON output** | Use `--json` to get structured JSON output instead of `key=value` lines. |
| **Error handling** | Clear messages for invalid JSON, missing files, missing arguments, and inconsistent keys. |
| **Zero dependencies** | Uses only Python stdlib modules: `json`, `argparse`, `sys`, `re`. |

## Usage

```
python scripts/json_flattener.py flatten [--file PATH | -s STRING] [--separator SEP] [--json]
python scripts/json_flattener.py unflatten [--file PATH | -s STRING] [--separator SEP] [--json]
```

### Global options

| Option | Description |
|---|---|
| `--file PATH` | Read JSON input from a file. |
| `-s STRING` | Provide JSON input as a string. |
| `--separator SEP` | Separator between key segments (default: `.`). |
| `--json` | Output result as JSON instead of `key=value` lines. |

### Subcommands

- **flatten** — Convert nested JSON to flat key-value pairs.
- **unflatten** — Convert flat key-value pairs back to nested JSON.

## Examples

### Flatten a nested object from a string

```bash
python scripts/json_flattener.py flatten -s '{"user":{"name":"Alice","age":30}}'
```

Output:
```
user.name=Alice
user.age=30
```

### Flatten with JSON output

```bash
python scripts/json_flattener.py flatten -s '{"a":{"b":[1,2]}}' --json
```

Output:
```json
{"a.b[0]": 1, "a.b[1]": 2}
```

### Unflatten flat pairs back to nested JSON

```bash
python scripts/json_flattener.py unflatten -s 'user.name=Alice
user.age=30' --json
```

Output:
```json
{"user": {"name": "Alice", "age": 30}}
```

### Read from a file with custom separator

```bash
python scripts/json_flattener.py flatten --file data.json --separator "/"
```

## Reference

- **Flatten rules**: Nested objects become `parent.child: value`. Array elements become `key[0]: value`, `key[1]: value`, etc.
- **Unflatten rules**: Dot-notation keys (or custom separator) are split and rebuilt into nested dicts. Array indices `key[N]` are recognized and produce lists.
- **Error cases**:
  - Invalid JSON input → exit code 1 with descriptive message.
  - File not found → exit code 1 with descriptive message.
  - Neither `--file` nor `-s` provided → exit code 1 with usage hint.
  - Inconsistent keys during unflatten (e.g. same path as both leaf and object) → exit code 1 with conflict detail.
