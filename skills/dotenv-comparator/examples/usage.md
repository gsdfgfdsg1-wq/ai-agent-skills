# Usage Examples

## 1. Basic comparison

```bash
python skills/dotenv-comparator/scripts/dotenv_comparator.py .env.dev .env.prod
```

Output:

```text
Comparing .env.dev vs .env.prod:

  Added (1):
    + REDIS_URL=redis://prod-redis:6379

  Removed (1):
    - DEBUG=true

  Changed (1):
    ~ LOG_LEVEL: 'debug' -> 'warning'
```

## 2. Key-only comparison (ignore values)

```bash
python skills/dotenv-comparator/scripts/dotenv_comparator.py .env.example .env --ignore-values
```

Only reports added and removed keys, useful for checking if .env covers all required variables.

## 3. JSON output

```bash
python skills/dotenv-comparator/scripts/dotenv_comparator.py .env.staging .env.production --json
```

Returns JSON with added, removed, changed arrays and unchanged_count.

## 4. Strict mode (CI)

```bash
python skills/dotenv-comparator/scripts/dotenv_comparator.py .env.example .env --strict
```

Exits with code 1 if any differences found, making it CI-friendly.
