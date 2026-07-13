# Tar Toolkit — Usage Examples

## 1. List archive contents

```bash
python skills/tar-toolkit/scripts/tar_tool.py list --archive backup.tar.gz
```

```
Archive: backup.tar.gz
Type        Size  Name
----        ----  ----
dir             -  src/
file          142  src/main.py
file           58  src/utils.py
file          220  README.md

Total: 4 entries
```

## 2. Create a tar.gz archive

```bash
python skills/tar-toolkit/scripts/tar_tool.py create --source ./myproject --output backup.tar.gz
```

## 3. Extract an archive

```bash
python skills/tar-toolkit/scripts/tar_tool.py extract --archive backup.tar.gz --output ./restored
```

## 4. Show archive info

```bash
python skills/tar-toolkit/scripts/tar_tool.py info --archive backup.tar.gz
```

```
Archive: backup.tar.gz
Archive size:     1,024 bytes
Content size:     3,200 bytes
Compression:      68.0%
Files:            3
Directories:      1
```

## Error handling

Missing archive:

```bash
python skills/tar-toolkit/scripts/tar_tool.py list --archive missing.tar
```

```
Error: cannot open missing.tar: [Errno 2] No such file or directory
```
