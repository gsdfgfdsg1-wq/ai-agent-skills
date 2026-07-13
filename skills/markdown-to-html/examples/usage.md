# Markdown to HTML — Usage Examples

## 1. Convert with default style

```bash
python skills/markdown-to-html/scripts/md2html.py convert --file README.md
```

Outputs HTML to stdout.

## 2. Convert with GitHub style

```bash
python skills/markdown-to-html/scripts/md2html.py convert --file README.md --style github --output readme.html
```

## 3. Add table of contents

```bash
python skills/markdown-to-html/scripts/md2html.py convert --file README.md --toc --style dark --output docs.html
```

## 4. Custom title

```bash
python skills/markdown-to-html/scripts/md2html.py convert --file README.md --title "My Docs"
```

## Error handling

Missing file:

```bash
python skills/markdown-to-html/scripts/md2html.py convert --file nonexistent.md
```

```
Error: cannot read nonexistent.md: [Errno 2] No such file or directory
```
