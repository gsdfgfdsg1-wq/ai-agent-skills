#!/usr/bin/env python3
"""Scaffold a new AI Agent skill module.

Creates the canonical directory layout under skills/<slug>/:
    SKILL.md            capability description + trigger conditions (frontmatter)
    scripts/            runnable helper scripts (optional but encouraged)
    examples/usage.md   real, reproducible usage examples
    references/         extra docs (only with --with-refs)

Usage:
    python tools/scaffold_skill.py <slug> --name "Display Name" --desc "..." [--with-refs]
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")

TEMPLATE = """---
name: {slug}
description: {desc}
license: MIT
---

# {name}

> 一句话说明这个技能解决什么问题、何时使用。

## 何时使用 / 触发条件
- 列出明确的触发场景，让智能体知道何时加载本技能

## 能力概览
- 本技能能做什么（要点式）

## 使用方法
\`\`\`bash
# 示例调用
\`\`\`

## 示例
见 `examples/usage.md`。

## 参考
见 `references/`（如有）。
"""

EXAMPLE = """# 使用示例

## 基础用法
\`\`\`bash
# 替换为真实可复现的命令
\`\`\`

## 进阶用法
\`\`\`bash
# 更复杂的场景
\`\`\`

## 预期输出
\`\`\`text
# 贴出示例输出，便于用户对照
\`\`\`
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--name", required=True)
    ap.add_argument("--desc", required=True)
    ap.add_argument("--with-refs", action="store_true")
    args = ap.parse_args()

    slug = args.slug.strip().lower().replace(" ", "-").replace("_", "-")
    dest = os.path.join(SKILLS_DIR, slug)
    if os.path.exists(dest):
        print(f"ERROR: {dest} already exists")
        sys.exit(1)

    os.makedirs(os.path.join(dest, "scripts"))
    os.makedirs(os.path.join(dest, "examples"))
    if args.with_refs:
        os.makedirs(os.path.join(dest, "references"))

    with open(os.path.join(dest, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(slug=slug, name=args.name, desc=args.desc))
    with open(os.path.join(dest, "examples", "usage.md"), "w", encoding="utf-8") as f:
        f.write(EXAMPLE)
    # keep scripts dir tracked even before a script is added
    with open(os.path.join(dest, "scripts", ".gitkeep"), "w", encoding="utf-8") as f:
        f.write("")

    print(f"Created skill skeleton at {dest}")


if __name__ == "__main__":
    main()
