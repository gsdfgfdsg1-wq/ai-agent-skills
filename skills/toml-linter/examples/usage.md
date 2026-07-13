# TOML Linter — Usage Examples

## 1. Lint a TOML file

```bash
python skills/toml-linter/scripts/toml_linter.py lint --file pyproject.toml
```

Output:

```
Issues in pyproject.toml:
  ✗ [error] missing-project-name: [project] missing required 'name' field
  ℹ [info] missing-build-system: pyproject.toml missing [build-system] section

Total: 2 issue(s)
```

## 2. Lint pyproject.toml with type hint

```bash
python skills/toml-linter/scripts/toml_linter.py lint --file pyproject.toml --type pyproject
```

## 3. JSON output

```bash
python skills/toml-linter/scripts/toml_linter.py lint --file config.toml --json
```

```json
{
  "file": "config.toml",
  "issues": []
}
```

## Error handling

Invalid TOML syntax:

```bash
python skills/toml-linter/scripts/toml_linter.py lint --file bad.toml
```

```
Issues in bad.toml:
  ✗ [error] parse-error: TOML parse error: ...
```
