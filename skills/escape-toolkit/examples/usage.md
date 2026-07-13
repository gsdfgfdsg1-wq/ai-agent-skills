# Escape Toolkit — Usage Examples

## 1. Escape for JSON

```bash
python skills/escape-toolkit/scripts/escape_tool.py escape --text 'Hello "world"' --context json
```

```
"Hello \"world\""
```

## 2. Escape for HTML

```bash
python skills/escape-toolkit/scripts/escape_tool.py escape --text '<script>alert("xss")</script>' --context html
```

```
&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;
```

## 3. Unescape HTML entities

```bash
python skills/escape-toolkit/scripts/escape_tool.py unescape --text '&lt;div&gt;Hello &amp; world&lt;/div&gt;' --context html
```

```
<div>Hello & world</div>
```

## 4. Escape for C

```bash
python skills/escape-toolkit/scripts/escape_tool.py escape --text $'Line1\nLine2' --context c
```

```
"Line1\nLine2"
```

## 5. Unescape JSON string

```bash
python skills/escape-toolkit/scripts/escape_tool.py unescape --text '"Hello \\\"world\\\""' --context json
```

```
Hello "world"
```

## Error handling

Invalid context:

```bash
python skills/escape-toolkit/scripts/escape_tool.py escape --text "test" --context unknown
```

```
Error: argument --context: invalid choice: 'unknown'
```
