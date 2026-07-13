---
name: makefile-lint
description: Lint Makefiles for common issues and best practices without external dependencies.
license: MIT
---

# Makefile Lint

> Check Makefiles for common pitfalls, style issues, and best practice violations.

## When to Use / Triggers

- Review a Makefile for correctness and style.
- Ensure Makefile follows best practices (PHONY, proper tabs, etc.).
- Audit Makefiles in CI.

## Capabilities

- `lint`: check a Makefile for issues.
- Checks: missing .PHONY, tab vs space indentation, missing shebang,
  recursive make without $(MAKE), unused variables, double-colon rules, etc.
- `--json` for machine-readable output.

## Usage

```bash
python skills/makefile-lint/scripts/makefile_lint.py lint --file Makefile
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/makefile_lint.py --help` for all options.
