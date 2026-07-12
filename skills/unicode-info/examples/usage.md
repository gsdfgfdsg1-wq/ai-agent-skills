# unicode-info Usage Examples

## Example 1: Look up a single ASCII character

```bash
python scripts/unicode_info.py char -s "A"
```

Output:

```
Character:     A
Codepoint:     U+0041
Name:          LATIN CAPITAL LETTER A
Category:      Lu (Letter, Uppercase)
Bidirectional: L
Combining:     0
Block:         Basic Latin
Decimal:       65
Hex:           0x41
Octal:         0o101
```

## Example 2: Look up multiple CJK characters at once

```bash
python scripts/unicode_info.py char -s "你好世界"
```

Output:

```
Character:     你
Codepoint:     U+4F60
Name:          CJK UNIFIED IDEOGRAPH-4F60
Category:      Lo (Letter, Other)
Bidirectional: L
Combining:     0
Block:         CJK Unified Ideographs
Decimal:       20320
Hex:           0x4F60
Octal:         0o47740

Character:     好
Codepoint:     U+597D
Name:          CJK UNIFIED IDEOGRAPH-597D
Category:      Lo (Letter, Other)
Bidirectional: L
Combining:     0
Block:         CJK Unified Ideographs
Decimal:       22909
Hex:           0x597D
Octal:         0o54775

...
```

## Example 3: Look up a character by codepoint (U+XXXX format)

```bash
python scripts/unicode_info.py codepoint -s U+4E2D
```

Output:

```
Character:     中
Codepoint:     U+4E2D
Name:          CJK UNIFIED IDEOGRAPH-4E2D
Category:      Lo (Letter, Other)
Bidirectional: L
Combining:     0
Block:         CJK Unified Ideographs
Decimal:       20013
Hex:           0x4E2D
Octal:         0o47255
```

## Example 4: Look up a character by codepoint (0xXXXX format) with JSON output

```bash
python scripts/unicode_info.py codepoint -s 0x00A9 --json
```

Output:

```json
{
  "character": "\u00a9",
  "codepoint": "U+00A9",
  "name": "COPYRIGHT SIGN",
  "category": "So",
  "category_name": "Symbol, Other",
  "bidirectional": "ON",
  "combining_class": 0,
  "block": "Latin-1 Supplement",
  "decimal": 169,
  "hex": "0xA9",
  "octal": "0o251"
}
```

## Example 5: List characters in a Unicode range (Miscellaneous Symbols)

```bash
python scripts/unicode_info.py range --from U+2600 --to U+260F --limit 10
```

Output:

```
Character:     ☀
Codepoint:     U+2600
Name:          BLACK SUN WITH RAYS
Category:      So (Symbol, Other)
Bidirectional: ON
Combining:     0
Block:         Miscellaneous Symbols
Decimal:       9728
Hex:           0x2600
Octal:         0o23000

Character:     ☁
Codepoint:     U+2601
Name:          CLOUD
...

... showing 10 of 16 characters (use --limit to show more)
```

## Example 6: Search for characters by name pattern

```bash
python scripts/unicode_info.py search -s "ARROW"
```

Output:

```
U+2190  ←  LEFTWARDS ARROW  [Sm]  Arrows
U+2191  ↑  UPWARDS ARROW  [Sm]  Arrows
U+2192  →  RIGHTWARDS ARROW  [Sm]  Arrows
U+2193  ↓  DOWNWARDS ARROW  [Sm]  Arrows
U+2194  ↔  LEFT RIGHT ARROW  [Sm]  Arrows
U+2195  ↕  UP DOWN ARROW  [Sm]  Arrows
U+2196  ↖  NORTH WEST ARROW  [Sm]  Arrows
U+2197  ↗  NORTH EAST ARROW  [Sm]  Arrows
U+2198  ↘  SOUTH EAST ARROW  [Sm]  Arrows
U+2199  ↙  SOUTH WEST ARROW  [Sm]  Arrows
...

Found 20 result(s)
```

## Example 7: Search with category filter (decimal digits only)

```bash
python scripts/unicode_info.py search -s "DIGIT" --category Nd --limit 10
```

Output:

```
U+0030  0  DIGIT ZERO  [Nd]  Basic Latin
U+0031  1  DIGIT ONE  [Nd]  Basic Latin
U+0032  2  DIGIT TWO  [Nd]  Basic Latin
U+0033  3  DIGIT THREE  [Nd]  Basic Latin
U+0034  4  DIGIT FOUR  [Nd]  Basic Latin
U+0035  5  DIGIT FIVE  [Nd]  Basic Latin
U+0036  6  DIGIT SIX  [Nd]  Basic Latin
U+0037  7  DIGIT SEVEN  [Nd]  Basic Latin
U+0038  8  DIGIT EIGHT  [Nd]  Basic Latin
U+0039  9  DIGIT NINE  [Nd]  Basic Latin

Found 10 result(s)
```

## Example 8: Error handling — invalid codepoint

```bash
python scripts/unicode_info.py codepoint -s U+ZZZZ
```

Output (stderr):

```
Error: Invalid codepoint format: 'U+ZZZZ'  (expected U+XXXX or 0xXXXX)
```

## Example 9: Range with JSON output for piping

```bash
python scripts/unicode_info.py range --from U+0030 --to U+0039 --json
```

Output:

```json
[
  {
    "character": "0",
    "codepoint": "U+0030",
    "name": "DIGIT ZERO",
    "category": "Nd",
    "category_name": "Number, Decimal Digit",
    "bidirectional": "EN",
    "combining_class": 0,
    "block": "Basic Latin",
    "decimal": 48,
    "hex": "0x30",
    "octal": "0o60"
  },
  ...
]
```

## Example 10: Search for emoji-related characters

```bash
python scripts/unicode_info.py search -s "HEART" --limit 5
```

Output:

```
U+2661  ♡  WHITE HEART SUIT  [So]  Miscellaneous Symbols
U+2665  ♥  BLACK HEART SUIT  [So]  Miscellaneous Symbols
U+2764  ❤  HEAVY BLACK HEART  [So]  Miscellaneous Symbols
U+1F499  💙  BLUE HEART  [So]  Miscellaneous Symbols and Pictographs
U+1F49A  💚  GREEN HEART  [So]  Miscellaneous Symbols and Pictographs

Found 5 result(s)
```
