# CSV Schema Audit Examples

Create `customer-schema.json`:

```json
{
  "required_columns": ["customer_id", "email", "display_name"],
  "columns": {
    "customer_id": {"nullable": false},
    "email": {"nullable": false},
    "display_name": {"nullable": true}
  }
}
```

Audit a CSV and print a readable result:

```bash
python scripts/audit_csv.py customers.csv customer-schema.json
```

Emit a JSON result for CI:

```bash
python scripts/audit_csv.py customers.csv customer-schema.json --json
```

The following input fails because `email` occurs twice and line 2 has an empty required value:

```csv
customer_id,email,email,display_name
c-100,,second@example.test,Ada
```

The JSON output contains `valid`, `error_count`, and an `errors` array. Each error includes a stable `rule`, a message, and relevant header or row details.
