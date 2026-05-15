#!/usr/bin/env python3
"""Compare two progress payment, invoice, payment, or quantity sources by key."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
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


def load_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            for key in ("items", "rows", "records", "invoices", "payments"):
                if isinstance(data.get(key), list):
                    return data[key]
            return [data]
        if isinstance(data, list):
            return data
        raise SystemExit("JSON içinde liste veya bilinen kayıt alanı beklenir.")
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    raise SystemExit("Desteklenen dosya türleri: .json, .csv")


def norm_key(value: Any) -> str:
    return str(value or "").strip().upper()


def get(row: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def aggregate(rows: list[dict[str, Any]], key_field: str, quantity_fields: list[str], amount_fields: list[str]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    duplicate_count: defaultdict[str, int] = defaultdict(int)
    for index, row in enumerate(rows, start=1):
        key = norm_key(row.get(key_field) or get(row, "code", "document_no", "invoice_no", "payment_ref"))
        if not key:
            key = f"ROW-{index}"
        duplicate_count[key] += 1
        if key not in grouped:
            grouped[key] = {"key": key, "quantity": 0.0, "amount": 0.0, "currency": str(get(row, "currency") or "").strip(), "rows": []}
        grouped[key]["quantity"] += as_float(get(row, *quantity_fields))
        grouped[key]["amount"] += as_float(get(row, *amount_fields))
        grouped[key]["rows"].append(index)
        currency = str(get(row, "currency") or "").strip()
        if currency and grouped[key]["currency"] and currency != grouped[key]["currency"]:
            grouped[key]["currency"] = "MIXED"
        elif currency:
            grouped[key]["currency"] = currency
    for key, count in duplicate_count.items():
        grouped[key]["duplicate_count"] = count
    return grouped


def compare(args: argparse.Namespace) -> dict[str, Any]:
    quantity_fields = [field.strip() for field in args.quantity_fields.split(",") if field.strip()]
    compare_quantity = bool(quantity_fields) and [field.lower() for field in quantity_fields] != ["none"]
    if not compare_quantity:
        quantity_fields = []
    amount_fields = [field.strip() for field in args.amount_fields.split(",") if field.strip()]
    source_a = aggregate(load_rows(Path(args.source_a)), args.key_field, quantity_fields, amount_fields)
    source_b = aggregate(load_rows(Path(args.source_b)), args.key_field, quantity_fields, amount_fields)
    issues: list[dict[str, Any]] = []
    matches = []
    for key in sorted(set(source_a) | set(source_b)):
        a = source_a.get(key)
        b = source_b.get(key)
        if a is None:
            issues.append({"type": "missing_in_source_a", "key": key, "source_b_amount": round(b["amount"], 2) if b else 0})
            continue
        if b is None:
            issues.append({"type": "missing_in_source_b", "key": key, "source_a_amount": round(a["amount"], 2)})
            continue
        delta_quantity = a["quantity"] - b["quantity"]
        delta_amount = a["amount"] - b["amount"]
        key_issues = []
        if compare_quantity and abs(delta_quantity) > args.quantity_tolerance:
            key_issues.append("quantity_mismatch")
            issues.append({"type": "quantity_mismatch", "key": key, "source_a_quantity": round(a["quantity"], 6), "source_b_quantity": round(b["quantity"], 6), "delta_quantity": round(delta_quantity, 6)})
        if abs(delta_amount) > args.amount_tolerance:
            key_issues.append("amount_mismatch")
            issues.append({"type": "amount_mismatch", "key": key, "source_a_amount": round(a["amount"], 2), "source_b_amount": round(b["amount"], 2), "delta_amount": round(delta_amount, 2)})
        if a.get("currency") and b.get("currency") and a["currency"] != b["currency"]:
            key_issues.append("currency_mismatch")
            issues.append({"type": "currency_mismatch", "key": key, "source_a_currency": a["currency"], "source_b_currency": b["currency"]})
        if a.get("duplicate_count", 1) > 1:
            issues.append({"type": "duplicate_key_source_a", "key": key, "count": a["duplicate_count"]})
        if b.get("duplicate_count", 1) > 1:
            issues.append({"type": "duplicate_key_source_b", "key": key, "count": b["duplicate_count"]})
        matches.append(
            {
                "key": key,
                "source_a_quantity": round(a["quantity"], 6),
                "source_b_quantity": round(b["quantity"], 6),
                "source_a_amount": round(a["amount"], 2),
                "source_b_amount": round(b["amount"], 2),
                "status": "issue" if key_issues else "matched",
            }
        )
    return {
        "summary": {
            "source_a_count": len(source_a),
            "source_b_count": len(source_b),
            "matched_count": sum(1 for item in matches if item["status"] == "matched"),
            "issue_count": len(issues),
        },
        "matches": matches,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-a", required=True)
    parser.add_argument("--source-b", required=True)
    parser.add_argument("--key-field", default="code")
    parser.add_argument("--quantity-fields", default="approved_current_quantity,current_quantity,quantity")
    parser.add_argument("--amount-fields", default="current_amount,amount,total,line_total")
    parser.add_argument("--quantity-tolerance", type=float, default=0.0001)
    parser.add_argument("--amount-tolerance", type=float, default=0.01)
    parser.add_argument("--output", help="JSON çıktı dosyası")
    args = parser.parse_args()
    payload = compare(args)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
