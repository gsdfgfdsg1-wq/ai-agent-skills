# CSV Merge — Usage Examples

## 1. Inner join two CSV files

```bash
python skills/csv-merge/scripts/csv_merge.py merge --key id --files users.csv orders.csv
```

## 2. Left join with output file

```bash
python skills/csv-merge/scripts/csv_merge.py merge --key email --how left --files users.csv orders.csv --output merged.csv
```

## 3. Outer join with JSON output

```bash
python skills/csv-merge/scripts/csv_merge.py merge --key id --how outer --files a.csv b.csv --json
```

```json
{
  "headers": ["id", "name", "amount"],
  "rows": [
    {"id": "1", "name": "Alice", "amount": "100"},
    {"id": "2", "name": "Bob", "amount": ""},
    {"id": "3", "name": "", "amount": "200"}
  ],
  "count": 3
}
```

## Error handling

Missing key column:

```bash
python skills/csv-merge/scripts/csv_merge.py merge --key missing_id --files a.csv b.csv
```

```
Error: key column 'missing_id' not found in a.csv
```
