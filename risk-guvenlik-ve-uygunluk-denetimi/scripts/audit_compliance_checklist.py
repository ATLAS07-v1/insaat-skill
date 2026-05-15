#!/usr/bin/env python3
"""Audit compliance checklist requirements against provided evidence records."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


PASS_STATUSES = {"pass", "passed", "ok", "accepted", "approved", "provided", "uygun", "kabul"}
FAIL_STATUSES = {"fail", "failed", "rejected", "expired", "not_ok", "uygunsuz", "red"}
PENDING_STATUSES = {"pending", "review", "waiting", "open", "beklemede", "incelenecek"}
NA_STATUSES = {"na", "n/a", "not_applicable", "not applicable", "uygulanmaz"}
CLOSED_STATUSES = {"closed", "done", "complete", "completed", "resolved", "kapalı", "kapali", "tamamlandı", "tamamlandi"}


def load_records(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            for key in ("requirements", "checklist", "controls", "items", "evidence", "rows", "records"):
                if isinstance(data.get(key), list):
                    return data[key]
            return [data]
        if isinstance(data, list):
            return data
        raise SystemExit("JSON içinde liste veya bilinen kayıt alanı beklenir.")
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    raise SystemExit("Desteklenen dosya türleri: .json, .csv")


def get(row: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return default


def norm(value: Any) -> str:
    return str(value or "").strip()


def norm_key(value: Any) -> str:
    return norm(value).upper()


def boolish(value: Any, default: bool = False) -> bool:
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    text = norm(value).lower()
    if text in {"1", "true", "yes", "y", "evet", "required", "zorunlu"}:
        return True
    if text in {"0", "false", "no", "n", "hayır", "hayir", "optional", "opsiyonel"}:
        return False
    return default


def parse_date(value: Any) -> date | None:
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        return None


def classify_status(value: Any) -> str:
    text = norm(value).lower()
    if text in PASS_STATUSES:
        return "pass"
    if text in FAIL_STATUSES:
        return "fail"
    if text in NA_STATUSES:
        return "not_applicable"
    if text in PENDING_STATUSES:
        return "pending"
    return ""


def group_evidence(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        key = norm_key(get(row, "requirement_id", "control_id", "check_id", "requirement", "id"))
        if not key:
            continue
        grouped.setdefault(key, []).append(row)
    return grouped


def audit(requirements: list[dict[str, Any]], evidence_rows: list[dict[str, Any]], today: date) -> dict[str, Any]:
    evidence_by_req = group_evidence(evidence_rows)
    results: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    counts = {"pass": 0, "fail": 0, "missing_evidence": 0, "pending": 0, "not_applicable": 0}

    for index, req in enumerate(requirements, start=1):
        req_id = norm(get(req, "id", "requirement_id", "control_id", "code", default=f"REQ-{index:03d}"))
        key = norm_key(req_id)
        evidence = evidence_by_req.get(key, [])
        mandatory = boolish(get(req, "mandatory", "required", "zorunlu"), default=True)
        evidence_required = boolish(get(req, "evidence_required", "requires_evidence", "kanit_gerekli", "kanıt_gerekli"), default=False)
        owner = norm(get(req, "owner", "responsible", "sorumlu", default=""))
        source = norm(get(req, "source", "kaynak", default=""))
        due = parse_date(get(req, "due_date", "deadline", "termin"))
        direct_status = classify_status(get(req, "status", "result", "durum"))
        evidence_statuses = [classify_status(get(item, "status", "result", "durum")) for item in evidence]
        evidence_statuses = [item for item in evidence_statuses if item]

        flags: list[str] = []
        if not source:
            flags.append("missing_source")
        if not owner:
            flags.append("missing_owner")
        if due and due < today and direct_status not in {"pass", "not_applicable"}:
            flags.append("overdue")

        if direct_status == "not_applicable":
            status = "not_applicable"
        elif direct_status == "fail" or "fail" in evidence_statuses:
            status = "fail"
        elif evidence_required and not evidence:
            status = "missing_evidence"
            flags.append("mandatory_missing_evidence" if mandatory else "missing_evidence")
        elif direct_status == "pass":
            status = "pass"
        elif evidence and all(item in {"pass", ""} for item in evidence_statuses):
            status = "pass"
        elif direct_status == "pending" or evidence_statuses:
            status = "pending"
        else:
            status = "pending"

        if mandatory and status in {"fail", "missing_evidence"}:
            flags.append("failed_mandatory" if status == "fail" else "mandatory_missing_evidence")

        counts[status] += 1
        for flag in sorted(set(flags)):
            issues.append({"requirement_id": req_id, "flag": flag})

        results.append(
            {
                "id": req_id,
                "category": norm(get(req, "category", "kategori", default="")),
                "source": source,
                "requirement": norm(get(req, "requirement", "title", "description", "madde", default="")),
                "mandatory": mandatory,
                "evidence_required": evidence_required,
                "evidence_count": len(evidence),
                "status": status,
                "owner": owner,
                "due_date": due.isoformat() if due else "",
                "flags": sorted(set(flags)),
            }
        )

    return {
        "summary": {
            "requirement_count": len(results),
            "pass_count": counts["pass"],
            "fail_count": counts["fail"],
            "missing_evidence_count": counts["missing_evidence"],
            "pending_count": counts["pending"],
            "not_applicable_count": counts["not_applicable"],
            "issue_count": len(issues),
        },
        "results": results,
        "issues": issues,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# Uygunluk ve Kanıt Denetimi", ""]
    lines.append(
        f"- Gereksinim: {summary['requirement_count']} | Pass: {summary['pass_count']} | Fail: {summary['fail_count']} | Eksik kanıt: {summary['missing_evidence_count']} | Pending: {summary['pending_count']}"
    )
    lines.append(f"- Bayrak sayısı: {summary['issue_count']}")
    lines.extend(["", "## Gereksinim Matrisi", "", "| ID | Kategori | Durum | Kanıt | Sorumlu | Bayraklar |", "|---|---|---|---:|---|---|"])
    for item in payload["results"]:
        flags = ", ".join(item["flags"])
        lines.append(
            f"| {item['id']} | {item['category']} | {item['status']} | {item['evidence_count']} | {item['owner']} | {flags} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checklist")
    parser.add_argument("--evidence", help="Kanıt register JSON/CSV dosyası")
    parser.add_argument("--today", help="YYYY-MM-DD; test ve rapor sabitleme için")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", help="Çıktı dosyası")
    args = parser.parse_args()
    today = parse_date(args.today) if args.today else date.today()
    if today is None:
        raise SystemExit("--today tarihi YYYY-MM-DD olmalıdır.")
    payload = audit(load_records(Path(args.checklist)), load_records(Path(args.evidence)) if args.evidence else [], today)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
