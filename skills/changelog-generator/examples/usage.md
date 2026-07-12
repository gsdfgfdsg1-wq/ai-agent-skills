# Conventional Changelog Generator - 使用示例

假设两个版本之间有以下提交：

```text
feat(auth): add passwordless login
fix(api): return 404 for deleted resources
perf(search): cache normalized query
refactor!: replace legacy configuration format
docs: explain local development setup
```

生成发布说明：

```bash
python skills/changelog-generator/scripts/generate.py \
  --range v1.4.0..HEAD --version 1.5.0 --date 2026-07-13
```

输出：

```markdown
## [1.5.0] - 2026-07-13

### Breaking Changes
- replace legacy configuration format

### Features
- **auth:** add passwordless login

### Bug Fixes
- **api:** return 404 for deleted resources

### Performance
- **search:** cache normalized query

### Refactoring
- replace legacy configuration format

### Documentation
- explain local development setup
```

不符合 Conventional Commit 格式的提交不会被丢弃，而是会放到 `Other Changes` 区块。