# Pip Requirements Extractor — Usage Examples

## 1. Extract imports from a single file

```bash
python skills/pip-req-extractor/scripts/pip_req_extractor.py extract --path myapp.py
```

Output:

```
Files scanned: 1
Third-party packages (3):
  flask
  requests
  yaml
```

## 2. Extract imports from a directory

```bash
python skills/pip-req-extractor/scripts/pip_req_extractor.py extract --path src/
```

Output:

```
Files scanned: 12
Third-party packages (5):
  click
  flask
  pydantic
  requests
  yaml
```

## 3. Generate requirements.txt

```bash
python skills/pip-req-extractor/scripts/pip_req_extractor.py extract --path src/ --output requirements.txt
```

Output:

```
Files scanned: 12
Third-party packages (5):
  click
  flask
  pydantic
  requests
  yaml
Written to: requirements.txt
```

## 4. JSON output

```bash
python skills/pip-req-extractor/scripts/pip_req_extractor.py extract --path src/ --json
```

```json
{
  "source": "src/",
  "files_scanned": 12,
  "third_party": ["click", "flask", "pydantic", "requests", "yaml"],
  "stdlib": ["json", "os", "sys"]
}
```

## Error handling

Non-existent path:

```bash
python skills/pip-req-extractor/scripts/pip_req_extractor.py extract --path nonexistent/
```

```
No Python files found in: nonexistent/
```
