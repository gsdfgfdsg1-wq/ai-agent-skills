# json-path-query — Usage Examples

All examples assume your working directory contains the script. Adjust paths as needed.

```bash
SCRIPT=scripts/json_path_query.py
```

---

## Example 1: Query a top-level key from a JSON file

Given `package.json`:

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "private": true
}
```

```bash
python $SCRIPT query --file package.json -p '$.name'
```

Output:

```
my-project
```

---

## Example 2: Access a nested key with dot notation

Given `config.json`:

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "credentials": {
      "user": "admin",
      "password": "secret"
    }
  }
}
```

```bash
python $SCRIPT query --file config.json -p '$.database.credentials.user'
```

Output:

```
admin
```

---

## Example 3: Get all elements from an array with `[*]`

Given `users.json`:

```json
{
  "users": [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
    {"name": "Carol", "email": "carol@example.com"}
  ]
}
```

```bash
python $SCRIPT query --file users.json -p '$.users[*].email'
```

Output:

```
alice@example.com
bob@example.com
carol@example.com
```

With `--json` flag:

```bash
python $SCRIPT query --file users.json -p '$.users[*].email' --json
```

Output:

```json
["alice@example.com", "bob@example.com", "carol@example.com"]
```

---

## Example 4: Access an array element by index

Given `api.json`:

```json
{
  "data": {
    "results": [
      {"id": 101, "label": "alpha"},
      {"id": 202, "label": "beta"},
      {"id": 303, "label": "gamma"}
    ]
  }
}
```

```bash
python $SCRIPT query --file api.json -p '$.data.results[1].label'
```

Output:

```
beta
```

---

## Example 5: Recursive descent with `..key`

Given `deep.json`:

```json
{
  "id": "root",
  "children": [
    {
      "id": "child-1",
      "label": "A",
      "children": [
        {"id": "grandchild-1", "label": "A1"},
        {"id": "grandchild-2", "label": "A2"}
      ]
    },
    {
      "id": "child-2",
      "label": "B"
    }
  ]
}
```

Find all `id` values at any depth:

```bash
python $SCRIPT query --file deep.json -p '$..id'
```

Output:

```
root
child-1
grandchild-1
grandchild-2
child-2
```

Find all `label` values:

```bash
python $SCRIPT query --file deep.json -p '$..label'
```

Output:

```
A
A1
A2
B
```

---

## Example 6: Extract fields from a JSONL file

Given `events.jsonl`:

```
{"event": {"type": "click", "ts": 1001}, "user": "alice"}
{"event": {"type": "scroll", "ts": 1002}, "user": "bob"}
{"event": {"type": "click", "ts": 1003}, "user": "carol"}
```

```bash
python $SCRIPT extract --file events.jsonl -p '$.event.type'
```

Output:

```
click
scroll
click
```

Extract user names as JSON array:

```bash
python $SCRIPT extract --file events.jsonl -p '$.user' --json
```

Output:

```json
["alice", "bob", "carol"]
```

---

## Example 7: Combine recursive descent with JSONL extraction

Given `logs.jsonl`:

```
{"request": {"headers": {"X-Request-Id": "abc123"}}, "status": 200}
{"request": {"headers": {"X-Request-Id": "def456"}}, "status": 404}
```

```bash
python $SCRIPT extract --file logs.jsonl -p '$..X-Request-Id'
```

Output:

```
abc123
def456
```

---

## Example 8: Error — file not found

```bash
python $SCRIPT query --file nonexistent.json -p '$.name'
```

Output (stderr):

```
Error: file not found: nonexistent.json
```

Exit code: `1`

---

## Example 9: Error — invalid path expression

```bash
python $SCRIPT query --file package.json -p 'name'
```

Output (stderr):

```
Error: path expression must start with '$': name
```

Exit code: `2`

---

## Example 10: Error — key not found

Given `package.json` from Example 1:

```bash
python $SCRIPT query --file package.json -p '$.description'
```

Output (stderr):

```
Error: key 'description' not found in object
```

Exit code: `4`

---

## Example 11: Error — index out of range

Given `users.json` from Example 3:

```bash
python $SCRIPT query --file users.json -p '$.users[10]'
```

Output (stderr):

```
Error: index 10 out of range (length 3)
```

Exit code: `4`

---

## Example 12: Error — malformed JSON

Given `bad.json`:

```
{invalid json content}
```

```bash
python $SCRIPT query --file bad.json -p '$.key'
```

Output (stderr):

```
Error: malformed JSON in bad.json: Expecting property name enclosed in double quotes: line 2 column 1 (char 1)
```

Exit code: `3`
