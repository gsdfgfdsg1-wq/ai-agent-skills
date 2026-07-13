# UTF-8 Validator — Usage Examples

## 1. Validate a UTF-8 file

```bash
python skills/utf8-validator/scripts/utf8_validator.py validate --file README.md
```

Output:

```
✓ README.md is valid UTF-8
```

## 2. Check for BOM

```bash
python skills/utf8-validator/scripts/utf8_validator.py validate --file data.txt --bom
```

Output (if BOM present):

```
Issues in data.txt:
  ✗ offset 0: UTF-8 BOM (EF BB BF) detected — usually unnecessary
```

## 3. JSON output

```bash
python skills/utf8-validator/scripts/utf8_validator.py validate --file data.txt --json
```

```json
{
  "file": "data.txt",
  "valid": true,
  "errors": []
}
```

## Error handling

File not found:

```bash
python skills/utf8-validator/scripts/utf8_validator.py validate --file missing.txt
```

```json
{
  "file": "missing.txt",
  "valid": false,
  "errors": [{"error": "cannot_read", "message": "..."}]
}
```
