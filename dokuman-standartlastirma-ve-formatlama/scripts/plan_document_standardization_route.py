#!/usr/bin/env python3
"""Plan a document standardization and formatting route for construction documents."""

from __future__ import annotations

import argparse
import json
from typing import Any


JOBS: dict[str, dict[str, Any]] = {
    "technical_report_formatting": {
        "label": "Teknik rapor formatlama",
        "phases": ["doküman türünü sabitle", "başlık/kapak/revizyon standardını uygula", "stil ve dil QA yap", "PDF/DOCX teslim paketi üret"],
        "tools": ["Pandoc", "python-docx", "Vale", "LanguageTool"],
        "outputs": ["standart teknik rapor", "format QA raporu"],
    },
    "method_statement_package": {
        "label": "Method statement paketi",
        "phases": ["zorunlu bölümleri kontrol et", "çizim/revizyon ve ekleri bağla", "İSG/kalite kontrol noktalarını ayır", "onay ve teslim formatı üret"],
        "tools": ["Pandoc", "python-docx", "validate_markdown_document.py"],
        "outputs": ["method statement DOCX/PDF", "eksik bölüm listesi"],
    },
    "specification_standardization": {
        "label": "Teknik şartname standardizasyonu",
        "phases": ["madde hiyerarşisini düzenle", "tanım ve referansları standartlaştır", "tablo/görsel formatını kontrol et", "revizyon ve onay sınırını yaz"],
        "tools": ["python-docx", "Open XML SDK", "Vale"],
        "outputs": ["standart şartname", "madde format QA"],
    },
    "meeting_minutes_pack": {
        "label": "Toplantı tutanağı paketi",
        "phases": ["katılımcı/gündem/karar/aksiyon ayrımı yap", "aksiyon tablosunu normalize et", "tutanak formatını uygula", "gönderim/transmittal notunu hazırla"],
        "tools": ["Pandoc", "OpenProject Meetings", "musteri-ve-taseron-iletisim-hazirlayici"],
        "outputs": ["toplantı tutanağı", "aksiyon listesi"],
    },
    "rfi_submittal_transmittal_pack": {
        "label": "RFI / submittal / transmittal paketi",
        "phases": ["belge listesini ve revizyonları kontrol et", "ekleri manifest'e bağla", "gönderim amacını netleştir", "PDF/DOCX/CSV çıktı üret"],
        "tools": ["inspect_document_package.py", "musteri-ve-taseron-iletisim-hazirlayici"],
        "outputs": ["transmittal manifest", "gönderim notu"],
    },
    "markdown_to_docx_pdf": {
        "label": "Markdown -> DOCX/PDF dönüşümü",
        "phases": ["Markdown QA yap", "Pandoc şablonu/reference-doc seç", "DOCX/PDF üret", "render ve sayfa QA kontrolü yap"],
        "tools": ["validate_markdown_document.py", "Pandoc", "LibreOffice"],
        "outputs": ["DOCX", "PDF", "Markdown QA raporu"],
    },
    "pdf_export_qa": {
        "label": "PDF export QA",
        "phases": ["kaynak belgeyi kontrol et", "PDF export üret", "sayfa/görsel/tablo/header/footer kontrolü yap", "riskleri raporla"],
        "tools": ["LibreOffice", "pypdf", "PyMuPDF", "qpdf"],
        "outputs": ["PDF QA raporu", "dönüşüm risk notu"],
    },
    "document_set_audit": {
        "label": "Doküman paket denetimi",
        "phases": ["klasörü tara", "dosya adı/revizyon/format kontrolü yap", "duplicate ve desteklenmeyen dosyaları bayrakla", "manifest üret"],
        "tools": ["inspect_document_package.py"],
        "outputs": ["doküman manifest", "paket QA raporu"],
    },
    "template_creation": {
        "label": "Doküman şablonu oluşturma",
        "phases": ["doküman türlerini sınıflandır", "kapak/revizyon/içindekiler stilini tanımla", "zorunlu bölüm listesini oluştur", "örnek çıktı ve QA kurallarını yaz"],
        "tools": ["python-docx", "Pandoc reference-doc", "Jinja2"],
        "outputs": ["şablon doküman", "şablon kullanım notu"],
    },
}


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    job = JOBS[args.job_type]
    tools = list(job["tools"])
    outputs = list(job["outputs"])
    qa_gates = [
        "Doküman kodu, revizyon, tarih ve proje kodu kontrol edildi",
        "Başlık hiyerarşisi ve zorunlu bölümler doğrulandı",
        "Placeholder ve örnek metin kalmadı",
        "PDF/DOCX dönüşümü sonrası görsel QA gerektiği işaretlendi",
        "Teknik/hukuki/sözleşmesel içerik onay sınırı yazıldı",
    ]
    notes = []

    if args.source_format:
        notes.append(f"Kaynak format: {args.source_format}.")
    if args.target_format:
        target_format = args.target_format.upper()
        outputs.append(target_format)
        notes.append(f"Hedef format: {target_format}.")
    if args.needs_pdf:
        if "LibreOffice" not in tools:
            tools.append("LibreOffice")
        outputs.append("PDF")
        notes.append("PDF export sonrası sayfa ve tablo taşması görsel QA gerektirir.")
    if args.has_template:
        notes.append("Mevcut kurumsal şablon kullanılmalı; stil elle taklit edilmemeli.")
    if args.bilingual:
        if "LanguageTool" not in tools:
            tools.append("LanguageTool")
        notes.append("İki dilli dokümanda terminoloji ve bölüm eşleşmesi ayrıca kontrol edilmeli.")
    if args.contract_sensitive:
        notes.append("Sözleşmesel/hukuki içerik var; yetkili onay gerekir.")

    return {
        "job_type": args.job_type,
        "label": job["label"],
        "phases": job["phases"],
        "tools": sorted(dict.fromkeys(tools)),
        "outputs": sorted(dict.fromkeys(outputs)),
        "qa_gates": qa_gates,
        "notes": notes,
        "approval_required": bool(args.contract_sensitive),
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [f"# {plan['label']} Rotası", ""]
    lines.append(f"- Onay gerekli: {'evet' if plan['approval_required'] else 'hayır'}")
    lines.extend(["", "## Fazlar", ""])
    for index, phase in enumerate(plan["phases"], start=1):
        lines.append(f"{index}. {phase}")
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
    parser.add_argument("--source-format")
    parser.add_argument("--target-format")
    parser.add_argument("--needs-pdf", action="store_true")
    parser.add_argument("--has-template", action="store_true")
    parser.add_argument("--bilingual", action="store_true")
    parser.add_argument("--contract-sensitive", action="store_true")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    plan = build_plan(args)
    print(json.dumps(plan, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
