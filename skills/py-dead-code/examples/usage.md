# Usage Examples

## 1. Scan a directory

```bash
python skills/py-dead-code/scripts/py_dead_code.py src/
```

Output:

```text
src/utils.py:3: Unused import: os (imported as 'os')
src/api.py:45: Unreachable code after return on line 45
```

## 2. Single file analysis

```bash
python skills/py-dead-code/scripts/py_dead_code.py myfile.py
```

Reports unused imports and unreachable code in the specified file.

## 3. JSON output

```bash
python skills/py-dead-code/scripts/py_dead_code.py src/ --json
```

Returns JSON array with file, line, type, name, and message for each finding.

## 4. Skip unreachable code check

```bash
python skills/py-dead-code/scripts/py_dead_code.py . --ignore-unreachable
```

Only reports unused imports, ignoring unreachable code paths.

## 5. CI mode

```bash
python skills/py-dead-code/scripts/py_dead_code.py src/ || echo "Dead code found!"
```

Exits with code 1 if any dead code is found, making it CI-friendly.
