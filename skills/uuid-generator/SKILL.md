---
name: uuid-generator
description: Generate UUID v4 and v5, validate UUID strings, and inspect UUID components without external dependencies.
license: MIT
---

# uuid-generator

A zero-dependency UUID toolkit that generates, validates, and inspects UUIDs using only the Python standard library.

## When to Use

Invoke this skill when the user needs to:

- Generate one or more UUIDs (v4 random or v5 namespace-based)
- Validate whether a string is a well-formed UUID
- Inspect a UUID to reveal its version, variant, and component fields
- Batch-produce UUIDs for test fixtures, database seeding, or configuration files
- Generate deterministic UUIDs from a namespace and name (v5) for reproducible identifiers

## Capabilities

| Command     | Description                                                  |
|-------------|--------------------------------------------------------------|
| `generate`  | Create new UUID v4 (random) or v5 (namespace-name SHA-1)    |
| `validate`  | Check whether a string is a valid UUID and report its version|
| `inspect`   | Display version, variant, fields, and time/node (if applicable) |

### generate

| Flag           | Description                                    | Default |
|----------------|------------------------------------------------|---------|
| `--version`    | UUID version: `4` or `5`                       | `4`     |
| `--namespace`  | Namespace for v5: `dns`, `url`, `oid`, `null`  | —       |
| `--name`       | Name string for v5                             | —       |
| `--count`      | Number of UUIDs to generate                    | `1`     |
| `--upper`      | Output uppercase hex                           | `false` |
| `--json`       | Output as JSON                                 | `false` |

### validate

| Flag           | Description                                    | Default |
|----------------|------------------------------------------------|---------|
| `-s`           | UUID string to validate                        | —       |
| `--json`       | Output as JSON                                 | `false` |

### inspect

| Flag           | Description                                    | Default |
|----------------|------------------------------------------------|---------|
| `-s`           | UUID string to inspect                         | —       |
| `--json`       | Output as JSON                                 | `false` |

## Usage

```bash
# Generate a single v4 UUID
python scripts/uuid_generator.py generate

# Generate 5 v4 UUIDs in uppercase
python scripts/uuid_generator.py generate --version 4 --count 5 --upper

# Generate a v5 UUID from the DNS namespace
python scripts/uuid_generator.py generate --version 5 --namespace dns --name example.com

# Validate a UUID
python scripts/uuid_generator.py validate -s 550e8400-e29b-41d4-a716-446655440000

# Inspect a UUID
python scripts/uuid_generator.py inspect -s 550e8400-e29b-41d4-a716-446655440000

# JSON output for scripting
python scripts/uuid_generator.py generate --count 3 --json
```

## Examples

See [examples/usage.md](examples/usage.md) for detailed, annotated examples covering every flag and error case.

## Reference

- [RFC 4122](https://tools.ietf.org/html/rfc4122) — A Universally Unique IDentifier (UUID) URN Namespace
- Python `uuid` module — standard library implementation used internally
- v4: Generated from random bits (128-bit random with version/variant bits set)
- v5: Generated from a namespace UUID and name via SHA-1 hashing
