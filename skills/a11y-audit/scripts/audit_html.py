#!/usr/bin/env python3
"""Dependency-free static HTML accessibility audit for common WCAG issues."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path


@dataclass
class Finding:
    line: int
    rule: str
    severity: str
    message: str


class Auditor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.findings: list[Finding] = []
        self.ids: dict[str, int] = {}
        self.labels: set[str] = set()
        self.heading_level = 0
        self.html_seen = False
        self.lang_seen = False
        self.stack: list[dict] = []

    def add(self, rule: str, severity: str, message: str) -> None:
        self.findings.append(Finding(self.getpos()[0], rule, severity, message))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_seen = True
            self.lang_seen = bool(values.get("lang"))
            if not self.lang_seen:
                self.add("A11Y001", "warning", "The <html> element has no lang attribute.")

        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.add("A11Y002", "warning", f"Duplicate id {element_id!r}; first seen on line {self.ids[element_id]}.")
            else:
                self.ids[element_id] = self.getpos()[0]

        if tag == "label" and values.get("for"):
            self.labels.add(values["for"])

        if tag == "img" and "alt" not in values:
            self.add("A11Y010", "warning", "Image is missing an alt attribute.")

        if tag in {"input", "select", "textarea"}:
            input_type = values.get("type", "text").lower()
            if input_type not in {"hidden", "submit", "button", "reset", "image"}:
                has_name = bool(values.get("aria-label") or values.get("aria-labelledby") or values.get("id"))
                if not has_name:
                    self.add("A11Y020", "warning", f"<{tag}> has no id or ARIA accessible name.")
                elif values.get("id") and values["id"] not in self.labels and not values.get("aria-label") and not values.get("aria-labelledby"):
                    self.add("A11Y021", "review", f"<{tag} id={values['id']!r}> has no matching <label for=...> or ARIA name.")

        if tag in {"button", "a"}:
            self.stack.append({"tag": tag, "line": self.getpos()[0], "named": bool(values.get("aria-label") or values.get("aria-labelledby")), "href": values.get("href")})

        if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            level = int(tag[1])
            if self.heading_level and level > self.heading_level + 1:
                self.add("A11Y030", "review", f"Heading level jumps from h{self.heading_level} to h{level}.")
            self.heading_level = level

        if tag == "meta" and values.get("http-equiv", "").lower() == "refresh":
            self.add("A11Y040", "review", "Timed meta refresh can disrupt reading and navigation.")

    def handle_data(self, data: str) -> None:
        if data.strip() and self.stack:
            self.stack[-1]["named"] = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"button", "a"}:
            for index in range(len(self.stack) - 1, -1, -1):
                item = self.stack[index]
                if item["tag"] == tag:
                    self.stack.pop(index)
                    if not item["named"]:
                        noun = "Link" if tag == "a" else "Button"
                        self.findings.append(Finding(item["line"], "A11Y011", "warning", f"{noun} has no accessible name."))
                    break


def audit(path: Path) -> list[Finding]:
    parser = Auditor()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    parser.close()
    if not parser.html_seen:
        parser.findings.append(Finding(0, "A11Y000", "review", "No <html> root element found; document-level checks are limited."))
    return parser.findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit HTML files for common accessibility issues.")
    parser.add_argument("paths", nargs="+", help="HTML file paths")
    parser.add_argument("--json", action="store_true", help="Emit JSON results")
    parser.add_argument("--fail-on", choices=("review", "warning"), help="Exit 1 at or above severity")
    args = parser.parse_args()

    all_findings: dict[str, list[Finding]] = {}
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.is_file():
            parser.error(f"not a file: {path}")
        all_findings[str(path)] = audit(path)

    if args.json:
        print(json.dumps({path: [asdict(item) for item in findings] for path, findings in all_findings.items()}, ensure_ascii=False, indent=2))
    else:
        total = 0
        for path, findings in all_findings.items():
            if not findings:
                print(f"PASS: {path}")
            for item in findings:
                total += 1
                at = f"line {item.line}" if item.line else "file"
                print(f"[{item.severity.upper()}] {path}:{at} {item.rule}: {item.message}")
        print(f"Audited {len(all_findings)} file(s), found {total} issue(s).")

    if args.fail_on:
        rank = {"review": 1, "warning": 2}
        threshold = rank[args.fail_on]
        if any(rank[finding.severity] >= threshold for findings in all_findings.values() for finding in findings):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
