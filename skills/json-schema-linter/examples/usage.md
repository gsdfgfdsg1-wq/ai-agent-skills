# Usage Examples

## 1. Basic validation

Create `schema.json`:

```json
{
  "type": "object",
  "required": ["name", "version"],
  "properties": {
    "name": {"type": "string", "minLength": 1},
    "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
    "private": {"type": "boolean"}
  },
  "additionalProperties": false
}
```

Create `config.json`:

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "private": true
}
```

```bash
python skills/json-schema-linter/scripts/lint_json_schema.py config.json schema.json
```

Output:

```text
Valid
```

## 2. Catch missing required fields

```json
{"version": "1.0.0"}
```

Output:

```text
Validation failed with 1 error(s):

  $: missing required property 'name' (required)
```

## 3. Catch type mismatches

```json
{"name": "my-app", "version": 100}
```

Output:

```text
Validation failed with 1 error(s):

  $.version: expected string, got integer (type)
```

## 4. JSON output

```bash
python skills/json-schema-linter/scripts/lint_json_schema.py config.json schema.json --json
```

Returns `{"valid": true/false, "errors": [...]}`.

## 5. CI integration

```bash
python skills/json-schema-linter/scripts/lint_json_schema.py config.json schema.json --exit-code
echo $?
# 0 if valid, 1 if errors
```
