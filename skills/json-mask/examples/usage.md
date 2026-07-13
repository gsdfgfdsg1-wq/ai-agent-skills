# JSON Mask — Usage Examples

## 1. Mask exact keys

```bash
python skills/json-mask/scripts/json_mask.py mask --file user.json --keys password secret_token
```

```json
{
  "name": "Alice",
  "password": "***",
  "secret_token": "***"
}
```

## 2. Partial masking

```bash
python skills/json-mask/scripts/json_mask.py mask --file user.json --keys email --strategy partial
```

```json
{
  "email": "ali***com"
}
```

## 3. Hash strategy

```bash
python skills/json-mask/scripts/json_mask.py mask --file user.json --keys ssn --strategy hash
```

```json
{
  "ssn": "[masked:a1b2c3d4]"
}
```

## 4. Regex key matching

```bash
python skills/json-mask/scripts/json_mask.py mask --file data.json --regex-keys ".*secret.*" ".*key$"
```

## 5. Prefix matching

```bash
python skills/json-mask/scripts/json_mask.py mask --file data.json --prefix-keys "aws_" "db_"
```

## 6. Remove keys entirely

```bash
python skills/json-mask/scripts/json_mask.py mask --file user.json --keys password --strategy remove
```

## 7. Piped from stdin

```bash
cat data.json | python skills/json-mask/scripts/json_mask.py mask --keys password
```

## Error handling

Invalid JSON:

```bash
python skills/json-mask/scripts/json_mask.py mask --file broken.json --keys password
```

```
Error: cannot read broken.json: Expecting value: line 1 column 1 (char 0)
```
