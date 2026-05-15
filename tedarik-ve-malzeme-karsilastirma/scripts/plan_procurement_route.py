#!/usr/bin/env python3
"""Create a route for procurement and material comparison tasks."""

from __future__ import annotations

import argparse
import json
from typing import Any


ROUTES: dict[str, dict[str, Any]] = {
    "rfq_preparation": {
        "goal": "Malzeme ihtiyacını RFQ kapsamına, teknik kriterlere ve teklif kolonlarına çevirmek.",
        "tools": ["ERPNext RFQ route", "technical specification checklist", "CSV/JSON template"],
        "outputs": ["RFQ madde listesi", "zorunlu belge listesi", "teklif şablonu"],
    },
    "supplier_quote_comparison": {
        "goal": "Tedarikçi tekliflerini fiyat, termin, stok, teknik uygunluk ve riskle karşılaştırmak.",
        "tools": ["compare_supplier_quotes.py", "pandas/XlsxWriter optional", "OpenRefine/RapidFuzz optional"],
        "outputs": ["tedarikçi sıralaması", "risk listesi", "eksik bilgi aksiyonları"],
    },
    "material_spec_comparison": {
        "goal": "Malzeme datasheet/sertifika değerlerini şartname kriterleriyle karşılaştırmak.",
        "tools": ["compare_material_specs.py", "teknik-sartname-ve-uygulama-kontrolu", "PDF extraction optional"],
        "outputs": ["teknik uygunluk matrisi", "eksik sertifika", "muadil onay bayrakları"],
    },
    "stock_replenishment": {
        "goal": "Stok, minimum seviye, lot, expiry ve termin riskine göre tedarik önceliği çıkarmak.",
        "tools": ["OpenBoxes", "ERPNext Stock", "CSV stock register"],
        "outputs": ["stok risk listesi", "sipariş önceliği", "kritik terminler"],
    },
    "delivery_acceptance": {
        "goal": "Gelen malzemenin PO, onaylı ürün, irsaliye, lot ve kalite belgeleriyle eşleşmesini kontrol etmek.",
        "tools": ["ERPNext Purchase Receipt", "OpenBoxes receiving", "material spec comparison"],
        "outputs": ["teslim kabul kontrolü", "eksik/hasarlı/farklı ürün bayrakları"],
    },
    "pim_catalog_cleanup": {
        "goal": "Malzeme ürün kataloğunu marka/model/attribute/datasheet düzeyinde tekilleştirmek.",
        "tools": ["Akeneo/OpenPIM", "OpenRefine", "Frictionless"],
        "outputs": ["normalize ürün kataloğu", "duplicate/missing attribute listesi"],
    },
}


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    route = ROUTES[args.job_type]
    phases = [
        {
            "phase": "ihtiyac_normalizasyonu",
            "actions": [
                "Malzeme kodu, açıklama, miktar, birim, teslim yeri, şartname maddesi ve zorunlu belgeler ayrılır.",
                "Muadil ürün kabulü ve teknik onay gereksinimi açık yazılır.",
            ],
        },
        {
            "phase": "teklif_veri_kontrolu",
            "actions": [
                "Tedarikçi teklifleri aynı para birimi, KDV, nakliye, teslim yeri ve miktar zeminiyle normalize edilir.",
                "Eksik fiyat, stok, termin, garanti, ödeme ve belge alanları bayraklanır.",
            ],
        },
        {
            "phase": "karar_matrisi",
            "actions": [
                "Fiyat, termin, teknik uygunluk, stok teyidi, garanti ve ticari risk ayrı skorlanır.",
                "En ucuz teklif ile dengeli öneri ayrı gösterilir.",
            ],
        },
    ]
    if args.has_datasheets or args.job_type == "material_spec_comparison":
        phases.append(
            {
                "phase": "teknik_uygunluk",
                "actions": [
                    "Datasheet, sertifika ve test raporu değerleri şartname kriterleriyle eşleştirilir.",
                    "Eksik belge veya muadil ürün teknik onay bayrağı alır.",
                ],
            }
        )
    if args.has_stock_data or args.job_type == "stock_replenishment":
        phases.append(
            {
                "phase": "stok_termin",
                "actions": [
                    "Stok teyidi, lot, expiry, depo ve termin bilgisi kontrol edilir.",
                    "Kritik yol veya şantiye teslim riski rapora eklenir.",
                ],
            }
        )
    if args.needs_erp_route:
        phases.append(
            {
                "phase": "erp_pim_rotasi",
                "actions": [
                    "ERPNext/OpenBoxes/Akeneo/OpenPIM için aktarım alanları önerilir.",
                    "Satın alma ve teknik onay kararları kullanıcı yetkilisine bırakılır.",
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
            "Teknik uygunluk fiyat karşılaştırmasından önce netleştirilmeli.",
            "Para birimi, fiyat geçerliliği, KDV/nakliye dahil-hariç ve teslim yeri açık olmalı.",
            "Eksik sertifika, test raporu veya datasheet kritik bayrak almalı.",
            "Stok ve termin yazılı teklif/teyit olmadan kesin kabul edilmemeli.",
            "Satın alma, sözleşme, ödeme ve muadil ürün onayı yetkili onay gerektirir.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-type", choices=sorted(ROUTES), default="supplier_quote_comparison")
    parser.add_argument("--has-datasheets", action="store_true")
    parser.add_argument("--has-stock-data", action="store_true")
    parser.add_argument("--needs-erp-route", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_plan(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
