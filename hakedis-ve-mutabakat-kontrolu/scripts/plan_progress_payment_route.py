#!/usr/bin/env python3
"""Create a route for progress payment and reconciliation tasks."""

from __future__ import annotations

import argparse
import json
from typing import Any


ROUTES: dict[str, dict[str, Any]] = {
    "main_contract_progress": {
        "goal": "Ana sözleşme hakedişini önceki/cari/kümülatif miktar ve kesintilerle kontrol etmek.",
        "tools": ["calculate_progress_payment.py", "compare_progress_sources.py", "BOQ table"],
        "outputs": ["hakediş icmali", "kalem bazlı farklar", "kesinti özeti"],
    },
    "subcontractor_progress": {
        "goal": "Taşeron hakedişini sözleşme, metraj, fatura ve ödeme kayıtlarıyla karşılaştırmak.",
        "tools": ["calculate_progress_payment.py", "supplier invoice register", "payment register"],
        "outputs": ["taşeron mutabakatı", "eksik fatura/ödeme", "kesinti listesi"],
    },
    "invoice_payment_reconciliation": {
        "goal": "Fatura kayıtları ile ödeme/banka/ERP kayıtlarını mutabık hale getirmek.",
        "tools": ["compare_progress_sources.py", "ERPNext/Mint/Settler route", "Beancount/Ledger optional"],
        "outputs": ["fatura-ödeme farkı", "fazla/eksik ödeme", "belge referans listesi"],
    },
    "quantity_reconciliation": {
        "goal": "Metraj, BOQ, BIM quantity ve hakediş miktarlarını karşılaştırmak.",
        "tools": ["metraj-ve-mahal-kontrolu", "IfcOpenShell Ifc5D", "compare_progress_sources.py"],
        "outputs": ["miktar fark tablosu", "sözleşme üstü miktar", "ölçüm kuralı bayrakları"],
    },
    "variation_final_account": {
        "goal": "Variation/fiyat farkı/kesin hesap kalemlerini hakedişle ilişkilendirmek.",
        "tools": ["delta BOQ", "source revision trace", "calculate_progress_payment.py"],
        "outputs": ["artı/eksi hesap", "onay referansı eksikleri", "kesin hesap farkları"],
    },
}


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    route = ROUTES[args.job_type]
    phases = [
        {
            "phase": "kaynak_derleme",
            "actions": [
                "Sözleşme BOQ, önceki hakediş, cari ölçüm, onaylı metraj, fatura ve ödeme kaynakları ayrılır.",
                "Dönem, hakediş no, para birimi, KDV/vergi ve kesinti varsayımları yazılır.",
            ],
        },
        {
            "phase": "hesap_normalizasyonu",
            "actions": [
                "Kalemler kod, birim, sözleşme miktarı, önceki miktar, cari onaylı miktar ve birim fiyat alanlarına taşınır.",
                "Kümülatif miktar ve cari brüt tutar yeniden hesaplanır.",
            ],
        },
        {
            "phase": "mutabakat_qa",
            "actions": [
                "Hakediş, fatura, ödeme ve metraj kaynakları toleransla karşılaştırılır.",
                "Sözleşme üstü miktar, fazla ödeme, eksik fatura, duplicate kod ve kesinti farkı bayraklanır.",
            ],
        },
    ]
    if args.has_ifc or args.job_type == "quantity_reconciliation":
        phases.append(
            {
                "phase": "bim_5d_quantity",
                "actions": [
                    "IFC/5D quantity kaynakları BIM/metraj skill'leri ile doğrulanır.",
                    "Model quantity, hakediş ölçüm kuralıyla aynı değilse nihai mutabakat yapılmaz.",
                ],
            }
        )
    if args.has_erp or args.job_type == "invoice_payment_reconciliation":
        phases.append(
            {
                "phase": "erp_odeme_mutabakati",
                "actions": [
                    "ERPNext/Mint/Settler rotasıyla fatura, ödeme ve banka referansları eşleştirilir.",
                    "Ödeme kaydı belge/dekont referansı olmadan kapalı kabul edilmez.",
                ],
            }
        )
    if args.needs_xlsx:
        phases.append(
            {
                "phase": "xlsx_ods_cikti",
                "actions": [
                    "XLSX/ODS çıktı üretilirken formül sonuçları Python yeniden hesaplamasıyla kontrol edilir.",
                    "Gizli satır/sütun ve manuel formül değişikliği riski raporlanır.",
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
            "Sözleşme, önceki hakediş ve cari hakediş aynı kod/birim sistemine normalize edilmeli.",
            "Kümülatif miktar önceki miktardan düşükse açıklama gerekir.",
            "Sözleşme üstü miktar variation/onay olmadan kapatılmamalı.",
            "Fatura ve ödeme kayıtları belge numarası, tarih, taraf ve para birimiyle izlenebilir olmalı.",
            "Vergi, KDV, stopaj, teminat ve ödeme onayı yetkili ticari/muhasebe onayı gerektirir.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-type", choices=sorted(ROUTES), default="main_contract_progress")
    parser.add_argument("--has-ifc", action="store_true")
    parser.add_argument("--has-erp", action="store_true")
    parser.add_argument("--needs-xlsx", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_plan(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
