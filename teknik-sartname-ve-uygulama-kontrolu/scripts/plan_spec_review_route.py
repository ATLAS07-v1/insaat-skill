#!/usr/bin/env python3
"""Create a review route for technical specification and implementation checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROUTES: dict[str, dict[str, Any]] = {
    "technical_spec_review": {
        "goal": "Teknik şartname maddelerini kontrol listesine ve kanıt gereksinimlerine çevirmek.",
        "tools": ["pdfplumber/pypdf or python-docx", "extract_spec_clauses.py", "jsonschema"],
        "outputs": ["madde listesi", "kanıt gereksinimi", "belirsiz tolerans bayrakları"],
    },
    "method_statement_review": {
        "goal": "Uygulama yöntemini şartname, çizim notu ve saha koşullarıyla karşılaştırmak.",
        "tools": ["python-docx/pdfplumber", "clause checklist", "risk flagging"],
        "outputs": ["uygulama kontrol listesi", "çelişki listesi", "saha kanıt planı"],
    },
    "submittal_check": {
        "goal": "Malzeme/ürün onay dosyasını şartname gereksinimleriyle eşleştirmek.",
        "tools": ["pandas/openpyxl", "datasheet parser", "compare_evidence_to_checklist.py"],
        "outputs": ["eksik sertifika", "teknik föy uyuşmazlığı", "onay sınırı"],
    },
    "site_inspection": {
        "goal": "Saha gözlem ve kanıtlarını madde bazlı uygunluk kontrolüne bağlamak.",
        "tools": ["evidence register", "photo/test report metadata", "issue/BCF draft"],
        "outputs": ["uygunsuzluk listesi", "eksik kanıt listesi", "takip aksiyonları"],
    },
    "bim_ids_validation": {
        "goal": "Model bilgi gereksinimlerini IDS/IfcTester ile doğrulamak.",
        "tools": ["IDS", "IfcTester", "BCF reporter", "IfcOpenShell"],
        "outputs": ["IDS raporu", "model bilgi eksikleri", "BCF topic taslağı"],
    },
    "test_report_review": {
        "goal": "Deney/test raporlarını şartname kabul kriteriyle eşleştirmek.",
        "tools": ["pandas", "pdfplumber", "compare_evidence_to_checklist.py"],
        "outputs": ["geçti/kaldı tablosu", "eksik numune", "limit dışı sonuç"],
    },
}


def detect_type(source: str | None) -> str:
    if not source:
        return "technical_spec_review"
    suffix = Path(source).suffix.lower()
    name = Path(source).name.lower()
    if suffix in {".ifc", ".ids"} or "ids" in name:
        return "bim_ids_validation"
    if "method" in name or "uygulama" in name:
        return "method_statement_review"
    if "submittal" in name or "malzeme" in name or "material" in name:
        return "submittal_check"
    if "test" in name or "deney" in name or "rapor" in name:
        return "test_report_review"
    return "technical_spec_review"


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    source_type = args.source_type or detect_type(args.source)
    route = ROUTES[source_type]
    phases = [
        {
            "phase": "kaynak_incelemesi",
            "actions": [
                "Dosya türü, revizyon, tarih, sayfa/madde izi ve sözleşme önceliği kontrol edilir.",
                "Metin çıkarım kalitesi düşükse sonuç düşük güven bayrağıyla verilir.",
            ],
        },
        {
            "phase": "madde_normalizasyonu",
            "actions": [
                "Zorunlu şartlar, toleranslar, testler, submittal ve teslim maddeleri ayrılır.",
                "Her maddeye id, kategori, kanıt türü, kabul kriteri ve manuel inceleme bayrağı atanır.",
            ],
        },
        {
            "phase": "kanit_eslestirme",
            "actions": [
                "Kanıt kayıtları madde id, imalat kalemi, mahal, tarih ve dosya adı üzerinden eşleştirilir.",
                "Eksik, çelişkili, revizyon dışı ve tolerans dışı kanıtlar ayrı sınıflandırılır.",
            ],
        },
    ]
    if args.has_ifc or source_type == "bim_ids_validation":
        phases.append(
            {
                "phase": "bim_ids_kontrolu",
                "actions": [
                    "Model bilgi gereksinimleri IDS specification adayı olarak ayrılır.",
                    "IfcTester JSON/HTML/BCF raporu hedeflenir; model dışı saha uygunluğu ayrı tutulur.",
                ],
            }
        )
    if args.has_site_photos or args.has_test_reports:
        phases.append(
            {
                "phase": "saha_kanit_kontrolu",
                "actions": [
                    "Fotoğraf/test kanıtlarının tarih, mahal, imalat kalemi ve kaynak maddeyle izlenebilirliği kontrol edilir.",
                    "Nihai kabul yerine teknik bulgu ve takip aksiyonu üretilir.",
                ],
            }
        )
    return {
        "source": args.source,
        "source_type": source_type,
        "strictness": args.strictness,
        "goal": route["goal"],
        "recommended_tools": route["tools"],
        "expected_outputs": route["outputs"],
        "phases": phases,
        "qa_gates": [
            "Her bulgu kaynak madde veya dosya izine bağlanmalı.",
            "Belirsiz tolerans ve eksik standart metni nihai uygunluk olarak yorumlanmamalı.",
            "Kanıt revizyonu ve şartname revizyonu aynı bağlama oturmalı.",
            "Resmi kabul, sözleşmesel karar ve mühendislik onayı kullanıcı/teknik sorumluya bırakılmalı.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Kaynak dosya adı veya kısa açıklaması")
    parser.add_argument("--source-type", choices=sorted(ROUTES), help="Kontrol tipi")
    parser.add_argument("--strictness", choices=["normal", "strict", "forensic"], default="normal")
    parser.add_argument("--has-ifc", action="store_true")
    parser.add_argument("--has-site-photos", action="store_true")
    parser.add_argument("--has-test-reports", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_plan(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
