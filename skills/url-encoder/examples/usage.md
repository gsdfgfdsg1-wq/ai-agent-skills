# URL Encoder — Usage Examples

## 1. Encoding a Full URL with Special Characters

When a URL contains spaces or reserved characters, you must percent-encode it before using it in an HTTP request.

```bash
python scripts/url_encoder.py encode -s "https://example.com/search?q=hello world&lang=en 中文"
```

Output:

```
https%3A//example.com/search%3Fq%3Dhello%20world%26lang%3Den%20%E4%B8%AD%E6%96%87
```

With JSON output for programmatic consumption:

```bash
python scripts/url_encoder.py encode -s "https://example.com/search?q=hello world&lang=en 中文" --json
```

Output:

```json
{"input": "https://example.com/search?q=hello world&lang=en 中文", "component": "full", "encoded": "https%3A//example.com/search%3Fq%3Dhello%20world%26lang%3Den%20%E4%B8%AD%E6%96%87"}
```

## 2. Encoding Individual Components

Sometimes you only need to encode a specific part of a URL — for example, just the query string or path segment — while preserving the delimiter characters of other components.

### Encode a query string

```bash
python scripts/url_encoder.py encode -s "q=hello world&filter=status>active" --component query
```

Output:

```
q=hello+world&filter=status%3Eactive
```

`--component query` uses `quote_plus` (spaces become `+`) and preserves `=` and `&` as safe characters.

### Encode a path segment

```bash
python scripts/url_encoder.py encode -s "/api/v1/users/john doe/profile" --component path
```

Output:

```
/api/v1/users/john%20doe/profile
```

`--component path` preserves `/` as a safe character so the path structure remains intact.

### Encode a fragment

```bash
python scripts/url_encoder.py encode -s "section 1 — introduction" --component fragment
```

Output:

```
section%201%20%E2%80%94%20introduction
```

## 3. Decoding Percent-Encoded URLs

### Decode a full encoded URL

```bash
python scripts/url_encoder.py decode -s "https%3A//example.com/search%3Fq%3Dhello%20world"
```

Output:

```
https://example.com/search?q=hello world
```

### Decode a query string (handles `+` as space)

```bash
python scripts/url_encoder.py decode -s "q=hello+world&filter=status%3Eactive" --component query
```

Output:

```
q=hello world&filter=status>active
```

### Decode with JSON output

```bash
python scripts/url_encoder.py decode -s "name=%E5%BC%A0%E4%B8%89" --json
```

Output:

```json
{"input": "name=%E5%BC%A0%E4%B8%89", "component": "full", "decoded": "name=张三"}
```

## 4. Parsing a URL into Components

Break a complex URL into all its structural parts for inspection or transformation.

```bash
python scripts/url_encoder.py parse -s "https://admin:secret@api.example.com:8443/v2/users?role=admin&active=true#user-list"
```

Output:

```
  scheme      https
  netloc      admin:secret@api.example.com:8443
  path        /v2/users
  params
  query       role=admin&active=true
  fragment    user-list
  username    admin
  password    secret
  hostname    api.example.com
  port        8443
```

JSON variant for scripting:

```bash
python scripts/url_encoder.py parse -s "https://admin:secret@api.example.com:8443/v2/users?role=admin&active=true#user-list" --json
```

Output:

```json
{
  "scheme": "https",
  "netloc": "admin:secret@api.example.com:8443",
  "path": "/v2/users",
  "params": "",
  "query": "role=admin&active=true",
  "fragment": "user-list",
  "username": "admin",
  "password": "secret",
  "hostname": "api.example.com",
  "port": 8443
}
```

## 5. Building a URL from Components

Construct a complete URL by specifying each part individually. This is useful for building API endpoints dynamically.

### Basic URL

```bash
python scripts/url_encoder.py build --scheme https --host api.example.com --path "/v2/users"
```

Output:

```
https://api.example.com/v2/users
```

### URL with query parameters and fragment

```bash
python scripts/url_encoder.py build \
  --scheme https \
  --host api.example.com \
  --port 8443 \
  --path "/v2/search" \
  --query "q=python url encode" \
  --query "page=1" \
  --query "limit=20" \
  --fragment "results"
```

Output:

```
https://api.example.com:8443/v2/search?q=python+url+encode&page=1&limit=20#results
```

### Build with JSON output to see all components

```bash
python scripts/url_encoder.py build \
  --scheme https \
  --host example.com \
  --path "/api/data" \
  --query "format=json" \
  --query "lang=zh" \
  --fragment "top" \
  --json
```

Output:

```json
{
  "scheme": "https",
  "host": "example.com",
  "port": null,
  "path": "/api/data",
  "query": "format=json&lang=zh",
  "fragment": "top",
  "url": "https://example.com/api/data?format=json&lang=zh#top"
}
```

## 6. Error Handling

The script provides clear error messages for common mistakes.

### Missing required argument

```bash
python scripts/url_encoder.py encode
```

Output (stderr):

```
Error: -s/--string is required
```

### Invalid query parameter format in build

```bash
python scripts/url_encoder.py build --scheme https --host example.com --query "badformat"
```

Output (stderr):

```
Error: invalid query parameter 'badformat', expected KEY=VAL
```

### Missing required build arguments

```bash
python scripts/url_encoder.py build --scheme https
```

Output (stderr):

```
Error: --host is required
```

## 7. Piping and Automation

Combine with other CLI tools for URL processing pipelines.

### Encode a string from another command

```bash
echo "search term with spaces" | xargs -I {} python scripts/url_encoder.py encode -s "{}" --component query
```

Output:

```
search+term+with+spaces
```

### Parse and extract a single field with jq

```bash
python scripts/url_encoder.py parse -s "https://example.com/api?key=val#section" --json | python -m json.tool --extract ".query"
```

Or more simply:

```bash
python scripts/url_encoder.py parse -s "https://example.com/api?key=val#section" --json | jq .query
```

Output:

```
"key=val"
```
