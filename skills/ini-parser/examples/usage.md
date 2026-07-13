# INI Parser — Usage Examples

## 1. Parse and display an INI file

```bash
python skills/ini-parser/scripts/ini_parser.py parse --file config.ini
```

Output:

```
[database]
  host = localhost
  port = 5432
  name = mydb

[server]
  host = 0.0.0.0
  port = 8080
```

## 2. Get a specific key value

```bash
python skills/ini-parser/scripts/ini_parser.py get --file config.ini --section database --key host
```

Output:

```
localhost
```

## 3. List sections

```bash
python skills/ini-parser/scripts/ini_parser.py sections --file config.ini
```

## 4. List keys in a section

```bash
python skills/ini-parser/scripts/ini_parser.py keys --file config.ini --section database
```

## 5. JSON output

```bash
python skills/ini-parser/scripts/ini_parser.py parse --file config.ini --json
```

```json
{
  "database": {"host": "localhost", "port": "5432", "name": "mydb"},
  "server": {"host": "0.0.0.0", "port": "8080"}
}
```

## Error handling

Missing section:

```bash
python skills/ini-parser/scripts/ini_parser.py get --file config.ini --section missing --key x
```

```
Error: section 'missing' not found
```
