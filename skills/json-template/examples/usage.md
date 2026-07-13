# json-template Usage Examples

## Template and variables

Create `config.template.json`:

```json
{
  "service": {
    "name": "{{ app.name }}",
    "port": "{{ app.port }}",
    "enabled": "{{ app.enabled }}",
    "tags": "{{ app.tags }}",
    "url": "https://{{ app.host }}/v1"
  }
}
```

Create `values.json`:

```json
{
  "app": {
    "name": "catalog",
    "port": 8080,
    "enabled": true,
    "tags": ["internal", "stable"],
    "host": "api.example.test"
  }
}
```

## Render formatted JSON

```bash
python scripts/json_template.py config.template.json --variables values.json
```

Output:

```json
{
  "service": {
    "name": "catalog",
    "port": 8080,
    "enabled": true,
    "tags": [
      "internal",
      "stable"
    ],
    "url": "https://api.example.test/v1"
  }
}
```

Values that occupy a full placeholder preserve their JSON types. `port` remains a number, `enabled` remains a boolean, and `tags` remains an array.

## Write compact JSON

```bash
python scripts/json_template.py config.template.json --variables values.json --output config.json --json
```

`config.json` contains compact valid JSON.

## Missing variable failure

A template with `"owner": "{{ app.owner }}"` fails when `values.json` has no `app.owner`:

```bash
python scripts/json_template.py config.template.json --variables values.json
```

Output to stderr:

```text
Error: missing variable: app.owner
```

The command exits with status `1` and writes no rendered JSON.

## Invalid JSON failure

Invalid template or variables files are rejected before rendering:

```bash
python scripts/json_template.py invalid-template.json --variables values.json
```

The command exits with status `1` and identifies the invalid JSON file and location.
