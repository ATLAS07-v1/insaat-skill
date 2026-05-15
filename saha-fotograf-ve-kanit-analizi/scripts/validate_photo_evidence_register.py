#!/usr/bin/env python3
"""Validate a photo evidence register for completeness, duplicates, and privacy flags."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


REQUIRED_CONTEXT = ["project", "location", "subject", "source"]
PRIVACY_KEYWORDS = {
    "face": "privacy_sensitive",
    "person": "privacy_sensitive",
    "worker": "privacy_sensitive",
    "yüz": "privacy_sensitive",
    "yuz": "privacy_sensitive",
    "kişi": "privacy_sensitive",
    "kisi": "privacy_sensitive",
    "plaka": "privacy_sensitive",
    "plate": "privacy_sensitive",
    "injury": "health_sensitive",
    "yaralanma": "health_sensitive",
    "gps": "location_sensitive",
}


def load_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            for key in ("photos", "items", "rows", "records"):
                if isinstance(data.get(key), list):
                    return data[key]
            return [data]
        if isinstance(data, list):
            return data
        raise SystemExit("JSON içinde liste veya photos/items/rows/records alanı beklenir.")
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    raise SystemExit("Desteklenen dosya türleri: .json, .csv")


def get(row: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return default


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes", "evet", "var"}


def intish(value: Any) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 0


def row_text(row: dict[str, Any]) -> str:
    return " ".join(str(value or "") for value in row.values()).lower()


def validate(rows: list[dict[str, Any]], check_files: bool = True, min_pixels: int = 640 * 480) -> dict[str, Any]:
    sha_groups: defaultdict[str, list[str]] = defaultdict(list)
    for index, row in enumerate(rows, start=1):
        evidence_id = str(get(row, "evidence_id", "id", default=f"PH-{index:04d}")).strip()
        sha = str(get(row, "sha256", default="")).strip()
        if sha:
            sha_groups[sha].append(evidence_id)

    duplicate_ids = {item for values in sha_groups.values() if len(values) > 1 for item in values}
    results: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    for index, row in enumerate(rows, start=1):
        evidence_id = str(get(row, "evidence_id", "id", default=f"PH-{index:04d}")).strip()
        flags: list[str] = []
        file_path = str(get(row, "file_path", "path", default="")).strip()
        sha = str(get(row, "sha256", default="")).strip()
        captured_at = str(get(row, "captured_at", "date_taken", "taken_at", default="")).strip()
        width = intish(get(row, "width", default=0))
        height = intish(get(row, "height", default=0))

        if not file_path:
            flags.append("missing_file_path")
        elif check_files and not Path(file_path).exists():
            flags.append("file_missing")
        if not sha:
            flags.append("missing_sha256")
        if evidence_id in duplicate_ids:
            flags.append("duplicate_sha256")
        if not captured_at:
            flags.append("missing_capture_date")
        for field in REQUIRED_CONTEXT:
            if not str(get(row, field, default="")).strip():
                flags.append(f"missing_{field}")
        if not boolish(get(row, "exif_present", default=False)):
            flags.append("metadata_absent")
        if boolish(get(row, "gps_present", default=False)):
            flags.append("gps_present")
            flags.append("privacy_review")
        if width and height and width * height < min_pixels:
            flags.append("low_resolution")

        text = row_text(row)
        for keyword, flag in PRIVACY_KEYWORDS.items():
            if keyword in text:
                flags.append(flag)
                flags.append("privacy_review")

        strong_requirements = {
            "missing_file_path",
            "file_missing",
            "missing_sha256",
            "missing_project",
            "missing_location",
            "missing_subject",
            "missing_capture_date",
            "duplicate_sha256",
            "low_resolution",
        }
        status = "ready" if not set(flags).intersection(strong_requirements) and "privacy_review" not in flags else "needs_review"
        unique_flags = sorted(set(flags))
        for flag in unique_flags:
            issues.append({"evidence_id": evidence_id, "flag": flag})
        results.append(
            {
                "evidence_id": evidence_id,
                "file_name": str(get(row, "file_name", default=Path(file_path).name if file_path else "")),
                "status": status,
                "flags": unique_flags,
            }
        )

    return {
        "summary": {
            "photo_count": len(results),
            "ready_count": sum(1 for item in results if item["status"] == "ready"),
            "needs_review_count": sum(1 for item in results if item["status"] == "needs_review"),
            "issue_count": len(issues),
        },
        "photos": results,
        "issues": issues,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# Fotoğraf Kanıt Register Kontrolü", ""]
    lines.append(
        f"- Fotoğraf: {summary['photo_count']} | Hazır: {summary['ready_count']} | İnceleme gerekli: {summary['needs_review_count']} | Bayrak: {summary['issue_count']}"
    )
    lines.extend(["", "## Fotoğraflar", "", "| ID | Dosya | Durum | Bayraklar |", "|---|---|---|---|"])
    for item in payload["photos"]:
        flags = ", ".join(item["flags"])
        lines.append(f"| {item['evidence_id']} | {item['file_name']} | {item['status']} | {flags} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("register")
    parser.add_argument("--no-file-check", action="store_true")
    parser.add_argument("--min-pixels", type=int, default=640 * 480)
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output")
    args = parser.parse_args()
    payload = validate(load_rows(Path(args.register)), check_files=not args.no_file_check, min_pixels=args.min_pixels)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
