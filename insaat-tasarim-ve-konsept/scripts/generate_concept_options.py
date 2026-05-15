#!/usr/bin/env python3
"""Generate early construction design concept options from a JSON brief."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


OPTION_LIBRARY = [
    {
        "id": "OPT-01",
        "name": "Compact Block",
        "family": "compact_block",
        "footprint_factor": 1.0,
        "concept": "Kompakt, ekonomik ve hızlı uygulanabilir kütle.",
        "strengths": ["basit taşıyıcı düzen", "düşük cephe karmaşıklığı", "kolay fazlama"],
        "risks": ["derin planlarda gün ışığı zayıflayabilir", "cephe karakteri tekdüze kalabilir"],
        "tool_route": ["FreeCAD", "Blender"],
    },
    {
        "id": "OPT-02",
        "name": "Courtyard Block",
        "family": "courtyard",
        "footprint_factor": 1.18,
        "concept": "İç avlu etrafında sosyal açık alan ve gün ışığı odaklı kurgu.",
        "strengths": ["güçlü ortak alan", "doğal ışık ve yönlenme potansiyeli", "korunaklı açık alan"],
        "risks": ["küçük arsada alan verimi düşebilir", "cephe ve su yalıtımı karmaşıklığı artabilir"],
        "tool_route": ["FreeCAD BIM", "Bonsai", "Ladybug"],
    },
    {
        "id": "OPT-03",
        "name": "Linear Bar",
        "family": "linear_bar",
        "footprint_factor": 0.92,
        "concept": "Yol, manzara veya güneş yönüne uzanan net lineer kütle.",
        "strengths": ["okunabilir plan", "cephe ve manzara kontrolü", "basit servis omurgası"],
        "risks": ["uzun koridor riski", "arsa oranı uygun değilse boşluk kalitesi zayıflar"],
        "tool_route": ["SketchUp", "Blender"],
    },
    {
        "id": "OPT-04",
        "name": "Stepped Terrace",
        "family": "stepped_terrace",
        "footprint_factor": 1.08,
        "concept": "Katlarda geri çekilerek teras, manzara ve gölge kontrolü kuran kütle.",
        "strengths": ["teras kullanımı", "insan ölçeği", "gölge ve manzara yönetimi"],
        "risks": ["taşıyıcı ve yalıtım karmaşıklığı", "brüt/net verimi düşebilir"],
        "tool_route": ["Blender", "FreeCAD", "Ladybug"],
    },
]


def load_brief(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def get_number(mapping: dict[str, Any], key: str, default: float) -> float:
    value = mapping.get(key, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def estimate_site_area(site: dict[str, Any]) -> float:
    area = get_number(site, "area_m2", 0)
    if area > 0:
        return area
    width = get_number(site, "width_m", 0)
    depth = get_number(site, "depth_m", 0)
    return width * depth if width > 0 and depth > 0 else 1000.0


def option_metrics(site_area: float, target_gfa: float, floors: int, factor: float) -> dict[str, float]:
    base_footprint = target_gfa / max(floors, 1)
    footprint = min(base_footprint * factor, site_area * 0.85)
    gfa = footprint * floors
    return {
        "footprint_area_m2": round(footprint, 2),
        "gross_floor_area_m2": round(gfa, 2),
        "average_floor_plate_m2": round(footprint, 2),
        "coverage_ratio": round(footprint / site_area, 4),
        "floor_area_ratio": round(gfa / site_area, 4),
        "open_space_ratio": round(max(site_area - footprint, 0) / site_area, 4),
    }


def infer_flags(metrics: dict[str, float], brief: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    site = brief.get("site", {})
    if not site.get("north"):
        flags.append("north_missing")
    if not site.get("setbacks_m"):
        flags.append("setbacks_not_verified")
    if metrics["coverage_ratio"] > 0.6:
        flags.append("high_site_coverage")
    if metrics["floor_area_ratio"] > get_number(brief.get("constraints", {}), "max_far", 999):
        flags.append("far_may_exceed_constraint")
    if not brief.get("zoning_verified", False):
        flags.append("zoning_not_verified")
    return flags


def score_option(option: dict[str, Any], metrics: dict[str, float], goals: list[str]) -> dict[str, float]:
    program_fit = max(0.0, 10.0 - abs(metrics["gross_floor_area_m2"] - metrics["target_gfa_m2"]) / max(metrics["target_gfa_m2"], 1) * 10)
    cost_simplicity = {"compact_block": 9, "linear_bar": 8, "courtyard": 6.5, "stepped_terrace": 5.5}.get(option["family"], 6)
    daylight = {"courtyard": 8.5, "linear_bar": 8, "stepped_terrace": 7.5, "compact_block": 6}.get(option["family"], 6)
    site_response = {"stepped_terrace": 8, "courtyard": 7.5, "linear_bar": 7, "compact_block": 6.5}.get(option["family"], 6)
    flexibility = {"compact_block": 8, "linear_bar": 7, "courtyard": 6.5, "stepped_terrace": 6}.get(option["family"], 6)
    if "daylight" in goals or "natural_light" in goals:
        daylight += 0.7
    if "cost_efficiency" in goals or "fast_construction" in goals:
        cost_simplicity += 0.7
    if "open_space" in goals or "social_space" in goals:
        site_response += 0.6
    return {
        "program_fit": round(min(program_fit, 10), 2),
        "site_response": round(min(site_response, 10), 2),
        "daylight_potential": round(min(daylight, 10), 2),
        "cost_simplicity": round(min(cost_simplicity, 10), 2),
        "flexibility": round(min(flexibility, 10), 2),
    }


def generate_options(brief: dict[str, Any]) -> dict[str, Any]:
    site = brief.get("site", {})
    program = brief.get("program", {})
    site_area = estimate_site_area(site)
    target_gfa = get_number(program, "target_gfa_m2", site_area * 1.2)
    floors = max(1, int(get_number(program, "floors", 3)))
    goals = [str(goal).lower() for goal in brief.get("goals", [])]

    options = []
    for option in OPTION_LIBRARY:
        metrics = option_metrics(site_area, target_gfa, floors, option["footprint_factor"])
        metrics["target_gfa_m2"] = round(target_gfa, 2)
        criteria = score_option(option, metrics, goals)
        weighted_score = (
            criteria["program_fit"] * 0.3
            + criteria["site_response"] * 0.2
            + criteria["daylight_potential"] * 0.2
            + criteria["cost_simplicity"] * 0.2
            + criteria["flexibility"] * 0.1
        )
        options.append(
            {
                "id": option["id"],
                "name": option["name"],
                "family": option["family"],
                "concept": option["concept"],
                "metrics": {k: v for k, v in metrics.items() if k != "target_gfa_m2"},
                "criteria_scores": criteria,
                "weighted_score": round(weighted_score, 2),
                "strengths": option["strengths"],
                "risks": option["risks"],
                "flags": infer_flags(metrics, brief),
                "tool_route": option["tool_route"],
                "next_skill": "blender-3d-modelleme-ve-render",
            }
        )
    options.sort(key=lambda item: item["weighted_score"], reverse=True)
    return {
        "metadata": {
            "project_type": brief.get("project_type", "unknown"),
            "site_area_m2": round(site_area, 2),
            "target_gfa_m2": round(target_gfa, 2),
            "floors": floors,
            "concept_only": True,
        },
        "options": options,
    }


def to_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Konsept Alternatifleri",
        "",
        f"- Proje tipi: {payload['metadata']['project_type']}",
        f"- Arsa alanı: {payload['metadata']['site_area_m2']} m2",
        f"- Hedef brüt alan: {payload['metadata']['target_gfa_m2']} m2",
        f"- Kat adedi: {payload['metadata']['floors']}",
        "",
        "| Sıra | Alternatif | Skor | Kaplama | FAR | Açık Alan | Araç Rotası |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for index, option in enumerate(payload["options"], start=1):
        metrics = option["metrics"]
        route = ", ".join(option["tool_route"])
        lines.append(
            f"| {index} | {option['name']} | {option['weighted_score']} | "
            f"{metrics['coverage_ratio']} | {metrics['floor_area_ratio']} | {metrics['open_space_ratio']} | {route} |"
        )
    lines.extend(["", "## Not", "", "Bu çıktı konsept ön değerlendirmedir; imar, ruhsat, statik, MEP ve yangın uygunluğu ayrıca doğrulanmalıdır."])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", help="JSON tasarım brief dosyası")
    parser.add_argument("--output", help="Çıktı dosyası")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    payload = generate_options(load_brief(Path(args.brief)))
    rendered = to_markdown(payload) if args.format == "markdown" else json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
