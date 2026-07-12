# Usage Examples

## 1. Validate a daily cron

```bash
python skills/cron-validator/scripts/validate_cron.py "0 9 * * *"
```

Output:

```text
Valid cron expression (5 fields)
```

## 2. Show next runs

```bash
python skills/cron-validator/scripts/validate_cron.py "0 9 * * MON-FRI" --next 3
```

Output:

```text
Valid cron expression (5 fields)

Next runs:
  2026-07-13T09:00:00
  2026-07-14T09:00:00
  2026-07-15T09:00:00
```

## 3. Catch invalid expressions

```bash
python skills/cron-validator/scripts/validate_cron.py "60 0 * * *"
```

Output (exit code 1):

```text
Invalid: value out of range [0-59]: 60
```

## 4. Day and month names

```bash
python skills/cron-validator/scripts/validate_cron.py "0 0 1 JAN-MAR MON" --next 3 --json
```

Returns JSON with `valid`, `fields`, `parsed` breakdown, and `next_runs`.

## 5. Six-field (with seconds)

```bash
python skills/cron-validator/scripts/validate_cron.py "0 30 9 * * MON-FRI" --next 2
```

Validates and shows next two Monday–Friday 9:30 AM runs.
