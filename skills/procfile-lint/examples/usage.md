# Procfile Lint Examples

Lint a Procfile locally:

```bash
python skills/procfile-lint/scripts/procfile_lint.py Procfile
```

Example input:

```procfile
web: gunicorn app:app
worker:
web: python app.py
1invalid: npm start
```

Example output:

```text
Issues in Procfile:
  line 2: [empty-command] process command must not be empty
  line 3: [duplicate-process-type] process type 'web' was already declared on line 1
  line 4: [invalid-process-type] process type must start with a letter and contain only letters, digits, '_' or '-'
Total: 3 issue(s)
```

Use JSON output in CI:

```bash
python skills/procfile-lint/scripts/procfile_lint.py Procfile --json
```

The command exits with code `1` when it finds any issue.
