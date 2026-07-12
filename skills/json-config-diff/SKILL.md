---
name: json-config-diff
description: This skill should be used when comparing two JSON configuration files and reporting added, removed, or changed settings in text or JSON format.
agent_created: true
---

# JSON Config Diff

Compare JSON configuration files using a deterministic standard-library Python script. Use this skill to review configuration changes, verify generated config files, or inspect environment-specific JSON settings.

## Workflow

1. Run `scripts/json_config_diff.py` with the old and new JSON files.
2. Review added, removed, and changed paths in the text report.
3. Pass `--json` to integrate the report with another program.
4. Treat exit code `0` as no differences, `1` as differences found, and `2` as an input error.

## Comparison Rules

Traverse JSON objects recursively and compare their keys. Report missing old keys as added and missing new keys as removed. Compare arrays, scalars, and values whose JSON types differ as whole values at their path. Render object paths with dot notation and escape literal `.`, `[` , `]`, and `\\` characters.

See [examples/usage.md](examples/usage.md) for commands and output shape.

## Resource

Run `scripts/json_config_diff.py --help` for command options.
