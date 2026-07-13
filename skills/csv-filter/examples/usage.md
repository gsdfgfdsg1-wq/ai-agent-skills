# CSV Filter — Usage Examples

## 1. Filter by equality

```bash
python skills/csv-filter/scripts/csv_filter.py filter --file users.csv --column "status" --op eq --value "active"
```

## 2. Numeric comparison

```bash
python skills/csv-filter/scripts/csv_filter.py filter --file data.csv --column "age" --op gt --value "25"
```

## 3. Regex match

```bash
python skills/csv-filter/scripts/csv_filter.py filter --file data.csv --column "email" --op regex --value ".*@example\\.com$"
```

## 4. Empty value check

```bash
python skills/csv-filter/scripts/csv_filter.py filter --file data.csv --column "phone" --op empty
```

## 5. Multiple conditions (AND)

```bash
python skills/csv-filter/scripts/csv_filter.py filter --file users.csv --column "status" --op eq --value "active" --and "age:gte:18" --and "country:eq:US"
```

## 6. Write to file

```bash
python skills/csv-filter/scripts/csv_filter.py filter --file data.csv --column "score" --op gte --value "80" --output high_scores.csv
```

## 7. JSON output

```bash
python skills/csv-filter/scripts/csv_filter.py filter --file data.csv --column "type" --op eq --value "A" --json
```

## Error handling

Missing column:

```bash
python skills/csv-filter/scripts/csv_filter.py filter --file data.csv --column "nonexistent" --op eq --value "x"
```

```
Error: column 'nonexistent' not found in CSV. Available: name, age, status
```
