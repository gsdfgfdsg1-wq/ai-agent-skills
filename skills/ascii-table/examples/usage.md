# Usage Examples

## 1. Look up a decimal value

```bash
python skills/ascii-table/scripts/ascii_table.py lookup --decimal 65
```

```text
Dec  Hex   Binary     Character  Category
---  ----  ---------  ---------  --------
 65  0x41  0b1000001  A          printable
```

## 2. Look up a hexadecimal value

```bash
python skills/ascii-table/scripts/ascii_table.py lookup --hex 0x1B
```

## 3. Look up a character as JSON

```bash
python skills/ascii-table/scripts/ascii_table.py lookup --char A --json
```

## 4. Print printable punctuation

```bash
python skills/ascii-table/scripts/ascii_table.py range 32 47
```

## 5. Print a range as JSON

```bash
python skills/ascii-table/scripts/ascii_table.py range 48 57 --json
```
