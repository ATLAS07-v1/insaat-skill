#!/usr/bin/env python3
"""Draft construction customer/subcontractor messages from structured input."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SENSITIVE_TYPES = {"delay_notice_draft", "variation_notice_draft", "payment_followup", "formal_letter"}


def load_payload(path: str | None, args: argparse.Namespace) -> dict[str, Any]:
    if path:
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise SystemExit("Girdi JSON tek bir iletişim brief nesnesi olmalıdır.")
        return data
    return {
        "message_type": args.message_type,
        "channel": args.channel,
        "recipient_type": args.recipient_type,
        "recipient": args.recipient,
        "sender": args.sender,
        "project": args.project,
        "subject": args.subject,
        "facts": args.fact or [],
        "request": args.request,
        "due_date": args.due_date,
        "references": args.reference or [],
        "attachments": args.attachment or [],
        "tone": args.tone,
        "approval_required": args.approval_required,
    }


def as_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in value.replace("|", ";").split(";") if part.strip()]
    return [str(value).strip()]


def value(payload: dict[str, Any], key: str, default: str = "") -> str:
    return str(payload.get(key) or default).strip()


def risk_notes(payload: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    message_type = value(payload, "message_type")
    channel = value(payload, "channel")
    if payload.get("approval_required") or message_type in SENSITIVE_TYPES or channel == "formal_letter":
        notes.append("Gönderim öncesi yetkili onay gerekir.")
    if message_type in {"delay_notice_draft", "variation_notice_draft"}:
        notes.append("Gecikme/varyasyon içeriği sözleşmesel hak iddiası doğurabilir; hukuki/ticari dil yetkili tarafından kontrol edilmelidir.")
    if message_type == "payment_followup":
        notes.append("Ödeme/hakediş içeriği finansal onay ve mutabakat kontrolü gerektirir.")
    return notes


def subject_line(payload: dict[str, Any]) -> str:
    subject = value(payload, "subject")
    project = value(payload, "project")
    message_type = value(payload, "message_type", "iletişim")
    if subject:
        return subject
    if project:
        return f"{project} - {message_type}"
    return message_type


def draft(payload: dict[str, Any]) -> dict[str, Any]:
    facts = as_list(payload.get("facts"))
    references = as_list(payload.get("references"))
    attachments = as_list(payload.get("attachments"))
    actions = as_list(payload.get("actions"))
    request = value(payload, "request")
    due_date = value(payload, "due_date")
    recipient = value(payload, "recipient", "İlgili kişi")
    recipient_type = value(payload, "recipient_type")
    channel = value(payload, "channel", "email")
    tone = value(payload, "tone", "resmi")
    project = value(payload, "project")
    message_type = value(payload, "message_type", "general")

    greeting = "Merhaba"
    if channel == "formal_letter":
        greeting = "Sayın Yetkili"
    elif recipient:
        greeting = f"Merhaba {recipient},"

    lines: list[str] = [greeting, ""]
    if project:
        lines.append(f"{project} kapsamında aşağıdaki konu için iletişim taslağı hazırlanmıştır.")
        lines.append("")
    if facts:
        lines.append("Doğrulanmış bilgiler:")
        for item in facts:
            lines.append(f"- {item}")
        lines.append("")
    if references:
        lines.append("Referanslar:")
        for item in references:
            lines.append(f"- {item}")
        lines.append("")
    if request:
        lines.append("Beklenen aksiyon / talep:")
        lines.append(f"- {request}")
        lines.append("")
    if actions:
        lines.append("Aksiyonlar:")
        for item in actions:
            lines.append(f"- {item}")
        lines.append("")
    if due_date:
        lines.append(f"Beklenen dönüş / hedef tarih: {due_date}")
        lines.append("")
    if attachments:
        lines.append("Ekler:")
        for item in attachments:
            lines.append(f"- {item}")
        lines.append("")

    if recipient_type in {"taseron", "taşeron"}:
        lines.append("Uygulamaya başlamadan önce eksik bilgi veya çakışma varsa yazılı teyit rica ederiz.")
    elif message_type == "rfi":
        lines.append("Uygulama planını etkilememesi için yazılı teyidinizi rica ederiz.")
    else:
        lines.append("Bilgilerinize sunar, gerekli aksiyonlar için dönüşünüzü rica ederiz.")

    notes = risk_notes(payload)
    if notes:
        lines.extend(["", "Onay notu:"])
        for note in notes:
            lines.append(f"- {note}")

    return {
        "subject": subject_line(payload),
        "channel": channel,
        "tone": tone,
        "body": "\n".join(lines),
        "sections": {
            "facts": facts,
            "references": references,
            "request": [request] if request else [],
            "actions": actions,
            "attachments": attachments,
        },
        "risk_notes": notes,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = ["# İletişim Taslağı", "", f"**Konu:** {payload['subject']}", "", payload["body"]]
    if payload["risk_notes"]:
        lines.extend(["", "## Risk / Onay Notları", ""])
        for note in payload["risk_notes"]:
            lines.append(f"- {note}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="Communication brief JSON dosyası")
    parser.add_argument("--message-type", default="general")
    parser.add_argument("--channel", default="email")
    parser.add_argument("--recipient-type", default="")
    parser.add_argument("--recipient", default="")
    parser.add_argument("--sender", default="")
    parser.add_argument("--project", default="")
    parser.add_argument("--subject", default="")
    parser.add_argument("--fact", action="append")
    parser.add_argument("--request", default="")
    parser.add_argument("--due-date", default="")
    parser.add_argument("--reference", action="append")
    parser.add_argument("--attachment", action="append")
    parser.add_argument("--tone", default="resmi")
    parser.add_argument("--approval-required", action="store_true")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output", help="Çıktı dosyası")
    args = parser.parse_args()
    payload = draft(load_payload(args.input, args))
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(payload)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
