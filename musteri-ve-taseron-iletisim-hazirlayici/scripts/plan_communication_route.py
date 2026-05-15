#!/usr/bin/env python3
"""Plan the route for a construction customer/subcontractor communication package."""

from __future__ import annotations

import argparse
import json
from typing import Any


JOBS: dict[str, dict[str, Any]] = {
    "client_update": {
        "label": "Müşteri durum güncellemesi",
        "sections": ["kısa özet", "tamamlanan işler", "bekleyen kararlar", "riskler", "beklenen aksiyon"],
        "tools": ["draft_construction_message.py", "validate_communication_pack.py", "OpenProject / ERPNext"],
        "outputs": ["resmi e-posta", "aksiyon takip özeti"],
    },
    "subcontractor_instruction": {
        "label": "Taşeron saha/iş talimatı",
        "sections": ["mahal", "iş kapsamı", "referans çizim", "termin", "kalite ve İSG koşulları"],
        "tools": ["draft_construction_message.py", "OpenProject work package"],
        "outputs": ["iş talimatı", "takip görevi"],
    },
    "rfi": {
        "label": "RFI hazırlığı",
        "sections": ["referans", "saha durumu", "net soru", "etki", "beklenen cevap tarihi", "ekler"],
        "tools": ["draft_construction_message.py", "validate_communication_pack.py"],
        "outputs": ["RFI e-postası", "RFI kayıt özeti"],
    },
    "submittal": {
        "label": "Submittal hazırlığı",
        "sections": ["belge listesi", "revizyon", "amaç", "şartname referansı", "beklenen dönüş", "ekler"],
        "tools": ["draft_construction_message.py", "validate_communication_pack.py"],
        "outputs": ["submittal notu", "belge listesi"],
    },
    "transmittal": {
        "label": "Transmittal hazırlığı",
        "sections": ["paket no", "belge listesi", "revizyon", "gönderim amacı", "beklenen aksiyon"],
        "tools": ["draft_construction_message.py"],
        "outputs": ["transmittal notu", "ek listesi"],
    },
    "meeting_minutes": {
        "label": "Toplantı tutanağı",
        "sections": ["katılımcılar", "gündem", "kararlar", "aksiyonlar", "açık konular"],
        "tools": ["OpenProject Meetings", "validate_communication_pack.py"],
        "outputs": ["toplantı tutanağı", "aksiyon tablosu"],
    },
    "delay_notice_draft": {
        "label": "Gecikme bildirimi taslağı",
        "sections": ["olay", "etki", "kanıt", "beklenen karar", "hak saklı / onay notu"],
        "tools": ["draft_construction_message.py", "validate_communication_pack.py"],
        "outputs": ["onay gerektiren taslak", "risk notu"],
        "approval_required": True,
    },
    "variation_notice_draft": {
        "label": "Varyasyon / ek iş taslağı",
        "sections": ["talep nedeni", "kapsam farkı", "etki", "referans", "onay talebi"],
        "tools": ["draft_construction_message.py", "validate_communication_pack.py"],
        "outputs": ["onay gerektiren taslak", "ticari risk notu"],
        "approval_required": True,
    },
    "payment_followup": {
        "label": "Hakediş / ödeme takip mesajı",
        "sections": ["hakediş no", "tutar", "vade", "beklenen aksiyon", "ekler"],
        "tools": ["draft_construction_message.py", "validate_communication_pack.py"],
        "outputs": ["ödeme takip e-postası", "onay notu"],
        "approval_required": True,
    },
    "ncr_response": {
        "label": "Uygunsuzluk yanıtı",
        "sections": ["NCR no", "bulgu", "kök neden", "düzeltici aksiyon", "kapatma kanıtı"],
        "tools": ["draft_construction_message.py", "risk-guvenlik-ve-uygunluk-denetimi"],
        "outputs": ["NCR yanıt taslağı", "CAPA aksiyon listesi"],
    },
    "procurement_followup": {
        "label": "Tedarik / teslim takip mesajı",
        "sections": ["sipariş", "malzeme", "termin", "stok/üretim durumu", "beklenen teyit"],
        "tools": ["draft_construction_message.py", "tedarik-ve-malzeme-karsilastirma"],
        "outputs": ["tedarik takip mesajı", "teslim teyit listesi"],
    },
}


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    job = JOBS[args.job_type]
    approval_required = bool(job.get("approval_required")) or args.contract_risk or args.financial_risk
    qa_gates = [
        "Alıcı, proje, konu, talep ve termin net",
        "Gerçek bilgi ile yorum ayrıldı",
        "Ekler ve referanslar listelendi",
        "Gönderim öncesi onay gerektiren ifadeler bayraklandı",
        "Takip için sorumlu, kayıt no ve sonraki aksiyon tanımlandı",
    ]
    notes = []
    if args.channel == "whatsapp":
        notes.append("Kısa mesaj karar/talimat içeriyorsa ayrıca e-posta veya issue kaydı öner.")
    if args.channel == "formal_letter":
        approval_required = True
        notes.append("Resmi yazı formatı yetkili temsil ve imza kontrolü gerektirir.")
    if args.recipient:
        notes.append(f"Hedef alıcı tipi: {args.recipient}. Ton ve detay seviyesi buna göre ayarlanmalı.")
    if args.bilingual:
        notes.append("İki dilli çıktı isteniyor; hukuki/sözleşmesel ifadelerde iki dil tutarlılığı ayrıca kontrol edilmeli.")
    if approval_required:
        notes.append("Bu paket gönderim öncesi yetkili onay gerektirir.")

    return {
        "job_type": args.job_type,
        "label": job["label"],
        "channel": args.channel,
        "sections": job["sections"],
        "tools": job["tools"],
        "outputs": job["outputs"],
        "qa_gates": qa_gates,
        "approval_required": approval_required,
        "notes": notes,
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [f"# {plan['label']} Rotası", ""]
    lines.append(f"- Kanal: {plan['channel']}")
    lines.append(f"- Onay gerekli: {'evet' if plan['approval_required'] else 'hayır'}")
    lines.extend(["", "## Bölümler", ""])
    for section in plan["sections"]:
        lines.append(f"- {section}")
    lines.extend(["", "## Araçlar", ""])
    for tool in plan["tools"]:
        lines.append(f"- {tool}")
    lines.extend(["", "## Çıktılar", ""])
    for output in plan["outputs"]:
        lines.append(f"- {output}")
    lines.extend(["", "## QA Kapıları", ""])
    for gate in plan["qa_gates"]:
        lines.append(f"- {gate}")
    if plan["notes"]:
        lines.extend(["", "## Notlar", ""])
        for note in plan["notes"]:
            lines.append(f"- {note}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-type", choices=sorted(JOBS), required=True)
    parser.add_argument("--recipient", choices=["musteri", "isveren", "taseron", "tedarikci", "ic-ekip", "danisman"])
    parser.add_argument("--channel", choices=["email", "whatsapp", "formal_letter", "meeting", "issue", "crm_note"], default="email")
    parser.add_argument("--contract-risk", action="store_true")
    parser.add_argument("--financial-risk", action="store_true")
    parser.add_argument("--bilingual", action="store_true")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    plan = build_plan(args)
    print(json.dumps(plan, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
