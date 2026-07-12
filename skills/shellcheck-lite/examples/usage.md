# Usage Examples

## 1. Basic check

```bash
python skills/shellcheck-lite/scripts/shellcheck_lite.sh deploy.sh
```

Output:

```text
Found 2 issue(s):

[ERROR] SC1000 deploy.sh:1
  missing shebang line (#!/bin/sh or #!/bin/bash)

[WARNING] SC1002 deploy.sh:5
  unquoted variable $DIR
```

## 2. Check a directory recursively

```bash
python skills/shellcheck-lite/scripts/shellcheck_lite.py scripts/
```

Automatically finds all `.sh` and `.bash` files, plus extensionless files with a shell shebang.

## 3. Filter by severity

```bash
python skills/shellcheck-lite/scripts/shellcheck_lite.py . --severity warning
```

Only reports `warning` and `error` level issues (suppresses `info`).

## 4. JSON output

```bash
python skills/shellcheck-lite/scripts/shellcheck_lite.py deploy.sh --json
```

Returns a JSON array with `rule`, `severity`, `line`, `message`, `file` per finding.

## 5. CI integration

```bash
python skills/shellcheck-lite/scripts/shellcheck_lite.py . --exit-code --severity warning
echo $?
# 0 if no issues, 1 if any warning or error found
```
