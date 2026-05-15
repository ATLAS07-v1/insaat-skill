#!/usr/bin/env python3
"""Create a route for construction bid and cost table tasks."""

from __future__ import annotations

import argparse
import json
from typing import Any


ROUTES: dict[str, dict[str, Any]] = {
    "rough_order_cost": {
        "goal": "Sınırlı veriyle yaklaşık maliyet aralığı ve riskli varsayımlar üretmek.",
        "tools": ["build_cost_table.py", "historical/user price list", "risk flags"],
        "outputs": ["yaklaşık maliyet", "varsayım listesi", "fiyat doğrulama ihtiyaçları"],
    },
    "detailed_boq": {
        "goal": "Metraj ve birim fiyatlardan detaylı BOQ/teklif tablosu hazırlamak.",
        "tools": ["build_cost_table.py", "validate_cost_table.py", "pandas/XlsxWriter"],
        "outputs": ["BOQ tablosu", "kategori toplamları", "markup/KDV özeti", "QA raporu"],
    },
    "supplier_quote_comparison": {
        "goal": "Taşeron/tedarikçi tekliflerini kapsam ve risk eşitlemesiyle karşılaştırmak.",
        "tools": ["CSV/JSON quote register", "rapidfuzz optional", "spreadsheet output"],
        "outputs": ["normalize edilmiş teklif karşılaştırması", "kapsam dışı işler", "risk notları"],
    },
    "bim_5d_cost": {
        "goal": "IFC/BIM quantity bilgisini cost item ve BOQ kalemlerine bağlamak.",
        "tools": ["IfcOpenShell Ifc5D", "bim-revit-ifc-model-kontrolu", "metraj-ve-mahal-kontrolu"],
        "outputs": ["IFC quantity-cost map", "5D maliyet raporu", "quantity QA bayrakları"],
    },
    "tender_bid_package": {
        "goal": "Müşteri/ihale için teklif eki, varsayımlar, kapsam dışı işler ve fiyat geçerlilik notu hazırlamak.",
        "tools": ["Markdown report", "XLSX/ODS route", "musteri-ve-taseron-iletisim-hazirlayici"],
        "outputs": ["teklif özeti", "ek tablo", "kapsam/istisna notları"],
    },
    "variation_order": {
        "goal": "Revizyon veya değişiklik emri için ek/azalan maliyet tablosu üretmek.",
        "tools": ["delta BOQ", "validate_cost_table.py", "source revision trace"],
        "outputs": ["artı/eksi maliyet", "revizyon izi", "onay notu"],
    },
}


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    route = ROUTES[args.job_type]
    phases = [
        {
            "phase": "kaynak_derleme",
            "actions": [
                "Metraj, fiyat, para birimi, KDV, kur, revizyon ve fiyat tarihi ayrılır.",
                "Güncel fiyat gerekiyorsa canlı araştırma veya kullanıcı fiyat listesi zorunlu kabul edilir.",
            ],
        },
        {
            "phase": "tablo_normalizasyonu",
            "actions": [
                "Kalemler kod, açıklama, kategori, miktar, birim, birim fiyat ve kaynak alanlarına dönüştürülür.",
                "Fire/zayiat, kapsam dışı işler ve notlar ayrı kolonlarda tutulur.",
            ],
        },
        {
            "phase": "hesap_ve_qa",
            "actions": [
                "Direkt toplam, markup, iskonto, KDV ve genel toplam hesaplanır.",
                "Eksik alan, duplicate kod, sıfır fiyat, yüksek fire ve toplam farkı kontrol edilir.",
            ],
        },
    ]
    if args.has_ifc or args.job_type == "bim_5d_cost":
        phases.append(
            {
                "phase": "bim_5d",
                "actions": [
                    "IFC quantity kaynakları IfcOpenShell/Ifc5D rotasına bağlanır.",
                    "Model quantity doğruluğu maliyet hesabından önce bayraklanır.",
                ],
            }
        )
    if args.has_supplier_quotes or args.job_type == "supplier_quote_comparison":
        phases.append(
            {
                "phase": "teklif_karsilastirma",
                "actions": [
                    "Taşeron kapsam, istisna, marka/model, teslim süresi ve ödeme şartları eşitlenir.",
                    "Sadece toplam bedelle karar verilmez; risk ve kapsam puanı eklenir.",
                ],
            }
        )
    if args.needs_xlsx:
        phases.append(
            {
                "phase": "xlsx_ods_cikti",
                "actions": [
                    "XLSX için XlsxWriter/openpyxl, ODS için LibreOffice/odfdo rotası önerilir.",
                    "Spreadsheet formülleri Python hesap sonucu ile kontrol edilir.",
                ],
            }
        )
    return {
        "job_type": args.job_type,
        "goal": route["goal"],
        "recommended_tools": route["tools"],
        "expected_outputs": route["outputs"],
        "phases": phases,
        "qa_gates": [
            "Her kalemin miktar, birim, birim fiyat, para birimi ve kaynak alanı olmalı.",
            "Fiyat tarihi ve KDV dahil/hariç durumu açık yazılmalı.",
            "Metraj doğrulanmadıysa sonuç bağlayıcı teklif gibi sunulmamalı.",
            "Canlı piyasa fiyatı istenirse tarihli kaynak linkleriyle doğrulama yapılmalı.",
            "Sözleşmesel/vergi/kur kararları kullanıcı veya ticari sorumlu onayı gerektirir.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-type", choices=sorted(ROUTES), default="detailed_boq")
    parser.add_argument("--has-ifc", action="store_true")
    parser.add_argument("--has-supplier-quotes", action="store_true")
    parser.add_argument("--needs-xlsx", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_plan(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
