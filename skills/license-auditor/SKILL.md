---
name: license-auditor
description: Audit local Node.js and Python dependency license metadata against allow and deny policies without external services. Supports strict mode, JSON, and CI exit codes.
license: MIT
---

# Dependency License Auditor

> 在发布或引入依赖前，扫描已安装的 Node.js/Python 包许可证元数据，并按许可证策略标记潜在合规问题。

## 何时使用 / 触发条件
- 用户需要审计依赖许可证、开源合规或第三方包风险。
- 发布前或 CI 中需要阻断 GPL/自定义禁止许可证。
- 已有 `node_modules`、虚拟环境或 site-packages，希望零网络检查现有依赖。

## 能力概览
- 扫描 Node.js `node_modules/**/package.json` 与 Python `*.dist-info/METADATA`。
- 默认识别常用宽松许可证：MIT、ISC、BSD、Apache-2.0、MPL-2.0、Python-2.0。
- `--deny` 标记明确禁止的许可证，`--strict --allow` 只放行指定许可证。
- `--json` 提供机器可读结果；按 warning/error 阈值提供 CI 退出码。

## 使用方法

```bash
# 扫描本项目已安装依赖
python skills/license-auditor/scripts/audit.py .

# CI：禁止 GPL-3.0 与 AGPL-3.0
python skills/license-auditor/scripts/audit.py . \
  --deny GPL-3.0,AGPL-3.0 --fail-on warning

# 严格 allow list 与 JSON 报告
python skills/license-auditor/scripts/audit.py . \
  --strict --allow MIT,Apache-2.0,BSD-3-Clause --json
```

该工具读取本地元数据，并不替代法务意见；`UNKNOWN` 结果需人工确认。

## 示例
见 `examples/usage.md`。