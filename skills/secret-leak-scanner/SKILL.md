---
name: secret-leak-scanner
description: 扫描代码库中的 API Key、私钥、Token 等敏感凭证，支持 CI 退出码与 JSON 输出，防止密钥泄露被提交到仓库。
license: MIT
---

# Secret Leak Scanner

> 在代码合入前，自动揪出 accidental 提交到仓库的密钥与令牌，避免凭证泄露。

## 何时使用 / 触发条件
- 提交/PR 前想快速自查是否误提交了密钥。
- CI 中需要一道“密钥门禁”，发现高危凭证就让构建失败。
- 接手老项目，想批量排查历史/现有代码里的敏感信息。

## 能力概览
- 覆盖 15+ 类常见凭证：AWS / GCP / Slack / Stripe / GitHub / GitLab / OpenAI 等。
- 支持 PEM 私钥、JWT、`.env` 明文密码等通用模式。
- 自动跳过 `.git`、`node_modules`、二进制等无关内容。
- `--json` 机器可读输出；`--exit-code` 接入 CI；`--severity` 控制阈值。

## 使用方法
\`\`\`bash
# 扫描整个项目（高危及以上才报告）
python skills/secret-leak-scanner/scripts/scan.py .

# CI 模式：发现 medium 及以上直接失败
python skills/secret-leak-scanner/scripts/scan.py . --exit-code --severity medium

# 机器可读
python skills/secret-leak-scanner/scripts/scan.py src/ --json
\`\`\`

## 示例
见 `examples/usage.md`。

## 参考
扫描规则见 `scripts/scan.py` 顶部的 `RULES` 列表，可按需增删。
