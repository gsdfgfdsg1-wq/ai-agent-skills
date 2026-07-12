# gzip-toolkit Usage Examples

## 1. Compress a Log File with Default Settings

Compress `app.log` to `app.log.gz` using the default compression level (6):

```bash
python gzip_toolkit.py compress --file /var/log/app.log
```

Output:

```
success: True
input_file: /var/log/app.log
output_file: /var/log/app.log.gz
original_size: 10485760
compressed_size: 1234567
compression_ratio: 11.8%
level: 6
```

## 2. Compress with Maximum Compression and JSON Output

Use level 9 for best compression ratio, and pipe JSON output to another tool:

```bash
python gzip_toolkit.py compress --file data.csv --level 9 --json
```

Output:

```json
{
  "success": true,
  "input_file": "data.csv",
  "output_file": "data.csv.gz",
  "original_size": 5242880,
  "compressed_size": 456789,
  "compression_ratio": "8.7%",
  "level": 9
}
```

Use in a pipeline:

```bash
python gzip_toolkit.py compress --file data.csv --level 9 --json | python -c "import sys,json; d=json.load(sys.stdin); print(d['output_file'])"
```

## 3. Compress to a Custom Output Path

Specify a different output location:

```bash
python gzip_toolkit.py compress --file report.pdf --output /backups/2024/report.pdf.gz --level 5
```

## 4. Decompress a Gzip File

Decompress `data.csv.gz` back to `data.csv` (output path is derived automatically by stripping `.gz`):

```bash
python gzip_toolkit.py decompress --file data.csv.gz
```

Output:

```
success: True
input_file: data.csv.gz
output_file: data.csv
output_size: 5242880
```

Decompress to a custom path:

```bash
python gzip_toolkit.py decompress --file archive/data.csv.gz --output /tmp/restored.csv
```

## 5. Inspect Gzip Metadata

View original size, compressed size, compression ratio, and modification time:

```bash
python gzip_toolkit.py inspect --file data.csv.gz
```

Output:

```
success: True
file: data.csv.gz
original_size: 5242880
compressed_size: 456789
compression_ratio: 8.7%
modification_time: 2024-03-15 14:30:00 UTC
```

With JSON for scripting:

```bash
python gzip_toolkit.py inspect --file data.csv.gz --json
```

## 6. Test Gzip File Integrity

Verify that a gzip file is not corrupt:

```bash
python gzip_toolkit.py test --file data.csv.gz
```

Output:

```
success: True
file: data.csv.gz
integrity: OK
```

Use `--json` to integrate integrity checks into automation:

```bash
python gzip_toolkit.py test --file data.csv.gz --json
if [ $? -eq 0 ]; then
    echo "File is intact"
else
    echo "File is corrupt or missing"
fi
```

## 7. Error Handling Examples

### File not found

```bash
python gzip_toolkit.py compress --file nonexistent.txt
```

Output (stderr):

```
Error: File not found: nonexistent.txt
```

Exit code: 1

### Not a gzip file

```bash
python gzip_toolkit.py decompress --file plain.txt
```

Output (stderr):

```
Error: Not a gzip file (missing .gz extension): plain.txt
```

Exit code: 1

### Invalid compression level

```bash
python gzip_toolkit.py compress --file data.csv --level 12
```

Output (stderr):

```
Error: Invalid compression level: 12 (must be 1-9)
```

Exit code: 1

### Output file already exists

```bash
python gzip_toolkit.py decompress --file data.csv.gz
# data.csv already exists
```

Output (stderr):

```
Error: Output file already exists: data.csv
```

Exit code: 1

All errors also produce JSON output when `--json` is used:

```json
{
  "success": false,
  "error": "File not found: nonexistent.txt"
}
```

## 8. Batch Integrity Check with Shell Loop

Test all `.gz` files in a directory and report any corrupt ones:

```bash
for f in /backups/*.gz; do
    python gzip_toolkit.py test --file "$f" --json 2>/dev/null || echo "CORRUPT: $f"
done
```
