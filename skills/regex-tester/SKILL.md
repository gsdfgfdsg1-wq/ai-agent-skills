---
name: regex-tester
description: Test regular expressions against sample strings, outputting match results, groups, and positions without external dependencies.
license: MIT
---

# Regex Tester

> Quickly test regex patterns against sample strings — no browser or REPL needed.

## When to Use / Triggers

- Verify a regex pattern matches expected input.
- Debug why a regex fails to match.
- Batch-test multiple patterns against multiple strings.
- CI: validate regex patterns in config files.

## Capabilities

- Match a regex pattern against one or more test strings.
- Reports: match/nomatch, matched text, group captures, match positions.
- Supports `--flags` for IGNORECASE, DOTALL, MULTILINE, VERBOSE.
- `--findall` to find all non-overlapping matches.
- `--json` for machine-readable output.
- `--file` to read test strings from a file (one per line).

## Usage

```bash
python skills/regex-tester/scripts/regex_tester.py -p '^\d{3}-\d{4}$' -s '123-4567'
python skills/regex-tester/scripts/regex_tester.py -p '(\w+)@(\w+)\.(\w+)' -s 'user@example.com' --findall --json
python skills/regex-tester/scripts/regex_tester.py -p 'TODO:\s*(.+)' -f todos.txt --flags IGNORECASE
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/regex_tester.py --help` for all options.
