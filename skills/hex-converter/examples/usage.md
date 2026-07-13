# Hex Converter — Usage Examples

## 1. Convert a hex value

```bash
python skills/hex-converter/scripts/hex_convert.py convert --value 0xFF
```

```
Input:  0xFF
  Dec: 255
  Hex: 0xff
  Oct: 0o377
  Bin: 0b11111111
```

## 2. Convert decimal to all bases

```bash
python skills/hex-converter/scripts/hex_convert.py convert --value 42 --base 10
```

## 3. Show bit layout

```bash
python skills/hex-converter/scripts/hex_convert.py bits --value 0xAB
```

```
Value:  171 (0xab)
Binary: 1010 1011
Width:  8 bits
```

## 4. Bitwise AND mask

```bash
python skills/hex-converter/scripts/hex_convert.py mask --value-a 0xFF --value-b 0x0F --op and
```

```
A: 255 (0xff)
B: 15 (0xf)
Op: AND
Result: 15 (0xf)
  Bin: 0b1111
```

## 5. Bitwise XOR

```bash
python skills/hex-converter/scripts/hex_convert.py mask --value-a 0xFF --value-b 0xFF --op xor
```

```
A: 255 (0xff)
B: 255 (0xff)
Op: XOR
Result: 0 (0x0)
  Bin: 0b0
```

## Error handling

Invalid number:

```bash
python skills/hex-converter/scripts/hex_convert.py convert --value "xyz"
```

```
Error: cannot determine base for 'xyz'
```
