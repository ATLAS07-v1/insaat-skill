#!/usr/bin/env python3
"""Build a construction cost table from JSON items and markup assumptions."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_payload(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, list):
        return {"items": data}
    if not isinstance(data, dict):
        raise SystemExit("Girdi JSON nesne veya liste olmalıdır.")
    return data


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


def normalize_item(raw: dict[str, Any], default_currency: str, index: int) -> dict[str, Any]:
    quantity = as_float(raw.get("quantity") or raw.get("qty"))
    unit_price = as_float(raw.get("unit_price") or raw.get("rate") or raw.get("price"))
    waste_percent = as_float(raw.get("waste_percent") or raw.get("waste") or raw.get("fire_percent"))
    adjusted_quantity = quantity * (1.0 + waste_percent / 100.0)
    line_total = adjusted_quantity * unit_price
    code = str(raw.get("code") or raw.get("poz") or raw.get("item_code") or f"ITEM-{index:03d}").strip()
    category = str(raw.get("category") or raw.get("trade") or "Genel").strip()
    item = {
        "code": code,
        "description": str(raw.get("description") or raw.get("name") or "").strip(),
        "category": category,
        "quantity": round(quantity, 6),
        "unit": str(raw.get("unit") or "").strip(),
        "unit_price": round(unit_price, 6),
        "waste_percent": round(waste_percent, 4),
        "adjusted_quantity": round(adjusted_quantity, 6),
        "line_total": round(line_total, 2),
        "currency": str(raw.get("currency") or default_currency).strip(),
        "source": str(raw.get("source") or "").strip(),
        "notes": str(raw.get("notes") or "").strip(),
    }
    return item


def build_cost(payload: dict[str, Any]) -> dict[str, Any]:
    default_currency = str(payload.get("currency") or "TRY").strip()
    items = [
        normalize_item(raw, default_currency, index)
        for index, raw in enumerate(payload.get("items", []), start=1)
        if isinstance(raw, dict)
    ]
    direct_total = sum(item["line_total"] for item in items)
    markups = payload.get("markups", {}) if isinstance(payload.get("markups"), dict) else {}
    overhead_amount = direct_total * pct(markups, "overhead_percent")
    profit_amount = direct_total * pct(markups, "profit_percent")
    contingency_amount = direct_total * pct(markups, "contingency_percent")
    subtotal = direct_total + overhead_amount + profit_amount + contingency_amount
    discount_amount = subtotal * pct(markups, "discount_percent")
    subtotal_before_tax = subtotal - discount_amount
    vat_amount = subtotal_before_tax * pct(markups, "vat_percent")
    grand_total = subtotal_before_tax + vat_amount
    category_totals: dict[str, float] = defaultdict(float)
    for item in items:
        category_totals[item["category"]] += item["line_total"]
    return {
        "metadata": {
            "project": payload.get("project") or payload.get("name") or "Unnamed project",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "concept_only": True,
            "price_validity": payload.get("price_validity") or "",
        },
        "items": items,
        "category_totals": {key: round(value, 2) for key, value in sorted(category_totals.items())},
        "summary": {
            "direct_total": round(direct_total, 2),
            "overhead_amount": round(overhead_amount, 2),
            "profit_amount": round(profit_amount, 2),
            "contingency_amount": round(contingency_amount, 2),
            "discount_amount": round(discount_amount, 2),
            "subtotal_before_tax": round(subtotal_before_tax, 2),
            "vat_amount": round(vat_amount, 2),
            "grand_total": round(grand_total, 2),
            "currency": default_currency,
            "markup_percentages": {
                "overhead_percent": as_float(markups.get("overhead_percent")),
                "profit_percent": as_float(markups.get("profit_percent")),
                "contingency_percent": as_float(markups.get("contingency_percent")),
                "discount_percent": as_float(markups.get("discount_percent")),
                "vat_percent": as_float(markups.get("vat_percent")),
            },
        },
        "qa_flags": infer_flags(items, default_currency),
    }


def infer_flags(items: list[dict[str, Any]], default_currency: str) -> list[dict[str, Any]]:
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
        if item["quantity"] <= 0:
            flags.append({"type": "non_positive_quantity", "severity": "high", "item": code})
        if not item["unit"]:
            flags.append({"type": "missing_unit", "severity": "high", "item": code})
        if item["unit_price"] <= 0:
            flags.append({"type": "non_positive_unit_price", "severity": "high", "item": code})
        if item["waste_percent"] > 25:
            flags.append({"type": "high_waste_percent", "severity": "medium", "item": code, "value": item["waste_percent"]})
        if not item["source"]:
            flags.append({"type": "missing_price_source", "severity": "medium", "item": code})
        if item["currency"] != default_currency:
            flags.append({"type": "item_currency_differs", "severity": "high", "item": code, "currency": item["currency"]})
    return flags


def to_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Teklif / Maliyet Özeti",
        "",
        f"- Proje: {payload['metadata']['project']}",
        f"- Para birimi: {summary['currency']}",
        f"- Direkt toplam: {summary['direct_total']:.2f}",
        f"- Genel toplam: {summary['grand_total']:.2f}",
        "",
        "## Kalemler",
        "",
        "| Kod | Açıklama | Kategori | Miktar | Birim | Birim Fiyat | Fire % | Toplam |",
        "|---|---|---|---:|---|---:|---:|---:|",
    ]
    for item in payload["items"]:
        desc = item["description"].replace("|", "\\|")
        lines.append(
            f"| {item['code']} | {desc} | {item['category']} | {item['quantity']} | {item['unit']} | "
            f"{item['unit_price']:.2f} | {item['waste_percent']:.2f} | {item['line_total']:.2f} |"
        )
    lines.extend(["", "## Markup ve Vergi", ""])
    for key in ["overhead_amount", "profit_amount", "contingency_amount", "discount_amount", "subtotal_before_tax", "vat_amount", "grand_total"]:
        lines.append(f"- {key}: {summary[key]:.2f} {summary['currency']}")
    if payload["qa_flags"]:
        lines.extend(["", "## QA Bayrakları", ""])
        for flag in payload["qa_flags"]:
            lines.append(f"- {flag['severity']}: {flag['type']} {flag.get('item', '')}".strip())
    lines.extend(["", "## Onay Sınırı", "", "Bu çıktı taslak maliyet modelidir; güncel fiyat, vergi, kur, sözleşme ve ticari onay ayrıca doğrulanmalıdır."])
    return "\n".join(lines)


def write_csv(payload: dict[str, Any], path: Path) -> None:
    fieldnames = ["code", "description", "category", "quantity", "unit", "unit_price", "waste_percent", "adjusted_quantity", "line_total", "currency", "source", "notes"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows({key: item.get(key, "") for key in fieldnames} for item in payload["items"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Maliyet girdi JSON dosyası")
    parser.add_argument("--output", help="Çıktı dosyası")
    parser.add_argument("--format", choices=["json", "markdown", "csv"], default="json")
    args = parser.parse_args()
    payload = build_cost(load_payload(Path(args.input)))
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
