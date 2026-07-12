# Usage Examples

## 1. Basic scan

```bash
python skills/sql-injection-scanner/scripts/scan_sqli.py src/
```

Output:

```text
Found 2 potential SQL injection pattern(s):

  src/app.py
    L42 [HIGH] SQL string concatenation (Python)
           query = "SELECT * FROM users WHERE id = " + user_id
    L78 [MEDIUM] ORM raw() with dynamic query
           User.objects.raw(f"SELECT * FROM users WHERE name = '{name}'")
```

## 2. Only high confidence findings

```bash
python skills/sql-injection-scanner/scripts/scan_sqli.py src/ --severity high
```

## 3. JSON output

```bash
python skills/sql-injection-scanner/scripts/scan_sqli.py . --json
```

## 4. CI gate

```bash
python skills/sql-injection-scanner/scripts/scan_sqli.py . --exit-code
echo $?
# 1 if any patterns found, 0 if clean
```

## 5. Scan specific files

```bash
python skills/sql-injection-scanner/scripts/scan_sqli.py models.py views.py
```
