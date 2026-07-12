# Usage Examples

## 1. Basic scan

```bash
python skills/css-unused-finder/scripts/find_unused.py style.css --html src/
```

Output:

```text
CSS Unused Selector Report

  Total selectors parsed: 47
  Unused items: 3

  Unused classes (2):
    .legacy-banner
    .old-tooltip

  Unused IDs (1):
    #deprecated-modal

  Unused tags (0):
```

## 2. Multiple CSS and HTML files

```bash
python skills/css-unused-finder/scripts/find_unused.py reset.css layout.css --html index.html about.html
```

## 3. JSON output

```bash
python skills/css-unused-finder/scripts/find_unused.py style.css --html . --json
```

## 4. CI integration

```bash
python skills/css-unused-finder/scripts/find_unused.py style.css --html . --exit-code
echo $?
# 1 if unused selectors found, 0 if all are used
```
