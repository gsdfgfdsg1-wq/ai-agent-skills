# HTML Table Extractor — Usage Examples

## 1. Extract all tables as CSV

```bash
python skills/html-table-extractor/scripts/html_table.py extract --file page.html
```

## 2. Extract a specific table as JSON

```bash
python skills/html-table-extractor/scripts/html_table.py extract --file page.html --format json --table 0
```

```json
[
  {
    "table_index": 0,
    "headers": ["Name", "Age", "City"],
    "rows": [
      {"Name": "Alice", "Age": "30", "City": "Beijing"},
      {"Name": "Bob", "Age": "25", "City": "Shanghai"}
    ]
  }
]
```

## 3. List tables in a file

```bash
python skills/html-table-extractor/scripts/html_table.py list --file page.html
```

```
Table 0: 3 rows x 3 cols — headers: ['Name', 'Age', 'City']
```

## 4. Write to file

```bash
python skills/html-table-extractor/scripts/html_table.py extract --file page.html --output data.csv
```

## Error handling

File not found:

```bash
python skills/html-table-extractor/scripts/html_table.py extract --file missing.html
```

```
Error: cannot read missing.html: [Errno 2] No such file or directory
```

Invalid table index:

```bash
python skills/html-table-extractor/scripts/html_table.py extract --file page.html --table 99
```

```
Error: table index 99 out of range (0-0)
```
