# Dependency License Auditor - 使用示例

准备一个已安装依赖的项目目录后执行：

```bash
python skills/license-auditor/scripts/audit.py . --deny GPL-3.0,AGPL-3.0 --fail-on warning
```

若发现禁止许可证：

```text
Scanned 84 package(s).
[ERROR] node:example-copyleft@2.1.0 - GPL-3.0: matches deny policy
```

命令以退出码 `1` 结束，适合 CI 阻断。

严格模式示例：

```bash
python skills/license-auditor/scripts/audit.py . \
  --strict --allow MIT,Apache-2.0,BSD-3-Clause --json
```

输出的 `findings` 包含包名、版本、生态、许可证、元数据来源和触发原因，可直接提交到合规系统。