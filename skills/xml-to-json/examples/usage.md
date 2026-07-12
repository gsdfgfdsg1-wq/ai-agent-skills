# xml-to-json Usage Examples

## Example 1: Basic File Conversion

Given `books.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<catalog>
  <book id="1" lang="en">
    <title>Python 101</title>
    <author>Jane Doe</author>
    <price>29.99</price>
  </book>
  <book id="2" lang="fr">
    <title>Apprendre Python</title>
    <author>Jean Dupont</author>
    <price>34.50</price>
  </book>
</catalog>
```

Convert and pretty-print to stdout:

```bash
python scripts/xml_to_json.py convert --file books.xml --pretty
```

Output:

```json
{
  "catalog": {
    "book": [
      {
        "@id": "1",
        "@lang": "en",
        "title": "Python 101",
        "author": "Jane Doe",
        "price": "29.99"
      },
      {
        "@id": "2",
        "@lang": "fr",
        "title": "Apprendre Python",
        "author": "Jean Dupont",
        "price": "34.50"
      }
    ]
  }
}
```

Note: the two `<book>` elements are automatically collected into a JSON array.

---

## Example 2: Inline String with Custom Keys

Convert an inline XML string with custom text key and attribute prefix:

```bash
python scripts/xml_to_json.py convert \
  -s '<user id="42" role="admin"><name>Alice</name><bio>Engineer & maintainer</bio></user>' \
  --text-key "_text" \
  --attr-prefix "$" \
  --pretty
```

Output:

```json
{
  "user": {
    "$id": "42",
    "$role": "admin",
    "name": "Alice",
    "bio": "Engineer & maintainer"
  }
}
```

---

## Example 3: Inspect XML Structure

Before converting a large or unknown XML file, inspect its structure:

```bash
python scripts/xml_to_json.py inspect --file books.xml
```

Output:

```json
{
  "root_tag": "catalog",
  "max_depth": 2,
  "element_counts": {
    "catalog": 1,
    "book": 2,
    "title": 2,
    "author": 2,
    "price": 2
  },
  "attributes_by_tag": {
    "book": ["id", "lang"]
  }
}
```

This gives you a quick overview: root tag, nesting depth, element frequency, and which tags carry attributes.

---

## Example 4: Convert with Output File and Stats

Write JSON to a file and also print conversion metadata:

```bash
python scripts/xml_to_json.py convert \
  --file books.xml \
  --pretty \
  --output books.json \
  --json
```

`books.json` will contain the pretty-printed JSON. After the JSON output, stats are printed:

```json
{
  "input_file": "books.xml",
  "root_tag": "catalog",
  "output_file": "books.json",
  "pretty": true,
  "include_attrs": true,
  "text_key": "#text",
  "attr_prefix": "@"
}
```

---

## Example 5: Mixed Content (Text + Children)

XML with mixed content — text alongside child elements:

```bash
python scripts/xml_to_json.py convert \
  -s '<p class="intro">Hello <b>world</b> and <i>everyone</i></p>' \
  --pretty
```

Output:

```json
{
  "p": {
    "@class": "intro",
    "#text": "Hello",
    "b": "world",
    "i": "everyone"
  }
}
```

The text "Hello" is stored under the `#text` key, while child elements remain separate keys.

---

## Example 6: Namespace Handling

XML with namespaces is supported. Namespace URIs are preserved in tag names:

```bash
python scripts/xml_to_json.py convert \
  -s '<feed xmlns="http://www.w3.org/2005/Atom"><title>My Blog</title></feed>' \
  --pretty
```

Output:

```json
{
  "{http://www.w3.org/2005/Atom}feed": {
    "{http://www.w3.org/2005/Atom}title": "My Blog"
  }
}
```

---

## Example 7: Excluding Attributes

Strip attributes and get a clean data-only view:

```bash
python scripts/xml_to_json.py convert \
  --file books.xml \
  --no-attrs \
  --pretty
```

Output:

```json
{
  "catalog": {
    "book": [
      {
        "title": "Python 101",
        "author": "Jane Doe",
        "price": "29.99"
      },
      {
        "title": "Apprendre Python",
        "author": "Jean Dupont",
        "price": "34.50"
      }
    ]
  }
}
```

---

## Example 8: Error Handling

The script provides clear error messages for common problems.

**File not found:**

```bash
python scripts/xml_to_json.py convert --file missing.xml
# Error: File not found: missing.xml
```

**Malformed XML:**

```bash
python scripts/xml_to_json.py convert -s '<root><unclosed>'
# Error: Malformed XML — no element found: line 1, column 19
```

**Empty input:**

```bash
python scripts/xml_to_json.py convert -s ''
# Error: Empty XML input.
```

**Missing --file for inspect:**

```bash
python scripts/xml_to_json.py inspect
# Error: --file is required for inspect.
```
