# Timestamp Converter — Usage Examples

## 1. Convert a Unix timestamp to all formats (default)

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py from_unix -t 1700000000
```

Output:
```
       iso: 2023-11-14T22:13:20+00:00
     epoch: 1700000000.0
  readable: Tuesday, November 14, 2023 10:13:20 PM UTC
```

## 2. Convert a Unix timestamp with timezone offset

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py from_unix -t 1700000000 --tz +8
```

Output:
```
       iso: 2023-11-15T06:13:20+08:00
     epoch: 1700000000.0
  readable: Wednesday, November 15, 2023 06:13:20 AM UTC+08:00
```

## 3. Convert an ISO 8601 string to Unix timestamp

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py from_iso -s '2023-11-14T22:13:20Z'
```

Output:
```
       iso: 2023-11-14T22:13:20+00:00
     epoch: 1700000000.0
  readable: Tuesday, November 14, 2023 10:13:20 PM UTC
```

## 4. Get current time in JSON format with timezone

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py now --tz +8 --json
```

Output:
```json
{
  "iso": "2026-07-13T21:30:00+08:00",
  "epoch": 1752442200.0,
  "readable": "Monday, July 13, 2026 09:30:00 PM UTC+08:00"
}
```

## 5. ISO-only output from a Unix timestamp

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py from_unix -t 0 --format iso
```

Output:
```
       iso: 1970-01-01T00:00:00+00:00
```

## 6. Epoch-only output from an ISO string

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py from_iso -s '2025-01-01' --format epoch
```

Output:
```
     epoch: 1735689600.0
```

## 7. Error handling — invalid timestamp

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py from_unix -t abc
```

Output (stderr):
```
Error: invalid timestamp 'abc'. Must be an integer or float.
```

## 8. Error handling — invalid ISO string

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py from_iso -s 'not-a-date'
```

Output (stderr):
```
Error: invalid ISO 8601 string 'not-a-date'.
```

## 9. Millisecond-precision Unix timestamp

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py from_unix -t 1700000000.123 --format iso
```

Output:
```
       iso: 2023-11-14T22:13:20.123000+00:00
```

## 10. Current time in UTC (default)

```bash
python skills/timestamp-converter/scripts/timestamp_converter.py now
```

Output:
```
       iso: 2026-07-13T13:30:00+00:00
     epoch: 1752442200.0
  readable: Monday, July 13, 2026 01:30:00 PM UTC
```
