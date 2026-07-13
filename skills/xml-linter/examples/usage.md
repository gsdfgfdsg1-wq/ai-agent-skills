# XML Linter — Usage Examples

## 1. Lint an XML file

```bash
python skills/xml-linter/scripts/xml_lint.py lint --file config.xml
```

```
config.xml: 2 issue(s) (0 errors, 1 warnings, 1 info)
  [WARNING] trailing-whitespace line 3: Trailing whitespace on line 3
  [INFO] missing-encoding: No encoding declaration in XML header — UTF-8 is assumed
```

## 2. Check well-formedness

```bash
python skills/xml-linter/scripts/xml_lint.py check-well-formed --file data.xml
```

```
OK: data.xml is well-formed XML.
```

## 3. JSON output

```bash
python skills/xml-linter/scripts/xml_lint.py lint --file config.xml --json
```

## Error handling

Invalid XML:

```bash
python skills/xml-linter/scripts/xml_lint.py check-well-formed --file broken.xml
```

```
  [ERROR] not well-formed (line 5): unclosed tag: <item>
```

Non-existent file:

```bash
python skills/xml-linter/scripts/xml_lint.py lint --file missing.xml
```

```
Error: cannot read missing.xml: [Errno 2] No such file or directory: 'missing.xml'
```
