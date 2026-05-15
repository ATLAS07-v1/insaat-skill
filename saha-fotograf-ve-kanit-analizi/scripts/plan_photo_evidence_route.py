#!/usr/bin/env python3
"""Plan the tool route for construction photo and visual evidence analysis."""

from __future__ import annotations

import argparse
import json
from typing import Any


JOBS: dict[str, dict[str, Any]] = {
    "photo_register_build": {
        "label": "Fotoğraf kanıt register üretimi",
        "phases": [
            "Orijinal dosya klasörünü ve kapsamı sabitle",
            "SHA256, dosya boyutu, tarih ve temel metadata çıkar",
            "Proje/mahal/konu bağlamını register'a ekle",
            "Eksik metadata, duplicate ve gizlilik bayraklarını kontrol et",
        ],
        "tools": ["build_photo_evidence_register.py", "validate_photo_evidence_register.py", "ExifTool"],
        "outputs": ["fotoğraf register", "metadata bütünlük raporu"],
    },
    "progress_photo_review": {
        "label": "İlerleme fotoğraf incelemesi",
        "phases": [
            "Önce/sonra veya tarih sıralı fotoğrafları grupla",
            "Mahale, iş kalemine ve taşerona göre eşleştir",
            "Görsel ilerleme bulgusunu metraj/hakediş verisiyle sınırla",
            "Eksik açı, düşük kalite ve duplicate fotoğrafları bayrakla",
        ],
        "tools": ["build_photo_evidence_register.py", "ImageHash", "OpenCV"],
        "outputs": ["ilerleme görsel özeti", "eksik kanıt listesi"],
    },
    "quality_defect_photo_review": {
        "label": "Kalite / uygunsuzluk fotoğraf incelemesi",
        "phases": [
            "Fotoğrafları NCR, mahal, disiplin ve iş kalemiyle eşleştir",
            "Kusur/risk alanlarını anotasyonla işaretle",
            "Kapatma kanıtı ve önce-sonra karşılaştırmasını ayır",
            "Yetkili teknik doğrulama gerektiren noktaları raporla",
        ],
        "tools": ["CVAT", "Label Studio", "OpenCV", "validate_photo_evidence_register.py"],
        "outputs": ["NCR görsel eki", "anotasyon listesi", "aksiyon raporu"],
    },
    "safety_evidence_review": {
        "label": "İSG fotoğraf kanıt incelemesi",
        "phases": [
            "Fotoğrafları risk/uygunluk gereksinimiyle eşleştir",
            "Bariyer, KKD, izin, levha ve kritik alan görsellerini sınıflandır",
            "Kişi/yüz/plaka/GPS gizlilik kontrolünü yap",
            "İSG uzmanı doğrulaması gereken bulguları ayrı yaz",
        ],
        "tools": ["risk-guvenlik-ve-uygunluk-denetimi", "CVAT", "Tesseract OCR"],
        "outputs": ["İSG kanıt matrisi", "gizlilik bayrakları"],
    },
    "document_photo_ocr": {
        "label": "Fotoğraftan belge/levha OCR",
        "phases": [
            "Görseli netlik, açı ve çözünürlük için kontrol et",
            "OCR ön işleme ve metin çıkarımı yap",
            "Belge no, tarih, revizyon, izin no gibi kritik alanları manuel doğrulamaya ayır",
            "Ham OCR ve doğrulama notunu raporla",
        ],
        "tools": ["Tesseract OCR", "OpenCV", "pytesseract"],
        "outputs": ["OCR ham metni", "kritik alan kontrol listesi"],
    },
    "duplicate_photo_check": {
        "label": "Duplicate / near-duplicate kontrolü",
        "phases": [
            "SHA256 ile birebir tekrarları bul",
            "Perceptual hash ile benzer görselleri grupla",
            "Kanıt sayısını şişiren tekrarları raporla",
            "Tutulacak ana kanıt ve ek referansları ayır",
        ],
        "tools": ["ImageHash", "OpenCV", "FiftyOne"],
        "outputs": ["duplicate raporu", "temiz fotoğraf listesi"],
    },
    "drone_site_mapping": {
        "label": "Drone saha haritalama",
        "phases": [
            "Uçuş tarihi, kamera, koordinat sistemi ve foto setini doğrula",
            "OpenDroneMap/WebODM ile ortomozaik veya 3D çıktı üret",
            "QGIS ile georeferans, mahal ve katman bağlantısını kontrol et",
            "Harita çıktısını ilerleme/kanıt raporuna bağla",
        ],
        "tools": ["OpenDroneMap", "WebODM", "QGIS"],
        "outputs": ["ortomozaik", "3D model/nokta bulutu", "GIS raporu"],
    },
    "claim_evidence_pack": {
        "label": "Claim / gecikme / hak talebi kanıt paketi",
        "phases": [
            "Fotoğrafları olay, tarih, mahal ve yazışmalarla eşleştir",
            "Bütünlük, metadata, duplicate ve eksik bağlam kontrolü yap",
            "Sözleşmesel/hukuki iddia doğurabilecek yorumları onaya ayır",
            "Kanıt seviyesini ve yetkili doğrulama gereksinimini yaz",
        ],
        "tools": ["build_photo_evidence_register.py", "validate_photo_evidence_register.py", "musteri-ve-taseron-iletisim-hazirlayici"],
        "outputs": ["kanıt paketi özeti", "onay gerektiren risk notu"],
        "approval_required": True,
    },
}


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    job = JOBS[args.job_type]
    tools = list(job["tools"])
    outputs = list(job["outputs"])
    qa_gates = [
        "Orijinal dosya hash ve kaynak yolu kayıtlandı",
        "Metadata yoksa kanıt seviyesi düşürüldü",
        "Fotoğraftaki bulgu kesin karar gibi yazılmadı",
        "Hassas veri ve GPS paylaşım riski kontrol edildi",
        "Yetkili saha/teknik/İSG doğrulaması gereken noktalar ayrıldı",
    ]
    notes = []
    approval_required = bool(job.get("approval_required"))

    if args.has_gps:
        notes.append("GPS/konum bilgisi hassas veri olabilir; paylaşım öncesi gizlilik kontrolü gerekir.")
    if args.needs_ocr and "Tesseract OCR" not in tools:
        tools.extend(["Tesseract OCR", "OpenCV"])
        outputs.append("OCR ham metni")
    if args.has_drone and "OpenDroneMap" not in tools:
        tools.extend(["OpenDroneMap", "QGIS"])
        outputs.append("georeferans/drone çıktı notu")
    if args.large_set and "FiftyOne" not in tools:
        tools.append("FiftyOne")
        notes.append("Büyük görsel setinde dataset QA ve filtreleme rotası eklenmeli.")
    if args.privacy_sensitive:
        approval_required = True
        notes.append("Gizlilik açısından hassas içerik var; redaksiyon veya paylaşım onayı gerekir.")
    if args.claim_context:
        approval_required = True
        notes.append("Claim/hak talebi bağlamı var; hukuki/ticari yorumlar yetkili onaya ayrılmalı.")

    return {
        "job_type": args.job_type,
        "label": job["label"],
        "phases": job["phases"],
        "tools": sorted(dict.fromkeys(tools)),
        "outputs": sorted(dict.fromkeys(outputs)),
        "qa_gates": qa_gates,
        "approval_required": approval_required,
        "notes": notes,
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
    parser.add_argument("--has-gps", action="store_true")
    parser.add_argument("--needs-ocr", action="store_true")
    parser.add_argument("--has-drone", action="store_true")
    parser.add_argument("--large-set", action="store_true")
    parser.add_argument("--privacy-sensitive", action="store_true")
    parser.add_argument("--claim-context", action="store_true")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    plan = build_plan(args)
    print(json.dumps(plan, ensure_ascii=False, indent=2) if args.format == "json" else render_markdown(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
