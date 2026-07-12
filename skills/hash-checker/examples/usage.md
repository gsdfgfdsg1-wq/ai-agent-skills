# Hash Checker — Usage Examples

## 1. Compute SHA-256 hash of a file (default algorithm)

```bash
python skills/hash-checker/scripts/hash_checker.py compute --file README.md
```

Output:

```
a1b2c3d4e5f6...  README.md
```

JSON output with `--json`:

```bash
python skills/hash-checker/scripts/hash_checker.py compute --file README.md --json
```

```json
{
  "file": "README.md",
  "algorithm": "sha256",
  "hash": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
}
```

## 2. Compute MD5 hash of a file

```bash
python skills/hash-checker/scripts/hash_checker.py compute --file data.zip --algorithm md5
```

Output:

```
d41d8cd98f00b204e9800998ecf8427e  data.zip
```

JSON output:

```bash
python skills/hash-checker/scripts/hash_checker.py compute --file data.zip --algorithm md5 --json
```

```json
{
  "file": "data.zip",
  "algorithm": "md5",
  "hash": "d41d8cd98f00b204e9800998ecf8427e"
}
```

## 3. Verify a file against a known hash

```bash
python skills/hash-checker/scripts/hash_checker.py verify \
  --file release.tar.gz \
  --hash a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2 \
  --algorithm sha256
```

Output on match:

```
MATCH: release.tar.gz
  expected: a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2
  actual:   a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2
```

Output on mismatch:

```
MISMATCH: release.tar.gz
  expected: a1b2c3d4e5f6...
  actual:   f6e5d4c3b2a1...
```

JSON output:

```bash
python skills/hash-checker/scripts/hash_checker.py verify \
  --file release.tar.gz \
  --hash a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2 \
  --algorithm sha256 --json
```

```json
{
  "file": "release.tar.gz",
  "algorithm": "sha256",
  "expected": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
  "actual": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
  "match": true
}
```

## 4. Hash a text string

```bash
python skills/hash-checker/scripts/hash_checker.py text -s 'Hello, World!'
```

Output:

```
dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f  (text)
```

With SHA-512:

```bash
python skills/hash-checker/scripts/hash_checker.py text -s 'Hello, World!' --algorithm sha512
```

Output:

```
374d794a95cdcfd8b35993185fef9ba368f160d8daf432d08ba9f1ed1e5abe6cc69291e0fa2fe0006a52570ef18c19def4e617c33ce52ef0a6e5fbe318cb0387  (text)
```

JSON output:

```bash
python skills/hash-checker/scripts/hash_checker.py text -s 'Hello, World!' --json
```

```json
{
  "text": "Hello, World!",
  "algorithm": "sha256",
  "hash": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
}
```

## Error handling examples

File not found:

```bash
python skills/hash-checker/scripts/hash_checker.py compute --file nonexistent.txt
```

```
Error: file not found: nonexistent.txt
```

Missing required argument:

```bash
python skills/hash-checker/scripts/hash_checker.py compute
```

```
usage: hash_checker compute [-h] --file FILE [--algorithm {md5,sha1,sha256,sha512}]
hash_checker compute: error: the following arguments are required: --file
```
