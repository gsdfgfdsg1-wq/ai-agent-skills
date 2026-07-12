#!/usr/bin/env python3
"""Regenerate the skills catalog (SKILLS.md) and the README catalog section.

Looks for HTML markers <!-- CATALOG_START --> / <!-- CATALOG_END --> in README.md
and replaces the content between them with a generated table.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
CATALOG_MD = os.path.join(ROOT, "SKILLS.md")
README = os.path.join(ROOT, "README.md")


def parse_frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return fm, text
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2)


def collect():
    rows = []
    for d in sorted(os.listdir(SKILLS)):
        sd = os.path.join(SKILLS, d)
        if not os.path.isdir(sd):
            continue
        skill_md = os.path.join(sd, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        fm, _ = parse_frontmatter(skill_md)
        name = fm.get("name", d)
        desc = fm.get("description", "")
        rows.append((d, name, desc))
    return rows


def render(rows):
    if not rows:
        return "_No skills yet._\n"
    lines = ["| 模块 | 说明 |", "| --- | --- |"]
    for slug, name, desc in rows:
        lines.append(f"| [{name}](skills/{slug}/) | {desc} |")
    return "\n".join(lines) + "\n"


def main():
    rows = collect()
    body = render(rows)

    with open(CATALOG_MD, "w", encoding="utf-8") as f:
        f.write("# 技能目录 (Skills Catalog)\n\n")
        f.write(f"> 自动生成，共 {len(rows)} 个技能模块。请勿手动编辑，运行 `python tools/build_catalog.py` 更新。\n\n")
        f.write(body)

    if os.path.isfile(README):
        with open(README, encoding="utf-8") as f:
            text = f.read()
        new_text = re.sub(
            r"<!-- CATALOG_START -->.*?<!-- CATALOG_END -->",
            f"<!-- CATALOG_START -->\n\n{body}\n<!-- CATALOG_END -->",
            text,
            flags=re.S,
        )
        with open(README, "w", encoding="utf-8") as f:
            f.write(new_text)

    print(f"Catalog rebuilt with {len(rows)} skill(s)")


if __name__ == "__main__":
    main()
