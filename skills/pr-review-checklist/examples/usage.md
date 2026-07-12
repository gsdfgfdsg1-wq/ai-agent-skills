# PR Review Checklist - 使用示例

## 审查指定文件

```bash
python skills/pr-review-checklist/scripts/review.py --files \
  src/auth/session.py .github/workflows/release.yml package.json
```

输出会包含：

```text
[PASS] changes: Reviewing 3 changed file(s).
[WARN] tests: Source files changed but no test file is included. Confirm test coverage or explain why it is unnecessary.
[REVIEW] dependencies: Dependency manifest or lockfile changed: package.json. Review version, license, and supply-chain impact.
[REVIEW] delivery: Deployment, workflow, migration, or script files changed: .github/workflows/release.yml. Confirm rollback and least-privilege implications.
[PASS] secrets: No obviously sensitive filenames were changed.
[REVIEW] documentation: Source files changed without documentation updates. Check public API, configuration, and operator impact.
```

## 在 CI 中阻断警告

```bash
python skills/pr-review-checklist/scripts/review.py \
  --files src/auth/session.py --fail-on-warning
```

该命令会产生测试覆盖 warning，并以退出码 `1` 结束。

## JSON 输出

```bash
printf "tests/test_auth.py\ndocs/auth.md\n" | \
  python skills/pr-review-checklist/scripts/review.py --stdin --json
```

```json
[
  {
    "level": "pass",
    "check": "changes",
    "message": "Reviewing 2 changed file(s)."
  },
  {
    "level": "pass",
    "check": "tests",
    "message": "Test coverage was included or no source file changed."
  }
]
```
