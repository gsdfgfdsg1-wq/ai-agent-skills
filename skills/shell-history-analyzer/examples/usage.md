# Usage Examples

## 1. Analyze a Bash history file

```bash
python skills/shell-history-analyzer/scripts/shell_history_analyzer.py ~/.bash_history --top 5
```

Example output:

```text
History: C:\\Users\\me\\.bash_history
Commands: 27 total, 8 unique; 3 ignored

Count  Command
    9  git
    5  python
    4  cd
    3  npm
    2  ls
```

Blank lines and Bash timestamp lines such as `#1710000000` are ignored.

## 2. Analyze Zsh extended history

```bash
python skills/shell-history-analyzer/scripts/shell_history_analyzer.py ~/.zsh_history --top 0
```

Entries such as `: 1710000000:0;git status` are converted to the command `git` before counting. `--top 0` lists every command.

## 3. Read from standard input

```bash
printf 'git status\ngit commit\n#1710000000\npython app.py\n' | python skills/shell-history-analyzer/scripts/shell_history_analyzer.py -
```

## 4. JSON output

```bash
python skills/shell-history-analyzer/scripts/shell_history_analyzer.py ~/.bash_history --top 3 --json
```

The JSON object includes totals, ignored-line count, unique-command count, and ranked `commands` entries.
