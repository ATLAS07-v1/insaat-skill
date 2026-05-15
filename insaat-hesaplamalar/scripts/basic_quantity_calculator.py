#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path


DEFAULT_SPEC = {
    "project": "ornek_insaat_hesabi",
    "items": [
        {"name": "Zemin kat döşeme betonu", "type": "slab_concrete", "length_m": 10, "width_m": 8, "thickness_m": 0.15, "waste_factor": 0.03},
        {"name": "Kolon betonu", "type": "column_concrete", "width_m": 0.4, "depth_m": 0.4, "height_m": 3.2, "count": 8, "waste_factor": 0.03},
        {"name": "Kolon kalıbı", "type": "column_formwork", "width_m": 0.4, "depth_m": 0.4, "height_m": 3.2, "count": 8},
        {"name": "Duvar boya", "type": "wall_finish", "length_m": 12, "height_m": 2.8, "openings_m2": 4.2, "waste_factor": 0.08},
        {"name": "Ø12 donatı", "type": "rebar_weight", "diameter_mm": 12, "length_m": 6, "count": 120, "waste_factor": 0.07},
        {"name": "Kazı", "type": "excavation", "length_m": 12, "width_m": 9, "depth_m": 1.2, "bulking_factor": 1.15},
        {"name": "Rampa eğimi", "type": "slope", "rise_m": 0.75, "run_m": 12},
    ],
}


def positive(value):
    try:
        return float(value) > 0
    except Exception:
        return False


def add_waste(quantity, item):
    waste = float(item.get("waste_factor", 0) or 0)
    return quantity * (1 + waste), waste


