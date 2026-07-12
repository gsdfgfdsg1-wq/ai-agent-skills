# Usage

Create `schema.json`:

```json
{
  "required": ["DATABASE_URL", "DEBUG"],
  "properties": {
    "DATABASE_URL": {"type": "string", "minLength": 1},
    "DEBUG": {"type": "boolean"},
    "PORT": {"type": "integer"},
    "TAGS": {"type": "array"}
  },
  "additionalProperties": false
}
```

Create `.env`:

```dotenv
DATABASE_URL=postgres://localhost/app
DEBUG=false
PORT=8080
TAGS=["api","worker"]
```

Validate it:

```bash
python scripts/validate_env.py .env schema.json
python scripts/validate_env.py --json .env schema.json
```

An invalid value, omitted required key, or unknown key when `additionalProperties` is `false` produces exit code `1`. Invalid files or unsupported schema inputs produce exit code `2`.
