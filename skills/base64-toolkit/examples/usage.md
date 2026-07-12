# Usage Examples

## 1. Encode a string

```bash
python skills/base64-toolkit/scripts/base64_toolkit.py encode -s 'Hello, World!'
```

Output:

```text
SGVsbG8sIFdvcmxkIQ==
```

## 2. Decode a Base64 string

```bash
python skills/base64-toolkit/scripts/base64_toolkit.py decode -s 'SGVsbG8sIFdvcmxkIQ=='
```

Output:

```text
Hello, World!
```

## 3. URL-safe Base64

```bash
python skills/base64-toolkit/scripts/base64_toolkit.py encode -s 'Hello?' --urlsafe
python skills/base64-toolkit/scripts/base64_toolkit.py decode -s 'SGVsbG8_'
```

URL-safe mode replaces `+`/`/` with `-`/`_`.

## 4. Auto-detect Base64

```bash
python skills/base64-toolkit/scripts/base64_toolkit.py detect -s 'SGVsbG8sIFdvcmxkIQ=='
```

Output:

```text
VALID Base64 (standard)
preview: Hello, World!
```

## 5. Encode/decode a file

```bash
python skills/base64-toolkit/scripts/base64_toolkit.py encode --file config.json --json
python skills/base64-toolkit/scripts/base64_toolkit.py decode --file encoded.txt
```

Returns JSON with input_length and output for encoding; decoded text for decoding.
