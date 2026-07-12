# mime-type-checker Usage Examples

## Example 1: Detect MIME Type of a PDF File

Detect the MIME type using both extension and content analysis:

```bash
python scripts/mime_type_checker.py detect --file report.pdf
```

Output:

```
File:       /home/user/report.pdf
Method:     both
Extension:  application/pdf
Content:    application/pdf
Best match: application/pdf
Confidence: high
```

When both methods agree, confidence is reported as `high`. If a `.pdf` file actually contained PNG data, the two results would differ and confidence would drop to `medium`.

---

## Example 2: Detect Using Content Magic Bytes Only

Ignore the file extension and detect purely from the file's binary header:

```bash
python scripts/mime_type_checker.py detect --file renamed_image.png --method content
```

This is useful when the file extension may be incorrect or spoofed. Even if `renamed_image.png` is actually a JPEG, the content detection will report `image/jpeg`.

Output:

```
File:       /home/user/renamed_image.png
Method:     content
Content:    image/jpeg
Best match: image/jpeg
Confidence: high
```

---

## Example 3: JSON Output for Scripting

Use `--json` to produce machine-readable output for pipeline integration:

```bash
python scripts/mime_type_checker.py detect --file data.json --json
```

Output:

```json
{
  "file": "/home/user/data.json",
  "method": "both",
  "results": {
    "extension": {
      "mime": "application/json",
      "description": "Extension: .json"
    },
    "content": {
      "mime": "application/json",
      "description": "JSON data"
    }
  },
  "best_mime": "application/json",
  "confidence": "high"
}
```

This format is easy to parse with `jq` or other JSON tools:

```bash
MIME=$(python scripts/mime_type_checker.py detect --file upload.bin --json | jq -r '.best_mime')
echo "Detected: $MIME"
```

---

## Example 4: Lookup MIME Type by Extension

Find the MIME type associated with a file extension:

```bash
python scripts/mime_type_checker.py lookup -s py
```

Output:

```
Extension: .py
MIME type: text/x-python
```

Other examples:

```bash
# HTML files
python scripts/mime_type_checker.py lookup -s html
# => Extension: .html
# => MIME type: text/html

# ZIP archives
python scripts/mime_type_checker.py lookup -s zip
# => Extension: .zip
# => MIME type: application/zip

# With JSON output
python scripts/mime_type_checker.py lookup -s json --json
# => {"extension": "json", "mime_type": "application/json"}
```

---

## Example 5: Find Extensions for a MIME Type

Reverse lookup — find all known file extensions for a given MIME type:

```bash
python scripts/mime_type_checker.py ext -s application/json
```

Output:

```
MIME type:  application/json
Extensions: json, map
```

More reverse-lookup examples:

```bash
# Image types
python scripts/mime_type_checker.py ext -s image/jpeg
# => MIME type:  image/jpeg
# => Extensions: jfif, jpe, jpeg, jpg

# Video types
python scripts/mime_type_checker.py ext -s video/mp4
# => MIME type:  video/mp4
# => Extensions: mp4

# With JSON output
python scripts/mime_type_checker.py ext -s text/html --json
# => {"mime_type": "text/html", "extensions": ["htm", "html"]}
```

---

## Example 6: Detect an Archive File with Mismatched Extension

Sometimes files are renamed with wrong extensions. Content detection can reveal the true format:

```bash
# A ZIP file renamed to .dat
python scripts/mime_type_checker.py detect --file backup.dat --method both
```

Output:

```
File:       /home/user/backup.dat
Method:     both
Extension:  unknown
Content:    application/zip
Best match: application/zip
Confidence: medium
```

Since the extension `.dat` has no standard MIME mapping, extension detection returns `unknown`, but content magic bytes (`PK\x03\x04`) correctly identify it as a ZIP archive.

---

## Example 7: Error Handling

The tool provides clear error messages for common issues:

```bash
# File does not exist
python scripts/mime_type_checker.py detect --file missing.txt
# => Error: File not found: missing.txt

# Unknown extension
python scripts/mime_type_checker.py lookup -s xyz123
# => Error: Unknown extension: .xyz123

# Unknown MIME type
python scripts/mime_type_checker.py ext -s application/x-nonexistent
# => Error: Unknown MIME type: application/x-nonexistent
```

All errors exit with code `1`, making them easy to catch in scripts:

```bash
if ! python scripts/mime_type_checker.py detect --file "$FILE" --json > /dev/null 2>&1; then
    echo "Detection failed for $FILE"
fi
```

---

## Example 8: Batch Detection in a Shell Loop

Combine with standard Unix tools for batch MIME type detection:

```bash
for file in uploads/*; do
    mime=$(python scripts/mime_type_checker.py detect --file "$file" --json 2>/dev/null \
           | python -c "import sys,json; print(json.load(sys.stdin)['best_mime'])" 2>/dev/null)
    echo "$file -> $mime"
done
```

Sample output:

```
uploads/doc.pdf -> application/pdf
uploads/image.png -> image/png
uploads/data.csv -> text/csv
uploads/archive.zip -> application/zip
uploads/script.py -> text/x-python
```
