---
name: json-path-query
description: Query JSON and JSONL files with JSONPath-like expressions without external dependencies.
license: MIT
---

# json-path-query

Query JSON and JSONL files using a simplified JSONPath expression engine — no external dependencies required.

## When to Use

- You need to extract specific values from a JSON file using path expressions rather than writing custom parsing code.
- You want to query each line of a JSONL (newline-delimited JSON) file with the same path expression.
- You need recursive descent search to find a key at any nesting depth within a JSON document.
- You are working in an environment where installing external packages (like `jsonpath-ng`) is not possible or desirable.
- You want a lightweight, zero-dependency CLI tool for quick JSON data extraction in scripts or pipelines.

## Capabilities

- **Simplified JSONPath syntax**: Supports root (`$`), dot-access (`.key`), array index (`[n]`), wildcard array (`[*]`), nested dot-access (`.key1.key2`), and recursive descent (`..key`).
- **Two subcommands**:
  - `query` — query a single JSON file with a path expression.
  - `extract` — apply a path expression to each line of a JSONL file.
- **Output formats**: plain text (one value per line) or JSON array (`--json` flag).
- **Error handling**: clear error messages for file not found, invalid path expressions, missing keys, and malformed JSON.
- **Zero dependencies**: uses only Python standard library modules (`json`, `argparse`, `sys`, `re`).

## Usage

```bash
# Query a JSON file
python scripts/json_path_query.py query --file data.json -p '$.store.book[0].title'

# Query with JSON array output
python scripts/json_path_query.py query --file data.json -p '$.store.book[*].author' --json

# Extract from a JSONL file
python scripts/json_path_query.py extract --file logs.jsonl -p '$.user.name'

# Recursive descent — find all "id" keys at any depth
python scripts/json_path_query.py query --file data.json -p '$..id'
```

### Common Path Expressions

| Expression | Meaning |
|---|---|
| `$` | Root element |
| `.key` | Access object key |
| `[n]` | Access array index (0-based) |
| `[*]` | Iterate all array elements |
| `.key1.key2` | Nested key access |
| `..key` | Recursive descent — find key at any depth |

## Examples

### Query a single field

```bash
python scripts/json_path_query.py query --file package.json -p '$.name'
```

### Get all items from an array

```bash
python scripts/json_path_query.py query --file users.json -p '$.users[*].email'
```

### Nested access with array index

```bash
python scripts/json_path_query.py query --file api.json -p '$.data.results[2].id'
```

### Recursive descent

```bash
python scripts/json_path_query.py query --file deep.json -p '$..label'
```

### Extract fields from JSONL

```bash
python scripts/json_path_query.py extract --file events.jsonl -p '$.event.type'
```

### Output as JSON array

```bash
python scripts/json_path_query.py query --file data.json -p '$.items[*].price' --json
```

## Reference

### Subcommand: `query`

| Flag | Short | Description |
|---|---|---|
| `--file` | | Path to JSON file |
| `-p` | | JSONPath expression |
| `--json` | | Output results as JSON array |

### Subcommand: `extract`

| Flag | Short | Description |
|---|---|---|
| `--file` | | Path to JSONL file |
| `-p` | | JSONPath expression |
| `--json` | | Output results as JSON array |

### Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | File not found or unreadable |
| 2 | Invalid path expression |
| 3 | Malformed JSON |
| 4 | Key or index not found |
