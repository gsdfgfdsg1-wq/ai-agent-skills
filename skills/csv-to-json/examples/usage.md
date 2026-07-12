# csv-to-json Usage Examples

All examples assume you are running from the skill root directory (`skills/csv-to-json/`).

---

## Example 1: Basic CSV to JSON

Given `data.csv`:

```csv
name,age,score,active
Alice,30,95.5,yes
Bob,25,88.0,no
Charlie,,77.3,true
Diana,28,null,false
```

Run:

```bash
python scripts/csv_to_json.py --file data.csv
```

Output:

```json
[{"name": "Alice", "age": 30, "score": 95.5, "active": true}, {"name": "Bob", "age": 25, "score": 88.0, "active": false}, {"name": "Charlie", "age": null, "score": 77.3, "active": true}, {"name": "Diana", "age": 28, "score": null, "active": false}]
```

Type inference results:
- `"30"` → `30` (integer)
- `"95.5"` → `95.5` (float)
- `"yes"` → `true` (boolean)
- Empty cell → `null`
- `"null"` → `null`

---

## Example 2: Pretty-Printed Output to File

```bash
python scripts/csv_to_json.py --file data.csv --output result.json --pretty
```

The file `result.json` will contain:

```json
[
  {
    "name": "Alice",
    "age": 30,
    "score": 95.5,
    "active": true
  },
  {
    "name": "Bob",
    "age": 25,
    "score": 88.0,
    "active": false
  },
  {
    "name": "Charlie",
    "age": null,
    "score": 77.3,
    "active": true
  },
  {
    "name": "Diana",
    "age": 28,
    "score": null,
    "active": false
  }
]
```

---

## Example 3: Tab-Separated File with Stats

Given `inventory.tsv`:

```tsv
item	quantity	price	in_stock
Widget	100	9.99	true
Gadget	0	24.95	false
Doohickey	50	null	yes
```

Run:

```bash
python scripts/csv_to_json.py --file inventory.tsv --delimiter "\t" --json --pretty
```

Output:

```json
{
  "input_file": "inventory.tsv",
  "delimiter": "\t",
  "no_infer": false,
  "row_count": 3,
  "column_count": 4,
  "columns": [
    "item",
    "quantity",
    "price",
    "in_stock"
  ],
  "type_distribution": {
    "str": 1,
    "int": 3,
    "float": 2,
    "bool": 2,
    "NoneType": 1
  }
}
```

This is useful for logging, monitoring, or piping into downstream tooling.

---

## Example 4: Keep All Values as Strings

Sometimes you want the raw string values without any type conversion — for example, when leading zeros in IDs must be preserved.

Given `users.csv`:

```csv
id,zip_code,country
001,01001,US
002,90210,US
003,null,UK
```

Run:

```bash
python scripts/csv_to_json.py --file users.csv --no-infer --pretty
```

Output:

```json
[
  {
    "id": "001",
    "zip_code": "01001",
    "country": "US"
  },
  {
    "id": "002",
    "zip_code": "90210",
    "country": "US"
  },
  {
    "id": "003",
    "zip_code": null,
    "country": "UK"
  }
]
```

Note: `id` values remain strings `"001"` and `"002"`, preserving leading zeros. Null conversion still applies even in `--no-infer` mode.

---

## Example 5: Semicolon-Delimited CSV (European Format)

Many European locales use semicolons as CSV delimiters.

Given `sales_eu.csv`:

```csv
product;revenue;tax;profit
Desk;1200.50;yes;950.00
Chair;450.00;no;360.00
Lamp;null;false;null
```

Run:

```bash
python scripts/csv_to_json.py --file sales_eu.csv --delimiter ";" --pretty
```

Output:

```json
[
  {
    "product": "Desk",
    "revenue": 1200.5,
    "tax": true,
    "profit": 950.0
  },
  {
    "product": "Chair",
    "revenue": 450.0,
    "tax": false,
    "profit": 360.0
  },
  {
    "product": "Lamp",
    "revenue": null,
    "tax": false,
    "profit": null
  }
]
```

---

## Example 6: Error Handling — File Not Found

```bash
python scripts/csv_to_json.py --file nonexistent.csv
```

Output (stderr):

```
Error: Input file not found: nonexistent.csv
```

Exit code: `1`

---

## Example 7: Error Handling — Empty CSV

Given `empty.csv` (zero bytes or completely blank):

```bash
python scripts/csv_to_json.py --file empty.csv
```

Output (stderr):

```
Error: CSV file is empty (no data rows found)
```

Exit code: `2`

---

## Example 8: Error Handling — Header-Only CSV

Given `headers_only.csv`:

```csv
name,age,email
```

```bash
python scripts/csv_to_json.py --file headers_only.csv
```

Output (stderr):

```
Error: CSV file contains only headers (no data rows)
```

Exit code: `3`

---

## Example 9: Piping Output with Stats to Another Tool

Combine the `--json` stats flag with command-line tooling:

```bash
python scripts/csv_to_json.py --file data.csv --json | python -m json.tool
```

Or extract just the row count:

```bash
python scripts/csv_to_json.py --file data.csv --json | python -c "import sys,json; print(json.load(sys.stdin)['row_count'])"
```

---

## Example 10: Full Help Output

```bash
python scripts/csv_to_json.py --help
```

This displays the complete usage information including all flags and descriptions.
