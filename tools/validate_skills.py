#!/usr/bin/env python3
"""Validate every skill module in skills/.

Checks:
  - SKILL.md exists with YAML frontmatter
  - frontmatter has non-empty `name` and `description`
  - body is substantive (>= 80 chars)
  - examples/usage.md exists and is non-trivial
  - any script in scripts/ is syntactically importable / parseable (python/sh)

Exit code 0 = all good, 1 = problems found.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
REQUIRED_FIELDS = ["name", "description"]


def parse_frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2)


def check_script(path):
    """Light syntax sanity check for bundled scripts."""
    if path.endswith(".py"):
        import py_compile
        try:
            py_compile.compile(path, doraise=True)
            return None
        except py_compile.PyCompileError as e:
            return f"python syntax error: {e}"
    if path.endswith(".sh"):
        # best-effort: ensure it starts with a shebang
        with open(path, encoding="utf-8") as f:
            first = f.readline()
        if not first.startswith("#!"):
            return "shell script missing shebang"
    return None


def main():
    if not os.path.isdir(SKILLS):
        print("No skills/ directory found")
        sys.exit(1)

    problems = []
    count = 0
    for d in sorted(os.listdir(SKILLS)):
        sd = os.path.join(SKILLS, d)
        if not os.path.isdir(sd):
            continue
        count += 1
        skill_md = os.path.join(sd, "SKILL.md")
        if not os.path.isfile(skill_md):
            problems.append((d, "missing SKILL.md"))
            continue
        fm, body = parse_frontmatter(skill_md)
        if fm is None:
            problems.append((d, "missing/!valid YAML frontmatter"))
            continue
        for fld in REQUIRED_FIELDS:
            if not fm.get(fld):
                problems.append((d, f"frontmatter '{fld}' missing or empty"))
        if len(body.strip()) < 80:
            problems.append((d, "SKILL.md body too short (<80 chars)"))
        ex = os.path.join(sd, "examples", "usage.md")
        if not os.path.isfile(ex) or os.path.getsize(ex) < 30:
            problems.append((d, "missing or empty examples/usage.md"))
        for root, _, files in os.walk(os.path.join(sd, "scripts")):
            for fn in files:
                if fn == ".gitkeep":
                    continue
                err = check_script(os.path.join(root, fn))
                if err:
                    problems.append((d, f"scripts/{fn}: {err}"))

    if problems:
        print(f"VALIDATION FAILED: {len(problems)} issue(s) across {count} skill(s):")
        for d, p in problems:
            print(f"  - [{d}] {p}")
        sys.exit(1)
    print(f"VALIDATION PASSED: {count} skill(s) OK")
    sys.exit(0)


if __name__ == "__main__":
    main()
