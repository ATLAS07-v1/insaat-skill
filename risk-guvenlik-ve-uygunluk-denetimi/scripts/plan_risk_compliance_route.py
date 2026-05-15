#!/usr/bin/env python3
"""Plan the tool route for a construction risk, safety, or compliance audit."""

from __future__ import annotations

import argparse
import json
from typing import Any


JOBS: dict[str, dict[str, Any]] = {
    "construction_safety_audit": {
        "label": "Saha İSG denetimi",
        "phases": [
            "Kapsam, lokasyon, taraflar ve geçerli kaynakları sabitle",
            "İSG checklist ve kanıt envanterini oluştur",
            "Saha bulgularını risk seviyesi ve gereksinim id'si ile eşleştir",
            "Uygunsuzluk ve aksiyon planı üret",
        ],
        "tools": ["audit_compliance_checklist.py", "score_risk_register.py"],
        "outputs": ["denetim raporu", "uygunsuzluk listesi", "aksiyon planı"],
    },
    "risk_register_review": {
        "label": "Risk register incelemesi",
        "phases": [
            "Risk kayıtlarını normalize et",
            "Olasılık, şiddet, artık risk ve kontrol alanlarını doğrula",
            "Sahipsiz, kanıtsız, termin geçmiş ve yüksek riskleri bayrakla",
            "Öncelikli aksiyon listesi üret",
        ],
        "tools": ["score_risk_register.py"],
        "outputs": ["risk skoru", "öncelik listesi", "eksik alan raporu"],
    },
    "method_statement_risk_review": {
        "label": "Method statement / JSA risk kontrolü",
        "phases": [
            "Faaliyet adımlarını ve tehlikeleri çıkar",
            "Gerekli kontrol, izin, eğitim ve ekipman kayıtlarını eşleştir",
            "Eksik kontrol ve kanıtları risk seviyesine göre sırala",
            "Revizyon ve onay gerektiren maddeleri raporla",
        ],
        "tools": ["audit_compliance_checklist.py", "score_risk_register.py"],
        "outputs": ["JSA gap listesi", "method statement revizyon notu"],
    },
    "permit_document_control": {
        "label": "Çalışma izni ve belge kontrolü",
        "phases": [
            "İzin tipi ve geçerlilik tarihlerini belirle",
            "Ek belge, eğitim, ekipman kontrolü ve yetki kayıtlarını eşleştir",
            "Eksik veya süresi geçmiş kanıtları bayrakla",
            "Başlamadan önce tamamlanacak aksiyonları çıkar",
        ],
        "tools": ["audit_compliance_checklist.py"],
        "outputs": ["izin uygunluk matrisi", "eksik belge listesi"],
    },
    "compliance_evidence_audit": {
        "label": "Uygunluk ve kanıt denetimi",
        "phases": [
            "Gereksinim kataloğunu id, kaynak ve kabul kriteri ile kur",
            "Kanıt envanterini dosya, tarih, sahip ve durum ile normalize et",
            "Her gereksinimin kanıt durumunu denetle",
            "Eksik kanıt ve bağlayıcı onay sınırını raporla",
        ],
        "tools": ["audit_compliance_checklist.py", "Frictionless", "Great Expectations"],
        "outputs": ["uygunluk matrisi", "kanıt eksikliği raporu"],
    },
    "bim_model_compliance": {
        "label": "BIM/IFC model uygunluk denetimi",
        "phases": [
            "IFC model ve IDS gereksinim setini doğrula",
            "IfcTester ile IDS denetimi çalıştır",
            "Başarısız gereksinimleri element GUID ve kategori ile özetle",
            "Gerekirse BCF issue ve aksiyon listesi üret",
        ],
        "tools": ["IfcOpenShell", "IfcTester", "BCF API", "OpenProject BIM"],
        "outputs": ["IDS raporu", "BCF issue özeti", "model uygunsuzluk listesi"],
    },
    "incident_near_miss_review": {
        "label": "Kaza / ramak kala incelemesi",
        "phases": [
            "Olay zamanı, lokasyon, iş paketi ve etkilenen kişileri kaydet",
            "Kök neden, eksik kontrol ve tekrar riskini sınıflandır",
            "Düzeltici/önleyici aksiyonları sorumlu ve terminle bağla",
            "Kapanış kanıtı ve öğrenilen dersleri raporla",
        ],
        "tools": ["score_risk_register.py", "audit_compliance_checklist.py"],
        "outputs": ["olay inceleme özeti", "CAPA listesi"],
    },
    "environmental_compliance_check": {
        "label": "Çevre uygunluk kontrolü",
        "phases": [
            "Atık, hafriyat, toz, gürültü, kimyasal ve deşarj gereksinimlerini çıkar",
            "İzin, ölçüm, bertaraf ve taşıma kanıtlarını eşleştir",
            "Eksik belge ve yüksek etki risklerini bayrakla",
            "Aksiyon ve izleme planı üret",
        ],
        "tools": ["audit_compliance_checklist.py", "Frictionless"],
        "outputs": ["çevre uygunluk matrisi", "eksik izin/kanıt listesi"],
    },
}


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    job = JOBS[args.job_type]
    tools = list(job["tools"])
    outputs = list(job["outputs"])
    qa_gates = [
        "Kaynak adı, sürüm/tarih ve gereksinim id'si yazıldı",
        "Kritik bulgular sorumlu, termin ve kapatma kanıtı ile bağlandı",
        "Eksik kanıtlar uygun kabul edilmedi",
        "Resmi uygunluk veya güvenlik beyanı yerine kanıt temelli ön denetim dili kullanıldı",
    ]
    notes = []

    if args.has_ifc and "IfcTester" not in tools:
        tools.extend(["IfcOpenShell", "IfcTester"])
        outputs.append("model tabanlı uygunsuzluk özeti")
    if args.has_permits:
        notes.append("Çalışma izni, yetki, eğitim ve ekipman kontrol kayıtlarını ayrı kanıt olarak eşleştir.")
    if args.has_photos:
        notes.append("Fotoğrafları tarih, lokasyon, gereksinim id'si ve doğrulama notu olmadan güçlü kanıt sayma.")
    if args.has_pdf:
        tools.append("pypdf / pdfplumber")
        notes.append("PDF çıkarımı sonrası kritik alanları manuel doğrula.")
    if args.needs_xlsx:
        tools.extend(["pandas", "XlsxWriter"])
        outputs.append("XLSX denetim matrisi")
    if args.country:
        notes.append(f"Yerel mevzuat bağlamı: {args.country}. Güncel resmi kaynak ayrıca doğrulanmalı.")

    return {
        "job_type": args.job_type,
        "label": job["label"],
        "phases": job["phases"],
        "tools": sorted(dict.fromkeys(tools)),
        "outputs": sorted(dict.fromkeys(outputs)),
        "qa_gates": qa_gates,
        "notes": notes,
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [f"# {plan['label']} Araç Rotası", ""]
    lines.extend(["## Fazlar", ""])
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
    parser.add_argument("--country", help="Yerel mevzuat bağlamı, örn. Türkiye")
    parser.add_argument("--has-ifc", action="store_true")
    parser.add_argument("--has-pdf", action="store_true")
    parser.add_argument("--has-photos", action="store_true")
    parser.add_argument("--has-permits", action="store_true")
    parser.add_argument("--needs-xlsx", action="store_true")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    plan = build_plan(args)
    if args.format == "json":
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
