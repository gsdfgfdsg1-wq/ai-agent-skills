# Usage

Create `before.json`:

```json
{
  "service": {"port": 8080, "retries": 2},
  "features": ["search"]
}
```

Create `after.json`:

```json
{
  "service": {"port": 8081, "timeout": 30},
  "features": ["search", "export"]
}
```

Compare the files:

```bash
python scripts/json_config_diff.py before.json after.json
python scripts/json_config_diff.py --json before.json after.json
```

The text output reports `added service.timeout`, `removed service.retries`, and changed values for `service.port` and `features`. Exit code `1` indicates differences; invalid or unreadable JSON produces exit code `2`.
