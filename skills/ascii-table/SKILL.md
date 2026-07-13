---
name: ascii-table
description: Look up 7-bit ASCII values by decimal, hexadecimal, or character input, and print ASCII ranges in text or JSON without external dependencies.
license: MIT
agent_created: true
---

# ASCII Table

> Inspect ASCII codes and generate concise ASCII tables from a standard-library Python CLI.

## When to Use / Triggers

- Look up an ASCII code from a decimal or hexadecimal value.
- Find decimal, hexadecimal, or binary values for an ASCII character.
- Print a bounded range of the 7-bit ASCII table.
- Produce machine-readable ASCII lookup results.

## Capabilities

- `lookup` accepts exactly one of `--decimal`, `--hex`, or `--char`.
- `range` prints an inclusive decimal range from 0 through 127.
- Shows decimal, hexadecimal, binary, character/control-name, and category fields.
- `--json` emits a single object for lookups or an array for ranges.

## Usage

```bash
python skills/ascii-table/scripts/ascii_table.py lookup --decimal 65
python skills/ascii-table/scripts/ascii_table.py lookup --hex 0x41
python skills/ascii-table/scripts/ascii_table.py lookup --char A --json
python skills/ascii-table/scripts/ascii_table.py range 32 47
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/ascii_table.py --help` for all options.
