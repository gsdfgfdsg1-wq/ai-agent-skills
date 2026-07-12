# Usage Examples

## 1. Simple match test

```bash
python skills/regex-tester/scripts/regex_tester.py -p '^\d{3}-\d{4}$' -s '123-4567' -s 'abc-defg'
```

Output:

```text
MATCH: '123-4567'
  text: '123-4567' (pos 0-8)
NO MATCH: 'abc-defg'
```

## 2. Capture groups

```bash
python skills/regex-tester/scripts/regex_tester.py -p '(\w+)@(\w+)\.(\w+)' -s 'user@example.com'
```

Output:

```text
MATCH: 'user@example.com'
  text: 'user@example.com' (pos 0-16)
  group(1): 'user' (pos 0-4)
  group(2): 'example' (pos 5-12)
  group(3): 'com' (pos 13-16)
```

## 3. Find all matches

```bash
python skills/regex-tester/scripts/regex_tester.py -p '\d+' -s 'abc123def456ghi789' --findall
```

Output:

```text
MATCH: 'abc123def456ghi789'
  [0] '123'
  [1] '456'
  [2] '789'
```

## 4. Case-insensitive flag

```bash
python skills/regex-tester/scripts/regex_tester.py -p 'hello' -s 'HELLO world' --flags IGNORECASE --json
```

Returns JSON with match details including position and matched text.

## 5. Read strings from file

```bash
python skills/regex-tester/scripts/regex_tester.py -p 'TODO:\s*(.+)' -f todos.txt --flags IGNORECASE
```

Tests the pattern against each non-empty line in the file.
