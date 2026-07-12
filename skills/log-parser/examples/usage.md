# Usage Examples

## 1. Summary of log levels

```bash
python skills/log-parser/scripts/parse_logs.py /var/log/app/ --summary
```

Output:

```text
Log level summary:
  error: 5
  warning: 23
  info: 1450
  debug: 312
  Total: 1790
```

## 2. Show only errors and criticals

```bash
python skills/log-parser/scripts/parse_logs.py app.log --levels error,critical
```

Output:

```text
Found 5 matching log entries:

[ERROR] (3 entries)
  app.log:42 | 2026-07-13 01:23:45 ERROR Database connection refused
  app.log:78 | 2026-07-13 02:10:11 ERROR Failed to process request
  app.log:103 | 2026-07-13 03:45:00 ERROR Timeout waiting for response
```

## 3. Filter by pattern

```bash
python skills/log-parser/scripts/parse_logs.py app.log --pattern "timeout|refused"
```

Only shows lines matching the regex.

## 4. JSON output

```bash
python skills/log-parser/scripts/parse_logs.py app.log --json --levels error
```

Returns JSON with `entries`, `summary`, `total`, and any `errors`.

## 5. Limit output

```bash
python skills/log-parser/scripts/parse_logs.py app.log --top 5
```

Show at most 5 entries per level.
