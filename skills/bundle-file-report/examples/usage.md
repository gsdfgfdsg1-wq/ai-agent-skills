# Usage

Run the script with Python 3.9 or later.

## Show the largest files

```bash
python skills/bundle-file-report/scripts/bundle_file_report.py dist --top 10
```

Example output:

```text
  512000 B  assets/vendor.js
  180224 B  assets/app.js
   81920 B  assets/app.css
Summary: 3 reported of 42 included files; 774144 B reported, 2097152 B total
```

Equal-sized files are ordered by their relative path to keep output stable across runs.

## Limit candidates to JavaScript

```bash
python skills/bundle-file-report/scripts/bundle_file_report.py dist \
  --include '*.js' \
  --top 15
```

Add multiple `--include` values to include several glob classes:

```bash
python skills/bundle-file-report/scripts/bundle_file_report.py dist \
  --include '*.js' \
  --include '*.css' \
  --json
```

## Generate JSON

```bash
python skills/bundle-file-report/scripts/bundle_file_report.py build --top 5 --json
```

The JSON `summary.total_size_bytes` includes every included file, while `summary.reported_size_bytes` includes only the selected Top N records.

## Boundary and error handling

```bash
python skills/bundle-file-report/scripts/bundle_file_report.py dist --top 0 --json
python skills/bundle-file-report/scripts/bundle_file_report.py dist --top -1
```

`--top 0` succeeds with an empty `files` list. A negative value is rejected with exit code `2`.
