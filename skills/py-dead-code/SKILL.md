---
name: py-dead-code
description: Detect unused imports and unreachable code in Python files using AST analysis without external dependencies.
license: MIT
---

# Py Dead Code

> Find unused imports and dead code in Python — no flake8 or pylint needed.

## When to Use / Triggers

- Audit Python codebases for unused imports before cleanup.
- Detect unreachable code paths (code after return/break/raise/continue).
- CI: enforce no dead code policy.
- Pre-PR code review automation.

## Capabilities

- Uses Python's `ast` module for reliable analysis.
- Detects: unused imports (with `from X import Y` and `import X` styles), unreachable statements after return/break/raise/continue.
- `--ignore-imports` to skip import checking.
- `--ignore-unreachable` to skip unreachable code checking.
- `--json` for machine-readable output.
- Recursively scans directories.

## Usage

```bash
python skills/py-dead-code/scripts/py_dead_code.py src/
python skills/py-dead-code/scripts/py_dead_code.py myfile.py --json
python skills/py-dead-code/scripts/py_dead_code.py . --ignore-unreachable
```

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/py_dead_code.py --help` for all options.
