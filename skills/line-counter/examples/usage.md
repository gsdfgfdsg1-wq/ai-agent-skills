# Line Counter — Usage Examples

## 1. Count lines in a directory

```bash
python skills/line-counter/scripts/line_counter.py count --path ./src
```

```
Extension    Files    Total     Code    Blank  Comment
--------------------------------------------------------
.py             12      840      620      120      100
.js              8      520      400       80       40
.css             3      210      180       20       10
```

## 2. Filter by extension

```bash
python skills/line-counter/scripts/line_counter.py count --path ./src --ext .py .js
```

## 3. Summary with percentages

```bash
python skills/line-counter/scripts/line_counter.py summary --path ./src
```

```
Extensions:    3
Files:         23
Total lines:   1570
Code lines:    1200 (76.4%)
Blank lines:   220 (14.0%)
Comment lines: 150 (9.6%)
```

## 4. JSON output

```bash
python skills/line-counter/scripts/line_counter.py count --path ./src --json
```

## 5. Single file

```bash
python skills/line-counter/scripts/line_counter.py count --path ./main.py
```

```
File: ./main.py
  Extension: .py
  Total:     150
  Code:      120
  Blank:     20
  Comment:   10
```

## Error handling

Non-existent path:

```bash
python skills/line-counter/scripts/line_counter.py count --path ./nonexistent
```

```
Error: ./nonexistent is not a file or directory
```
