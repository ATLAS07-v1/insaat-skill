#!/usr/bin/env python3
import argparse
import importlib.util
import json


ROUTES = {
    "ifc_space": {
        "route": [
            "Validate IFC model first with BIM skill.",
            "Extract IfcSpace records, storey relation, Name/LongName and BaseQuantities.",
            "Flag missing storey, missing quantity sets and empty names.",
        ],
        "tools": ["ifcopenshell", "ifccsv", "bim-revit-ifc-model-kontrolu"],
        "qa": ["ifc_opens", "ifcspace_count", "storey_present", "quantities_present"],
    },
    "schedule_compare": {
        "route": [
            "Normalize source A and source B columns.",
            "Match by code+level, then name+level, then fuzzy name candidates.",
            "Compare area, volume and count against explicit tolerances.",
        ],
        "tools": ["compare_room_schedules.py", "pandas optional", "rapidfuzz optional"],
        "qa": ["duplicates_checked", "missing_checked", "area_delta_checked", "low_confidence_matches_flagged"],
    },
    "pdf_schedule": {
        "route": [
            "Check whether PDF is text-based or scanned.",
            "Use pdfplumber or Camelot to extract tables.",
            "Export to CSV and run schedule comparison.",
        ],
        "tools": ["pdfplumber", "camelot", "compare_room_schedules.py"],
        "qa": ["pdf_text_based", "table_accuracy_recorded", "manual_spot_check_required"],
    },
    "cad_area_list": {
        "route": [
            "Use CAD skill to verify layer, closed polylines and scale.",
            "Export area schedule to CSV.",
            "Compare against mahal list with tolerances.",
        ],
        "tools": ["cad-autocad-dwg-dxf-isleme", "compare_room_schedules.py"],
        "qa": ["scale_checked", "closed_polyline_checked", "layer_mapping_recorded"],
    },
    "boq_quantity": {
        "route": [
            "Separate BOQ item, element class, quantity type and unit.",
            "Use Ifc5D/QuantityTakeoff-style grouping when model data exists.",
            "Compare totals and spot-check source quantities.",
        ],
        "tools": ["ifc5d", "QuantityTakeoff-Python", "insaat-hesaplamalar"],
        "qa": ["unit_checked", "quantity_type_checked", "grouping_rule_recorded"],
    },
}


def module_exists(name):
    return importlib.util.find_spec(name) is not None


def main():
    parser = argparse.ArgumentParser(description="Plan metraj and room/space schedule QA route.")
    parser.add_argument("--source-type", choices=sorted(ROUTES), default="schedule_compare")
    parser.add_argument("--source", action="append", default=[])
    args = parser.parse_args()

    selected = ROUTES[args.source_type]
    modules = {
        name: module_exists(name)
        for name in ["pandas", "openpyxl", "ifcopenshell", "ifc5d", "ifccsv", "pdfplumber", "camelot", "rapidfuzz"]
    }
    result = {
        "source_type": args.source_type,
        "sources": args.source,
        "recommended_route": selected["route"],
        "tools": selected["tools"],
        "qa_gates": selected["qa"],
        "available_python_modules": modules,
        "approval_boundary": "Quantity and room/space QA is not a contractual measurement approval without project rules and responsible review.",
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
