# 使用示例

> 说明：下面的示例密钥均来自云厂商官方文档的 **示例值**（如 AWS 的
> `AKIAIOSFODNN7EXAMPLE` / `wJalrXUtnFEMI/...EXAMPLEKEY`），仅用于演示扫描器
> 行为，并非真实凭证，可安全提交到仓库。

## 0. 准备一个含密钥的测试样本

```bash
mkdir -p /tmp/demo && cd /tmp/demo
cat > .env <<'EOF'
DB_PASSWORD=supersecretpassword123
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
EOF
```

## 1. 基础扫描（全部严重程度）

```bash
python skills/secret-leak-scanner/scripts/scan.py /tmp/demo
```

预期输出：

```text
Found 3 potential secret(s):

[CRITICAL] AWS Secret Access Key
  /tmp/demo/.env:3
  match: AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMP...

[HIGH] AWS Access Key ID
  /tmp/demo/.env:2
  match: AKIAIOSFODNN7EXAMPLE

[MEDIUM] Generic secret assignment
  /tmp/demo/.env:1
  match: PASSWORD=supersecretpassword123
```

## 2. CI 门禁（发现即失败）

```bash
python skills/secret-leak-scanner/scripts/scan.py . --exit-code --severity medium
echo $?   # 有发现时输出 1，可用于在 CI 中阻断合并
```

## 3. 机器可读输出

```bash
python skills/secret-leak-scanner/scripts/scan.py /tmp/demo --json
```

输出为 JSON 数组，每个对象含 `rule` / `severity` / `line` / `match` / `file`，
便于接入自定义报告或看板。

## 4. 接入 GitHub Actions（节选）

```yaml
- name: Secret scan
  run: python skills/secret-leak-scanner/scripts/scan.py . --exit-code --severity high
```
