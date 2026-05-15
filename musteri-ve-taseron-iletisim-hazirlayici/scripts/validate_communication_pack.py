#!/usr/bin/env python3
"""Validate construction communication briefs for missing fields and risky language."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = ["project", "subject", "recipient", "request"]
FORMAL_TYPES = {"rfi", "submittal", "transmittal", "meeting_minutes", "delay_notice_draft", "variation_notice_draft", "payment_followup", "formal_letter"}
APPROVAL_TYPES = {"delay_notice_draft", "variation_notice_draft", "payment_followup", "formal_letter"}
RISKY_PHRASES = {
    "kusurumuz": "liability_admission",
    "hata bizde": "liability_admission",
    "kesin uygundur": "overcommitment",
    "kesin teslim": "overcommitment",
    "garanti ediyoruz": "overcommitment",
    "ceza": "contractual_risk",
    "fesih": "contractual_risk",
    "ihtar": "contractual_risk",
    "sözleşmeye aykırı": "contractual_risk",
    "sozlesmeye aykiri": "contractual_risk",
    "ek bedel": "financial_risk",
    "varyasyon": "financial_risk",
    "gecikme": "delay_risk",
    "claim": "claim_risk",
}


def load_messages(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            for key in ("messages", "items", "rows", "records"):
                if isinstance(data.get(key), list):
                    return data[key]
            return [data]
        if isinstance(data, list):
            return data
        raise SystemExit("JSON içinde liste veya tek iletişim nesnesi beklenir.")
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    raise SystemExit("Desteklenen dosya türleri: .json, .csv")


def get(row: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return default


def as_text(value: Any) -> str:
    if value in (None, ""):
        return ""
    if isinstance(value, list):
        return " ".join(as_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(as_text(item) for item in value.values())
    return str(value)


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes", "evet", "required", "gerekli"}


def validate(messages: list[dict[str, Any]]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    approval_count = 0

    for index, row in enumerate(messages, start=1):
        msg_id = str(get(row, "id", "message_id", "code", default=f"MSG-{index:03d}")).strip()
        message_type = str(get(row, "message_type", "type", "communication_type", default="general")).strip()
        channel = str(get(row, "channel", default="email")).strip()
        flags: list[str] = []

        for field in REQUIRED_FIELDS:
            if not str(get(row, field, default="")).strip():
                flags.append(f"missing_{field}")

        if message_type in FORMAL_TYPES and not str(get(row, "due_date", "deadline", "termin", default="")).strip():
            flags.append("missing_due_date")

        if message_type in {"rfi", "submittal", "transmittal"} and not str(get(row, "references", "reference", "referans", default="")).strip():
            flags.append("missing_reference")

        if message_type in {"submittal", "transmittal"} and not str(get(row, "attachments", "attachment", "ekler", default="")).strip():
            flags.append("missing_attachments")

        body = " ".join(
            [
                as_text(row),
                as_text(get(row, "body", "message", "taslak", default="")),
            ]
        ).lower()
        for phrase, flag in RISKY_PHRASES.items():
            if phrase in body:
                flags.append(flag)

        approval_required = boolish(get(row, "approval_required", "onay_gerekli")) or message_type in APPROVAL_TYPES or any(
            flag in flags
            for flag in {"liability_admission", "overcommitment", "contractual_risk", "financial_risk", "delay_risk", "claim_risk"}
        )
        if approval_required:
            flags.append("approval_required")
            approval_count += 1

        unique_flags = sorted(set(flags))
        for flag in unique_flags:
            issues.append({"message_id": msg_id, "flag": flag})

        status = "ready" if not unique_flags else "needs_review"
        results.append(
            {
                "id": msg_id,
                "message_type": message_type,
                "channel": channel,
                "status": status,
                "approval_required": approval_required,
                "flags": unique_flags,
            }
        )

    return {
        "summary": {
            "message_count": len(results),
            "ready_count": sum(1 for item in results if item["status"] == "ready"),
            "needs_review_count": sum(1 for item in results if item["status"] == "needs_review"),
            "approval_required_count": approval_count,
            "issue_count": len(issues),
        },
        "messages": results,
        "issues": issues,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = ["# İletişim Paketi Kontrolü", ""]
    lines.append(
        f"- Mesaj: {summary['message_count']} | Hazır: {summary['ready_count']} | İnceleme gerekli: {summary['needs_review_count']} | Onay gerekli: {summary['approval_required_count']}"
    )
    lines.append(f"- Bayrak sayısı: {summary['issue_count']}")
    lines.extend(["", "## Mesajlar", "", "| ID | Tip | Kanal | Durum | Bayraklar |", "|---|---|---|---|---|"])
    for item in payload["messages"]:
        flags = ", ".join(item["flags"])
        lines.append(f"| {item['id']} | {item['message_type']} | {item['channel']} | {item['status']} | {flags} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("communication_pack")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", help="Çıktı dosyası")
    args = parser.parse_args()
    payload = validate(load_messages(Path(args.communication_pack)))
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
