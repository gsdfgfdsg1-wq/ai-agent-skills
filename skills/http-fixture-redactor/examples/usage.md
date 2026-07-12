# Usage

Create `response.json`:

```json
{
  "user": {
    "email": "person@example.test",
    "api_key": "key-123",
    "profile": {"accessToken": "token-456"}
  },
  "items": [{"password": "secret"}]
}
```

Redact exact names and a field-name pattern:

```bash
python scripts/redact_json_fixture.py response.json --output redacted.json \
  --field password --field-regex '(?i)(api[_-]?key|access[_-]?token)'
```

The output retains the field names and replaces `api_key`, `accessToken`, and `password` values with `[REDACTED]`. Matching is recursive through objects and arrays. The script exits `2` when no matching rule is provided, a regex is invalid, or input/output cannot be processed.
