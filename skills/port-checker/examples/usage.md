# Port Checker — Usage Examples

## 1. Check a single port

```bash
python skills/port-checker/scripts/port_checker.py check --host localhost --port 8080
```

Output:

```
localhost:8080 — CLOSED (3001.2ms)
```

## 2. Check with JSON output

```bash
python skills/port-checker/scripts/port_checker.py check --host localhost --port 80 --json
```

```json
{
  "host": "localhost",
  "port": 80,
  "status": "CLOSED",
  "latency_ms": 3000.5
}
```

## 3. Scan a range of ports

```bash
python skills/port-checker/scripts/port_checker.py range --host localhost --start 8000 --end 8010
```

## 4. Scan with open-only filter

```bash
python skills/port-checker/scripts/port_checker.py range --host localhost --start 1 --end 1024 --open-only
```

## 5. Batch check multiple pairs

```bash
python skills/port-checker/scripts/port_checker.py batch --pairs localhost:80 localhost:443 localhost:8080
```

## Error handling

Invalid port number:

```bash
python skills/port-checker/scripts/port_checker.py check --host localhost --port 99999
```

```
localhost:99999 — CLOSED (0.0ms)
```
