#!/usr/bin/env python3
import argparse
import json


def get_psets(ifcopenshell, element):
    try:
        return ifcopenshell.util.element.get_psets(element, qtos_only=False)
    except Exception:
        return {}


def get_container(ifcopenshell, element):
    try:
        container = ifcopenshell.util.element.get_container(element)
        return getattr(container, "Name", None) if container else None
    except Exception:
        return None


def flatten_quantities(psets):
    quantities = {}
    for pset_name, values in psets.items():
        if not isinstance(values, dict):
            continue
        for key, value in values.items():
            if key == "id":
                continue
            if isinstance(value, (int, float)):
                quantities[key] = value
            elif isinstance(value, str):
                try:
                    quantities[key] = float(value)
                except ValueError:
                    pass
    return quantities


def main():
    parser = argparse.ArgumentParser(description="Extract IfcSpace records and basic quantities from IFC.")
    parser.add_argument("ifc_path")
    args = parser.parse_args()

    try:
        import ifcopenshell
        import ifcopenshell.util.element
    except Exception as exc:
        print(json.dumps({
            "error": "ifcopenshell_not_available",
            "detail": str(exc),
            "hint": "Install ifcopenshell or use bim-revit-ifc-model-kontrolu to plan extraction.",
        }, indent=2, ensure_ascii=True))
        return

    model = ifcopenshell.open(args.ifc_path)
    spaces = model.by_type("IfcSpace")
    records = []
    for space in spaces:
        psets = get_psets(ifcopenshell, space)
        quantities = flatten_quantities(psets)
        flags = []
        if not getattr(space, "Name", None) and not getattr(space, "LongName", None):
            flags.append("missing_space_name")
        level = get_container(ifcopenshell, space)
        if not level:
            flags.append("missing_storey")
        if not quantities:
            flags.append("missing_quantities")
        records.append({
            "global_id": getattr(space, "GlobalId", None),
            "code": getattr(space, "Name", None),
            "name": getattr(space, "LongName", None) or getattr(space, "Name", None),
            "object_type": getattr(space, "ObjectType", None),
            "level": level,
            "quantities": quantities,
            "qa_flags": flags,
        })

    result = {
        "ifc_path": args.ifc_path,
        "space_count": len(records),
        "records": records,
        "qa_flags": sorted({flag for record in records for flag in record["qa_flags"]}),
    }
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
