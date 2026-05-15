#!/usr/bin/env python3
"""Score construction risk register records and flag missing controls/evidence."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


SCALE = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "very low": 1,
    "low": 2,
    "medium": 3,
    "moderate": 3,
    "high": 4,
    "very high": 5,
    "critical": 5,
    "çok düşük": 1,
    "cok dusuk": 1,
    "düşük": 2,
    "dusuk": 2,
    "orta": 3,
    "yüksek": 4,
    "yuksek": 4,
    "çok yüksek": 5,
    "cok yuksek": 5,
    "kritik": 5,
}

CLOSED_STATUSES = {
    "closed",
    "done",
    "complete",
    "completed",
    "resolved",
    "verified",
    "kapali",
    "kapalı",
    "tamamlandi",
    "tamamlandı",
    "kapatildi",
    "kapatıldı",
}


def load_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            for key in ("risks", "items", "rows", "records"):
                if isinstance(data.get(key), list):
                    return data[key]
            return [data]
        if isinstance(data, list):
            return data
        raise SystemExit("JSON içinde liste, risks/items/rows/records alanı veya tek kayıt beklenir.")
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    raise SystemExit("Desteklenen dosya türleri: .json, .csv")


def get(row: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return default


def norm_text(value: Any) -> str:
    return str(value or "").strip().lower()


def as_score(value: Any, default: int = 1) -> int:
    if isinstance(value, (int, float)):
        return min(5, max(1, int(round(value))))
    text = norm_text(value).replace(",", ".")
    if text in SCALE:
        return SCALE[text]
    try:
        return min(5, max(1, int(round(float(text)))))
    except ValueError:
        return default


def as_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [item for item in value if item not in (None, "")]
    if isinstance(value, dict):
        return [value] if value else []
    if isinstance(value, str):
        parts = [part.strip() for part in value.replace("|", ";").split(";")]
        return [part for part in parts if part]
    return [value]


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


def level(score: int) -> str:
    if score >= 17:
        return "critical"
    if score >= 10:
        return "high"
    if score >= 5:
        return "medium"
    return "low"


def score_rows(rows: list[dict[str, Any]], today: date) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}

    for index, row in enumerate(rows, start=1):
        risk_id = str(get(row, "id", "risk_id", "code", default=f"R-{index:03d}")).strip()
        likelihood = as_score(get(row, "likelihood", "probability", "olasilik", "olasılık"))
        severity = as_score(get(row, "severity", "consequence", "impact", "siddet", "şiddet"))
        inherent_score = likelihood * severity
        inherent_level = level(inherent_score)
        residual_likelihood_raw = get(row, "residual_likelihood", "residual_probability", "artik_olasilik", "artık_olasılık")
        residual_severity_raw = get(row, "residual_severity", "residual_consequence", "residual_impact", "artik_siddet", "artık_şiddet")
        residual_assessed = residual_likelihood_raw not in (None, "") and residual_severity_raw not in (None, "")
        residual_likelihood = as_score(residual_likelihood_raw, likelihood) if residual_assessed else likelihood
        residual_severity = as_score(residual_severity_raw, severity) if residual_assessed else severity
        residual_score = residual_likelihood * residual_severity
        residual_level = level(residual_score)
        counts[residual_level] += 1

        controls = as_list(get(row, "controls", "control_measures", "existing_controls", "kontroller"))
        evidence = as_list(get(row, "evidence", "evidence_files", "kanit", "kanıt"))
        owner = str(get(row, "owner", "responsible", "sorumlu", default="")).strip()
        due = parse_date(get(row, "due_date", "deadline", "termin"))
        status = norm_text(get(row, "status", "durum", default="open"))
        closed = status in CLOSED_STATUSES

        flags: list[str] = []
        if inherent_level in {"high", "critical"} or residual_level in {"high", "critical"}:
            flags.append("critical_or_high")
        if not controls:
            flags.append("missing_controls")
        if not owner:
            flags.append("missing_owner")
        if due and due < today and not closed:
            flags.append("overdue")
        if residual_level in {"high", "critical"} and not evidence:
            flags.append("missing_evidence_for_high")
        if not residual_assessed:
            flags.append("residual_not_assessed")
        if residual_level in {"high", "critical"} or "missing_controls" in flags:
            flags.append("needs_management_review")

        for flag in flags:
            issues.append({"risk_id": risk_id, "flag": flag})

        results.append(
            {
                "id": risk_id,
                "activity": get(row, "activity", "work", "faaliyet", default=""),
                "hazard": get(row, "hazard", "tehlike", "title", default=""),
                "location": get(row, "location", "mahal", "lokasyon", default=""),
                "likelihood": likelihood,
                "severity": severity,
                "inherent_score": inherent_score,
                "inherent_level": inherent_level,
                "residual_likelihood": residual_likelihood,
                "residual_severity": residual_severity,
                "residual_score": residual_score,
                "residual_level": residual_level,
                "control_count": len(controls),
                "evidence_count": len(evidence),
                "owner": owner,
                "due_date": due.isoformat() if due else "",
                "status": status or "open",
                "flags": flags,
            }
        )

    priority = sorted(
        results,
        key=lambda item: (
            item["residual_score"],
            "overdue" in item["flags"],
            "missing_controls" in item["flags"],
        ),
        reverse=True,
    )
    return {
        "summary": {
            "risk_count": len(results),
            "low_count": counts["low"],
            "medium_count": counts["medium"],
            "high_count": counts["high"],
            "critical_count": counts["critical"],
            "issue_count": len(issues),
        },
        "risks": results,
        "priority": priority,
        "issues": issues,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# Risk Register Skor Özeti", ""]
    lines.append(
        f"- Risk sayısı: {summary['risk_count']} | Critical: {summary['critical_count']} | High: {summary['high_count']} | Medium: {summary['medium_count']} | Low: {summary['low_count']}"
    )
    lines.append(f"- Bayrak sayısı: {summary['issue_count']}")
    lines.extend(["", "## Öncelikli Riskler", "", "| ID | Tehlike | Artık Skor | Seviye | Sorumlu | Termin | Bayraklar |", "|---|---|---:|---|---|---|---|"])
    for item in payload["priority"]:
        flags = ", ".join(item["flags"])
        lines.append(
            f"| {item['id']} | {item['hazard']} | {item['residual_score']} | {item['residual_level']} | {item['owner']} | {item['due_date']} | {flags} |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("risk_register")
    parser.add_argument("--today", help="YYYY-MM-DD; test ve rapor sabitleme için")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", help="Çıktı dosyası")
    args = parser.parse_args()
    today = parse_date(args.today) if args.today else date.today()
    if today is None:
        raise SystemExit("--today tarihi YYYY-MM-DD olmalıdır.")
    payload = score_rows(load_rows(Path(args.risk_register)), today)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
