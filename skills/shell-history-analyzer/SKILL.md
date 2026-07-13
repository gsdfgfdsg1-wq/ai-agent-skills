---
name: shell-history-analyzer
description: Parse Bash or Zsh history text, ignore blank lines and timestamps, and report most-used commands with optional JSON output.
license: MIT
---

# Shell History Analyzer

> Summarize commands in Bash or Zsh history files using a zero-dependency Python CLI.

## When to Use / Triggers

- Find the commands used most often in a local shell history file.
- Inspect Bash history that includes `#<epoch>` timestamp lines.
- Analyze Zsh extended history entries such as `: 1710000000:0;git status`.
- Feed command-frequency data to another script through JSON output.

## Capabilities

- Reads a history file or standard input.
- Ignores empty lines and Bash timestamp lines.
- Parses Zsh extended-history timestamps before extracting commands.
- Counts commands, ranks them by frequency, and limits output with `--top`.
- Supports machine-readable `--json` output with standard library modules only.

## Usage

```bash
# Show the 10 most frequent commands
python skills/shell-history-analyzer/scripts/shell_history_analyzer.py ~/.bash_history

# Analyze Zsh history and show five commands
python skills/shell-history-analyzer/scripts/shell_history_analyzer.py ~/.zsh_history --top 5

# Read from standard input as JSON
history | python skills/shell-history-analyzer/scripts/shell_history_analyzer.py --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/shell_history_analyzer.py --help` for all options.
