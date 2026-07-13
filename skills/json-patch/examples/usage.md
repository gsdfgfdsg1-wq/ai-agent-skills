# JSON Patch — Usage Examples

## 1. Apply a patch

Given `data.json`:
```json
{"name": "Alice", "age": 30}
```

Given `patch.json`:
```json
[{"op": "replace", "path": "/age", "value": 31}, {"op": "add", "path": "/city", "value": "Beijing"}]
```

```bash
python skills/json-patch/scripts/json_patch.py apply --doc data.json --patch patch.json
```

Output:
```json
{
  "name": "Alice",
  "age": 31,
  "city": "Beijing"
}
```

## 2. Dry run

```bash
python skills/json-patch/scripts/json_patch.py apply --doc data.json --patch patch.json --dry-run
```

## 3. Validate a patch file

```bash
python skills/json-patch/scripts/json_patch.py validate --patch patch.json
```

## 4. Write result to file

```bash
python skills/json-patch/scripts/json_patch.py apply --doc data.json --patch patch.json --output result.json
```

## Error handling

Invalid patch:

```bash
python skills/json-patch/scripts/json_patch.py validate --patch bad.json
```

```
Validation FAILED: 1 error(s):
  - Op 0: unknown op 'delete'
```

Test failure:

```bash
python skills/json-patch/scripts/json_patch.py apply --doc data.json --patch test-patch.json
```

```
Error applying patch: Test failed at '/age': expected 25, got 30
```
