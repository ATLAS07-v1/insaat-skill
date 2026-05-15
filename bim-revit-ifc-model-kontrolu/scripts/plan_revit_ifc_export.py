#!/usr/bin/env python3
"""Create a safe Revit-to-IFC export plan without opening or mutating RVT files."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="RVT/IFC model path or project name")
    parser.add_argument("--schema", default="IFC4 Reference View", help="Requested IFC schema/view")
    parser.add_argument("--discipline", default="unknown", help="Architecture/structure/MEP/etc.")
    args = parser.parse_args()

    model = Path(args.model)
    pyrevit = shutil.which("pyrevit")
    freecad = shutil.which("FreeCADCmd") or shutil.which("freecadcmd")
    blender = shutil.which("blender")
    ifcconvert = shutil.which("IfcConvert") or shutil.which("ifcconvert")

    result = {
        "source": str(model.resolve()) if model.exists() else args.model,
        "requested_schema": args.schema,
        "discipline": args.discipline,
        "available_tools": {
            "pyrevit": pyrevit,
            "ifcconvert": ifcconvert,
            "freecadcmd": freecad,
            "blender": blender,
        },
        "recommended_route": [
            "Confirm Revit version and install matching Autodesk revit-ifc exporter.",
            "Export a working IFC copy from Revit; do not treat RVT as directly parsed open-source data.",
            "Enable rooms/spaces, property sets, base quantities, and classification mapping when required.",
            "Run IfcOpenShell inspection on the exported IFC.",
            "Run visual QA in Bonsai/Blender, FreeCAD, xeokit, or another viewer.",
            "If IDS is available, validate with IfcTester.",
        ],
        "export_settings_to_record": [
            "Revit version",
            "revit-ifc exporter version",
            "IFC schema/view",
            "coordinate/base point setting",
            "rooms/spaces export",
            "property sets export",
            "base quantities export",
            "linked models export",
            "phase/design option/workset scope",
        ],
        "qa_after_export": [
            "Schema and authoring tool read correctly.",
            "Project/site/building/storey/space hierarchy exists.",
            "Element counts match expected discipline scope.",
            "Units and coordinates are present.",
            "Property sets and quantity sets are present where required.",
            "Geometry has been visually checked.",
        ],
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
