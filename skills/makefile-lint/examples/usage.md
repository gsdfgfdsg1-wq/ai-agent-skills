# Makefile Lint — Usage Examples

## 1. Lint a Makefile

```bash
python skills/makefile-lint/scripts/makefile_lint.py lint --file Makefile
```

Output:

```
Issues in Makefile:
  ⚠ [warning] missing-phony: target 'clean' should be declared .PHONY
  ⚠ [warning] missing-phony: target 'test' should be declared .PHONY
  ℹ [info] non-default-first-target: first target is 'build' — convention is 'all'

Total: 3 issue(s)
```

## 2. JSON output

```bash
python skills/makefile-lint/scripts/makefile_lint.py lint --file Makefile --json
```

## Error handling

File not found:

```bash
python skills/makefile-lint/scripts/makefile_lint.py lint --file MissingMakefile
```

```
Error: cannot read MissingMakefile: ...
```
