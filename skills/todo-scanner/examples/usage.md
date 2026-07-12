# Usage Examples

## 1. Basic scan

```bash
python skills/todo-scanner/scripts/scan_todos.py .
```

Output:

```text
Found 3 TODO item(s):

  src/app.py
    L42 [TODO] Refactor this to use the shared helper
    L108 [FIXME] Race condition when concurrent requests arrive
  tests/test_app.py
    L15 [NOTE] This test depends on external service
```

## 2. Custom tags

```bash
python skills/todo-scanner/scripts/scan_todos.py src/ --tags FIXME,BUG
```

Only reports lines matching `FIXME` or `BUG`.

## 3. Summary mode

```bash
python skills/todo-scanner/scripts/scan_todos.py . --summary
```

Output:

```text
TODO item summary:
  TODO: 12
  FIXME: 3
  HACK: 1
  Total: 16
```

## 4. JSON output for tooling

```bash
python skills/todo-scanner/scripts/scan_todos.py src/ --json
```

Returns a JSON array, each element has `tag`, `line`, `text`, `file`.

## 5. CI integration

```bash
python skills/todo-scanner/scripts/scan_todos.py . --exit-code
echo $?
# 0 if no items found, 1 if any exist
```
