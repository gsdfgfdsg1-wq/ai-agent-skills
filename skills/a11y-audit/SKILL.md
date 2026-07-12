---
name: a11y-audit
description: Statically audit HTML for common accessibility issues including missing document language, image alt text, control labels, accessible button names, heading jumps, and duplicate IDs.
license: MIT
---

# HTML Accessibility Audit

> 在页面上线前快速发现静态 HTML 中常见的无障碍问题，为人工 WCAG 审查提供明确的修复清单。

## 何时使用 / 触发条件
- 用户要求检查 HTML 页面无障碍性、a11y 或 WCAG 常见问题。
- 前端 PR 或 CI 需要轻量级的静态可访问性门禁。
- 需要在不引入浏览器或第三方依赖的场景下，筛查明显的标记问题。

## 能力概览
- 检查 `<html lang>`、重复 `id`、缺少 `alt` 的图片。
- 检查表单控件是否有 id 或 ARIA 名称，以及与 `<label for>` 的关联。
- 检查无名称的 button/link、标题级别跳跃和 meta refresh。
- 支持多文件、JSON 报告和按 review/warning 阈值的 CI 退出码。

## 使用方法

```bash
# 检查单个页面
python skills/a11y-audit/scripts/audit_html.py public/index.html

# CI：warning 即失败
python skills/a11y-audit/scripts/audit_html.py dist/*.html --fail-on warning

# 输出机器可读报告
python skills/a11y-audit/scripts/audit_html.py public/index.html --json
```

这是静态规则检查，不代替键盘操作、读屏器和真实用户测试。

## 示例
见 `examples/usage.md`。