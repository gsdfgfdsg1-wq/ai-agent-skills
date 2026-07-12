# Usage Examples

## 1. Basic minification

```bash
python skills/html-minifier/scripts/minify_html.py index.html
```

Outputs minified HTML to stdout.

## 2. Write to file with stats

```bash
python skills/html-minifier/scripts/minify_html.py index.html -o index.min.html --stats
```

Output:

```text
Original: 15234 bytes
Minified: 11401 bytes
Saved:    3833 bytes (25.2%)
```

## 3. From stdin

```bash
cat index.html | python skills/html-minifier/scripts/minify_html.py -
```

## 4. Keep IE conditional comments

```bash
python skills/html-minifier/scripts/minify_html.py index.html --keep-conditional-comments
```

## 5. Batch minification

```bash
for f in src/*.html; do
  python skills/html-minifier/scripts/minify_html.py "$f" -o "dist/$(basename $f)" --stats
done
```
