# Usage Examples

## 1. Basic comparison

```bash
python skills/bundle-size-delta/scripts/bundle_size_delta.py build-v1/ build-v2/
```

Output:

```text
Comparing build-v1/ vs build-v2/
Total: 1.2 MB -> 1.4 MB (delta: 204.8 KB, +16.7%)

Increased (2):
  + main.js: 512.0 KB -> 640.0 KB (128.0 KB, +25.0%)
  + styles.css: 48.0 KB -> 52.0 KB (4.0 KB, +8.3%)

Decreased (1):
  - vendor.js: 640.0 KB -> 580.0 KB (-60.0 KB, -9.4%)

Unchanged: 12 file(s)
```

## 2. Threshold filter

```bash
python skills/bundle-size-delta/scripts/bundle_size_delta.py dist-old/ dist/ --threshold 10
```

Only reports files with changes greater than 10%.

## 3. JSON output

```bash
python skills/bundle-size-delta/scripts/bundle_size_delta.py prev/ curr/ --json
```

Returns JSON with total stats, increased, decreased, added, removed arrays.

## 4. CI gate

```bash
python skills/bundle-size-delta/scripts/bundle_size_delta.py prev/ curr/ --fail-threshold 20
```

Exits with code 1 if any file increased by more than 20%, making it a CI quality gate.

## 5. Sort by delta size

```bash
python skills/bundle-size-delta/scripts/bundle_size_delta.py prev/ curr/ --sort delta --top 5
```

Shows the top 5 largest changes, sorted by absolute delta.
