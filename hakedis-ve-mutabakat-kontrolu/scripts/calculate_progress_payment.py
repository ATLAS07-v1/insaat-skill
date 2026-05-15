#!/usr/bin/env python3
"""Calculate a progress payment summary from contract and current quantities."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def as_float(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    if isinstance(value, str):
        value = value.replace("%", "").replace(" ", "").replace(",", ".")
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def pct(mapping: dict[str, Any], key: str) -> float:
    return as_float(mapping.get(key), 0.0) / 100.0


def load_payload(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        return {"items": data}
    if not isinstance(data, dict):
        raise SystemExit("Girdi JSON nesne veya liste olmalıdır.")
    return data


def normalize_item(raw: dict[str, Any], index: int, default_currency: str) -> dict[str, Any]:
    code = str(raw.get("code") or raw.get("poz") or raw.get("item_code") or f"ITEM-{index:03d}").strip()
    description = str(raw.get("description") or raw.get("name") or "").strip()
    unit = str(raw.get("unit") or "").strip()
    contract_quantity = as_float(raw.get("contract_quantity") or raw.get("contract_qty"))
    unit_price = as_float(raw.get("unit_price") or raw.get("rate") or raw.get("price"))
    previous_quantity = as_float(raw.get("previous_quantity") or raw.get("previous_qty"))
    current_quantity = as_float(raw.get("current_quantity") or raw.get("current_qty"))
    approved_value = raw.get("approved_current_quantity")
    approved_current_quantity = as_float(approved_value, current_quantity)
    cumulative_quantity = previous_quantity + approved_current_quantity
    provided_cumulative = raw.get("cumulative_quantity")
    previous_amount = previous_quantity * unit_price
    current_amount = approved_current_quantity * unit_price
    cumulative_amount = cumulative_quantity * unit_price
    item = {
        "code": code,
        "description": description,
        "category": str(raw.get("category") or "Genel").strip(),
        "unit": unit,
        "contract_quantity": round(contract_quantity, 6),
        "unit_price": round(unit_price, 6),
        "previous_quantity": round(previous_quantity, 6),
        "current_quantity": round(current_quantity, 6),
        "approved_current_quantity": round(approved_current_quantity, 6),
        "cumulative_quantity": round(cumulative_quantity, 6),
        "previous_amount": round(previous_amount, 2),
        "current_amount": round(current_amount, 2),
        "cumulative_amount": round(cumulative_amount, 2),
        "currency": str(raw.get("currency") or default_currency).strip(),
        "source": str(raw.get("source") or "").strip(),
        "notes": str(raw.get("notes") or "").strip(),
    }
    flags = []
    if approved_value in (None, ""):
        flags.append("approved_current_quantity_missing_used_current")
    if provided_cumulative not in (None, "") and abs(as_float(provided_cumulative) - cumulative_quantity) > 0.0001:
        flags.append("provided_cumulative_mismatch")
    item["flags"] = flags
    return item


def build_payment(payload: dict[str, Any]) -> dict[str, Any]:
    default_currency = str(payload.get("currency") or "TRY").strip()
    items = [
        normalize_item(raw, index, default_currency)
        for index, raw in enumerate(payload.get("items", []), start=1)
        if isinstance(raw, dict)
    ]
    current_gross = sum(item["current_amount"] for item in items)
    previous_gross = sum(item["previous_amount"] for item in items)
    cumulative_gross = sum(item["cumulative_amount"] for item in items)
    deductions = payload.get("deductions", {}) if isinstance(payload.get("deductions"), dict) else {}
    additions = payload.get("additions", {}) if isinstance(payload.get("additions"), dict) else {}
    retention_amount = current_gross * pct(deductions, "retention_percent") + as_float(deductions.get("retention_amount"))
    advance_recovery_amount = current_gross * pct(deductions, "advance_recovery_percent") + as_float(deductions.get("advance_recovery_amount"))
    other_deductions = as_float(deductions.get("other_deductions"))
    penalty_amount = as_float(deductions.get("penalty_amount"))
    withholding_amount = current_gross * pct(deductions, "withholding_percent") + as_float(deductions.get("withholding_amount"))
    price_escalation_amount = as_float(additions.get("price_escalation_amount"))
    variation_addition_amount = as_float(additions.get("variation_addition_amount"))
    net_before_tax = current_gross + price_escalation_amount + variation_addition_amount - retention_amount - advance_recovery_amount - other_deductions - penalty_amount - withholding_amount
    vat_amount = net_before_tax * pct(deductions, "vat_percent")
    payable_current = net_before_tax + vat_amount
    category_totals: dict[str, float] = defaultdict(float)
    for item in items:
        category_totals[item["category"]] += item["current_amount"]
    return {
        "metadata": {
            "project": payload.get("project") or "Unnamed project",
            "payment_no": payload.get("payment_no") or "",
            "period": payload.get("period") or "",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "control_output_only": True,
        },
        "items": items,
        "category_current_totals": {key: round(value, 2) for key, value in sorted(category_totals.items())},
        "summary": {
            "previous_gross": round(previous_gross, 2),
            "current_gross": round(current_gross, 2),
            "cumulative_gross": round(cumulative_gross, 2),
            "retention_amount": round(retention_amount, 2),
            "advance_recovery_amount": round(advance_recovery_amount, 2),
            "other_deductions": round(other_deductions, 2),
            "penalty_amount": round(penalty_amount, 2),
            "withholding_amount": round(withholding_amount, 2),
            "price_escalation_amount": round(price_escalation_amount, 2),
            "variation_addition_amount": round(variation_addition_amount, 2),
            "net_before_tax": round(net_before_tax, 2),
            "vat_amount": round(vat_amount, 2),
            "payable_current": round(payable_current, 2),
            "currency": default_currency,
        },
        "qa_flags": infer_flags(items, default_currency, payload, payable_current),
    }


def infer_flags(items: list[dict[str, Any]], default_currency: str, payload: dict[str, Any], payable_current: float) -> list[dict[str, Any]]:
    flags: list[dict[str, Any]] = []
    seen: set[str] = set()
    currencies = {item["currency"] for item in items if item["currency"]}
    if len(currencies) > 1:
        flags.append({"type": "mixed_currency", "severity": "high", "detail": ", ".join(sorted(currencies))})
    for item in items:
        code = item["code"]
        if code in seen:
            flags.append({"type": "duplicate_code", "severity": "high", "item": code})
        seen.add(code)
        if not item["description"]:
            flags.append({"type": "missing_description", "severity": "medium", "item": code})
        if not item["unit"]:
            flags.append({"type": "missing_unit", "severity": "high", "item": code})
        if item["unit_price"] <= 0:
            flags.append({"type": "non_positive_unit_price", "severity": "high", "item": code})
        if item["current_quantity"] < 0 or item["approved_current_quantity"] < 0:
            flags.append({"type": "negative_current_quantity", "severity": "high", "item": code})
        if item["cumulative_quantity"] < item["previous_quantity"]:
            flags.append({"type": "cumulative_less_than_previous", "severity": "high", "item": code})
        if item["contract_quantity"] > 0 and item["cumulative_quantity"] > item["contract_quantity"]:
            flags.append({"type": "over_contract_quantity", "severity": "high", "item": code, "over_qty": round(item["cumulative_quantity"] - item["contract_quantity"], 6)})
        if not item["source"]:
            flags.append({"type": "missing_measurement_source", "severity": "medium", "item": code})
        for item_flag in item.get("flags", []):
            flags.append({"type": item_flag, "severity": "medium", "item": code})
        if item["currency"] != default_currency:
            flags.append({"type": "item_currency_differs", "severity": "high", "item": code, "currency": item["currency"]})
    expected_payable = payload.get("expected_payable_current")
    if expected_payable not in (None, ""):
        delta = payable_current - as_float(expected_payable)
        if abs(delta) > 0.01:
            flags.append({"type": "payable_current_mismatch", "severity": "high", "expected": round(as_float(expected_payable), 2), "actual": round(payable_current, 2), "delta": round(delta, 2)})
    return flags


def to_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Hakediş / Mutabakat Özeti",
        "",
        f"- Proje: {payload['metadata']['project']}",
        f"- Hakediş no: {payload['metadata']['payment_no']}",
        f"- Para birimi: {summary['currency']}",
        f"- Cari brüt: {summary['current_gross']:.2f}",
        f"- Net ödenecek kontrol tutarı: {summary['payable_current']:.2f}",
        "",
        "## Kalemler",
        "",
        "| Kod | Açıklama | Birim | Sözleşme Miktarı | Önceki | Cari Onaylı | Kümülatif | Cari Tutar |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for item in payload["items"]:
        desc = item["description"].replace("|", "\\|")
        lines.append(
            f"| {item['code']} | {desc} | {item['unit']} | {item['contract_quantity']} | {item['previous_quantity']} | "
            f"{item['approved_current_quantity']} | {item['cumulative_quantity']} | {item['current_amount']:.2f} |"
        )
    lines.extend(["", "## Kesinti ve Vergi", ""])
    for key in ["retention_amount", "advance_recovery_amount", "other_deductions", "penalty_amount", "withholding_amount", "price_escalation_amount", "variation_addition_amount", "net_before_tax", "vat_amount", "payable_current"]:
        lines.append(f"- {key}: {summary[key]:.2f} {summary['currency']}")
    if payload["qa_flags"]:
        lines.extend(["", "## QA Bayrakları", ""])
        for flag in payload["qa_flags"]:
            lines.append(f"- {flag['severity']}: {flag['type']} {flag.get('item', '')}".strip())
    lines.extend(["", "## Onay Sınırı", "", "Bu çıktı hakediş kontrol modelidir; resmi ödeme, vergi, kesinti ve sözleşme onayı yerine geçmez."])
    return "\n".join(lines)


def write_csv(payload: dict[str, Any], path: Path) -> None:
    fieldnames = ["code", "description", "category", "unit", "contract_quantity", "unit_price", "previous_quantity", "current_quantity", "approved_current_quantity", "cumulative_quantity", "previous_amount", "current_amount", "cumulative_amount", "currency", "source", "notes"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows({key: item.get(key, "") for key in fieldnames} for item in payload["items"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Hakediş girdi JSON dosyası")
    parser.add_argument("--output", help="Çıktı dosyası")
    parser.add_argument("--format", choices=["json", "markdown", "csv"], default="json")
    args = parser.parse_args()
    payload = build_payment(load_payload(Path(args.input)))
    if args.format == "csv":
        if not args.output:
            raise SystemExit("CSV formatı için --output gereklidir.")
        write_csv(payload, Path(args.output))
        return 0
    rendered = to_markdown(payload) if args.format == "markdown" else json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
