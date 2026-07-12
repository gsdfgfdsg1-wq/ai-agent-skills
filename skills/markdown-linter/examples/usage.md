# Usage Examples

## 1. Basic check

```bash
python skills/markdown-linter/scripts/lint_markdown.py README.md
```

Output:

```text
Found 2 issue(s):

[WARNING] MD005 README.md:15
  heading level jump from H1 to H3

[WARNING] MD010 README.md:45
  missing newline at end of file
```

## 2. Check a directory

```bash
python skills/markdown-linter/scripts/lint_markdown.py docs/
```

Finds all `.md`, `.markdown`, and `.mdx` files recursively.

## 3. CI integration

```bash
python skills/markdown-linter/scripts/lint_markdown.py . --exit-code --severity warning
echo $?
# 0 if no issues, 1 if any warning or error found
```

## 4. JSON output

```bash
python skills/markdown-linter/scripts/lint_markdown.py . --json
```

Returns a JSON array with `rule`, `severity`, `line`, `message`, `file` per finding.

## 5. Custom line length

```bash
python skills/markdown-linter/scripts/lint_markdown.py . --max-line 80
```

Flags lines longer than 80 characters (excluding table rows).
