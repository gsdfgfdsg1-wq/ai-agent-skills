# Usage Examples

## 1. Basic conversion

```bash
python skills/openapi-to-markdown/scripts/openapi2md.py openapi.json
```

Outputs Markdown to stdout with all endpoints grouped by tag.

## 2. Write to file

```bash
python skills/openapi-to-markdown/scripts/openapi2md.py openapi.json -o docs/API.md
```

Writes the generated Markdown to `docs/API.md`.

## 3. Filter by tag

```bash
python skills/openapi-to-markdown/scripts/openapi2md.py openapi.json --tag users
```

Only includes endpoints tagged with "users".

## 4. Include component schemas

```bash
python skills/openapi-to-markdown/scripts/openapi2md.py openapi.json --include-schemas -o API.md
```

Appends a "Schemas" section with property tables for each component schema.

## 5. Sample output structure

```markdown
# Pet Store API

**Version:** 1.0.0

## pets

### GET /pets

**List all pets**

| Name | In | Type | Required | Description |
| --- | --- | --- | --- | --- |
| `limit` | query | `integer` | No | max items per page |

**Responses:**

- **200**: A list of pets
- **default**: unexpected error
```