def calc_item(item):
    item_type = item.get("type")
    name = item.get("name", item_type or "unnamed")
    flags = []
    assumptions = []
    formula = ""
    quantity = None
    unit = ""
    category = item_type or "unknown"

    def require(*keys):
        missing = [key for key in keys if key not in item]
        for key in missing:
            flags.append(f"missing_{key}")
        for key in keys:
            if key in item and not positive(item[key]):
                flags.append(f"non_positive_{key}")
        return not missing and not any(f"non_positive_{key}" in flags for key in keys)

    if item_type == "area_rect":
        if require("length_m", "width_m"):
            quantity = float(item["length_m"]) * float(item["width_m"])
            unit = "m2"
            formula = "length_m * width_m"
    elif item_type == "volume_rect":
        if require("length_m", "width_m", "height_m"):
            quantity = float(item["length_m"]) * float(item["width_m"]) * float(item["height_m"])
            unit = "m3"
            formula = "length_m * width_m * height_m"
    elif item_type == "slab_concrete":
        if require("length_m", "width_m", "thickness_m"):
            gross = float(item["length_m"]) * float(item["width_m"]) * float(item["thickness_m"])
            quantity, waste = add_waste(gross, item)
            unit = "m3"
            formula = "length_m * width_m * thickness_m * (1 + waste_factor)"
            if waste:
                assumptions.append(f"waste_factor={waste}")
            category = "concrete"
    elif item_type == "column_concrete":
        if require("width_m", "depth_m", "height_m", "count"):
            gross = float(item["width_m"]) * float(item["depth_m"]) * float(item["height_m"]) * float(item["count"])
            quantity, waste = add_waste(gross, item)
            unit = "m3"
            formula = "width_m * depth_m * height_m * count * (1 + waste_factor)"
            if waste:
                assumptions.append(f"waste_factor={waste}")
            category = "concrete"
    elif item_type == "beam_concrete":
        if require("length_m", "width_m", "height_m", "count"):
            gross = float(item["length_m"]) * float(item["width_m"]) * float(item["height_m"]) * float(item["count"])
            quantity, waste = add_waste(gross, item)
            unit = "m3"
            formula = "length_m * width_m * height_m * count * (1 + waste_factor)"
            if waste:
                assumptions.append(f"waste_factor={waste}")
            category = "concrete"
    elif item_type == "wall_finish":
        if require("length_m", "height_m"):
            gross = float(item["length_m"]) * float(item["height_m"])
            openings = float(item.get("openings_m2", 0) or 0)
            if openings < 0:
                flags.append("negative_openings")
            if openings > gross:
                flags.append("opening_exceeds_gross_area")
            net = max(gross - openings, 0)
            quantity, waste = add_waste(net, item)
            unit = "m2"
            formula = "(length_m * height_m - openings_m2) * (1 + waste_factor)"
            assumptions.append(f"openings_m2={openings}")
            if waste:
                assumptions.append(f"waste_factor={waste}")
            category = "finish_area"
    elif item_type == "column_formwork":
        if require("width_m", "depth_m", "height_m", "count"):
            quantity = 2 * (float(item["width_m"]) + float(item["depth_m"])) * float(item["height_m"]) * float(item["count"])
            unit = "m2"
            formula = "2 * (width_m + depth_m) * height_m * count"
            category = "formwork"
    elif item_type == "beam_formwork":
        if require("length_m", "width_m", "height_m", "count"):
            quantity = (2 * float(item["height_m"]) + float(item["width_m"])) * float(item["length_m"]) * float(item["count"])
            unit = "m2"
            formula = "(2 * height_m + width_m) * length_m * count"
            category = "formwork"
            assumptions.append("beam top face excluded")
    elif item_type == "rebar_weight":
        if require("diameter_mm", "length_m", "count"):
            kg_per_m = float(item["diameter_mm"]) ** 2 / 162.0
            gross = kg_per_m * float(item["length_m"]) * float(item["count"])
            quantity, waste = add_waste(gross, item)
            unit = "kg"
            formula = "(diameter_mm^2 / 162) * length_m * count * (1 + waste_factor)"
            assumptions.append(f"kg_per_m={kg_per_m:.4f}")
            if waste:
                assumptions.append(f"waste_factor={waste}")
            category = "rebar"
    elif item_type == "excavation":
        if require("length_m", "width_m", "depth_m"):
            gross = float(item["length_m"]) * float(item["width_m"]) * float(item["depth_m"])
            factor = float(item.get("bulking_factor", 1) or 1)
            if factor <= 0:
                flags.append("non_positive_bulking_factor")
                factor = 1
            quantity = gross * factor
            unit = "m3"
            formula = "length_m * width_m * depth_m * bulking_factor"
            assumptions.append(f"bulking_factor={factor}")
            category = "earthwork"
    elif item_type == "slope":
        if require("rise_m", "run_m"):
            quantity = float(item["rise_m"]) / float(item["run_m"]) * 100
            unit = "percent"
            formula = "rise_m / run_m * 100"
            category = "slope"
    else:
        flags.append("unknown_item_type")

    if quantity is None:
        quantity = 0.0
    return {
        "name": name,
        "type": item_type,
        "category": category,
        "formula": formula,
        "quantity": round(quantity, 6),
        "unit": unit,
        "assumptions": assumptions,
        "qa_flags": flags,
    }


def load_spec(path):
    if not path:
        return DEFAULT_SPEC
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main():
    parser = argparse.ArgumentParser(description="Calculate basic construction quantities from JSON.")
    parser.add_argument("--spec", help="JSON spec path. Uses a sample if omitted.")
    args = parser.parse_args()

    spec = load_spec(args.spec)
    results = [calc_item(item) for item in spec.get("items", [])]
    totals = defaultdict(float)
    for result in results:
        if result["unit"] == "m3" and result["category"] == "concrete":
            totals["concrete_m3"] += result["quantity"]
        elif result["unit"] == "m2" and result["category"] == "formwork":
            totals["formwork_m2"] += result["quantity"]
        elif result["unit"] == "kg" and result["category"] == "rebar":
            totals["rebar_kg"] += result["quantity"]
        elif result["category"] == "earthwork":
            totals["earthwork_m3"] += result["quantity"]
        elif result["category"] == "finish_area":
            totals["finish_area_m2"] += result["quantity"]

    qa_flags = sorted({flag for result in results for flag in result["qa_flags"]})
    output = {
        "project": spec.get("project", "unnamed_project"),
        "items": results,
        "totals": {key: round(value, 6) for key, value in totals.items()},
        "qa_flags": qa_flags,
        "approval_boundary": "For quantity pre-calculation only; structural design and code compliance require qualified professional review.",
    }
    print(json.dumps(output, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
