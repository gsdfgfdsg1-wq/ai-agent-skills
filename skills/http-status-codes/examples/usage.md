# Usage Examples

## 1. Look up a response code

```bash
python skills/http-status-codes/scripts/http_status_codes.py --code 404
```

Output:

```text
404 Not Found (Client Error)
  The server cannot find the requested resource.
```

## 2. List an HTTP category

```bash
python skills/http-status-codes/scripts/http_status_codes.py --category 5xx
```

Lists built-in server-error codes such as `500 Internal Server Error`, `502 Bad Gateway`, and `503 Service Unavailable`.

## 3. Search descriptions

```bash
python skills/http-status-codes/scripts/http_status_codes.py --search timeout
```

Matches codes whose phrase, category, or description contains `timeout`, including `408 Request Timeout` and `504 Gateway Timeout`.

## 4. Produce JSON

```bash
python skills/http-status-codes/scripts/http_status_codes.py --code 429 --json
```

```json
[
  {
    "code": 429,
    "phrase": "Too Many Requests",
    "category": "Client Error",
    "description": "The client sent too many requests in a period of time."
  }
]
```
