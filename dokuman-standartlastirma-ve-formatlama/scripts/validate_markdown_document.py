#!/usr/bin/env python3
"""Validate Markdown document structure for construction deliverables."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
PLACEHOLDER_RE = re.compile(r"(\bTODO\b|\bTBD\b|\bFIXME\b|\[insert\b|\[todo\b|\[\s*\]|<[^>\n]*(?:todo|insert|placeholder)[^>\n]*>)", re.IGNORECASE)


def validate(path: Path, required_sections: list[str], max_line_length: int) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    issues: list[dict[str, Any]] = []
    headings: list[dict[str, Any]] = []
    previous_level = 0

    if text and not text.endswith("\n"):
        issues.append({"line": len(lines), "flag": "missing_final_newline", "message": "Dosya final newline ile bitmiyor."})

    for index, line in enumerate(lines, start=1):
        if "\t" in line:
            issues.append({"line": index, "flag": "tab_character", "message": "Tab karakteri kullanılmış."})
        if len(line) > max_line_length and not line.startswith("|") and not line.startswith("http"):
            issues.append({"line": index, "flag": "line_too_long", "message": f"Satır {max_line_length} karakteri aşıyor."})
        if PLACEHOLDER_RE.search(line):
            issues.append({"line": index, "flag": "placeholder", "message": "Placeholder/TODO/TBD teslim dokümanında kalmamalı."})
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip().rstrip("#").strip()
        headings.append({"line": index, "level": level, "title": title})
        if previous_level and level > previous_level + 1:
            issues.append({"line": index, "flag": "heading_level_skip", "message": f"H{previous_level} seviyesinden H{level} seviyesine atlandı."})
        previous_level = level
        if title.endswith("."):
            issues.append({"line": index, "flag": "heading_trailing_period", "message": "Başlık nokta ile bitmemeli."})

    h1_count = sum(1 for item in headings if item["level"] == 1)
    if h1_count == 0:
        issues.append({"line": 1, "flag": "missing_h1", "message": "Dokümanda H1 başlık yok."})
    elif h1_count > 1:
        issues.append({"line": 1, "flag": "multiple_h1", "message": "Dokümanda birden fazla H1 başlık var."})

    title_counts = Counter(item["title"].lower() for item in headings)
    for title, count in title_counts.items():
        if count > 1:
            first_line = next(item["line"] for item in headings if item["title"].lower() == title)
            issues.append({"line": first_line, "flag": "duplicate_heading", "message": f"Başlık tekrar ediyor: {title}"})

    normalized_headings = {item["title"].strip().lower() for item in headings}
    for section in required_sections:
        if section.strip().lower() not in normalized_headings:
            issues.append({"line": 1, "flag": "missing_required_section", "message": f"Zorunlu bölüm yok: {section}"})

    return {
        "summary": {
            "file": str(path),
            "heading_count": len(headings),
            "issue_count": len(issues),
            "status": "ready" if not issues else "needs_review",
        },
        "headings": headings,
        "issues": issues,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# Markdown Doküman QA", ""]
    lines.append(f"- Başlık: {summary['heading_count']} | Bayrak: {summary['issue_count']} | Durum: {summary['status']}")
    lines.extend(["", "## Bulgular", "", "| Satır | Bayrak | Mesaj |", "|---:|---|---|"])
    for issue in payload["issues"]:
        lines.append(f"| {issue['line']} | {issue['flag']} | {issue['message']} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown_file")
    parser.add_argument("--required-section", action="append", default=[])
    parser.add_argument("--max-line-length", type=int, default=140)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = validate(Path(args.markdown_file), args.required_section, args.max_line_length)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
