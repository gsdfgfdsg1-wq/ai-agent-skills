# json-flattener Usage Examples

## Example 1 — Flatten a nested JSON object

Given a nested JSON structure representing a user profile:

```json
{
  "user": {
    "name": "Alice",
    "age": 30,
    "address": {
      "city": "Shanghai",
      "zip": "200000"
    }
  }
}
```

**Command:**

```bash
python scripts/json_flattener.py flatten -s '{
  "user": {
    "name": "Alice",
    "age": 30,
    "address": {
      "city": "Shanghai",
      "zip": "200000"
    }
  }
}'
```

**Output:**

```
user.name=Alice
user.age=30
user.address.city=Shanghai
user.address.zip=200000
```

With `--json` flag:

```bash
python scripts/json_flattener.py flatten -s '{"user":{"name":"Alice","age":30}}' --json
```

**Output:**

```json
{
  "user.name": "Alice",
  "user.age": 30
}
```

---

## Example 2 — Flatten arrays with index notation

JSON arrays use `[N]` notation for each element:

```json
{
  "project": "Orion",
  "tags": ["alpha", "beta", "rc1"],
  "members": [
    {"name": "Bob", "role": "lead"},
    {"name": "Carol", "role": "dev"}
  ]
}
```

**Command:**

```bash
python scripts/json_flattener.py flatten -s '{
  "project": "Orion",
  "tags": ["alpha", "beta", "rc1"],
  "members": [
    {"name": "Bob", "role": "lead"},
    {"name": "Carol", "role": "dev"}
  ]
}' --json
```

**Output:**

```json
{
  "project": "Orion",
  "tags[0]": "alpha",
  "tags[1]": "beta",
  "tags[2]": "rc1",
  "members[0].name": "Bob",
  "members[0].role": "lead",
  "members[1].name": "Carol",
  "members[1].role": "dev"
}
```

---

## Example 3 — Unflatten key=value pairs back to nested JSON

You can reconstruct the original nested structure from flat key=value pairs:

**Command:**

```bash
python scripts/json_flattener.py unflatten -s 'user.name=Alice
user.age=30
user.address.city=Shanghai
user.address.zip=200000' --json
```

**Output:**

```json
{
  "user": {
    "name": "Alice",
    "age": 30,
    "address": {
      "city": "Shanghai",
      "zip": "200000"
    }
  }
}
```

You can also unflatten from a flat JSON object (useful when the flat data was stored as JSON):

```bash
python scripts/json_flattener.py unflatten -s '{"user.name":"Alice","user.age":30}' --json
```

**Output:**

```json
{
  "user": {
    "name": "Alice",
    "age": 30
  }
}
```

---

## Example 4 — Read from a file with a custom separator

Suppose you have `config.json`:

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "credentials": {
      "user": "admin",
      "password": "secret"
    }
  },
  "logging": {
    "level": "info"
  }
}
```

**Command with `/` separator:**

```bash
python scripts/json_flattener.py flatten --file config.json --separator "/"
```

**Output:**

```
database/host=localhost
database/port=5432
database/credentials/user=admin
database/credentials/password=secret
logging/level=info
```

Unflatten with the same separator:

```bash
python scripts/json_flattener.py unflatten --file flat_config.txt --separator "/" --json
```

---

## Example 5 — Round-trip: flatten then unflatten

A common workflow is to flatten, edit specific values, then unflatten:

```bash
# Step 1: Flatten to a file
python scripts/json_flattener.py flatten --file data.json > flat.txt

# Step 2: Edit flat.txt (e.g. change server.port from 8080 to 9090)
sed -i 's/server.port=8080/server.port=9090/' flat.txt

# Step 3: Unflatten back to nested JSON
python scripts/json_flattener.py unflatten --file flat.txt --json > data_updated.json
```

---

## Example 6 — Error handling

### Invalid JSON input

```bash
python scripts/json_flattener.py flatten -s '{invalid json}'
```

**Output (stderr):**

```
Error: Invalid JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

### File not found

```bash
python scripts/json_flattener.py flatten --file nonexistent.json
```

**Output (stderr):**

```
Error: File not found: nonexistent.json
```

### Missing input argument

```bash
python scripts/json_flattener.py flatten
```

**Output (stderr):**

```
Error: Either --file or -s must be provided
```

### Key conflict during unflatten

```bash
python scripts/json_flattener.py unflatten -s 'a=1
a.b=2' --json
```

**Output (stderr):**

```
Error: Key conflict: 'a' is already a leaf but also used as container
```

---

## Example 7 — Flatten a top-level array

```bash
python scripts/json_flattener.py flatten -s '[{"id":1},{"id":2}]' --json
```

**Output:**

```json
{
  "[0].id": 1,
  "[1].id": 2
}
```

Unflatten it back:

```bash
python scripts/json_flattener.py unflatten -s '{"[0].id":1,"[1].id":2}' --json
```

**Output:**

```json
[
  {
    "id": 1
  },
  {
    "id": 2
  }
]
```
