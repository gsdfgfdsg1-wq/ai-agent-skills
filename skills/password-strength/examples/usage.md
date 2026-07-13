# Password Strength — Usage Examples

## 1. Full analysis

```bash
python skills/password-strength/scripts/pw_strength.py analyze --password "MyP@ss123!"
```

```
Password: **********
  Length:      10
  Entropy:     59.5 bits
  Score:       62/100 (strong)
  Char types:  4/4
  Patterns (1):
    [INFO] Password is 10 chars (12+ recommended)
```

## 2. Quick score

```bash
python skills/password-strength/scripts/pw_strength.py score --password "abc123"
```

```
12/100 (very-weak)
```

## 3. Strong password

```bash
python skills/password-strength/scripts/pw_strength.py analyze --password "K9$mP2xL#vR7nQ!w"
```

```
Password: ****************
  Length:      16
  Entropy:     100.4 bits
  Score:       96/100 (very-strong)
  Char types:  4/4
```

## 4. Common password detection

```bash
python skills/password-strength/scripts/pw_strength.py analyze --password "password123"
```

```
Password: ***********
  Length:      11
  Entropy:     55.7 bits
  Score:       15/100 (very-weak)
  Char types:  2/4
  Patterns (1):
    [CRITICAL] 'password123' is in common password list
```
