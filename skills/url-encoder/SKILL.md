---
name: url-encoder
description: Encode and decode URLs and query parameters with component-level control without external dependencies.
license: MIT
---

# url-encoder

Encode, decode, parse, and build URLs with fine-grained component-level control. Pure Python, no external dependencies.

## When to Use

- Encoding or decoding full URLs or individual components (path, query, fragment) safely
- Parsing a URL into its structural components (scheme, host, path, query, fragment, etc.)
- Building a URL from individual components, including multi-value query parameters
- Debugging or inspecting URL encoding issues in logs, configs, or API calls
- Preparing URLs for API requests where certain characters must be percent-encoded
- Validating URL structure before making HTTP calls

## Capabilities

| Subcommand | Description |
|------------|-------------|
| `encode` | Percent-encode a URL or a specific component (full, query, fragment, path) |
| `decode` | Decode a percent-encoded URL or component back to its original form |
| `parse` | Parse a URL into its components (scheme, netloc, path, params, query, fragment) |
| `build` | Build a URL from individual components (scheme, host, port, path, query key=value pairs, fragment) |

Key features:

- **Component-level control** — encode/decode only the part you need (query, fragment, path, or full URL)
- **Safe encoding** — uses `urllib.parse.quote` / `quote_plus` with appropriate safe characters per component
- **JSON output** — add `--json` to any subcommand for structured, machine-readable output
- **Multi-value query params** — `build` supports repeated `--query KEY=VAL` flags
- **Error handling** — meaningful error messages for invalid URLs, missing arguments, and decode failures
- **Zero dependencies** — uses only Python standard library (`urllib.parse`, `argparse`, `json`, `sys`)

## Usage

```
python scripts/url_encoder.py <subcommand> [options]
```

### Subcommands

#### encode

```
python scripts/url_encoder.py encode -s STRING [--component {full,query,fragment,path}] [--json]
```

#### decode

```
python scripts/url_encoder.py decode -s STRING [--component {full,query,fragment,path}] [--json]
```

#### parse

```
python scripts/url_encoder.py parse -s URL [--json]
```

#### build

```
python scripts/url_encoder.py build --scheme SCHEME --host HOST [--port PORT] [--path PATH] [--query KEY=VAL] [--fragment FRAGMENT] [--json]
```

### Common Options

| Option | Description |
|--------|-------------|
| `-s`, `--string` | Input string or URL (required for encode, decode, parse) |
| `--component` | Target component: `full`, `query`, `fragment`, `path` (default: `full`) |
| `--json` | Output result as JSON |
| `--scheme` | URL scheme for build (e.g. `https`) |
| `--host` | Host for build (e.g. `example.com`) |
| `--port` | Port number for build |
| `--path` | URL path for build (e.g. `/api/v1/users`) |
| `--query` | Query parameter as `KEY=VAL`; may be repeated |
| `--fragment` | Fragment identifier for build |

## Examples

```bash
# Encode a full URL
python scripts/url_encoder.py encode -s "https://example.com/path with spaces?key=hello world"

# Encode only the query component
python scripts/url_encoder.py encode -s "key=hello world&filter=status>active" --component query

# Decode a percent-encoded URL
python scripts/url_encoder.py decode -s "https://example.com/path%20with%20spaces"

# Parse a URL into components
python scripts/url_encoder.py parse -s "https://user:pass@example.com:8080/api?q=test#section1"

# Build a URL from components
python scripts/url_encoder.py build --scheme https --host example.com --path "/search" --query "q=python url" --query "page=1" --fragment "results"

# Get JSON output for scripting
python scripts/url_encoder.py parse -s "https://example.com/api?key=val" --json
```

## Reference

- [`urllib.parse`](https://docs.python.org/3/library/urllib.parse.html) — Python standard library URL parsing and encoding
- [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986) — Uniform Resource Identifier (URI): Generic Syntax
- [Percent-encoding](https://en.wikipedia.org/wiki/Percent-encoding) — URL encoding specification
