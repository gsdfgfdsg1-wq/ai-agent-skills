# Usage Examples

## 1. Convert to stdout

```bash
python skills/swagger-to-markdown/scripts/swagger_to_markdown.py swagger.json
```

Outputs Markdown documentation to the terminal.

## 2. Write to file

```bash
python skills/swagger-to-markdown/scripts/swagger_to_markdown.py api.json --output docs/api.md
```

Writes the generated Markdown to the specified file.

## 3. Include model definitions

```bash
python skills/swagger-to-markdown/scripts/swagger_to_markdown.py swagger.json --include-models
```

Definitions section is included by default; this flag is kept for compatibility.

## 4. Multiple specs

```bash
python skills/swagger-to-markdown/scripts/swagger_to_markdown.py v1.json v2.json --output combined.md
```

Generates combined Markdown from multiple Swagger specs, separated by horizontal rules.
