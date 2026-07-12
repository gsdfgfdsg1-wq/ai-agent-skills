---
name: shellcheck-lite
description: Lightweight static checker for shell scripts — detects unquoted variables, missing shebangs, deprecated backtick syntax, unsafe cd, useless cat and more without external dependencies.
license: MIT
---

# ShellCheck Lite

> A zero-dependency static analysis tool for bash/sh scripts that catches the most common pitfalls before they bite.

## When to Use / Triggers

- Before committing shell scripts, run a quick sanity check.
- CI pipeline needs a lightweight shell linter (no external binary install).
- Code review of shell scripts, flag common anti-patterns automatically.
- Learning shell scripting, get instant feedback on bad practices.

## Capabilities

- 9 built-in rules covering: missing shebang, unquoted variables, deprecated backticks, cd without error handling, useless cat, etc.
- Works on `.sh`, `.bash`, `.ksh`, `.zsh` files and shebang-detected extensionless scripts.
- `--json` machine-readable output; `--severity` filter; `--exit-code` for CI.

## Usage

```bash
# Check all shell scripts in a project
python skills/shellcheck-lite/scripts/shellcheck_lite.py .

# Only errors
python skills/shellcheck-lite/scripts/shellcheck_lite.py scripts/ --severity error

# CI mode
python skills/shellcheck-lite/scripts/shellcheck_lite.py . --exit-code --severity warning

# JSON output
python skills/shellcheck-lite/scripts/shellcheck_lite.py deploy.sh --json
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/shellcheck_lite.py --help` for all options.
