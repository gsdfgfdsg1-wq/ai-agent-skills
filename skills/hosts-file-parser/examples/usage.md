# Hosts File Parser Examples

Create a sample file named `hosts.txt`:

```text
127.0.0.1 localhost loopback
::1 localhost
192.0.2.10 app.internal api.internal
192.0.2.10 app.internal # duplicate mapping
invalid-ip bad.example
198.51.100.3
```

Parse it as text:

```bash
python skills/hosts-file-parser/scripts/hosts_file_parser.py hosts.txt
```

Parse it as JSON for CI or another program:

```bash
python skills/hosts-file-parser/scripts/hosts_file_parser.py hosts.txt --json
```

Read hosts data from standard input:

```bash
python skills/hosts-file-parser/scripts/hosts_file_parser.py - --json < hosts.txt
```

The sample returns exit status `1` because it contains an invalid address and a line without an alias. Duplicate mappings are reported separately and do not make the input invalid.
