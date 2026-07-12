# Usage Examples

## 1. Basic check

```bash
python skills/yaml-linter/scripts/lint_yaml.py docker-compose.yml
```

Output:

```text
Found 2 issue(s):

[ERROR] Y001 docker-compose.yml:8
  tab character in indentation (use spaces)

[WARNING] Y002 docker-compose.yml:12
  trailing whitespace
```

## 2. Check a directory recursively

```bash
python skills/yaml-linter/scripts/lint_yaml.py config/
```

Automatically finds all `.yaml` and `.yml` files.

## 3. Filter by severity

```bash
python skills/yaml-linter/scripts/lint_yaml.py . --severity warning
```

Only reports `warning` and `error` level issues.

## 4. JSON output

```bash
python skills/yaml-linter/scripts/lint_yaml.py k8s/ --json
```

Returns a JSON array with `rule`, `severity`, `line`, `message`, `file` per finding.

## 5. CI integration

```bash
python skills/yaml-linter/scripts/lint_yaml.py . --exit-code --severity warning
echo $?
# 0 if no issues, 1 if any warning or error found
```
