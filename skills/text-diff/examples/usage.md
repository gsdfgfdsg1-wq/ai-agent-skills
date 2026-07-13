# Text Diff — Usage Examples

## 1. Compare two strings

```bash
python skills/text-diff/scripts/text_diff.py diff --s1 "hello world foo" --s2 "hello earth foo"
```

Output:

```
  hello [world→earth] foo

Stats: 0 added, 0 deleted, 1 changed, 2 unchanged
```

## 2. Compare two files

```bash
python skills/text-diff/scripts/text_diff.py diff --file1 v1.txt --file2 v2.txt
```

## 3. JSON output

```bash
python skills/text-diff/scripts/text_diff.py diff --s1 "the quick fox" --s2 "the slow fox jumps" --json
```

```json
{
  "stats": {"adds": 1, "dels": 0, "changes": 1, "equals": 2},
  "diff": [
    {"op": "equal", "word": "the"},
    {"op": "change", "from": ["quick"], "to": ["slow"]},
    {"op": "equal", "word": "fox"},
    {"op": "add", "word": "jumps"}
  ]
}
```

## Error handling

Missing input:

```bash
python skills/text-diff/scripts/text_diff.py diff --s1 "hello"
```

```
Error: provide --file2 or --s2
```
