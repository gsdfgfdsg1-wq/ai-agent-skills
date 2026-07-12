# 贡献指南

## 新增一个技能模块

```bash
# 1. 生成骨架
python tools/scaffold_skill.py my-cool-skill \
  --name "My Cool Skill" \
  --desc "一句话说清这个技能解决什么问题、何时使用"

# 2. 填充内容
#    - skills/my-cool-skill/SKILL.md   能力说明 + 触发条件
#    - skills/my-cool-skill/scripts/   可运行脚本（强烈建议）
#    - skills/my-cool-skill/examples/usage.md  真实可复现示例

# 3. 校验 + 提交
python tools/publish.py
```

## 质量标准

- `SKILL.md` 必须有 `name` 与 `description` 字段（供智能体检索）。
- 核心能力尽量由 `scripts/` 中的真实脚本承载，而非纯提示词。
- `examples/usage.md` 必须包含可复现的命令与预期输出。
- 通过 `python tools/validate_skills.py`。

## 目录约定

```
skills/<slug>/
├── SKILL.md          # 能力说明（必填）
├── scripts/          # 可运行脚本（建议）
├── examples/usage.md # 真实示例（必填）
└── references/       # 额外文档（可选）
```
