#!/usr/bin/env python3
"""Validate construction cost tables in JSON or CSV form."""

from __future__ import annotations

import argparse
import csv
import json
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
        if isinstance(data, dict) and isinstance(data.get("items"), list):
            return data["items"]
        if isinstance(data, list):
            return data
        raise SystemExit("JSON içinde `items` listesi veya doğrudan liste beklenir.")
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    raise SystemExit("Desteklenen dosya türleri: .json, .csv")


def get(row: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def validate(rows: list[dict[str, Any]], tolerance: float, waste_warning: float) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    seen: set[str] = set()
    currencies: set[str] = set()
    direct_total = 0.0
    for index, row in enumerate(rows, start=1):
        code = str(get(row, "code", "poz", "item_code") or f"ROW-{index}").strip()
        desc = str(get(row, "description", "name") or "").strip()
        quantity = as_float(get(row, "quantity", "qty"))
        unit = str(get(row, "unit") or "").strip()
        unit_price = as_float(get(row, "unit_price", "rate", "price"))
        waste_percent = as_float(get(row, "waste_percent", "waste", "fire_percent"))
        line_total = as_float(get(row, "line_total", "total", "amount"))
        expected_total = quantity * (1.0 + waste_percent / 100.0) * unit_price
        currency = str(get(row, "currency") or "").strip()
        if currency:
            currencies.add(currency)
        if code in seen:
            issues.append({"type": "duplicate_code", "severity": "high", "row": index, "code": code})
        seen.add(code)
        if not desc:
            issues.append({"type": "missing_description", "severity": "medium", "row": index, "code": code})
        if quantity <= 0:
            issues.append({"type": "non_positive_quantity", "severity": "high", "row": index, "code": code, "value": quantity})
        if not unit:
            issues.append({"type": "missing_unit", "severity": "high", "row": index, "code": code})
        if unit_price <= 0:
            issues.append({"type": "non_positive_unit_price", "severity": "high", "row": index, "code": code, "value": unit_price})
        if waste_percent > waste_warning:
            issues.append({"type": "high_waste_percent", "severity": "medium", "row": index, "code": code, "value": waste_percent})
        if not get(row, "source"):
            issues.append({"type": "missing_price_source", "severity": "medium", "row": index, "code": code})
        if line_total and abs(line_total - expected_total) > tolerance:
            issues.append(
                {
                    "type": "line_total_mismatch",
                    "severity": "high",
                    "row": index,
                    "code": code,
                    "expected": round(expected_total, 2),
                    "actual": round(line_total, 2),
                }
            )
        direct_total += expected_total
    if len(currencies) > 1:
        issues.append({"type": "mixed_currency", "severity": "high", "currencies": sorted(currencies)})
    return {
        "summary": {
            "row_count": len(rows),
            "issue_count": len(issues),
            "direct_total_recalculated": round(direct_total, 2),
            "currencies": sorted(currencies),
        },
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("table", help="JSON veya CSV maliyet tablosu")
    parser.add_argument("--tolerance", type=float, default=0.01)
    parser.add_argument("--waste-warning", type=float, default=25.0)
    parser.add_argument("--output", help="JSON çıktı dosyası")
    args = parser.parse_args()
    payload = validate(load_rows(Path(args.table)), args.tolerance, args.waste_warning)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
