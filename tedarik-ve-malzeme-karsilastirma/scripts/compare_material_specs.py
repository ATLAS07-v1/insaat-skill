#!/usr/bin/env python3
"""Compare offered material attributes against technical requirements."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, str):
        value = value.replace("%", "").replace(" ", "").replace(",", ".")
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_payload(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit("Girdi JSON nesne olmalıdır.")
    return data


def values_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip().lower() for item in value]
    return [str(value).strip().lower()]


def check_requirement(requirement: dict[str, Any], attributes: dict[str, Any]) -> dict[str, Any]:
    attribute = str(requirement.get("attribute") or "").strip()
    offered = attributes.get(attribute)
    status = "pass"
    detail = ""
    if offered in (None, ""):
        return {"attribute": attribute, "status": "missing", "offered": offered, "detail": "Teklif/datasheet değeri yok."}
    offered_num = as_float(offered)
    min_value = as_float(requirement.get("min"))
    max_value = as_float(requirement.get("max"))
    expected_values = values_list(requirement.get("required_values") or requirement.get("equals") or requirement.get("value"))
    if min_value is not None:
        if offered_num is None or offered_num < min_value:
            status = "fail"
            detail = f"Minimum {min_value} beklenir."
    if status == "pass" and max_value is not None:
        if offered_num is None or offered_num > max_value:
            status = "fail"
            detail = f"Maksimum {max_value} beklenir."
    if status == "pass" and expected_values:
        offered_values = values_list(offered)
        missing = [value for value in expected_values if value not in offered_values]
        if missing:
            status = "fail"
            detail = "Eksik/uyuşmayan değer: " + ", ".join(missing)
    if status == "pass" and requirement.get("requires_approval"):
        status = "needs_approval"
        detail = "Muadil veya teknik yorum onayı gerekir."
    return {
        "attribute": attribute,
        "status": status,
        "offered": offered,
        "required": {key: requirement.get(key) for key in ("min", "max", "required_values", "equals", "value", "unit") if requirement.get(key) is not None},
        "detail": detail,
    }


def compare(payload: dict[str, Any]) -> dict[str, Any]:
    requirements = [item for item in payload.get("requirements", []) if isinstance(item, dict)]
    results = []
    for offer in payload.get("offers", []):
        if not isinstance(offer, dict):
            continue
        attributes = offer.get("attributes", {}) if isinstance(offer.get("attributes"), dict) else {}
        checks = [check_requirement(req, attributes) for req in requirements]
        pass_count = sum(1 for check in checks if check["status"] == "pass")
        fail_count = sum(1 for check in checks if check["status"] == "fail")
        missing_count = sum(1 for check in checks if check["status"] == "missing")
        approval_count = sum(1 for check in checks if check["status"] == "needs_approval")
        total = len(checks) or 1
        score = max(0.0, (pass_count * 10 + approval_count * 5 - fail_count * 4 - missing_count * 2) / total)
        risk_flags = []
        if fail_count:
            risk_flags.append("technical_fail")
        if missing_count:
            risk_flags.append("missing_datasheet_values")
        if approval_count:
            risk_flags.append("technical_approval_required")
        if not offer.get("datasheet_ref"):
            risk_flags.append("datasheet_reference_missing")
        if payload.get("required_certificates"):
            offered_certs = values_list(offer.get("certificates"))
            missing_certs = [cert for cert in values_list(payload.get("required_certificates")) if cert not in offered_certs]
            if missing_certs:
                risk_flags.append("missing_certificates:" + ",".join(missing_certs))
        results.append(
            {
                "supplier": str(offer.get("supplier") or ""),
                "product": str(offer.get("product") or offer.get("model") or ""),
                "score": round(min(score, 10.0), 2),
                "status": "fail" if fail_count else ("needs_approval" if approval_count or missing_count else "pass"),
                "checks": checks,
                "risk_flags": risk_flags,
            }
        )
    results.sort(key=lambda row: row["score"], reverse=True)
    return {"summary": {"offer_count": len(results), "requirement_count": len(requirements)}, "results": results}


def to_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Malzeme Teknik Uygunluk Karşılaştırması",
        "",
        "| Sıra | Tedarikçi | Ürün | Skor | Durum | Risk |",
        "|---|---|---|---:|---|---|",
    ]
    for index, item in enumerate(payload["results"], start=1):
        risks = ", ".join(item["risk_flags"]) or "-"
        lines.append(f"| {index} | {item['supplier']} | {item['product']} | {item['score']} | {item['status']} | {risks} |")
    lines.extend(["", "## Onay Sınırı", "", "Bu çıktı datasheet/teklif verisiyle teknik ön kontroldür; ürün onayı için teknik sorumlu, numune ve belge doğrulaması gerekir."])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Malzeme teknik karşılaştırma JSON dosyası")
    parser.add_argument("--output", help="Çıktı dosyası")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    payload = compare(load_payload(Path(args.input)))
    rendered = to_markdown(payload) if args.format == "markdown" else json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
