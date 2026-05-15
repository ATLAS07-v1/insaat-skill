#!/usr/bin/env python3
"""Compare supplier quotes by price, lead time, compliance, warranty, stock and risks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PASS_VALUES = {"pass", "passed", "uygun", "ok", "compliant", "true", "evet"}
FAIL_VALUES = {"fail", "failed", "uygunsuz", "nok", "noncompliant", "false", "hayır"}
CONDITIONAL_VALUES = {"conditional", "partial", "kısmi", "needs_approval", "review"}


def as_float(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    if isinstance(value, str):
        value = value.replace("%", "").replace(" ", "").replace(",", ".")
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def load_payload(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit("Girdi JSON nesne olmalıdır.")
    return data


def technical_score(status: Any) -> tuple[float, str]:
    text = str(status or "").strip().lower()
    if text in PASS_VALUES:
        return 10.0, "pass"
    if text in FAIL_VALUES:
        return 0.0, "fail"
    if text in CONDITIONAL_VALUES:
        return 5.0, "needs_approval"
    return 4.0, "unknown"


def quote_total(quote: dict[str, Any], required_items: dict[str, dict[str, Any]], default_currency: str) -> dict[str, Any]:
    items = []
    risk_flags: list[str] = []
    total = 0.0
    technical_scores = []
    lead_times = []
    currency = str(quote.get("currency") or default_currency).strip()
    quote_items = quote.get("items", []) if isinstance(quote.get("items"), list) else []
    seen_codes = set()
    for raw in quote_items:
        if not isinstance(raw, dict):
            continue
        code = str(raw.get("code") or raw.get("item_code") or "").strip()
        seen_codes.add(code)
        required = required_items.get(code, {})
        quantity = as_float(raw.get("quantity"), as_float(required.get("quantity"), 1.0))
        unit_price = as_float(raw.get("unit_price") or raw.get("price") or raw.get("rate"))
        line_total = quantity * unit_price
        total += line_total
        score, status = technical_score(raw.get("technical_status") or raw.get("compliance_status"))
        technical_scores.append(score)
        lead_time = as_float(raw.get("lead_time_days") or quote.get("lead_time_days"))
        if lead_time > 0:
            lead_times.append(lead_time)
        if unit_price <= 0:
            risk_flags.append(f"{code}:missing_or_zero_price")
        if status == "fail":
            risk_flags.append(f"{code}:technical_fail")
        if status in {"needs_approval", "unknown"}:
            risk_flags.append(f"{code}:technical_review")
        if not raw.get("brand") and not quote.get("brand"):
            risk_flags.append(f"{code}:brand_model_missing")
        if required.get("unit") and raw.get("unit") and str(required.get("unit")).lower() != str(raw.get("unit")).lower():
            risk_flags.append(f"{code}:unit_mismatch")
        items.append(
            {
                "code": code,
                "quantity": round(quantity, 6),
                "unit_price": round(unit_price, 4),
                "line_total": round(line_total, 2),
                "technical_status": status,
                "lead_time_days": lead_time,
            }
        )
    for code in required_items:
        if code not in seen_codes:
            risk_flags.append(f"{code}:missing_required_item")
    if quote.get("stock_confirmed") is not True:
        risk_flags.append("stock_not_confirmed")
    if not quote.get("price_valid_until"):
        risk_flags.append("price_validity_missing")
    if quote.get("exclusions"):
        risk_flags.append("commercial_exclusions")
    if currency != default_currency:
        risk_flags.append("currency_differs")
    return {
        "supplier": str(quote.get("supplier") or "Unnamed supplier"),
        "currency": currency,
        "items": items,
        "total_price": round(total + as_float(quote.get("delivery_cost")) + as_float(quote.get("extra_costs")), 2),
        "avg_technical_score": round(sum(technical_scores) / len(technical_scores), 2) if technical_scores else 0.0,
        "lead_time_days": round(max(lead_times), 2) if lead_times else as_float(quote.get("lead_time_days")),
        "warranty_months": as_float(quote.get("warranty_months")),
        "stock_confirmed": quote.get("stock_confirmed") is True,
        "payment_terms": str(quote.get("payment_terms") or ""),
        "risk_flags": sorted(set(risk_flags)),
    }


def score_quotes(payload: dict[str, Any]) -> dict[str, Any]:
    default_currency = str(payload.get("currency") or "TRY").strip()
    required_items = {
        str(item.get("code") or item.get("item_code") or "").strip(): item
        for item in payload.get("items", [])
        if isinstance(item, dict) and (item.get("code") or item.get("item_code"))
    }
    evaluated = [
        quote_total(quote, required_items, default_currency)
        for quote in payload.get("quotes", [])
        if isinstance(quote, dict)
    ]
    positive_prices = [item["total_price"] for item in evaluated if item["total_price"] > 0 and item["currency"] == default_currency]
    min_price = min(positive_prices) if positive_prices else 0.0
    lead_times = [item["lead_time_days"] for item in evaluated if item["lead_time_days"] > 0]
    min_lead = min(lead_times) if lead_times else 0.0
    ranking = []
    for item in evaluated:
        price_score = 0.0
        if min_price > 0 and item["total_price"] > 0 and item["currency"] == default_currency:
            price_score = min(10.0, (min_price / item["total_price"]) * 10.0)
        lead_score = 5.0
        if min_lead > 0 and item["lead_time_days"] > 0:
            lead_score = min(10.0, (min_lead / item["lead_time_days"]) * 10.0)
        stock_score = 10.0 if item["stock_confirmed"] else 4.0
        warranty_score = min(10.0, item["warranty_months"] / 24.0 * 10.0) if item["warranty_months"] else 3.0
        risk_penalty = min(3.0, len(item["risk_flags"]) * 0.35)
        weighted = price_score * 0.35 + item["avg_technical_score"] * 0.3 + lead_score * 0.15 + stock_score * 0.1 + warranty_score * 0.1 - risk_penalty
        note = "Dengeli teknik ve ticari aday."
        if any("technical_fail" in flag for flag in item["risk_flags"]):
            note = "Teknik uygunsuzluk var; satın alma öncesi elenmeli veya teknik onay gerekir."
        elif item["risk_flags"]:
            note = "Riskleri kapatılırsa değerlendirilebilir."
        ranking.append({**item, "score": round(max(weighted, 0.0), 2), "decision_note": note})
    ranking.sort(key=lambda row: row["score"], reverse=True)
    return {
        "summary": {
            "supplier_count": len(evaluated),
            "required_item_count": len(required_items),
            "currency": default_currency,
        },
        "ranking": ranking,
    }


def to_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Tedarikçi Teklif Karşılaştırması",
        "",
        "| Sıra | Tedarikçi | Skor | Toplam | Para | Termin | Teknik | Risk |",
        "|---|---|---:|---:|---|---:|---:|---|",
    ]
    for index, item in enumerate(payload["ranking"], start=1):
        risks = ", ".join(item["risk_flags"]) or "-"
        lines.append(
            f"| {index} | {item['supplier']} | {item['score']} | {item['total_price']:.2f} | {item['currency']} | "
            f"{item['lead_time_days']} | {item['avg_technical_score']} | {risks} |"
        )
    lines.extend(["", "## Onay Sınırı", "", "Bu çıktı satın alma öneri matrisi değildir; teknik, ticari, sözleşmesel ve ödeme onayı ayrıca gerekir."])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Tedarikçi teklif JSON dosyası")
    parser.add_argument("--output", help="Çıktı dosyası")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    payload = score_quotes(load_payload(Path(args.input)))
    rendered = to_markdown(payload) if args.format == "markdown" else json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
