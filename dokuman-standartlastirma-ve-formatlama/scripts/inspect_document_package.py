#!/usr/bin/env python3
"""Inspect a construction document package for naming, revision, and format issues."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUPPORTED_EXTENSIONS = {".docx", ".pdf", ".md", ".xlsx", ".xls", ".odt", ".ods", ".pptx", ".html", ".txt", ".csv"}
REVISION_RE = re.compile(r"(?:^|[-_ ])R(?:EV)?\.?(\d{1,3})(?:[-_ .]|$)", re.IGNORECASE)
DATE_RE = re.compile(r"(20\d{2})[-_.]?(0[1-9]|1[0-2])[-_.]?([0-2]\d|3[01])")
UNSAFE_RE = re.compile(r"[^A-Za-z0-9._-]")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def revision_from_name(name: str) -> str:
    match = REVISION_RE.search(name)
    if not match:
        return ""
    return f"R{int(match.group(1)):02d}"


def date_from_name(name: str) -> str:
    match = DATE_RE.search(name)
    if not match:
        return ""
    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"


def inspect_folder(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.folder).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Klasör bulunamadı: {root}")
    files = [path for path in root.rglob("*") if path.is_file()]
    sha_groups: defaultdict[str, list[str]] = defaultdict(list)
    rows = []
    for index, path in enumerate(sorted(files), start=1):
        relative = str(path.relative_to(root))
        sha = sha256_file(path)
        sha_groups[sha].append(relative)
        revision = revision_from_name(path.name)
        doc_date = date_from_name(path.name)
        flags = []
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            flags.append("unsupported_extension")
        if args.require_revision and not revision:
            flags.append("missing_revision")
        if args.require_date and not doc_date:
            flags.append("missing_date")
        if UNSAFE_RE.search(path.stem):
            flags.append("unsafe_filename")
        if len(path.name) > args.max_name_length:
            flags.append("filename_too_long")
        rows.append(
            {
                "document_id": f"DOC-{index:04d}",
                "file_path": str(path),
                "relative_path": relative,
                "file_name": path.name,
                "extension": path.suffix.lower(),
                "file_size": path.stat().st_size,
                "sha256": sha,
                "revision": revision,
                "date": doc_date,
                "flags": flags,
            }
        )

    duplicate_shas = {sha for sha, names in sha_groups.items() if len(names) > 1}
    issues = []
    for row in rows:
        if row["sha256"] in duplicate_shas:
            row["flags"].append("duplicate_sha256")
        row["flags"] = sorted(set(row["flags"]))
        row["status"] = "ready" if not row["flags"] else "needs_review"
        for flag in row["flags"]:
            issues.append({"document_id": row["document_id"], "file_name": row["file_name"], "flag": flag})

    return {
        "summary": {
            "folder": str(root),
            "file_count": len(rows),
            "supported_count": sum(1 for row in rows if row["extension"] in SUPPORTED_EXTENSIONS),
            "needs_review_count": sum(1 for row in rows if row["status"] == "needs_review"),
            "issue_count": len(issues),
            "generated_at": datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        },
        "files": rows,
        "issues": issues,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# Doküman Paketi Kontrolü", ""]
    lines.append(
        f"- Dosya: {summary['file_count']} | Desteklenen: {summary['supported_count']} | İnceleme gerekli: {summary['needs_review_count']} | Bayrak: {summary['issue_count']}"
    )
    lines.extend(["", "## Dosyalar", "", "| ID | Dosya | Revizyon | Tarih | Durum | Bayraklar |", "|---|---|---|---|---|---|"])
    for item in payload["files"]:
        flags = ", ".join(item["flags"])
        lines.append(f"| {item['document_id']} | {item['file_name']} | {item['revision']} | {item['date']} | {item['status']} | {flags} |")
    return "\n".join(lines)


def write_csv(payload: dict[str, Any], output: Path) -> None:
    fieldnames = ["document_id", "relative_path", "file_name", "extension", "file_size", "sha256", "revision", "date", "status", "flags"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in payload["files"]:
            item = {key: row.get(key, "") for key in fieldnames}
            item["flags"] = ";".join(row.get("flags") or [])
            writer.writerow(item)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder")
    parser.add_argument("--require-revision", action="store_true")
    parser.add_argument("--require-date", action="store_true")
    parser.add_argument("--max-name-length", type=int, default=120)
    parser.add_argument("--format", choices=["json", "markdown", "csv"], default="json")
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = inspect_folder(args)
    if args.format == "markdown":
        rendered = render_markdown(payload)
    elif args.format == "csv":
        if not args.output:
            raise SystemExit("--format csv için --output gerekir.")
        write_csv(payload, Path(args.output))
        return 0
    else:
        rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
