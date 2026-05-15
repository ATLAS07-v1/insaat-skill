#!/usr/bin/env python3
"""Inspect an IFC model with IfcOpenShell and emit a compact JSON report."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ELEMENT_CLASSES = [
    "IfcWall",
    "IfcSlab",
    "IfcRoof",
    "IfcDoor",
    "IfcWindow",
    "IfcStair",
    "IfcBeam",
    "IfcColumn",
    "IfcFooting",
    "IfcPile",
    "IfcMember",
    "IfcSpace",
    "IfcFlowSegment",
    "IfcFlowTerminal",
    "IfcDistributionElement",
    "IfcFurnishingElement",
    "IfcCovering",
    "IfcRailing",
    "IfcRamp",
]


def safe_attr(entity: Any, attr: str, default: Any = None) -> Any:
    try:
        value = getattr(entity, attr)
        return value if value is not None else default
    except Exception:
        return default


def entity_summary(entity: Any) -> dict[str, Any]:
    return {
        "class": entity.is_a() if entity else None,
        "global_id": safe_attr(entity, "GlobalId"),
        "name": safe_attr(entity, "Name"),
    }


def pset_count(ifcopenshell_util_element: Any, element: Any) -> tuple[int, int]:
    if ifcopenshell_util_element is None:
        return (0, 0)
    try:
        psets = ifcopenshell_util_element.get_psets(element, qtos_only=False)
        qtos = ifcopenshell_util_element.get_psets(element, qtos_only=True)
        return (len(psets or {}), len(qtos or {}))
    except Exception:
        return (0, 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="IFC or IFCZIP file")
    parser.add_argument("--sample", type=int, default=50, help="Sample element count")
    args = parser.parse_args()

    try:
        import ifcopenshell  # type: ignore
    except Exception:
        print("ifcopenshell is not installed. Install with: pip install ifcopenshell")
        return 2

    try:
        from ifcopenshell.util import element as ifc_element  # type: ignore
    except Exception:
        ifc_element = None

    path = Path(args.path)
    model = ifcopenshell.open(str(path))

    projects = model.by_type("IfcProject")
    sites = model.by_type("IfcSite")
    buildings = model.by_type("IfcBuilding")
    storeys = model.by_type("IfcBuildingStorey")
    spaces = model.by_type("IfcSpace")

    entity_counts: Counter[str] = Counter()
    for class_name in ELEMENT_CLASSES:
        try:
            entity_counts[class_name] = len(model.by_type(class_name))
        except Exception:
            entity_counts[class_name] = 0

    all_products = model.by_type("IfcProduct")
    sampled_elements = []
    with_psets = 0
    with_qtos = 0
    missing_globalid = 0
    missing_name = 0

    for element in all_products[: args.sample]:
        pset_total, qto_total = pset_count(ifc_element, element)
        with_psets += int(pset_total > 0)
        with_qtos += int(qto_total > 0)
        if not safe_attr(element, "GlobalId"):
            missing_globalid += 1
        if not safe_attr(element, "Name"):
            missing_name += 1
        sampled_elements.append(
            {
                "class": element.is_a(),
                "global_id": safe_attr(element, "GlobalId"),
                "name": safe_attr(element, "Name"),
                "type": safe_attr(element, "ObjectType"),
                "pset_count": pset_total,
                "qto_count": qto_total,
            }
        )

    quality_flags: list[str] = []
    if not projects:
        quality_flags.append("missing_project")
    if not storeys:
        quality_flags.append("missing_storeys")
    if not spaces:
        quality_flags.append("missing_spaces")
    if all_products and with_qtos == 0:
        quality_flags.append("missing_quantities_in_sample")
    if missing_globalid:
        quality_flags.append("missing_globalid_in_sample")
    if missing_name:
        quality_flags.append("missing_name_in_sample")
    quality_flags.append("geometry_not_checked")

    result = {
        "source_file": str(path.resolve()),
        "schema": getattr(model, "schema", None),
        "tool_route": ["ifcopenshell"],
        "projects": [entity_summary(item) for item in projects],
        "sites": [entity_summary(item) for item in sites],
        "buildings": [entity_summary(item) for item in buildings],
        "storeys": [
            {**entity_summary(item), "elevation": safe_attr(item, "Elevation")}
            for item in storeys
        ],
        "spaces_sample": [entity_summary(item) for item in spaces[: args.sample]],
        "entity_counts": dict(entity_counts),
        "product_count": len(all_products),
        "property_summary_sample": {
            "sample_size": min(len(all_products), args.sample),
            "with_psets": with_psets,
            "with_quantities": with_qtos,
        },
        "sampled_elements": sampled_elements,
        "quality_flags": quality_flags,
        "next_skill": "metraj-ve-mahal-kontrolu",
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
