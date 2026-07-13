# Lorem Generator — Usage Examples

## 1. Generate 3 paragraphs

```bash
python skills/lorem-generator/scripts/lorem_gen.py paragraphs --count 3
```

## 2. Start with classic Lorem ipsum

```bash
python skills/lorem-generator/scripts/lorem_gen.py paragraphs --count 2 --start-with-lorem
```

## 3. Generate 10 sentences

```bash
python skills/lorem-generator/scripts/lorem_gen.py sentences --count 10
```

## 4. Generate 30 words

```bash
python skills/lorem-generator/scripts/lorem_gen.py words --count 30
```

## 5. JSON output

```bash
python skills/lorem-generator/scripts/lorem_gen.py paragraphs --count 1 --json
```

```json
{
  "paragraphs": [
    "Rerum magnam quaerat minima nostrum exercitationem. Vel eum iure quam nihil impedit. Quo minus quod maxime placeat facere possimus."
  ],
  "count": 1
}
```
