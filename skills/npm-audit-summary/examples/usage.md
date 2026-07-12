# Usage Examples

## 1. Basic summary from a file

```bash
python skills/npm-audit-summary/scripts/npm_audit_summary.py audit.json
```

Output:

```text
npm audit summary: 4 vulnerability(ies)

  HIGH: 2
    - lodash (transitive) [fix available]
    - axios (direct)
  MODERATE: 1
    - debug (transitive) [fix available]
  LOW: 1
    - minimist (transitive)

  2 of 4 have fixes available.
```

## 2. From stdin

```bash
npm audit --json | python skills/npm-audit-summary/scripts/npm_audit_summary.py -
```

## 3. CI threshold — fail on high or above

```bash
python skills/npm-audit-summary/scripts/npm_audit_summary.py audit.json --threshold high
echo $?
# 1 if any high/critical vulns exist, 0 otherwise
```

## 4. JSON output for downstream tooling

```bash
python skills/npm-audit-summary/scripts/npm_audit_summary.py audit.json --json
```

Returns a JSON object with `total`, `by_severity`, `fixable`, and `vulnerabilities` array.

## 5. Show more packages per severity

```bash
python skills/npm-audit-summary/scripts/npm_audit_summary.py audit.json --top 20
```
