# Chmod Calculator — Usage Examples

## 1. Octal to symbolic

```bash
python skills/chmod-calculator/scripts/chmod_calc.py octal2symbolic --mode 755
```

```
755 → rwxr-xr-x
```

## 2. Symbolic to octal

```bash
python skills/chmod-calculator/scripts/chmod_calc.py symbolic2octal --mode rwxr-xr-x
```

```
rwxr-xr-x → 755
```

## 3. Explain permissions

```bash
python skills/chmod-calculator/scripts/chmod_calc.py explain --mode 644
```

```
Mode: 644 (rw-r--r--)
  user (owner): read, write
  group: read
  other: read
```

## 4. Apply symbolic changes

```bash
python skills/chmod-calculator/scripts/chmod_calc.py combine --base 644 --changes u+x,g-w
```

```
644 + u+x,g-w → 754 (rwxr-xr--)
```

## 5. Special bits (setuid, setgid, sticky)

```bash
python skills/chmod-calculator/scripts/chmod_calc.py octal2symbolic --mode 4755
```

```
4755 → rwsr-xr-x
```

## Error handling

Invalid octal:

```bash
python skills/chmod-calculator/scripts/chmod_calc.py octal2symbolic --mode 999
```

```
Error: Invalid octal digit '9'
```

Invalid symbolic:

```bash
python skills/chmod-calculator/scripts/chmod_calc.py symbolic2octal --mode rwx
```

```
Error: Invalid symbolic mode 'rwx': must be 9 characters
```
