---
name: xml-to-json
description: Convert XML files to JSON format with attribute and namespace handling without external dependencies.
license: MIT
---

# xml-to-json

Convert XML files and strings to JSON format with full attribute and namespace handling, using only Python standard library.

## When to Use

- Converting XML configuration files, API responses, or data exports to JSON for further processing
- Inspecting the structure of unknown or complex XML documents before parsing
- Integrating XML data sources into JSON-based pipelines or APIs
- Batch-transforming XML files in scripts without installing third-party dependencies
- Debugging XML content by viewing it in a more readable JSON representation

## Capabilities

- **convert** — Transform XML to JSON with configurable output
  - Read from file (`--file`) or inline string (`-s`)
  - Write to file (`--output`) or stdout
  - Pretty-print JSON (`--pretty`)
  - Toggle attribute inclusion (`--attrs`)
  - Customize text content key (`--text-key`, default `#text`)
  - Customize attribute prefix (`--attr-prefix`, default `@`)
  - Output conversion statistics as JSON (`--json`)
- **inspect** — Show XML structure summary
  - Lists all tags, their attributes, and nesting depth
  - Quick overview without full conversion
- Handles malformed XML, missing files, and empty input gracefully
- No external dependencies — uses only Python stdlib (`xml.etree.ElementTree`, `json`, `argparse`, `sys`, `os`, `re`)

## Usage

```bash
# Convert an XML file to JSON (stdout)
python scripts/xml_to_json.py convert --file input.xml

# Convert with pretty-print to a file
python scripts/xml_to_json.py convert --file input.xml --pretty --output output.json

# Convert an XML string
python scripts/xml_to_json.py convert -s '<root><item id="1">hello</item></root>'

# Custom keys and prefix
python scripts/xml_to_json.py convert --file input.xml --text-key "_text" --attr-prefix "$"

# Get conversion stats as JSON
python scripts/xml_to_json.py convert --file input.xml --json

# Inspect XML structure
python scripts/xml_to_json.py inspect --file input.xml
```

## Examples

### Basic Conversion

```bash
python scripts/xml_to_json.py convert --file data.xml
```

### Pretty-Printed Output to File

```bash
python scripts/xml_to_json.py convert --file data.xml --pretty --output data.json
```

### Inline XML String

```bash
python scripts/xml_to_json.py convert -s '<catalog><book id="1"><title>Python 101</title></book></catalog>'
```

### Inspect Structure

```bash
python scripts/xml_to_json.py inspect --file data.xml
```

More examples: see [examples/usage.md](examples/usage.md).

## Reference

### Conversion Rules

| XML Construct        | JSON Representation                                      |
|----------------------|----------------------------------------------------------|
| Element              | Object key named after the tag                           |
| Attributes           | Keys prefixed with `@` (e.g., `@id`)                    |
| Text content         | Key `#text` (customizable via `--text-key`)             |
| Repeated elements    | Array of objects                                         |
| Mixed content        | Text in `#text`, children as separate keys              |
| Namespace prefixes   | Preserved in tag names (e.g., `{ns}tag` or `ns:tag`)    |
| Empty element        | Empty object `{}` or `null` if no attributes/text       |

### Exit Codes

| Code | Meaning              |
|------|----------------------|
| 0    | Success              |
| 1    | General error        |
| 2    | Argument error       |

### Dependencies

None — Python 3.6+ standard library only.
