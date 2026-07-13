---
name: procfile-lint
description: Lint Procfile process declarations for malformed types, empty commands, and duplicate process types using only the Python standard library.
license: MIT
agent_created: true
---

# Procfile Lint

Validate Procfiles before deployment or CI runs. Detect empty commands, invalid process-type names, and duplicate declarations without external dependencies.

## When to Use

- Check a Procfile before deploying a process-based application.
- Enforce Procfile conventions in CI.
- Diagnose malformed process declarations.

## Usage

```bash
python skills/procfile-lint/scripts/procfile_lint.py Procfile
python skills/procfile-lint/scripts/procfile_lint.py Procfile --json
```

Return exit code `1` when any issue is found and `0` when the file is clean. Ignore blank lines and lines beginning with `#`.

## Rules

- Process types must match `[A-Za-z][A-Za-z0-9_-]*`.
- Every declaration must include a non-empty command after `:`.
- A process type may be declared only once.

## Examples

See `examples/usage.md`.

## Reference

Run `scripts/procfile_lint.py --help` for command options.
