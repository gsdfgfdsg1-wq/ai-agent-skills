# UUID Generator — Usage Examples

All examples assume the working directory is the skill root (`skills/uuid-generator/`).

---

## 1. Generate a single v4 UUID

```bash
python scripts/uuid_generator.py generate
```

Output:

```
f47ac10b-58cc-4372-a567-0e02b2c3d479
```

Every run produces a different random UUID.

---

## 2. Generate multiple v4 UUIDs in uppercase

```bash
python scripts/uuid_generator.py generate --count 5 --upper
```

Output:

```
A1B2C3D4-E5F6-4A7B-8C9D-0E1F2A3B4C5D
F7E6D5C4-B3A2-4980-1234-567890ABCDEF
...
```

Use `--upper` when you need uppercase hex (e.g. certain configuration formats).

---

## 3. Generate a v5 UUID (deterministic)

v5 UUIDs are reproducible: the same namespace + name always yields the same UUID.

```bash
python scripts/uuid_generator.py generate --version 5 --namespace dns --name example.com
```

Output:

```
cfbff0d1-9375-5685-ad9f-0e57e3b7c2e0
```

Running the same command again produces identical output — ideal for stable identifiers.

---

## 4. Generate v5 UUIDs with different namespaces

```bash
# URL namespace
python scripts/uuid_generator.py generate --version 5 --namespace url --name https://example.com/page

# OID namespace
python scripts/uuid_generator.py generate --version 5 --namespace oid --name 1.2.3.4.5

# Null namespace
python scripts/uuid_generator.py generate --version 5 --namespace null --name anything
```

Each namespace produces a distinct UUID even with the same name.

---

## 5. JSON output for scripting

```bash
python scripts/uuid_generator.py generate --count 3 --json
```

Output:

```json
[
  {
    "uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "version": 4
  },
  {
    "uuid": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
    "version": 4
  },
  {
    "uuid": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "version": 4
  }
]
```

Pipe into `jq` or other tools for further processing.

---

## 6. Validate a correct UUID

```bash
python scripts/uuid_generator.py validate -s 550e8400-e29b-41d4-a716-446655440000
```

Output:

```
Valid UUID — version 4, variant RFC 4122
```

---

## 7. Validate an invalid UUID

```bash
python scripts/uuid_generator.py validate -s not-a-uuid
```

Output:

```
Invalid: Invalid UUID string: 'not-a-uuid'
```

The command exits with code 0 for both valid and invalid results — check the output text or JSON `valid` field.

---

## 8. Validate with JSON output

```bash
python scripts/uuid_generator.py validate -s 550e8400-e29b-41d4-a716-446655440000 --json
```

Output:

```json
{
  "valid": true,
  "version": 4,
  "variant": "RFC 4122"
}
```

For an invalid UUID:

```json
{
  "valid": false,
  "error": "Invalid UUID string: 'not-a-uuid'"
}
```

---

## 9. Inspect a UUID (human-readable)

```bash
python scripts/uuid_generator.py inspect -s 6ba7b810-9dad-11d1-80b4-00c04fd430c8
```

Output:

```
UUID:     6ba7b810-9dad-11d1-80b4-00c04fd430c8
Version:  1
Variant:  RFC 4122
Hex:      6ba7b8109dad11d180b400c04fd430c8
URN:      urn:uuid:6ba7b810-9dad-11d1-80b4-00c04fd430c8
Fields:
  time_low                 1802462224
  time_mid                 40365
  time_hi_version          4561
  clock_seq_hi_variant     128
  clock_seq_low            180
  node                     50802530888
Time:     134879014261018000
Node:     50802530888
ClockSeq: 4660
```

---

## 10. Inspect a UUID (JSON output)

```bash
python scripts/uuid_generator.py inspect -s 550e8400-e29b-41d4-a716-446655440000 --json
```

Output:

```json
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "version": 4,
  "variant": "RFC 4122",
  "hex": "550e8400e29b41d4a716446655440000",
  "int": 113918325286362786267046464825819452160,
  "urn": "urn:uuid:550e8400-e29b-41d4-a716-446655440000",
  "fields": {
    "time_low": 1426214912,
    "time_mid": 58011,
    "time_hi_version": 16804,
    "clock_seq_hi_variant": 167,
    "clock_seq_low": 22,
    "node": 75986802401280
  }
}
```

---

## 11. Error: missing --name for v5

```bash
python scripts/uuid_generator.py generate --version 5 --namespace dns
```

Output (stderr):

```
Error: --name is required for v5 UUIDs.
```

Exit code is 1.

---

## 12. Error: invalid namespace

```bash
python scripts/uuid_generator.py generate --version 5 --namespace email --name test@example.com
```

Output (stderr):

```
Error: invalid namespace 'email'. Choose from: dns, url, oid, null
```

The `--namespace` flag only accepts the four standard RFC 4122 namespaces.

---

## 13. Error: invalid UUID on inspect

```bash
python scripts/uuid_generator.py inspect -s 12345
```

Output (stderr):

```
Error: Invalid UUID string: '12345'
```

Exit code is 1.

---

## 14. Piping generate output into validate

```bash
python scripts/uuid_generator.py generate | xargs -I{} python scripts/uuid_generator.py validate -s {}
```

Output:

```
Valid UUID — version 4, variant RFC 4122
```

This demonstrates composability for shell pipelines.

---

## 15. Generating bulk test fixtures

```bash
python scripts/uuid_generator.py generate --count 100 --json > fixtures/uuids.json
```

Produces a JSON array of 100 v4 UUIDs, suitable for seeding databases or test suites.
