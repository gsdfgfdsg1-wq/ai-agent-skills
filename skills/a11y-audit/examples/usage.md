# HTML Accessibility Audit - 使用示例

给定页面：

```html
<html>
  <body>
    <h1>Account</h1>
    <h3>Profile</h3>
    <img src="avatar.png">
    <input id="email" type="email">
    <button></button>
  </body>
</html>
```

执行：

```bash
python skills/a11y-audit/scripts/audit_html.py page.html --fail-on warning
```

输出：

```text
[WARNING] page.html:line 1 A11Y001: The <html> element has no lang attribute.
[REVIEW] page.html:line 4 A11Y030: Heading level jumps from h1 to h3.
[WARNING] page.html:line 5 A11Y010: Image is missing an alt attribute.
[REVIEW] page.html:line 6 A11Y021: <input id='email'> has no matching <label for=...> or ARIA name.
[WARNING] page.html:line 7 A11Y011: Button has no accessible name.
Audited 1 file(s), found 5 issue(s).
```

因为存在 warning，命令以退出码 `1` 结束。