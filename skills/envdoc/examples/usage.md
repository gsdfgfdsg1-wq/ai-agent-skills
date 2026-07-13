# Envdoc — Usage Examples

## 1. Generate Markdown documentation

Given `.env`:
```
# Database connection
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp

# API settings
API_KEY=
API_TIMEOUT=30
```

```bash
python skills/envdoc/scripts/envdoc.py generate --file .env --required DB_HOST,DB_NAME,API_KEY
```

Output:

```markdown
# Environment Variables

Auto-generated from `.env`.

| Variable | Default | Required | Description |
| --- | --- | --- | --- |
| `DB_HOST` | `localhost` | Yes | Database connection |
| `DB_PORT` | `5432` | No | Database connection |
| `DB_NAME` | `myapp` | Yes | Database connection |
| `API_KEY` | _empty_ | Yes | API settings |
| `API_TIMEOUT` | `30` | No | API settings |
```

## 2. Generate .env.example

```bash
python skills/envdoc/scripts/envdoc.py example --file .env --output .env.example
```

## 3. Audit required variables

```bash
python skills/envdoc/scripts/envdoc.py audit --file .env --required DB_HOST,DB_NAME,API_KEY
```

## Error handling

Missing file:

```bash
python skills/envdoc/scripts/envdoc.py generate --file missing.env
```

```
Error: cannot read missing.env: [Errno 2] No such file or directory
```
