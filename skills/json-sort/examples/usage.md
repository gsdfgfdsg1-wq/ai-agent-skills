# JSON Sort — Usage Examples

## 1. Sort JSON keys

```bash
python skills/json-sort/scripts/json_sort.py sort --file config.json
```

Input:
```json
{"z": 1, "a": 2, "m": {"z2": 3, "a2": 4}}
```

Output:
```json
{
  "a": 2,
  "m": {
    "a2": 4,
    "z2": 3
  },
  "z": 1
}
```

## 2. Reverse sort

```bash
python skills/json-sort/scripts/json_sort.py sort --file config.json --reverse
```

## 3. Limit depth

```bash
python skills/json-sort/scripts/json_sort.py sort --file nested.json --depth 1
```

## 4. Sort in-place

```bash
python skills/json-sort/scripts/json_sort.py sort --file config.json --inplace
```

## 5. Pipe from stdin

```bash
echo '{"c":3,"a":1,"b":2}' | python skills/json-sort/scripts/json_sort.py sort
```

## Error handling

Invalid JSON:

```bash
echo 'not json' | python skills/json-sort/scripts/json_sort.py sort
```

```
Error: invalid JSON: Expecting value: line 1 column 1 (char 0)
```
