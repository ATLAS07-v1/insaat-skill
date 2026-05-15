#!/usr/bin/env python3
"""Check availability of Blender-related tools used by this skill."""

from __future__ import annotations

import importlib.util
import json
import shutil


COMMANDS = ["blender", "python", "node", "IfcConvert", "ifcconvert"]
PYTHON_MODULES = ["bpy", "mathutils", "blenderproc", "ifcopenshell"]


def main() -> int:
    result = {
        "commands": {name: shutil.which(name) for name in COMMANDS},
        "python_modules": {
            name: importlib.util.find_spec(name) is not None for name in PYTHON_MODULES
        },
        "notes": [
            "bpy and mathutils usually exist inside Blender's bundled Python, not normal system Python.",
            "Use blender --background --python script.py -- --args for deterministic scene generation.",
            "Use Bonsai/IfcOpenShell for IFC/BIM workflows and CAD skill output for DXF workflows.",
        ],
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
