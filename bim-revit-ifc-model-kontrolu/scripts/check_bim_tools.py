#!/usr/bin/env python3
"""Check availability of BIM/IFC tools used by this skill."""

from __future__ import annotations

import importlib.util
import json
import shutil


COMMANDS = [
    "IfcConvert",
    "ifcconvert",
    "python",
    "pyrevit",
    "Revit",
    "FreeCADCmd",
    "freecadcmd",
    "blender",
    "node",
    "dotnet",
]
PYTHON_MODULES = ["ifcopenshell", "ifctester", "bcf", "win32com"]


def main() -> int:
    result = {
        "commands": {name: shutil.which(name) for name in COMMANDS},
        "python_modules": {
            name: importlib.util.find_spec(name) is not None for name in PYTHON_MODULES
        },
        "notes": [
            "IFC data extraction prefers ifcopenshell.",
            "Revit RVT files require Revit/API export to IFC; do not assume direct open-source RVT parsing.",
            "Geometry and visual QA can use Bonsai/Blender, FreeCAD, web-ifc, or xeokit depending on the environment.",
        ],
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
