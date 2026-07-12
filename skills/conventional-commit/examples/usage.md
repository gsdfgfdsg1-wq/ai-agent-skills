# Conventional Commit Helper — 使用示例

## 1. 校验合规的提交信息

```bash
python skills/conventional-commit/scripts/commit-msg.py validate "feat(api): add pagination support"
```

预期输出：
```
✅ Commit message is valid.
```

## 2. 校验不合规的提交信息

```bash
python skills/conventional-commit/scripts/commit-msg.py validate "i made some changes"
```

预期输出：
```
Found 1 issue(s):
  ❌ First line must match: type(scope)!: description
  Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
  Got: 'i made some changes'
```

## 3. 校验首行超长

```bash
python skills/conventional-commit/scripts/commit-msg.py validate "feat: this is an unreasonably long commit message that definitely exceeds the seventy two character limit wholeheartedly"
```

预期输出：
```
Found 1 issue(s):
  ❌ First line is 105 chars (max 72).
```

## 4. 生成提交信息

```bash
python skills/conventional-commit/scripts/commit-msg.py generate \
  --type feat --scope cli \
  --desc "add interactive review mode" \
  --body "Prompts the user before applying each change, allowing selective approval." \
  --footer "Refs: #89"
```

预期输出：
```
feat(cli): add interactive review mode

Prompts the user before applying each change, allowing selective approval.

Refs: #89
```

## 5. 生成 Breaking Change 提交信息

```bash
python skills/conventional-commit/scripts/commit-msg.py generate \
  --type refactor --scope db \
  --desc "migrate from SQLite to PostgreSQL" \
  --breaking
```

预期输出：
```
refactor(db)!: migrate from SQLite to PostgreSQL

BREAKING CHANGE: migrate from SQLite to PostgreSQL
```